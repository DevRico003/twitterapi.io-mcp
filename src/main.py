"""
MCP server for Twitter API integration.

This server provides tools to interact with the Twitter API.io service, including
fetching tweets, user information, and search functionality.
"""
from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Dict, Any
from dotenv import load_dotenv
from pathlib import Path
import httpx
import asyncio
import os

from utils import format_tweet, format_user

# Load environment variables from the project root .env file
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'

# Force override of existing environment variables
load_dotenv(dotenv_path, override=True)

# Create a dataclass for our application context
@dataclass
class TwitterAPIContext:
    """Context for the Twitter API MCP server."""
    api_key: str
    client: httpx.AsyncClient
    base_url: str = "https://api.twitterapi.io"
    cache_timeout: int = 3600  # Default: 1 hour

    async def get_tweet(self, tweet_id: str) -> Dict[str, Any]:
        """
        Get a tweet by ID.

        Args:
            tweet_id: The ID of the tweet to retrieve

        Returns:
            Tweet data as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/tweets",
            headers={"x-api-key": self.api_key},
            params={"tweet_ids": tweet_id}
        )
        response.raise_for_status()
        return response.json()

    async def get_user(self, username: str) -> Dict[str, Any]:
        """
        Get a user profile by username.

        Args:
            username: The Twitter username to retrieve

        Returns:
            User profile data as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/user/info",
            headers={"x-api-key": self.api_key},
            params={"userName": username}
        )
        response.raise_for_status()
        return response.json()

    async def get_user_tweets(self, username: str, count: int = 10) -> Dict[str, Any]:
        """
        Get recent tweets from a user.

        Args:
            username: The Twitter username
            count: Number of tweets to retrieve

        Returns:
            Recent tweets as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/user/tweets",
            headers={"x-api-key": self.api_key},
            params={"userName": username, "count": count}
        )
        response.raise_for_status()
        return response.json()

    async def get_user_followers(self, username: str, count: int = 10) -> Dict[str, Any]:
        """
        Get followers of a user.

        Args:
            username: The Twitter username
            count: Number of followers to retrieve

        Returns:
            Followers data as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/user/followers",
            headers={"x-api-key": self.api_key},
            params={"userName": username, "count": count}
        )
        response.raise_for_status()
        return response.json()

    async def get_user_following(self, username: str, count: int = 10) -> Dict[str, Any]:
        """
        Get accounts a user is following.

        Args:
            username: The Twitter username
            count: Number of following accounts to retrieve

        Returns:
            Following accounts data as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/user/followings",
            headers={"x-api-key": self.api_key},
            params={"userName": username, "count": count}
        )
        response.raise_for_status()
        return response.json()

    async def search_tweets(self, query: str, query_type: str = "Latest", count: int = 10, cursor: str = "") -> Dict[str, Any]:
        """
        Search for tweets.

        Args:
            query: The search query (can use Twitter search operators)
            query_type: Type of search, either "Latest" or "Top"
            count: Number of results to return
            cursor: Pagination cursor from previous search results

        Returns:
            Search results as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        params = {
            "query": query,
            "queryType": query_type,
            "count": count
        }
        if cursor:
            params["cursor"] = cursor

        response = await self.client.get(
            f"{self.base_url}/twitter/tweet/advanced_search",
            headers={"x-api-key": self.api_key},
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def get_tweet_replies(self, tweet_id: str, count: int = 10) -> Dict[str, Any]:
        """
        Get replies to a tweet.

        Args:
            tweet_id: The ID of the tweet
            count: Number of replies to retrieve

        Returns:
            Tweet replies as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/tweet/replies",
            headers={"x-api-key": self.api_key},
            params={"tweetId": tweet_id, "count": count}
        )
        response.raise_for_status()
        return response.json()

@asynccontextmanager
async def twitter_lifespan(server: FastMCP) -> AsyncIterator[TwitterAPIContext]:
    """
    Manages the Twitter API client lifecycle.
    
    Args:
        server: The FastMCP server instance
        
    Yields:
        TwitterAPIContext: The context containing the Twitter API client
    """
    # Get the API key from environment variables
    api_key = os.getenv("TWITTER_API_KEY")
    if not api_key:
        raise ValueError("TWITTER_API_KEY environment variable is required")
    
    # Create HTTP client with timeout and limits
    timeout = httpx.Timeout(30.0, connect=10.0)
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    
    try:
        async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
            # Test connection by making a simple API call
            test_ctx = TwitterAPIContext(api_key=api_key, client=client)
            try:
                # Test with a known username (the Twitter API's own account)
                await test_ctx.get_user("twitterapi")
                print("TwitterAPI connection test successful")
            except Exception as e:
                print(f"TwitterAPI connection test failed: {str(e)}")
                raise ValueError(f"Could not connect to TwitterAPI: {str(e)}")
            
            # Create and yield the context
            yield TwitterAPIContext(
                api_key=api_key,
                client=client
            )
    finally:
        # The AsyncClient is automatically cleaned up due to the context manager
        pass

# Initialize FastMCP server
mcp = FastMCP(
    "twitterapi-mcp",
    description="MCP server for Twitter API.io integration",
    lifespan=twitter_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8051")
)

@mcp.tool()
async def get_tweet(ctx: Context, tweet_id: str) -> str:
    """
    Get a tweet by its ID.
    
    Args:
        ctx: The MCP context
        tweet_id: The ID of the tweet to retrieve
        
    Returns:
        Formatted tweet information
    """
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_tweet(tweet_id)
        
        if not result.get("tweets"):
            return "Tweet not found"
        
        tweet = result["tweets"][0]
        return format_tweet(tweet)
    except Exception as e:
        return f"Error retrieving tweet: {str(e)}"

@mcp.tool()
async def get_user_profile(ctx: Context, username: str) -> str:
    """
    Get a Twitter user's profile information.
    
    Args:
        ctx: The MCP context
        username: The Twitter username without the @ symbol
        
    Returns:
        Formatted user profile information
    """
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_user(username)
        
        if not result.get("data"):
            return f"User @{username} not found"
        
        user = result["data"]
        return format_user(user)
    except Exception as e:
        return f"Error retrieving user profile: {str(e)}"

@mcp.tool()
async def get_user_recent_tweets(ctx: Context, username: str, count: int = 10) -> str:
    """
    Get a user's recent tweets.
    
    Args:
        ctx: The MCP context
        username: The Twitter username without the @ symbol
        count: Number of tweets to retrieve (default: 10, max: 100)
        
    Returns:
        Formatted list of user's recent tweets
    """
    max_tweets = int(os.getenv("MAX_TWEETS", "100"))
    if count > max_tweets:
        count = max_tweets  # Enforce maximum
    
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
async def search_tweets(ctx: Context, query: str, query_type: str = "Latest", count: int = 10) -> str:
    """
    Search for tweets based on a query.
    
    Args:
        ctx: The MCP context
        query: The search query (can use Twitter search operators)
        query_type: Type of search, either "Latest" or "Top" (default: "Latest")
        count: Number of results to return (default: 10, max: 50)
        
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
async def get_user_followers(ctx: Context, username: str, count: int = 10) -> str:
    """
    Get a list of users who follow the specified user.
    
    Args:
        ctx: The MCP context
        username: The Twitter username without the @ symbol
        count: Number of followers to retrieve (default: 10, max: 50)
        
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
async def get_user_following(ctx: Context, username: str, count: int = 10) -> str:
    """
    Get a list of users that the specified user follows.
    
    Args:
        ctx: The MCP context
        username: The Twitter username without the @ symbol
        count: Number of following users to retrieve (default: 10, max: 50)
        
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

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())