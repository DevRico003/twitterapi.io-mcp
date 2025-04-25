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

# Test influencer tweet caching
async def test_get_influencer_tweets_caching(twitter_ctx):
    # Setup mock response for first call
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tweets": [{
            "id": "123456",
            "text": "Test tweet",
            "author": {"userName": "testuser", "name": "Test User"},
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
            "likeCount": 10,
            "retweetCount": 5,
            "replyCount": 2,
            "quoteCount": 1
        }]
    }
    mock_response.raise_for_status = AsyncMock()
    twitter_ctx.client.get.return_value = mock_response
    
    # First call
    result1 = await twitter_ctx.get_influencer_tweets("testuser")
    
    # Check cache
    assert "influencer_testuser" in twitter_ctx.influencer_cache
    
    # Reset mock for second call
    twitter_ctx.client.get.reset_mock()
    
    # Second call should use cache
    result2 = await twitter_ctx.get_influencer_tweets("testuser")
    
    # Verify cache was used (no new API call)
    twitter_ctx.client.get.assert_not_called()
    assert result1 == result2

# Test error handling
async def test_error_handling(twitter_ctx):
    # Setup mock to raise exception
    twitter_ctx.client.get.side_effect = httpx.HTTPError("API error")
    
    # Test with pytest.raises
    with pytest.raises(httpx.HTTPError):
        await twitter_ctx.get_tweet("123456")

# Test analyze_influencer_topics
async def test_analyze_influencer_topics(twitter_ctx):
    # Mock get_influencer_tweets to return predefined data
    async def mock_get_influencer_tweets(username, days_lookback=7, count=20):
        return {
            "username": username,
            "high_engagement_tweets": [
                {
                    "text": "Tweet about #AI and #Python",
                    "entities": {
                        "hashtags": [{"text": "AI"}, {"text": "Python"}]
                    },
                    "engagement_score": 100
                }
            ],
            "total_analyzed": 1
        }
    
    # Patch the method
    with patch.object(twitter_ctx, 'get_influencer_tweets', side_effect=mock_get_influencer_tweets):
        result = await twitter_ctx.analyze_influencer_topics(["user1", "user2"])
        
        # Verify results
        assert result["influencers_analyzed"] == 2
        assert "ai" in [tag for tag, count in result["top_hashtags"]]
        assert "python" in [tag for tag, count in result["top_hashtags"]]
        assert "user1" in result["influencer_stats"]
        assert "user2" in result["influencer_stats"]