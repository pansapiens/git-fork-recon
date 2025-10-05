#!/usr/bin/env python

"""CLI for the git-fork-recon server."""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from dotenv import load_dotenv

from .app import create_app

app = typer.Typer()
console = Console()
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


@app.command()
def main(
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help="Host to bind the server to",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        help="Port to bind the server to",
    ),
    reload: bool = typer.Option(
        False,
        "--reload",
        help="Enable auto-reload for development",
    ),
    log_level: str = typer.Option(
        "info",
        "--log-level",
        help="Log level (debug, info, warning, error)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging",
    ),
) -> None:
    """Start the git-fork-recon server."""
    # Load .env file from current directory
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        logger.debug(f"Loading .env file from {env_path}")
        load_dotenv(env_path, override=True)
    else:
        logger.debug("No .env file found in current directory")

    # Set up logging
    setup_logging(verbose)

    # Set environment variables from command line overrides
    if host != "127.0.0.1":
        os.environ["SERVER_HOST"] = host
    if port != 8000:
        os.environ["SERVER_PORT"] = str(port)

    # Import uvicorn and start the server
    try:
        import uvicorn
    except ImportError:
        console.print("[red]Error: uvicorn is required to run the server[/red]")
        console.print("Install it with: pip install 'git-fork-recon[server]'")
        raise typer.Exit(1)

    # Show startup information
    console.print(f"[green]Starting Git Fork Recon server[/green]")
    console.print(f"Host: {host}")
    console.print(f"Port: {port}")
    console.print(f"Reload: {'Yes' if reload else 'No'}")
    console.print(f"Log level: {log_level}")

    if os.getenv("DISABLE_AUTH") == "1":
        console.print("[yellow]Authentication is disabled[/yellow]")
    else:
        console.print("Authentication is enabled")

    if os.getenv("ALLOWED_MODELS"):
        console.print(f"Allowed models: {os.getenv('ALLOWED_MODELS')}")

    console.print(f"Cache directory: {os.getenv('SERVER_CACHE_DIR', '.cache')}")
    console.print(f"Max parallel tasks: {os.getenv('PARALLEL_TASKS', '2')}")
    console.print("")

    # Start the server
    uvicorn.run(
        "git_fork_recon_server.app:create_app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        factory=True,
    )


if __name__ == "__main__":
    app()