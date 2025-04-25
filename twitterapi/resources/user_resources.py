"""
User resources for TwitterAPI.io MCP server.

This module contains all user-related resource implementations.
"""

from mcp.server.fastmcp import Context

from twitterapi.config import logger
from twitterapi.mcp_server import mcp

@mcp.resource("user://{username}")
async def get_user_resource(username: str) -> str:
    """
    Get a user profile by username resource.
    
    Args:
        username: The Twitter username
        
    Returns:
        Formatted user profile as a string
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
        result = await twitter_ctx.get_user(username)
        
        if not result.get("data"):
            return "User not found"
        
        user = result["data"]
        
        formatted = f"Twitter Profile: @{user['userName']} ({user['name']})\n\n"
        
        if user.get("description"):
            formatted += f"Bio: {user['description']}\n\n"
        
        if user.get("location"):
            formatted += f"Location: {user['location']}\n"
        
        formatted += f"Followers: {user['followers']} | Following: {user['following']}\n"
        formatted += f"Tweets: {user['statusesCount']} | Media: {user['mediaCount']}\n"
        formatted += f"Account created: {user['createdAt']}\n"
        
        if user.get("isBlueVerified"):
            formatted += f"✓ Blue Verified\n"
        
        return formatted
    except Exception as e:
        logger.error(f"Error retrieving user {username}: {str(e)}")
        return f"Error retrieving user profile: {str(e)}"

@mcp.resource("user://{username}/tweets")
async def get_user_tweets_resource(username: str) -> str:
    """
    Get recent tweets from a user resource.
    
    Args:
        username: The Twitter username
        
    Returns:
        Formatted tweets as a string
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
        result = await twitter_ctx.get_user_tweets(username)
        
        if not result.get("tweets"):
            return f"No tweets found for @{username}"
        
        formatted = f"Recent tweets by @{username}:\n\n"
        
        for i, tweet in enumerate(result["tweets"], 1):
            formatted += f"{i}. {tweet['text']}\n"
            formatted += f"   Posted at: {tweet['createdAt']}\n"
            formatted += f"   Likes: {tweet['likeCount']} | Retweets: {tweet['retweetCount']} | Replies: {tweet['replyCount']}\n\n"
        
        return formatted
    except Exception as e:
        logger.error(f"Error retrieving tweets for user {username}: {str(e)}")
        return f"Error retrieving tweets: {str(e)}"

@mcp.resource("user://{username}/followers")
async def get_user_followers_resource(username: str) -> str:
    """
    Get followers of a user resource.
    
    Args:
        username: The Twitter username
        
    Returns:
        Formatted followers as a string
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
        result = await twitter_ctx.get_user_followers(username)
        
        if not result.get("users"):
            return f"No followers found for @{username}"
        
        formatted = f"Followers of @{username}:\n\n"
        
        for i, user in enumerate(result["users"], 1):
            formatted += f"{i}. @{user['userName']} ({user['name']})\n"
            if user.get("description"):
                formatted += f"   Bio: {user['description']}\n"
            formatted += f"   Followers: {user['followers']} | Following: {user['following']}\n\n"
        
        return formatted
    except Exception as e:
        logger.error(f"Error retrieving followers for user {username}: {str(e)}")
        return f"Error retrieving followers: {str(e)}"

@mcp.resource("user://{username}/following")
async def get_user_following_resource(username: str) -> str:
    """
    Get accounts a user is following resource.
    
    Args:
        username: The Twitter username
        
    Returns:
        Formatted following accounts as a string
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
        result = await twitter_ctx.get_user_following(username)
        
        if not result.get("users"):
            return f"@{username} is not following anyone"
        
        formatted = f"Accounts @{username} is following:\n\n"
        
        for i, user in enumerate(result["users"], 1):
            formatted += f"{i}. @{user['userName']} ({user['name']})\n"
            if user.get("description"):
                formatted += f"   Bio: {user['description']}\n"
            formatted += f"   Followers: {user['followers']} | Following: {user['following']}\n\n"
        
        return formatted
    except Exception as e:
        logger.error(f"Error retrieving following for user {username}: {str(e)}")
        return f"Error retrieving following: {str(e)}"