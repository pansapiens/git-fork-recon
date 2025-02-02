from typing import List, Dict, Any
import logging
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from ..github.api import RepoInfo, ForkInfo
from ..git.repo import GitRepo, CommitInfo
from ..llm.client import LLMClient

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.env = Environment(
            loader=PackageLoader("git_fork_recon", "report/templates"),
            autoescape=select_autoescape(),
        )

    def _generate_interesting_forks_summary(
        self, analyses: List[Dict[str, Any]]
    ) -> str:
        """Generate a high-level summary of the most interesting forks using the LLM."""
        # Prepare the input for the LLM
        fork_summaries = []
        for analysis in analyses:
            fork = analysis["fork"]
            fork_summaries.append(
                f"Fork: {fork.repo_info.owner}/{fork.repo_info.name}\n"
                f"Stars: {fork.repo_info.stars}\n"
                f"Changes: {analysis['summary']}\n"
            )

        prompt = (
            "Below are summaries of changes made in different forks of a repository. "
            "Please provide a concise overview of the most interesting forks, focusing on "
            "those with significant feature additions or major changes. Give less emphasis "
            "to forks that are primarily about installation or minor fixes.\n\n"
            + "\n---\n".join(fork_summaries)
        )

        return self.llm_client.generate_summary(prompt)

    def generate(
        self, repo_info: RepoInfo, forks: List[ForkInfo], git_repo: GitRepo
    ) -> str:
        """Generate a Markdown report summarizing the forks."""
        template = self.env.get_template("master.md.jinja")

        # Construct GitHub repository URL
        repo_url = f"https://github.com/{repo_info.owner}/{repo_info.name}"

        # Analyze each fork
        fork_analyses = []
        for fork in forks:
            try:
                # Get commits unique to this fork
                commits = git_repo.get_fork_commits(fork)

                # Get a sample diff if there are many files changed
                diff = None
                if commits and len(commits[0].files_changed) > 0:
                    # Get diff of the first changed file in the first commit
                    diff = git_repo.get_file_diff(fork, commits[0].files_changed[0])

                # Get LLM summary of changes
                summary = self.llm_client.summarize_changes(commits, diff)

                fork_analyses.append(
                    {"fork": fork, "commits": commits, "summary": summary}
                )

            except Exception as e:
                logger.error(f"Error analyzing fork {fork.repo_info.name}: {e}")
                continue

        # Generate the interesting forks summary
        interesting_summary = self._generate_interesting_forks_summary(fork_analyses)

        # Generate the report
        return template.render(
            repo=repo_info,
            analyses=fork_analyses,
            repo_url=repo_url,
            summary=interesting_summary,
        )
