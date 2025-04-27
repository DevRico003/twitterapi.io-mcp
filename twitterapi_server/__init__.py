"""
TwitterAPI.io MCP Server entry module.

This module serves as the entry point for the TwitterAPI.io MCP server.
"""

from twitterapi import mcp
import twitterapi.resources
import twitterapi.tools

def main():
    """Run the TwitterAPI.io MCP server."""
    print("Starting TwitterAPI.io MCP server...")
    print("Press Ctrl+C to stop.")
    mcp.run()

if __name__ == "__main__":
    main()