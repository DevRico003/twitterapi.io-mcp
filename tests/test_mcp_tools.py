import pytest
import asyncio
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta

from twitterapi.api_client import TwitterAPIContext
from mcp.server.fastmcp import Context

# Mock Context for testing
@pytest.fixture
def mock_context():
    context = MagicMock()
    twitter_ctx = AsyncMock()
    
    # Setup required request_context attributes
    context.request_context = MagicMock()
    context.request_context.lifespan_context = twitter_ctx
    
    return context, twitter_ctx

# Test get_tweet tool
async def test_get_tweet_tool():
    from twitterapi.tools.basic_tools import get_tweet
    
    # Create mocks
    ctx, twitter_ctx = MagicMock(), AsyncMock()
    ctx.request_context.lifespan_context = twitter_ctx
    
    # Configure mock response
    twitter_ctx.get_tweet.return_value = {
        "tweets": [{
            "id": "123456",
            "text": "Test tweet",
            "author": {"userName": "testuser", "name": "Test User"},
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
            "likeCount": 10,
            "retweetCount": 5,
            "replyCount": 2
        }]
    }
    
    # Call tool function
    result = await get_tweet("123456", ctx)
    
    # Verify
    assert "Test tweet" in result
    assert "@testuser" in result
    twitter_ctx.get_tweet.assert_called_once_with("123456")

# Test search_tweets tool
async def test_search_tweets_tool():
    from twitterapi.tools.basic_tools import search_tweets
    
    # Create mocks
    ctx, twitter_ctx = MagicMock(), AsyncMock()
    ctx.request_context.lifespan_context = twitter_ctx
    
    # Configure mock response
    twitter_ctx.search_tweets.return_value = {
        "tweets": [{
            "id": "123456",
            "text": "Test tweet",
            "author": {"userName": "testuser", "name": "Test User"},
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
            "likeCount": 10,
            "retweetCount": 5,
            "replyCount": 2
        }],
        "has_next_page": True,
        "next_cursor": "cursor123"
    }
    
    # Call tool function
    result = await search_tweets("test query", "Latest", 10, ctx)
    
    # Verify
    assert "Test tweet" in result
    assert "More results available" in result
    assert "cursor123" in result
    twitter_ctx.search_tweets.assert_called_once_with("test query", "Latest", 10)