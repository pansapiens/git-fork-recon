from pathlib import Path
from typing import Optional

import typer

from .main import analyze

app = typer.Typer()


@app.command()
def main(
    repo_url: str = typer.Argument(..., help="URL of the GitHub repository to analyze"),
    output: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file path (defaults to {repo_name}-forks.md)",
    ),
    active_within: Optional[str] = typer.Option(
        None,
        "--active-within",
        help="Only consider forks with activity within this time period (e.g. '1 hour', '2 days', '6 months', '1 year')",
    ),
    env_file: Optional[Path] = typer.Option(
        None,
        "--env-file",
        help="Path to .env file",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        help="OpenRouter model to use (overrides MODEL env var)",
    ),
    context_length: Optional[int] = typer.Option(
        None,
        "--context-length",
        help="Override model context length (overrides CONTEXT_LENGTH env var)",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging"
    ),
) -> None:
    """Analyze a GitHub repository's fork network and generate a summary report."""
    analyze(
        repo_url=repo_url,
        output=output,
        active_within=active_within,
        env_file=env_file,
        model=model,
        context_length=context_length,
        verbose=verbose,
    )
