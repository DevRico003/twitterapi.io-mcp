import pytest
from unittest.mock import AsyncMock, MagicMock

from twitterapi.resources.tweet_resources import (
    get_tweet_resource, 
    get_tweet_replies_resource, 
    get_tweet_retweeters_resource
)
from twitterapi.resources.user_resources import (
    get_user_resource,
    get_user_tweets_resource,
    get_user_followers_resource,
    get_user_following_resource
)

# Global variable for context injection
_TEST_CONTEXT = None

# Test fixtures for resources
@pytest.fixture
def mock_context():
    """Create a mock context with TwitterAPIContext"""
    context = MagicMock()
    twitter_ctx = AsyncMock()
    context.request_context.lifespan_context = twitter_ctx
    
    # Store the context in a module global
    global _TEST_CONTEXT
    _TEST_CONTEXT = twitter_ctx
    
    return context, twitter_ctx

# Tweet resource tests
async def test_get_tweet_resource_success(mock_context):
    """Test successful tweet retrieval"""
    ctx, twitter_ctx = mock_context
    
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
    
    # Make ctx available in the global scope for frame inspection
    globals()['ctx_for_test'] = ctx
    result = await get_tweet_resource("123456")
    
    assert "Test tweet" in result
    assert "@testuser" in result
    twitter_ctx.get_tweet.assert_called_once_with("123456")

async def test_get_tweet_resource_not_found(mock_context):
    """Test tweet not found"""
    ctx, twitter_ctx = mock_context
    
    # Configure empty response
    twitter_ctx.get_tweet.return_value = {"tweets": []}
    
    globals()['ctx_for_test'] = ctx
    result = await get_tweet_resource("123456")
    
    assert "Tweet not found" == result
    twitter_ctx.get_tweet.assert_called_once_with("123456")

async def test_get_tweet_resource_error(mock_context):
    """Test error handling in tweet resource"""
    ctx, twitter_ctx = mock_context
    
    # Configure exception
    twitter_ctx.get_tweet.side_effect = Exception("API error")
    
    globals()['ctx_for_test'] = ctx
    result = await get_tweet_resource("123456")
    
    assert "Error retrieving tweet:" in result
    twitter_ctx.get_tweet.assert_called_once_with("123456")

# User resource tests
async def test_get_user_resource_success(mock_context):
    """Test successful user profile retrieval"""
    ctx, twitter_ctx = mock_context
    
    # Configure mock response
    twitter_ctx.get_user.return_value = {
        "data": {
            "userName": "testuser",
            "name": "Test User",
            "description": "Test bio",
            "location": "Test Location",
            "followers": 100,
            "following": 50,
            "statusesCount": 500,
            "mediaCount": 20,
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
            "isBlueVerified": True
        }
    }
    
    globals()['ctx_for_test'] = ctx
    result = await get_user_resource("testuser")
    
    assert "Twitter Profile: @testuser" in result
    assert "Test bio" in result
    assert "Test Location" in result
    assert "Followers: 100" in result
    assert "✓ Blue Verified" in result
    twitter_ctx.get_user.assert_called_once_with("testuser")

async def test_get_user_resource_not_found(mock_context):
    """Test user not found"""
    ctx, twitter_ctx = mock_context
    
    # Configure empty response
    twitter_ctx.get_user.return_value = {}
    
    globals()['ctx_for_test'] = ctx
    result = await get_user_resource("testuser")
    
    assert "User not found" == result
    twitter_ctx.get_user.assert_called_once_with("testuser")

# User tweets resource tests
async def test_get_user_tweets_resource_success(mock_context):
    """Test successful user tweets retrieval"""
    ctx, twitter_ctx = mock_context
    
    # Configure mock response
    twitter_ctx.get_user_tweets.return_value = {
        "tweets": [
            {
                "id": "123456",
                "text": "Test tweet 1",
                "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
                "likeCount": 10,
                "retweetCount": 5,
                "replyCount": 2
            },
            {
                "id": "654321",
                "text": "Test tweet 2",
                "createdAt": "Wed Apr 25 09:00:00 +0000 2025",
                "likeCount": 20,
                "retweetCount": 15,
                "replyCount": 12
            }
        ]
    }
    
    globals()['ctx_for_test'] = ctx
    result = await get_user_tweets_resource("testuser")
    
    assert "Recent tweets by @testuser" in result
    assert "Test tweet 1" in result
    assert "Test tweet 2" in result
    assert "Likes: 10" in result
    assert "Likes: 20" in result
    twitter_ctx.get_user_tweets.assert_called_once_with("testuser")

async def test_get_user_tweets_resource_empty(mock_context):
    """Test no tweets found"""
    ctx, twitter_ctx = mock_context
    
    # Configure empty response
    twitter_ctx.get_user_tweets.return_value = {"tweets": []}
    
    globals()['ctx_for_test'] = ctx
    result = await get_user_tweets_resource("testuser")
    
    assert "No tweets found for @testuser" == result
    twitter_ctx.get_user_tweets.assert_called_once_with("testuser")