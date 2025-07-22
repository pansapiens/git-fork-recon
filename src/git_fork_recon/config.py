from pathlib import Path
from typing import Optional
import sys
from platformdirs import user_cache_dir
import logging

from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)


class Config(BaseModel):
    github_token: str = Field(..., description="GitHub API token")
    openai_api_key: str = Field(..., description="OpenAI-compatible API key")
    api_key_source: str = Field(
        ..., description="Environment variable that provided the API key"
    )
    openai_api_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenAI-compatible API base URL",
    )
    cache_dir: Path = Field(
        default=Path.home() / ".cache" / "git-fork-recon",
        description="Directory for caching repository data",
    )
    model: str = Field(
        default="deepseek/deepseek-chat-v3-0324:free",
        description="OpenRouter model to use",
    )
    context_length: Optional[int] = Field(
        default=None,
        description="Override model context length (if not set, uses OpenRouter API value)",
    )


def load_config(
    env_file: Optional[Path] = None,
    api_key_env_var: Optional[str] = None,
) -> Config:
    """Load configuration from environment variables and .env file."""
    logger.debug("Loading config...")
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug(f"Looking for .env file: {env_file or '.env'}")

    # Only load from env_file if explicitly provided
    if env_file:
        logger.info(f"Loading .env from {env_file}")
        load_dotenv(env_file, override=True)
    else:
        # Try loading the default .env file from the current working directory
        logger.debug("Attempting to load default .env file from current directory")
        dotenv_path = Path(os.getcwd()) / ".env"
        dotenv_loaded = load_dotenv(dotenv_path=dotenv_path, override=True)
        logger.debug(f"load_dotenv() result: {dotenv_loaded} from path: {dotenv_path}")

    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_base_url = os.getenv(
        "OPENAI_API_BASE_URL", "https://openrouter.ai/api/v1"
    )

    # Get API key based on precedence rules
    openai_api_key = None
    api_key_source = None

    if api_key_env_var:
        # If api_key_env_var is specified, try that first
        openai_api_key = os.getenv(api_key_env_var)
        if openai_api_key:
            api_key_source = api_key_env_var

    if not openai_api_key:
        # If no key found and using OpenRouter, try OPENROUTER_API_KEY
        if "/openrouter.ai/" in openai_api_base_url:
            openai_api_key = os.getenv("OPENROUTER_API_KEY")
            if openai_api_key:
                api_key_source = "OPENROUTER_API_KEY"
        # Otherwise try OPENAI_API_KEY
        else:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key:
                api_key_source = "OPENAI_API_KEY"

    cache_dir = os.getenv("CACHE_DIR") or user_cache_dir("git-fork-recon")
    model = os.getenv("MODEL") or "deepseek/deepseek-chat-v3-0324:free"
    context_length = os.getenv("CONTEXT_LENGTH")
    if context_length is not None:
        try:
            context_length = int(context_length)
        except ValueError:
            logger.error(f"CONTEXT_LENGTH must be an integer, got {context_length}")
            sys.exit(1)

    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    if not openai_api_key:
        logger.error(
            "OPENAI_API_KEY or OPENROUTER_API_KEY environment variable is required"
        )
        sys.exit(1)

    # Create config with model_validate to ensure proper type handling
    return Config.model_validate(
        {
            "github_token": github_token,
            "openai_api_key": openai_api_key,
            "api_key_source": api_key_source,
            "openai_api_base_url": openai_api_base_url,
            "cache_dir": cache_dir,
            "model": model,
            "context_length": context_length,
        }
    )
