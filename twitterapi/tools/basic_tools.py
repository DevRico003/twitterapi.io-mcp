"""
Basic tools for TwitterAPI.io MCP server.

This module contains standard tool implementations for working with Twitter data.
"""

from typing import Optional

from mcp.server.fastmcp import Context

from twitterapi.config import MAX_TWEETS
from twitterapi.mcp_server import mcp

@mcp.tool()
async def get_tweet(tweet_id: str, ctx: Context) -> str:
    """
    Get a tweet by its ID.
    
    Args:
        tweet_id: The ID of the tweet to retrieve
        ctx: The MCP context
        
    Returns:
        Formatted tweet information
    """
    twitter_ctx = ctx.request_context.lifespan_context
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
        return f"Error retrieving tweet: {str(e)}"

@mcp.tool()
async def get_user_profile(username: str, ctx: Context) -> str:
    """
    Get a Twitter user's profile information.
    
    Args:
        username: The Twitter username without the @ symbol
        ctx: The MCP context
        
    Returns:
        Formatted user profile information
    """
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_user(username)
        
        if not result.get("data"):
            return f"User @{username} not found"
        
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
        return f"Error retrieving user profile: {str(e)}"

@mcp.tool()
async def get_user_recent_tweets(username: str, ctx: Context, count: int = 10) -> str:
    """
    Get a user's recent tweets.
    
    Args:
        username: The Twitter username without the @ symbol
        count: Number of tweets to retrieve (default: 10, max: 100)
        ctx: The MCP context
        
    Returns:
        Formatted list of user's recent tweets
    """
    if count > MAX_TWEETS:
        count = MAX_TWEETS  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_user_tweets(username, count)
        
        if not result.get("tweets"):
            return f"No tweets found for @{username}"
        
        formatted = f"Recent tweets by @{username}:\n\n"
        
        for i, tweet in enumerate(result["tweets"], 1):
            formatted += f"{i}. {tweet['text']}\n"
            formatted += f"   Posted at: {tweet['createdAt']}\n"
            formatted += f"   Likes: {tweet['likeCount']} | Retweets: {tweet['retweetCount']} | Replies: {tweet['replyCount']}\n\n"
        
        return formatted
    except Exception as e:
        return f"Error retrieving tweets: {str(e)}"

@mcp.tool()
async def search_tweets(query: str, ctx: Context, query_type: str = "Latest", count: int = 10) -> str:
    """
    Search for tweets based on a query.
    
    Args:
        query: The search query (can use Twitter search operators)
        query_type: Type of search, either "Latest" or "Top" (default: "Latest")
        count: Number of results to return (default: 10, max: 50)
        ctx: The MCP context
        
    Returns:
        Formatted search results
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    if query_type not in ["Latest", "Top"]:
        query_type = "Latest"  # Enforce valid values
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.search_tweets(query, query_type, count)
        
        if not result.get("tweets"):
            return f"No tweets found for query: {query}"
        
        formatted = f"Search results for \"{query}\" ({query_type}):\n\n"
        
        for i, tweet in enumerate(result["tweets"], 1):
            author = tweet["author"]
            formatted += f"{i}. @{author['userName']} ({author['name']}): {tweet['text']}\n"
            formatted += f"   Posted at: {tweet['createdAt']}\n"
            formatted += f"   Likes: {tweet['likeCount']} | Retweets: {tweet['retweetCount']} | Replies: {tweet['replyCount']}\n\n"
        
        # Add pagination info if available
        if result.get("has_next_page") and result.get("next_cursor"):
            formatted += f"\nMore results available. Use cursor: {result['next_cursor']}\n"
        
        return formatted
    except Exception as e:
        return f"Error searching tweets: {str(e)}"

@mcp.tool()
async def search_tweets_with_cursor(query: str, cursor: str, ctx: Context, query_type: str = "Latest", count: int = 10) -> str:
    """
    Search for tweets with a pagination cursor.
    
    Args:
        query: The search query (can use Twitter search operators)
        cursor: Pagination cursor from previous search results
        query_type: Type of search, either "Latest" or "Top" (default: "Latest")
        count: Number of results to return (default: 10, max: 50)
        ctx: The MCP context
        
    Returns:
        Formatted search results with pagination
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    if query_type not in ["Latest", "Top"]:
        query_type = "Latest"  # Enforce valid values
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.search_tweets(query, query_type, count, cursor)
        
        if not result.get("tweets"):
            return f"No tweets found for query: {query}"
        
        formatted = f"Search results for \"{query}\" ({query_type}) - page 2+:\n\n"
        
        for i, tweet in enumerate(result["tweets"], 1):
            author = tweet["author"]
            formatted += f"{i}. @{author['userName']} ({author['name']}): {tweet['text']}\n"
            formatted += f"   Posted at: {tweet['createdAt']}\n"
            formatted += f"   Likes: {tweet['likeCount']} | Retweets: {tweet['retweetCount']} | Replies: {tweet['replyCount']}\n\n"
        
        # Add pagination info if available
        if result.get("has_next_page") and result.get("next_cursor"):
            formatted += f"\nMore results available. Use cursor: {result['next_cursor']}\n"
        
        return formatted
    except Exception as e:
        return f"Error searching tweets: {str(e)}"

@mcp.tool()
async def get_user_followers(username: str, ctx: Context, count: int = 10) -> str:
    """
    Get a list of users who follow the specified user.
    
    Args:
        username: The Twitter username without the @ symbol
        count: Number of followers to retrieve (default: 10, max: 50)
        ctx: The MCP context
        
    Returns:
        Formatted list of followers
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_user_followers(username, count)
        
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
        return f"Error retrieving followers: {str(e)}"

@mcp.tool()
async def get_user_following(username: str, ctx: Context, count: int = 10) -> str:
    """
    Get a list of users that the specified user follows.
    
    Args:
        username: The Twitter username without the @ symbol
        count: Number of following users to retrieve (default: 10, max: 50)
        ctx: The MCP context
        
    Returns:
        Formatted list of accounts the user follows
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_user_following(username, count)
        
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
        return f"Error retrieving following: {str(e)}"

@mcp.tool()
async def get_tweet_replies(tweet_id: str, ctx: Context, count: int = 10) -> str:
    """
    Get replies to a specific tweet.
    
    Args:
        tweet_id: The ID of the tweet
        count: Number of replies to retrieve (default: 10, max: 50)
        ctx: The MCP context
        
    Returns:
        Formatted list of replies to the tweet
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_tweet_replies(tweet_id, count)
        
        if not result.get("tweets"):
            return "No replies found for this tweet"
        
        formatted = f"Replies to tweet {tweet_id}:\n\n"
        
        for i, tweet in enumerate(result["tweets"], 1):
            author = tweet["author"]
            formatted += f"{i}. @{author['userName']} ({author['name']}): {tweet['text']}\n"
            formatted += f"   Likes: {tweet['likeCount']} | Posted at: {tweet['createdAt']}\n\n"
        
        return formatted
    except Exception as e:
        return f"Error retrieving replies: {str(e)}"