#!/usr/bin/env python

from typing import Optional, Tuple
import logging
import sys
from pathlib import Path
import re
import shutil
from datetime import datetime, timedelta, timezone
import asyncio
import os
from dotenv import load_dotenv

import typer
from rich.console import Console
from rich.logging import RichHandler

from .config import load_config
from .github.api import GithubClient
from .git.repo import GitRepo
from .llm.client import LLMClient
from .report.generator import ReportGenerator

# Load environment variables from .env file at startup
load_dotenv()

app = typer.Typer()
console = Console()
logger = logging.getLogger(__name__)


def parse_time_duration(duration: str) -> timedelta:
    """Parse a human-readable time duration into a timedelta.

    Supports formats like:
    - '1 hour', '2 hours'
    - '1 day', '3 days'
    - '1 week', '2 weeks'
    - '1 month', '6 months'
    - '1 year', '3 years'
    - '1 year 6 months'
    """
    duration = duration.lower()
    total_days = 0
    total_seconds = 0

    # Extract all number-unit pairs, stripping plural 's' from unit
    pairs = re.findall(r"(\d+)\s*([a-z]+?)s?\b(?:\s+|$)", duration)
    if not pairs:
        raise ValueError(f"Could not parse time duration: {duration}")

    for value_str, unit in pairs:
        value = int(value_str)
        if unit in ("hour", "hr", "h"):
            total_seconds += value * 3600
        elif unit in ("day", "d"):
            total_days += value
        elif unit in ("week", "wk", "w"):
            total_days += value * 7
        elif unit in ("month", "mo", "m"):
            total_days += value * 30  # Approximate
        elif unit in ("year", "yr", "y"):
            total_days += value * 365  # Approximate
        else:
            raise ValueError(f"Unknown time unit: {unit}")

    return timedelta(days=total_days, seconds=total_seconds)


def parse_github_url(url: str) -> Tuple[str, str]:
    """Extract owner and repository name from a GitHub URL."""
    # Remove trailing slash if present
    url = url.rstrip("/")
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
    repo_url: str,
    output: Optional[Path] = None,
    active_within: Optional[str] = None,
    env_file: Optional[Path] = None,
    model: Optional[str] = None,
    context_length: Optional[int] = None,
    api_base_url: Optional[str] = typer.Option(
        None, "--api-base-url", help="OpenAI-compatible API base URL"
    ),
    api_key_env_var: Optional[str] = typer.Option(
        None,
        "--api-key-env-var",
        help="Environment variable containing the API key",
    ),
    parallel: int = typer.Option(
        5, "--parallel", "-p", help="Number of parallel requests"
    ),
    verbose: bool = False,
    clear_cache: bool = typer.Option(
        False, "--clear-cache", help="Clear cached repository data before analysis"
    ),
) -> None:
    """Analyze forks of a GitHub repository."""
    # Set up logging
    setup_logging(verbose)

    # Load config and apply overrides
    config = load_config(env_file, api_key_env_var=api_key_env_var)

    # Override config with command line options if provided
    if model is not None:
        config.model = model
    if context_length is not None:
        config.context_length = context_length
    if api_base_url is not None:
        config.openai_api_base_url = api_base_url

    # Log final configuration
    logger.info(f"Found GITHUB_TOKEN: {'yes' if config.github_token else 'no'}")
    logger.info(f"Using API key from: {config.api_key_source}")
    logger.info(f"Found API key: {'yes' if config.openai_api_key else 'no'}")
    logger.info(f"Using API base URL: {config.openai_api_base_url}")
    logger.info(f"Using CACHE_DIR: {config.cache_dir}")
    logger.info(f"Using MODEL: {config.model}")
    if config.context_length is not None:
        logger.info(f"Using CONTEXT_LENGTH override: {config.context_length}")

    # Initialize clients with parallel option
    github_client = GithubClient(config.github_token, max_parallel=parallel)
    llm_client = LLMClient(
        config.openai_api_key,
        model=config.model,
        context_length=config.context_length,
        api_base_url=config.openai_api_base_url,
        max_parallel=parallel,
    )

    try:
        # Parse repository URL
        owner, repo = parse_github_url(repo_url)
        repo_full_name = f"{owner}/{repo}"
        logger.debug(f"Analyzing repository: {repo_full_name}")

        # Set default output filename if none specified
        if output is None:
            output = Path(f"{owner}-{repo}-forks.md")
            logger.info(f"No output file specified, using default: {output}")

        # Parse active_within if provided
        activity_threshold = None
        if active_within:
            try:
                delta = parse_time_duration(active_within)
                activity_threshold = datetime.now(timezone.utc) - delta
                logger.info(f"Only considering forks active since {activity_threshold}")
            except ValueError as e:
                logger.error(f"Invalid active-within format: {e}")
                sys.exit(1)

        # Initialize report generator
        report_gen = ReportGenerator(llm_client)

        # Get repository and fork information
        repo_info = github_client.get_repository(repo_full_name)

        # Clear cache only if requested
        if clear_cache and config.cache_dir:
            repo_cache = config.cache_dir / f"{owner}-{repo}"
            clear_repo_cache(repo_cache)

        # Clone main repository
        git_repo = GitRepo(repo_info, config)

        # Get and filter forks
        forks = github_client.get_forks(repo_info)
        if activity_threshold:
            forks = [
                fork
                for fork in forks
                if datetime.fromisoformat(fork.last_updated) >= activity_threshold
            ]
            logger.info(f"Found {len(forks)} forks active within {active_within}")

        # Generate report
        report = report_gen.generate(repo_info, forks, git_repo)

        # Write report to file or stdout
        if str(output) == "-":
            console.print(report)
        else:
            output.write_text(report)
            logger.info(f"Report written to {output}")

    except Exception as e:
        logger.error(f"Error analyzing repository: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
