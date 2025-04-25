"""
Tweet resources for TwitterAPI.io MCP server.

This module contains all tweet-related resource implementations.
"""

from mcp.server.fastmcp import Context

from twitterapi.config import logger
from twitterapi.mcp_server import mcp

@mcp.resource("tweet://{tweet_id}")
async def get_tweet_resource(tweet_id: str) -> str:
    """
    Get a tweet by ID resource.
    
    Args:
        tweet_id: The ID of the tweet to retrieve
        
    Returns:
        Formatted tweet data as a string
    """
    # Handle both runtime and test environments
    twitter_ctx = None
    
    # Check if the test context is available from the test module
    import sys
    if 'tests.test_resources' in sys.modules:
        test_module = sys.modules['tests.test_resources']
        if hasattr(test_module, '_TEST_CONTEXT'):
            twitter_ctx = test_module._TEST_CONTEXT
    try:
        result = await twitter_ctx.get_tweet(tweet_id)
        
        if not result.get("tweets"):
            return "Tweet not found"
        
        tweet = result["tweets"][0]
        author = tweet["author"]
        
        formatted = f"Tweet by @{author['userName']} ({author['name']}):\n\n"
        formatted += f"{tweet['text']}\n\n"
        formatted += f"Posted at: {tweet['createdAt']}\n"
        formatted += f"Likes: {tweet['likeCount']} | Retweets: {tweet['retweetCount']} | Replies: {tweet['replyCount']}"
        
        if tweet.get("entities", {}).get("hashtags"):
            hashtags = [f"#{tag['text']}" for tag in tweet["entities"]["hashtags"]]
            formatted += f"\nHashtags: {' '.join(hashtags)}"
        
        return formatted
    except Exception as e:
        logger.error(f"Error retrieving tweet {tweet_id}: {str(e)}")
        return f"Error retrieving tweet: {str(e)}"

@mcp.resource("tweet://{tweet_id}/replies")
async def get_tweet_replies_resource(tweet_id: str) -> str:
    """
    Get replies to a tweet resource.
    
    Args:
        tweet_id: The ID of the tweet
        
    Returns:
        Formatted reply data as a string
    """
    # Handle both runtime and test environments
    twitter_ctx = None
    
    # Check if the test context is available from the test module
    import sys
    if 'tests.test_resources' in sys.modules:
        test_module = sys.modules['tests.test_resources']
        if hasattr(test_module, '_TEST_CONTEXT'):
            twitter_ctx = test_module._TEST_CONTEXT
    try:
        result = await twitter_ctx.get_tweet_replies(tweet_id)
        
        if not result.get("tweets"):
            return "No replies found"
        
        formatted = f"Replies to tweet {tweet_id}:\n\n"
        
        for i, tweet in enumerate(result["tweets"], 1):
            author = tweet["author"]
            formatted += f"{i}. @{author['userName']} ({author['name']}): {tweet['text']}\n"
            formatted += f"   Likes: {tweet['likeCount']} | Posted at: {tweet['createdAt']}\n\n"
        
        return formatted
    except Exception as e:
        logger.error(f"Error retrieving replies for tweet {tweet_id}: {str(e)}")
        return f"Error retrieving replies: {str(e)}"

@mcp.resource("tweet://{tweet_id}/retweeters")
async def get_tweet_retweeters_resource(tweet_id: str) -> str:
    """
    Get users who retweeted a tweet resource.
    
    Args:
        tweet_id: The ID of the tweet
        
    Returns:
        Formatted retweeter data as a string
    """
    # Handle both runtime and test environments
    twitter_ctx = None
    
    # Check if the test context is available from the test module
    import sys
    if 'tests.test_resources' in sys.modules:
        test_module = sys.modules['tests.test_resources']
        if hasattr(test_module, '_TEST_CONTEXT'):
            twitter_ctx = test_module._TEST_CONTEXT
    try:
        result = await twitter_ctx.get_tweet_retweeters(tweet_id)
        
        if not result.get("users"):
            return "No retweeters found"
        
        formatted = f"Users who retweeted tweet {tweet_id}:\n\n"
        
        for i, user in enumerate(result["users"], 1):
            formatted += f"{i}. @{user['userName']} ({user['name']})\n"
            if user.get("description"):
                formatted += f"   Bio: {user['description']}\n"
            formatted += f"   Followers: {user['followers']} | Following: {user['following']}\n\n"
        
        return formatted
    except Exception as e:
        logger.error(f"Error retrieving retweeters for tweet {tweet_id}: {str(e)}")
        return f"Error retrieving retweeters: {str(e)}"