from pathlib import Path
from typing import Optional
import sys

from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os


class Config(BaseModel):
    github_token: str = Field(..., description="GitHub API token")
    openrouter_api_key: str = Field(..., description="OpenRouter API key")
    cache_dir: Path = Field(
        default=Path.home() / ".cache" / "git-fork-recon",
        description="Directory for caching repository data",
    )


def load_config(env_file: Optional[Path] = None) -> Config:
    """Load configuration from environment variables and .env file."""
    print("Loading config...", file=sys.stderr)
    print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
    print(f"Looking for .env file: {env_file or '.env'}", file=sys.stderr)

    if env_file:
        print(f"Loading .env from {env_file}", file=sys.stderr)
        load_dotenv(env_file)
    else:
        print("Loading .env from current directory", file=sys.stderr)
        load_dotenv()

    github_token = os.getenv("GITHUB_TOKEN")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    print(f"Found GITHUB_TOKEN: {'yes' if github_token else 'no'}", file=sys.stderr)
    print(
        f"Found OPENROUTER_API_KEY: {'yes' if openrouter_api_key else 'no'}",
        file=sys.stderr,
    )

    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is required", file=sys.stderr)
        sys.exit(1)
    if not openrouter_api_key:
        print(
            "Error: OPENROUTER_API_KEY environment variable is required",
            file=sys.stderr,
        )
        sys.exit(1)

    # Create config with model_validate to ensure proper type handling
    return Config.model_validate(
        {
            "github_token": github_token,
            "openrouter_api_key": openrouter_api_key,
            "cache_dir": os.getenv("CACHE_DIR")
            or str(Path.home() / ".cache" / "git-fork-recon"),
        }
    )
