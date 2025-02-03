from dataclasses import dataclass
from typing import List, Optional
import logging
from pathlib import Path
import re

from github import Github
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


class GithubClient:
    def __init__(self, token: str):
        self.client = Github(token)

    def _parse_repo_url(self, url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL."""
        pattern = r"github\.com[:/]([^/]+)/([^/]+)"
        match = re.search(pattern, url)
        if not match:
            raise ValueError(f"Invalid GitHub URL: {url}")
        return match.group(1), match.group(2).rstrip(".git")

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

    def get_forks(self, repo_info: RepoInfo) -> List[ForkInfo]:
        """Get information about all forks of a repository."""
        repo = self.client.get_repo(f"{repo_info.owner}/{repo_info.name}")
        forks = []

        # Get all forks first
        all_forks = list(repo.get_forks())
        logger.info(
            f"Found {len(all_forks)} total forks for {repo_info.owner}/{repo_info.name}"
        )

        for fork in all_forks:
            try:
                logger.debug(f"Processing fork: {fork.full_name}")
                logger.debug(f"Fork default branch: {fork.default_branch}")
                logger.debug(f"Parent default branch: {repo.default_branch}")

                # Get comparison with parent
                # The comparison should be from parent's default branch to fork's default branch
                try:
                    # First try to get the fork's default branch
                    fork_branch = fork.get_branch(fork.default_branch)
                    logger.debug(f"Fork branch SHA: {fork_branch.commit.sha}")

                    # Then get parent's default branch
                    parent_branch = repo.get_branch(repo.default_branch)
                    logger.debug(f"Parent branch SHA: {parent_branch.commit.sha}")

                    # Compare using the full ref format
                    comparison = repo.compare(
                        parent_branch.commit.sha, fork_branch.commit.sha
                    )
                    logger.debug(
                        f"Comparison successful: ahead={comparison.ahead_by}, behind={comparison.behind_by}"
                    )

                except UnknownObjectException as e:
                    logger.warning(
                        f"Fork {fork.full_name} branch comparison failed - repository or branch may be deleted/private: {e}"
                    )
                    continue
                except Exception as e:
                    logger.warning(
                        f"Failed to compare branches for {fork.full_name}: {e}"
                    )
                    continue

                # Check for PRs from this fork
                pr_spec = f"{fork.owner.login}:{fork.default_branch}"
                logger.debug(f"Checking PRs with head: {pr_spec}")
                prs = repo.get_pulls(state="all", head=pr_spec)
                pr_urls = [pr.html_url for pr in prs]

                fork_info = ForkInfo(
                    repo_info=RepoInfo(
                        owner=fork.owner.login,
                        name=fork.name,
                        clone_url=fork.clone_url,
                        default_branch=fork.default_branch,
                        stars=fork.stargazers_count,
                        description=fork.description,
                    ),
                    parent_repo=repo_info,
                    ahead_commits=comparison.ahead_by,
                    behind_commits=comparison.behind_by,
                    has_pull_requests=prs.totalCount > 0,
                    pull_request_urls=pr_urls,
                    last_updated=fork.pushed_at.isoformat(),
                )

                logger.debug(
                    f"Fork {fork.full_name} stats: ahead={fork_info.ahead_commits}, "
                    f"behind={fork_info.behind_commits}, prs={prs.totalCount}"
                )

                # Only include forks that have made changes
                if fork_info.ahead_commits > 0:
                    logger.info(
                        f"Adding fork {fork.full_name} with {fork_info.ahead_commits} commits ahead"
                    )
                    forks.append(fork_info)
                else:
                    logger.debug(f"Skipping fork {fork.full_name} with no changes")

            except Exception as e:
                logger.warning(
                    f"Error processing fork {fork.full_name}: {e}", exc_info=True
                )
                continue

        logger.info(
            f"Found {len(forks)} active forks with changes out of {len(all_forks)} total forks"
        )
        # Sort forks by number of commits ahead and stars
        forks.sort(key=lambda x: (x.ahead_commits, x.repo_info.stars), reverse=True)
        return forks
