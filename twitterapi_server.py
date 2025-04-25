"""
TwitterAPI.io MCP Server.

This is the main entry point for running the TwitterAPI.io MCP server.
It provides a high-level interface for users and handles importing 
all necessary modules.
"""

# Import and register all components needed for the server
import twitterapi
from twitterapi import mcp

# Import resources
import twitterapi.resources

# Import tools
import twitterapi.tools

# Import prompts
import twitterapi.prompts

# Re-export main component for backward compatibility
from twitterapi import mcp

def main():
    # Run the server when called as a module or script
    print("Starting TwitterAPI.io MCP server...")
    print("Press Ctrl+C to stop.")
    mcp.run()

if __name__ == "__main__":
    main()