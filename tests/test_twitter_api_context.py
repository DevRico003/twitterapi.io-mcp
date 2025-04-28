import pytest
import asyncio
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import time

from twitterapi.api_client import TwitterAPIContext

# Test fixture for API context
@pytest.fixture
def twitter_ctx():
    mock_client = AsyncMock()
    return TwitterAPIContext(api_key="test_key", client=mock_client)

# Test get_tweet method
async def test_get_tweet(twitter_ctx):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {
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
    mock_response.raise_for_status = AsyncMock()
    twitter_ctx.client.get.return_value = mock_response

    # Call method
    result = await twitter_ctx.get_tweet("123456")

    # Verify
    assert result["tweets"][0]["text"] == "Test tweet"
    twitter_ctx.client.get.assert_called_once()
    assert "test_key" in twitter_ctx.client.get.call_args[1]["headers"]["x-api-key"]

# Test get_user method
async def test_get_user(twitter_ctx):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "userName": "testuser",
            "name": "Test User",
            "description": "Test bio",
            "followers": 100,
            "following": 50,
            "statusesCount": 500,
            "mediaCount": 20,
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025"
        }
    }
    mock_response.raise_for_status = AsyncMock()
    twitter_ctx.client.get.return_value = mock_response

    # Call method
    result = await twitter_ctx.get_user("testuser")

    # Verify
    assert result["data"]["userName"] == "testuser"
    twitter_ctx.client.get.assert_called_once()

# Test for get_influencer_tweets removed as method was deleted for neutrality.

# Test error handling
async def test_error_handling(twitter_ctx):
    # Setup mock to raise exception
    twitter_ctx.client.get.side_effect = httpx.HTTPError("API error")

    # Test with pytest.raises
    with pytest.raises(httpx.HTTPError):
        await twitter_ctx.get_tweet("123456")
