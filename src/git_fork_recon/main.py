#!/usr/bin/env python

from typing import Optional, Tuple
import logging
import sys
from pathlib import Path
import re
import shutil

import typer
from rich.console import Console
from rich.logging import RichHandler

from .config import load_config
from .github.api import GithubClient
from .git.repo import GitRepo
from .llm.client import LLMClient
from .report.generator import ReportGenerator

app = typer.Typer()
console = Console()
logger = logging.getLogger(__name__)


def parse_github_url(url: str) -> Tuple[str, str]:
    """Extract owner and repository name from a GitHub URL."""
    pattern = r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$"
    match = re.search(pattern, url)
    if not match:
        raise ValueError("Invalid GitHub repository URL")
    return match.group(1), match.group(2)


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


def clear_repo_cache(repo_dir: Path) -> None:
    """Clear the cached repository data."""
    if repo_dir.exists():
        logger.info(f"Clearing cache for {repo_dir}")
        shutil.rmtree(repo_dir)


@app.command()
def analyze(
    repo_url: str = typer.Argument(..., help="URL of the GitHub repository to analyze"),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path for the report. Use '-' for stdout. Defaults to {username}-{repo}-forks.md",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging"
    ),
    clear_cache: bool = typer.Option(
        False, "--clear-cache", help="Clear cached repository data before analysis"
    ),
) -> None:
    """Analyze a GitHub repository's fork network and generate a summary report."""
    setup_logging(verbose)

    try:
        config = load_config()
        github_client = GithubClient(config.github_token)
        llm_client = LLMClient(config.openrouter_api_key)

        # Parse repository URL
        owner, repo = parse_github_url(repo_url)
        repo_full_name = f"{owner}/{repo}"
        logger.debug(f"Analyzing repository: {repo_full_name}")

        # Set default output filename if none specified
        if output is None:
            output = Path(f"{owner}-{repo}-forks.md")
            logger.info(f"No output file specified, using default: {output}")

        # Initialize report generator
        report_gen = ReportGenerator(llm_client)

        # Get repository and fork information
        repo_info = github_client.get_repository(repo_full_name)

        # Clear cache if requested
        if clear_cache:
            repo_cache = config.cache_dir / f"{owner}-{repo}"
            clear_repo_cache(repo_cache)

        # Clone main repository
        git_repo = GitRepo(repo_info, config)

        forks = github_client.get_forks(repo_info)

        # Analyze forks and generate report
        report = report_gen.generate(repo_info, forks, git_repo)

        # Output report
        if str(output) == "-":
            console.print(report)
        else:
            output.write_text(report)
            logger.info(f"Report written to {output}")

    except Exception as e:
        logger.error(f"Error analyzing repository: {e}", exc_info=verbose)
        sys.exit(1)


if __name__ == "__main__":
    app()
