"""
TwitterAPI.io MCP Server package.

This package provides a Model Context Protocol (MCP) server that enables
AI applications to access and analyze Twitter data through TwitterAPI.io.
"""

from twitterapi.api_client import TwitterAPIContext
# Export main components for backward compatibility
from twitterapi.mcp_server import mcp, lifespan

__all__ = ["TwitterAPIContext", "mcp", "lifespan"]