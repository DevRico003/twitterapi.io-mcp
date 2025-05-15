# TwitterAPI.io MCP Server
Twitter Data Access Capabilities for AI Agents and AI Coding Assistants

A powerful implementation of the Model Context Protocol (MCP) integrated with TwitterAPI.io for providing AI agents and AI coding assistants with advanced Twitter data access capabilities.

With this MCP server, you can access tweets, user profiles, and search functionality and then use that knowledge anywhere.

## Overview
This MCP server provides tools that enable AI agents to access Twitter data through TwitterAPI.io's service, including retrieving tweets, user profiles, followers, and performing searches. It follows the best practices for building MCP servers.

## Features
- **Tweet Retrieval**: Get tweets by ID
- **User Profiles**: Access user profile information
- **Timeline Access**: Retrieve a user's recent tweets
- **Network Analysis**: Get user followers and following
- **Search Capabilities**: Search tweets with advanced query support
- **Replies Retrieval**: Get replies to specific tweets

## Tools
The server provides six essential Twitter data access tools:

- **get_tweet**: Get a tweet by its ID
- **get_user_profile**: Get a Twitter user's profile information
- **get_user_recent_tweets**: Get a user's recent tweets
- **search_tweets**: Search for tweets based on a query
- **get_user_followers**: Get a list of users who follow the specified user
- **get_user_following**: Get a list of users that the specified user follows

## Prerequisites
- Docker/Docker Desktop if running the MCP server as a container (recommended)
- Python 3.8+ if running the MCP server directly
- TwitterAPI.io API key

## Installation

### Using Docker (Recommended)
1. Clone this repository:
```bash
git clone https://github.com/yourusername/twitterapi.io-mcp.git
cd twitterapi.io-mcp
```

2. Build the Docker image:
```bash
docker build -t mcp/twitterapi-io --build-arg PORT=8051 .
```

3. Create a .env file based on the configuration section below

### Using Python directly (no Docker)
1. Clone this repository:
```bash
git clone https://github.com/yourusername/twitterapi.io-mcp.git
cd twitterapi.io-mcp
```

2. Install dependencies:
```bash
pip install -e .
```

3. Create a .env file based on the configuration section below

## Configuration
Create a `.env` file in the project root with the following variables:
```
# MCP Server Configuration
HOST=0.0.0.0
PORT=8051
TRANSPORT=sse

# TwitterAPI.io Configuration
TWITTER_API_KEY=your_twitterapi_io_key
```

## Running the Server

### Using Docker
```bash
docker run --env-file .env -p 8051:8051 mcp/twitterapi-io
```

### Using Python
```bash
python src/main.py
```

The server will start and listen on the configured host and port.

## Integration with MCP Clients

### SSE Configuration
Once you have the server running with SSE transport, you can connect to it using this configuration:

```json
{
  "mcpServers": {
    "twitterapi-mcp": {
      "transport": "sse",
      "url": "http://localhost:8051/sse"
    }
  }
}
```

Note for Windsurf users: Use `serverUrl` instead of `url` in your configuration:

```json
{
  "mcpServers": {
    "twitterapi-mcp": {
      "transport": "sse",
      "serverUrl": "http://localhost:8051/sse"
    }
  }
}
```

Note for Docker users: Use `host.docker.internal` instead of `localhost` if your client is running in a different container.

### Stdio Configuration
Add this server to your MCP configuration for Claude Desktop, Windsurf, or any other MCP client:

```json
{
  "mcpServers": {
    "twitterapi-mcp": {
      "command": "python",
      "args": ["path/to/twitterapi-mcp/src/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "TWITTER_API_KEY": "your_twitterapi_io_key"
      }
    }
  }
}
```

### Docker with Stdio Configuration
```json
{
  "mcpServers": {
    "twitterapi-mcp": {
      "command": "docker",
      "args": ["run", "--rm", "-i", 
               "-e", "TRANSPORT", 
               "-e", "TWITTER_API_KEY",
               "mcp/twitterapi-io"],
      "env": {
        "TRANSPORT": "stdio",
        "TWITTER_API_KEY": "your_twitterapi_io_key"
      }
    }
  }
}
```

## Usage Examples

```python
# Example of using the client with MCP
from mcp.client import Client

async with Client("twitterapi-mcp") as client:
    # Get a user profile
    user = await client.get_user_profile(username="twitterapi")
    print(user)
    
    # Search for tweets
    tweets = await client.search_tweets(query="python", count=5)
    print(tweets)
```

## License

MIT