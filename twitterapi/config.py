"""
Configuration module for the TwitterAPI.io MCP server.

This module contains constants, configuration values, and logging setup.
It loads environment variables from .env files using the utils module.
"""

import os
import logging
from typing import Dict, List, Any, Optional

from twitterapi.utils import load_environment

# Load environment variables from .env files
load_environment()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("twitterapi-mcp")

# Environment variable configuration
def get_env_var(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get an environment variable with validation.

    Args:
        name: Name of the environment variable
        default: Default value if environment variable is not set
        required: Whether the environment variable is required

    Returns:
        The environment variable value or default

    Raises:
        ValueError: If the environment variable is required but not set
    """
    value = os.environ.get(name, default)
    if required and value is None:
        logger.error(f"{name} environment variable is required")
        raise ValueError(f"{name} environment variable is required")
    return value

# API Configuration
API_KEY = get_env_var("TWITTER_API_KEY", required=True)
BASE_URL = get_env_var("TWITTER_API_BASE_URL", "https://api.twitterapi.io")
LOG_LEVEL = get_env_var("LOG_LEVEL", "INFO")
CACHE_TTL = int(get_env_var("CACHE_TTL", "3600"))  # Default: 1 hour
MAX_TWEETS = int(get_env_var("MAX_TWEETS", "100"))

# Set log level from environment
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logger.setLevel(log_level)

# Default influencers list removed for neutrality.
# Users should provide specific influencers via tool arguments if needed.

# AI-specific topic keywords removed for neutrality.
# Topic analysis should be driven by user input if needed.