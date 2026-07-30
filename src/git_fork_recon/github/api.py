from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import logging
from pathlib import Path
import re
import asyncio
from datetime import datetime

from github import Github, Repository, GithubException
from github.Repository import Repository
from github.PullRequest import PullRequest
from github.GithubException import UnknownObjectException

logger = logging.getLogger(__name__)


@dataclass
class RepoInfo:
    """Information about a GitHub repository."""

    owner: str
    name: str
    clone_url: str
    default_branch: str
    stars: int
    description: Optional[str] = None


@dataclass
class ForkInfo:
    """Information about a forked repository."""

    repo_info: RepoInfo
    parent_repo: RepoInfo
    ahead_commits: int
    behind_commits: int
    has_pull_requests: bool
    pull_request_urls: List[str]
    last_updated: str
    # Branch this comparison was made against - may differ from repo_info.default_branch,
    # since forks often carry their changes on non-default branches
    branch: str


class GithubClient:
    def __init__(self, token: str, max_parallel: int = 5):
        self.client = Github(token)
        self.max_parallel = max_parallel

    def _check_rate_limit(self):
        """Check rate limit status and log warning if getting low."""
        try:
            rate_limit = self.client.get_rate_limit()

            # PyGithub v2.8.1+ uses resources.core structure
            core = rate_limit.resources.core
            remaining = core.remaining
            total = core.limit
            reset_time = core.reset

            reset_time_str = reset_time.strftime("%Y-%m-%d %H:%M:%S UTC")

            if remaining < 100:
                logger.warning(
                    f"GitHub API rate limit low: {remaining}/{total} requests remaining. "
                    f"Resets at {reset_time_str}"
                )
            else:
                logger.debug(
                    f"GitHub API rate limit status: {remaining}/{total} requests remaining. "
                    f"Resets at {reset_time_str}"
                )

            return remaining

        except Exception as e:
            logger.warning(f"Failed to check rate limit: {e}")
            # Return a conservative estimate if we can't check
            return 100

    async def _process_fork(
        self,
        repo: Repository,
        fork: Repository,
        parent_branch,
        max_branches_per_fork: Optional[int] = 3,
    ) -> List[ForkInfo]:
        """Process a single fork asynchronously.

        Compares every branch on the fork (not just its default branch) against
        the parent's default branch, since forks often carry their changes on
        non-default/feature branches. Returns one ForkInfo per branch that is
        ahead, capped to the most-diverged `max_branches_per_fork` branches.
        """
        try:
            logger.debug(f"Processing fork: {fork.full_name}")

            try:
                fork_branches = list(fork.get_branches())
            except Exception as e:
                logger.warning(f"Failed to list branches for {fork.full_name}: {e}")
                return []

            branch_comparisons = []
            for branch in fork_branches:
                try:
                    comparison = repo.compare(
                        parent_branch.commit.sha, branch.commit.sha
                    )
                except UnknownObjectException as e:
                    logger.warning(
                        f"Comparison failed for {fork.full_name}:{branch.name} - "
                        f"branch may be deleted/private: {e}"
                    )
                    continue
                except GithubException as e:
                    # Commonly a 404 "No common ancestor" for orphan/disconnected branches
                    logger.debug(
                        f"Skipping {fork.full_name}:{branch.name} - not comparable: {e}"
                    )
                    continue
                except Exception as e:
                    logger.warning(
                        f"Failed to compare {fork.full_name}:{branch.name}: {e}"
                    )
                    continue

                if comparison.ahead_by > 0:
                    branch_comparisons.append((branch.name, comparison))

            if not branch_comparisons:
                logger.debug(f"Skipping fork {fork.full_name} with no changes on any branch")
                return []

            branch_comparisons.sort(key=lambda b: b[1].ahead_by, reverse=True)
            if max_branches_per_fork and len(branch_comparisons) > max_branches_per_fork:
                dropped = [name for name, _ in branch_comparisons[max_branches_per_fork:]]
                logger.info(
                    f"{fork.full_name}: {len(branch_comparisons)} branches ahead, "
                    f"keeping top {max_branches_per_fork} by commits ahead "
                    f"(dropped: {', '.join(dropped)})"
                )
                branch_comparisons = branch_comparisons[:max_branches_per_fork]

            fork_infos = []
            for branch_name, comparison in branch_comparisons:
                pr_spec = f"{fork.owner.login}:{branch_name}"
                try:
                    prs = repo.get_pulls(state="all", head=pr_spec)
                    pr_urls = [pr.html_url for pr in prs]
                    has_prs = prs.totalCount > 0
                except Exception as e:
                    logger.warning(f"Failed to check PRs for {pr_spec}: {e}")
                    pr_urls, has_prs = [], False

                fork_infos.append(
                    ForkInfo(
                        repo_info=RepoInfo(
                            owner=fork.owner.login,
                            name=fork.name,
                            clone_url=fork.clone_url,
                            default_branch=fork.default_branch,
                            stars=fork.stargazers_count,
                            description=fork.description,
                        ),
                        parent_repo=RepoInfo(
                            owner=repo.owner.login,
                            name=repo.name,
                            clone_url=repo.clone_url,
                            default_branch=repo.default_branch,
                            stars=repo.stargazers_count,
                            description=repo.description,
                        ),
                        ahead_commits=comparison.ahead_by,
                        behind_commits=comparison.behind_by,
                        has_pull_requests=has_prs,
                        pull_request_urls=pr_urls,
                        last_updated=fork.pushed_at.isoformat(),
                        branch=branch_name,
                    )
                )
                logger.info(
                    f"Adding fork {fork.full_name}:{branch_name} with {comparison.ahead_by} commits ahead"
                )

            return fork_infos

        except Exception as e:
            logger.warning(
                f"Error processing fork {fork.full_name}: {e}", exc_info=True
            )
            return []

    async def _process_fork_batch(
        self,
        repo: Repository,
        forks: List[Repository],
        parent_branch,
        max_branches_per_fork: Optional[int] = 3,
    ) -> List[ForkInfo]:
        """Process a batch of forks in parallel."""
        # Check rate limit before processing batch
        remaining = self._check_rate_limit()

        # Estimate requests needed: 1 to list branches, plus 1 compare + 1 PR
        # check per branch kept. Actual comparisons made may exceed this if a
        # fork has many branches - this is a rough guide, not a hard cap.
        branches_per_fork_estimate = max_branches_per_fork or 3
        requests_needed = len(forks) * (1 + branches_per_fork_estimate * 2)
        if remaining < requests_needed:
            logger.warning(
                f"Rate limit may be exceeded: need ~{requests_needed} requests but only {remaining} remaining. "
                "Processing may be incomplete."
            )

        tasks = []
        for fork in forks:
            tasks.append(
                self._process_fork(repo, fork, parent_branch, max_branches_per_fork)
            )

        results = await asyncio.gather(*tasks)
        return [fork_info for result in results for fork_info in result]

    async def async_get_forks(
        self,
        repo_info: RepoInfo,
        max_forks: Optional[int] = None,
        max_branches_per_fork: Optional[int] = 3,
    ) -> List[ForkInfo]:
        """Get information about all forks of a repository asynchronously.

        Args:
            repo_info: Repository information
            max_forks: Maximum number of forks to process after sorting by update time
            max_branches_per_fork: Maximum number of diverged branches to keep per
                fork (by commits ahead). Forks often carry changes on non-default
                branches, so every branch is compared, but only the most-diverged
                ones are kept to bound API usage and report size. None = no cap.
        """
        repo = self.client.get_repo(f"{repo_info.owner}/{repo_info.name}")
        parent_branch = repo.get_branch(repo.default_branch)
        forks = list(repo.get_forks())
        logger.info(
            f"Found {len(forks)} total forks for {repo_info.owner}/{repo_info.name}"
        )

        # Sort forks by updated_at before processing
        forks.sort(key=lambda x: x.updated_at, reverse=True)
        logger.debug("Sorted forks by last update time")

        # Limit number of forks to process if specified
        if max_forks and len(forks) > max_forks:
            logger.info(
                f"Limiting processing to {max_forks} most recently updated forks (out of {len(forks)} total)"
            )
            forks = forks[:max_forks]
        else:
            logger.debug(f"Processing all {len(forks)} forks (no limit specified)")

        # Check if we have enough rate limit for all forks
        branches_per_fork_estimate = max_branches_per_fork or 3
        requests_per_fork_estimate = 1 + branches_per_fork_estimate * 2
        remaining = self._check_rate_limit()
        total_requests_needed = len(forks) * requests_per_fork_estimate
        if remaining < total_requests_needed:
            logger.warning(
                f"Not enough rate limit for all forks. Need ~{total_requests_needed} requests but only have {remaining}. "
                "Will process as many as possible."
            )

        # Process forks in batches
        processed_forks = []
        for i in range(0, len(forks), self.max_parallel):
            if self._check_rate_limit() < self.max_parallel * requests_per_fork_estimate:
                logger.error(
                    "Rate limit too low to process next batch. Stopping early."
                )
                break

            batch = forks[i : i + self.max_parallel]
            batch_results = await self._process_fork_batch(
                repo, batch, parent_branch, max_branches_per_fork
            )
            processed_forks.extend(batch_results)

        logger.info(
            f"Found {len(processed_forks)} active fork branches with changes out of {len(forks)} processed forks"
        )
        # Final sort by significance (ahead commits and stars)
        processed_forks.sort(
            key=lambda x: (x.ahead_commits, x.repo_info.stars), reverse=True
        )
        return processed_forks

    def get_forks(
        self,
        repo_info: RepoInfo,
        max_forks: Optional[int] = None,
        max_branches_per_fork: Optional[int] = 3,
    ) -> List[ForkInfo]:
        """Synchronous wrapper for async_get_forks."""
        return asyncio.run(
            self.async_get_forks(repo_info, max_forks, max_branches_per_fork)
        )

    def get_repository(self, repo_identifier: str) -> RepoInfo:
        """Get information about a GitHub repository.

        Args:
            repo_identifier: Either a GitHub URL or a repository name in the format 'owner/repo'
        """
        if "/" in repo_identifier and "github.com" not in repo_identifier:
            # Already in owner/repo format
            owner, name = repo_identifier.split("/")
        else:
            # URL format
            owner, name = self._parse_repo_url(repo_identifier)

        repo = self.client.get_repo(f"{owner}/{name}")

        return RepoInfo(
            owner=repo.owner.login,
            name=repo.name,
            clone_url=repo.clone_url,
            default_branch=repo.default_branch,
            stars=repo.stargazers_count,
            description=repo.description,
        )

    def _parse_repo_url(self, url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL."""
        # Remove trailing slash if present
        url = url.rstrip("/")
        pattern = r"github\.com[:/]([^/]+)/([^/\s]+?)(?:\.git)?$"
        match = re.search(pattern, url)
        if not match:
            raise ValueError(f"Invalid GitHub URL: {url}")
        return match.group(1), match.group(2)
