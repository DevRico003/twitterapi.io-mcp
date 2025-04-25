# TwitterAPI.io MCP Server

A Model Context Protocol (MCP) server that provides LLM applications with access to Twitter data through the TwitterAPI.io service. This server enables AI assistants to retrieve and analyze tweets, user profiles, and other Twitter data in a structured and controlled manner, with special enhancements for AI development trend analysis.

## Features

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

## Installation

### Prerequisites
- Python 3.8 or higher
- TwitterAPI.io API key

### Setup

1. Clone this repository:
```
git clone https://github.com/yourusername/twitterapi-mcp.git
cd twitterapi-mcp
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Configure your TwitterAPI.io API key:

Create a `.env` file in the `twitterapi` directory with the following content:
```
TWITTER_API_KEY=your_api_key_here
LOG_LEVEL=INFO
CACHE_TTL=3600
MAX_TWEETS=100
```

### Running the Server

Run directly with Python:
```
python twitterapi_server.py
```

Or use the MCP development mode:
```
mcp dev twitterapi_server.py
```

### Install in Claude Desktop

To install in Claude Desktop:
```
mcp install twitterapi_server.py --name "Twitter AI Analysis"
```

## Configuration

The server supports the following environment variables:
- `TWITTER_API_KEY` (required): Your TwitterAPI.io API key
- `LOG_LEVEL` (optional): Logging level (default: INFO)
- `CACHE_TTL` (optional): Cache timeout in seconds (default: 3600/1 hour)
- `MAX_TWEETS` (optional): Maximum tweets per request (default: 100)

## Project Structure

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

## Usage Examples

### Getting a Tweet
```
URI: tweet://1234567890
```

### Getting a User Profile
```
URI: user://karpathy
```

### Tools
- `get_tweet(tweet_id)`
- `get_user_profile(username)`
- `search_tweets(query, query_type, count)`
- `monitor_ai_influencers(influencer_usernames, days_lookback)`
- `analyze_ai_coding_trends(influencer_usernames, days_lookback)`
- `search_ai_development_topics(query, query_type, count)`

### Prompts
- `analyze_ai_coding_influencers(influencers)`
- `ai_development_trend_analysis(days, influencers)`
- `research_ai_development_topic(topic)`
- `create_ai_development_post_ideas(topic, influencers)`

## Unit Tests

Run the tests with pytest:
```
python -m pytest
```

You can run specific test modules:
```
python -m pytest tests/test_utils.py
python -m pytest tests/test_api_client.py
```

## API Cost Considerations

TwitterAPI.io charges approximately $0.15 per 1,000 tweets retrieved. This server implements caching with a configurable TTL to reduce API costs while maintaining fresh data. The cache is particularly effective for frequently monitored influencers and popular searches.

## License

MIT