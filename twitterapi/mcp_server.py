"""
MCP Server module for Twitter API integration.

This module sets up the MCP server and its lifecycle management.
"""

import asyncio
import httpx
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Any

from mcp.server.fastmcp import FastMCP

from twitterapi.config import logger, API_KEY
from twitterapi.api_client import TwitterAPIContext

# Lifespan context manager
@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncIterator[TwitterAPIContext]:
    """
    Initialize and clean up TwitterAPI client.
    
    This context manager handles the lifecycle of the TwitterAPIContext,
    including setup, validation, and cleanup.
    
    Args:
        _: The FastMCP instance (not used directly)
        
    Yields:
        TwitterAPIContext: The initialized Twitter API context
        
    Raises:
        ValueError: If API key is missing or connection test fails
    """
    # API key validation handled by config module
    logger.info("Initializing TwitterAPI client")
    
    # Create HTTP client with timeout and limits
    timeout = httpx.Timeout(30.0, connect=10.0)
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    
    try:
        async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
            # Test connection by making a simple API call
            test_ctx = TwitterAPIContext(api_key=API_KEY, client=client)
            try:
                # Test with a known username (the Twitter API's own account)
                await test_ctx.get_user("twitterapi")
                logger.info("TwitterAPI connection test successful")
            except Exception as e:
                logger.error(f"TwitterAPI connection test failed: {str(e)}")
                raise ValueError(f"Could not connect to TwitterAPI: {str(e)}")
            
            # Create and yield the context
            yield TwitterAPIContext(api_key=API_KEY, client=client)
    except Exception as e:
        logger.error(f"Error in lifespan: {str(e)}")
        raise

# Create the MCP server
mcp = FastMCP(
    "TwitterAPI", 
    lifespan=lifespan,
    dependencies=["httpx", "asyncio", "datetime"],
    settings={
        "log_level": "INFO",  # Use uppercase log level
        "inject_context": True  # Inject context object automatically
    }
)