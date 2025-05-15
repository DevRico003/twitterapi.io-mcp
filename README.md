# TwitterAPI.io MCP Server

MCP server for Twitter API.io integration, allowing AI assistants to access Twitter data through a structured API.

## Features

- Fetch tweets by ID
- Get user profiles
- Retrieve user tweets
- Get user followers and following
- Search tweets with query support

## Requirements

- Python 3.8+
- An API key from [TwitterAPI.io](https://twitterapi.io/)

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/yourusername/twitterapi.io-mcp.git
cd twitterapi.io-mcp

# Install dependencies
pip install -e .
```

### For Claude Desktop

```bash
mcp install twitterapi.io-mcp
```

## Configuration

Create a `.env` file in the project root directory:

```
TWITTER_API_KEY=your_api_key_here
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8051
```

## Usage

### Running the server

```bash
# Run the server
python -m src.twitterapi_mcp
```

### Development mode

```bash
mcp dev src/twitterapi_mcp.py
```

### Examples

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

## Tools

| Tool | Description |
|------|-------------|
| `get_tweet` | Get a tweet by ID |
| `get_user_profile` | Get a user's profile information |
| `get_user_recent_tweets` | Get a user's recent tweets |
| `search_tweets` | Search for tweets using Twitter search syntax |
| `get_user_followers` | Get a list of users who follow the specified user |
| `get_user_following` | Get a list of users that the specified user follows |

## License

MIT