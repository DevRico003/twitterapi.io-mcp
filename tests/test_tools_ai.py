import pytest
from unittest.mock import AsyncMock, MagicMock

from twitterapi.tools.ai_tools import (
    monitor_ai_influencers,
    analyze_ai_coding_trends,
    search_ai_development_topics
)

# Create fixture for context
@pytest.fixture
def mock_context():
    """Create a mock context with TwitterAPIContext"""
    context = MagicMock()
    twitter_ctx = AsyncMock()
    context.request_context.lifespan_context = twitter_ctx
    return context, twitter_ctx

# Test monitor_ai_influencers with different inputs
@pytest.mark.parametrize("usernames,days", [
    (["user1", "user2"], 7),
    (["karpathy"], 3),
    (["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11"], 7),  # More than 10 users
    (["user1"], 40)  # More than 30 days
])
async def test_monitor_ai_influencers_inputs(mock_context, usernames, days):
    """Test monitor_ai_influencers with different input parameters"""
    ctx, twitter_ctx = mock_context
    
    # Configure mock response
    twitter_ctx.get_influencer_tweets.return_value = {
        "username": "testuser",
        "high_engagement_tweets": [{
            "text": "High engagement test tweet",
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
            "likeCount": 100,
            "retweetCount": 50,
            "replyCount": 20,
            "engagement_score": 240
        }],
        "total_analyzed": 10,
        "lookback_days": days
    }
    
    result = await monitor_ai_influencers(usernames, days, ctx)
    
    # Check that limits were enforced
    effective_days = min(days, 30)
    effective_users = usernames[:10] if len(usernames) > 10 else usernames
    
    assert "AI Influencer Analysis" in result
    assert f"Past {effective_days} Days" in result
    
    # Verify number of API calls
    assert twitter_ctx.get_influencer_tweets.call_count == len(effective_users)

async def test_monitor_ai_influencers_empty_results(mock_context):
    """Test monitor_ai_influencers with empty results"""
    ctx, twitter_ctx = mock_context
    
    # Configure empty response
    twitter_ctx.get_influencer_tweets.return_value = {
        "username": "testuser",
        "high_engagement_tweets": [],
        "total_analyzed": 0,
        "lookback_days": 7
    }
    
    result = await monitor_ai_influencers(["testuser"], 7, ctx)
    
    assert "AI Influencer Analysis" in result
    assert "High-engagement tweets: 0" in result
    twitter_ctx.get_influencer_tweets.assert_called_once_with("testuser", 7)

async def test_monitor_ai_influencers_api_error(mock_context):
    """Test monitor_ai_influencers with API error"""
    ctx, twitter_ctx = mock_context
    
    # Configure exception
    twitter_ctx.get_influencer_tweets.side_effect = Exception("API error")
    
    result = await monitor_ai_influencers(["testuser"], 7, ctx)
    
    assert "No influencer data could be retrieved" in result
    twitter_ctx.get_influencer_tweets.assert_called_once_with("testuser", 7)

# Test analyze_ai_coding_trends
async def test_analyze_ai_coding_trends_success(mock_context):
    """Test analyze_ai_coding_trends success case"""
    ctx, twitter_ctx = mock_context
    
    # Configure mock response
    twitter_ctx.analyze_influencer_topics.return_value = {
        "influencers_analyzed": 2,
        "total_high_engagement_tweets": 10,
        "top_hashtags": [("ai", 5), ("python", 3), ("machinelearning", 2)],
        "trending_topics": [("ai", 8), ("python", 6), ("llm", 4)],
        "influencer_stats": {
            "user1": {"high_engagement_count": 5, "total_analyzed": 20},
            "user2": {"high_engagement_count": 5, "total_analyzed": 15}
        }
    }
    
    result = await analyze_ai_coding_trends(["user1", "user2"], 7, ctx)
    
    assert "AI Coding Trend Analysis" in result
    assert "#ai: 5 mentions" in result
    assert "python: 6 mentions" in result
    assert "Analysis based on 10 high-engagement tweets" in result
    assert "@user1: 5 high-engagement tweets" in result
    twitter_ctx.analyze_influencer_topics.assert_called_once_with(["user1", "user2"], 7)

# Test search_ai_development_topics
async def test_search_ai_development_topics_enhance_query(mock_context):
    """Test search_ai_development_topics query enhancement"""
    ctx, twitter_ctx = mock_context
    
    # Configure mock response
    twitter_ctx.search_tweets.return_value = {
        "tweets": [{
            "id": "123456",
            "text": "Test tweet about AI development",
            "author": {"userName": "testuser", "name": "Test User"},
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
            "likeCount": 10,
            "retweetCount": 5,
            "replyCount": 2
        }]
    }
    
    # Test with query that doesn't have AI or dev terms
    await search_ai_development_topics("transformers", "Top", 5, ctx)
    
    # Verify that the query was enhanced with AI and dev terms
    call_args = twitter_ctx.search_tweets.call_args[0]
    assert "transformers" in call_args[0]
    assert "AI" in call_args[0]
    assert "coding" in call_args[0]
    assert "Top" == call_args[1]
    assert 5 == call_args[2]

async def test_search_ai_development_topics_no_enhancement(mock_context):
    """Test search_ai_development_topics without query enhancement"""
    ctx, twitter_ctx = mock_context
    
    # Configure mock response
    twitter_ctx.search_tweets.return_value = {
        "tweets": [{
            "id": "123456",
            "text": "Test tweet about AI development",
            "author": {"userName": "testuser", "name": "Test User"},
            "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
            "likeCount": 10,
            "retweetCount": 5,
            "replyCount": 2
        }]
    }
    
    # Test with query that already has AI and dev terms
    await search_ai_development_topics("AI coding transformers", "Top", 5, ctx)
    
    # Verify that the query was not enhanced with redundant terms
    call_args = twitter_ctx.search_tweets.call_args[0]
    assert "AI coding transformers" in call_args[0]
    assert not "(AI OR 'artificial intelligence' OR ML)" in call_args[0]
    assert not "(coding OR development OR programming)" in call_args[0]
    assert "Top" == call_args[1]
    assert 5 == call_args[2]