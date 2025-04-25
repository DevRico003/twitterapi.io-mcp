# TwitterAPI.io MCP Server

![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

A Model Context Protocol (MCP) server that provides LLM applications with access to Twitter data through the TwitterAPI.io service. This server enables AI assistants like Claude to retrieve and analyze tweets, user profiles, and other Twitter data in a structured way, with special enhancements for AI development trend analysis.

## 🚀 Features

### Resources
- Tweet data by ID (`tweet://{tweet_id}`)
- Tweet replies (`tweet://{tweet_id}/replies`)
- Tweet retweeters (`tweet://{tweet_id}/retweeters`)
- User profiles (`user://{username}`)
- User tweets (`user://{username}/tweets`)
- User followers (`user://{username}/followers`)
- User following (`user://{username}/following`)

### Tools
- Basic Twitter operations (get tweet, get user profile, search tweets)
- AI-specific analysis tools for monitoring influencers and trends
- Advanced search capabilities for AI development topics

### AI Development Capabilities
- Monitor 23 pre-configured AI influencers
- Analyze engagement metrics and trending topics
- Research specific AI development topics
- Generate content ideas based on trends

## 📋 Requirements

- Python 3.8 or higher
- TwitterAPI.io API key

## 🔧 Installation

### Option 1: Direct Installation from PyPI (Recommended)
```bash
# Install with pip
pip install twitterapi-mcp

# or with uv for better performance
uv pip install twitterapi-mcp
```

### Option 2: Use with MCP in Claude Desktop (No Installation)
You can use the server directly through uv run by adding to your `.mcp.json` file:
```json
"twitterapi-mcp": {
  "command": "uv",
  "args": [
    "run",
    "twitterapi-mcp"
  ],
  "env": {
    "TWITTER_API_KEY": "your_api_key_here"
  }
}
```

### Option 3: From Source
1. Clone this repository:
```bash
git clone https://github.com/DevRico003/twitterapi.io-mcp.git
cd twitterapi.io-mcp
```

2. Install as development package:
```bash
pip install -e .
```

3. Configure your TwitterAPI.io API key using environment variables or a `.env` file:
```
TWITTER_API_KEY=your_api_key_here
LOG_LEVEL=INFO
CACHE_TTL=3600
MAX_TWEETS=100
```

## 🚀 Usage

### Running the Server

Run directly with Python:
```bash
python twitterapi_server.py
```

Or use the MCP development mode:
```bash
mcp dev twitterapi_server.py
```

### Install in Claude Desktop

```bash
# If you have the package installed:
mcp install -m twitterapi-mcp --name "Twitter AI Analysis"

# Or directly from the code:
mcp install twitterapi_server.py --name "Twitter AI Analysis"
```

## ⚙️ Configuration

The server supports the following environment variables:
- `TWITTER_API_KEY` (required): Your TwitterAPI.io API key
- `LOG_LEVEL` (optional): Logging level (default: INFO)
- `CACHE_TTL` (optional): Cache timeout in seconds (default: 3600/1 hour) 
- `MAX_TWEETS` (optional): Maximum tweets per request (default: 100)

## 📁 Project Structure

```
twitterapi/
  __init__.py            # Package exports
  api_client.py          # TwitterAPI client
  config.py              # Configuration and constants
  mcp_server.py          # MCP server setup
  utils.py               # Utility functions
  resources/             # Resource implementations
    __init__.py
    tweet_resources.py
    user_resources.py
  tools/                 # Tool implementations
    __init__.py
    basic_tools.py
    ai_tools.py
  prompts/               # Prompt templates
    __init__.py
    ai_prompts.py
twitterapi_server.py     # Main entry point
```

## 🧪 Testing

Run the tests with pytest:
```bash
python -m pytest
```

You can run specific test modules:
```bash
python -m pytest tests/test_utils.py
python -m pytest tests/test_api_client.py
```

## 📊 API Cost Considerations

TwitterAPI.io charges approximately $0.15 per 1,000 tweets retrieved. This server implements caching with a configurable TTL to reduce API costs while maintaining fresh data. The cache is particularly effective for frequently monitored influencers and popular searches.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.