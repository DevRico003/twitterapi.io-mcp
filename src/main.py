"""
MCP server for Twitter API integration.

This server provides tools to interact with the Twitter API.io service, including
fetching tweets, user information, and search functionality.
"""
from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from pathlib import Path
import httpx
import asyncio
import os

from utils import format_tweet, format_user, format_tweet_list, format_trend

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
        
    async def batch_get_users_by_ids(self, user_ids: List[str]) -> Dict[str, Any]:
        """
        Get multiple user profiles by their user IDs.
        
        Args:
            user_ids: List of Twitter user IDs to retrieve
            
        Returns:
            Users data as a dictionary
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        ids_str = ",".join(user_ids)
        response = await self.client.get(
            f"{self.base_url}/twitter/user/user_by_ids",
            headers={"x-api-key": self.api_key},
            params={"userIds": ids_str}
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
        
    async def get_user_mentions(self, username: str, count: int = 20, cursor: str = "", 
                               since_time: int = None, until_time: int = None) -> Dict[str, Any]:
        """
        Get tweets that mention a specific user.
        
        Args:
            username: The Twitter username
            count: Number of mentions to retrieve (default: 20)
            cursor: Pagination cursor from previous results
            since_time: Optional Unix timestamp (in seconds) to get tweets after this time
            until_time: Optional Unix timestamp (in seconds) to get tweets before this time
            
        Returns:
            Tweets mentioning the user as a dictionary
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        params = {"userName": username, "count": count}
        
        if cursor:
            params["cursor"] = cursor
        if since_time:
            params["sinceTime"] = since_time
        if until_time:
            params["untilTime"] = until_time
            
        response = await self.client.get(
            f"{self.base_url}/twitter/user/mentions",
            headers={"x-api-key": self.api_key},
            params=params
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
        
    async def get_tweet_quotations(self, tweet_id: str, count: int = 10) -> Dict[str, Any]:
        """
        Get tweets that quote the specified tweet.
        
        Args:
            tweet_id: The ID of the tweet
            count: Number of quotes to retrieve
            
        Returns:
            Quote tweets as a dictionary
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/tweet/quotes",
            headers={"x-api-key": self.api_key},
            params={"tweetId": tweet_id, "count": count}
        )
        response.raise_for_status()
        return response.json()
        
    async def get_tweet_retweeters(self, tweet_id: str, count: int = 10) -> Dict[str, Any]:
        """
        Get users who retweeted the specified tweet.
        
        Args:
            tweet_id: The ID of the tweet
            count: Number of retweeters to retrieve
            
        Returns:
            Retweeters data as a dictionary
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/tweet/retweeters",
            headers={"x-api-key": self.api_key},
            params={"tweetId": tweet_id, "count": count}
        )
        response.raise_for_status()
        return response.json()
        
    async def get_tweet_thread_context(self, tweet_id: str) -> Dict[str, Any]:
        """
        Get the thread context of a tweet (parent tweets and replies).
        
        Args:
            tweet_id: The ID of the tweet
            
        Returns:
            Thread context as a dictionary
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/tweet/thread_context",
            headers={"x-api-key": self.api_key},
            params={"tweetId": tweet_id}
        )
        response.raise_for_status()
        return response.json()
        
    async def get_list_tweets(self, list_id: str, count: int = 20) -> Dict[str, Any]:
        """
        Get tweets from a Twitter list.
        
        Args:
            list_id: The ID of the Twitter list
            count: Number of tweets to retrieve
            
        Returns:
            List tweets as a dictionary
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/list/tweets",
            headers={"x-api-key": self.api_key},
            params={"listId": list_id, "count": count}
        )
        response.raise_for_status()
        return response.json()
        
    async def get_trends(self) -> Dict[str, Any]:
        """
        Get current trending topics on Twitter.
        
        Returns:
            Trending topics as a dictionary
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(
            f"{self.base_url}/twitter/trends",
            headers={"x-api-key": self.api_key}
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

@mcp.tool()
async def get_tweet_replies(ctx: Context, tweet_id: str, count: int = 10) -> str:
    """
    Get replies to a specific tweet.
    
    Args:
        ctx: The MCP context
        tweet_id: The ID of the tweet
        count: Number of replies to retrieve (default: 10, max: 50)
        
    Returns:
        Formatted list of replies to the tweet
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_tweet_replies(tweet_id, count)
        
        if not result.get("tweets"):
            return f"No replies found for tweet ID: {tweet_id}"
        
        formatted = f"Replies to tweet {tweet_id}:\n\n"
        
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
        return f"Error retrieving replies: {str(e)}"
        
@mcp.tool()
async def get_user_mentions(ctx: Context, username: str, count: int = 20) -> str:
    """
    Get tweets that mention a specific user.
    
    Args:
        ctx: The MCP context
        username: The Twitter username without the @ symbol
        count: Number of mentions to retrieve (default: 20, max: 50)
        
    Returns:
        Formatted list of tweets mentioning the user
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_user_mentions(username, count)
        
        if not result.get("tweets"):
            return f"No mentions found for @{username}"
        
        formatted = f"Tweets mentioning @{username}:\n\n"
        
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
        return f"Error retrieving mentions: {str(e)}"
        
@mcp.tool()
async def get_tweet_quotations(ctx: Context, tweet_id: str, count: int = 10) -> str:
    """
    Get quotes of a specific tweet.
    
    Args:
        ctx: The MCP context
        tweet_id: The ID of the tweet
        count: Number of quotes to retrieve (default: 10, max: 50)
        
    Returns:
        Formatted list of quotes of the tweet
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_tweet_quotations(tweet_id, count)
        
        if not result.get("tweets"):
            return f"No quotes found for tweet ID: {tweet_id}"
        
        formatted = f"Quotes of tweet {tweet_id}:\n\n"
        
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
        return f"Error retrieving quotes: {str(e)}"
        
@mcp.tool()
async def get_tweet_retweeters(ctx: Context, tweet_id: str, count: int = 10) -> str:
    """
    Get users who retweeted a specific tweet.
    
    Args:
        ctx: The MCP context
        tweet_id: The ID of the tweet
        count: Number of retweeters to retrieve (default: 10, max: 50)
        
    Returns:
        Formatted list of users who retweeted the tweet
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_tweet_retweeters(tweet_id, count)
        
        if not result.get("users"):
            return f"No retweeters found for tweet ID: {tweet_id}"
        
        formatted = f"Users who retweeted tweet {tweet_id}:\n\n"
        
        for i, user in enumerate(result["users"], 1):
            formatted += f"{i}. @{user['userName']} ({user['name']})\n"
            if user.get("description"):
                formatted += f"   Bio: {user['description']}\n"
            formatted += f"   Followers: {user['followers']} | Following: {user['following']}\n\n"
        
        return formatted
    except Exception as e:
        return f"Error retrieving retweeters: {str(e)}"
        
@mcp.tool()
async def get_tweet_thread_context(ctx: Context, tweet_id: str) -> str:
    """
    Get the full thread context of a tweet.
    
    Args:
        ctx: The MCP context
        tweet_id: The ID of the tweet
        
    Returns:
        Formatted thread context of the tweet
    """
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_tweet_thread_context(tweet_id)
        
        if not result.get("before") and not result.get("after"):
            return f"No thread context found for tweet ID: {tweet_id}"
        
        formatted = f"Thread context for tweet {tweet_id}:\n\n"
        
        # Add parent tweets (tweets before the specified tweet)
        if result.get("before") and len(result["before"]) > 0:
            formatted += "PARENT TWEETS:\n"
            for i, tweet in enumerate(result["before"], 1):
                author = tweet["author"]
                formatted += f"{i}. @{author['userName']}: {tweet['text']}\n"
                formatted += f"   Posted at: {tweet['createdAt']}\n\n"
        
        # Add the main tweet
        if result.get("main_tweet"):
            tweet = result["main_tweet"]
            author = tweet["author"]
            formatted += "MAIN TWEET:\n"
            formatted += f"@{author['userName']}: {tweet['text']}\n"
            formatted += f"Posted at: {tweet['createdAt']}\n"
            formatted += f"Likes: {tweet['likeCount']} | Retweets: {tweet['retweetCount']} | Replies: {tweet['replyCount']}\n\n"
        
        # Add reply tweets (tweets after the specified tweet)
        if result.get("after") and len(result["after"]) > 0:
            formatted += "REPLIES:\n"
            for i, tweet in enumerate(result["after"], 1):
                author = tweet["author"]
                formatted += f"{i}. @{author['userName']}: {tweet['text']}\n"
                formatted += f"   Posted at: {tweet['createdAt']}\n\n"
        
        return formatted
    except Exception as e:
        return f"Error retrieving thread context: {str(e)}"
        
@mcp.tool()
async def get_list_tweets(ctx: Context, list_id: str, count: int = 20) -> str:
    """
    Get tweets from a Twitter list.
    
    Args:
        ctx: The MCP context
        list_id: The ID of the Twitter list
        count: Number of tweets to retrieve (default: 20, max: 50)
        
    Returns:
        Formatted list of tweets from the Twitter list
    """
    if count > 50:
        count = 50  # Enforce maximum
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_list_tweets(list_id, count)
        
        if not result.get("tweets"):
            return f"No tweets found for list ID: {list_id}"
        
        list_name = result.get("list_name", "Twitter List")
        formatted = f"Tweets from {list_name} (ID: {list_id}):\n\n"
        
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
        return f"Error retrieving list tweets: {str(e)}"
        
@mcp.tool()
async def get_trends(ctx: Context) -> str:
    """
    Get current trending topics on Twitter.
    
    Args:
        ctx: The MCP context
        
    Returns:
        Formatted list of trending topics
    """
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.get_trends()
        
        if not result.get("trends"):
            return "No trending topics found"
        
        return format_trend(result["trends"])
    except Exception as e:
        return f"Error retrieving trends: {str(e)}"
        
@mcp.tool()
async def batch_get_users_by_ids(ctx: Context, user_ids: str) -> str:
    """
    Get multiple Twitter user profiles by their IDs.
    
    Args:
        ctx: The MCP context
        user_ids: Comma-separated list of Twitter user IDs
        
    Returns:
        Formatted user profiles information
    """
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        ids_list = [id.strip() for id in user_ids.split(",")]
        result = await twitter_ctx.batch_get_users_by_ids(ids_list)
        
        if not result.get("users") or len(result["users"]) == 0:
            return "No users found for the provided IDs"
        
        formatted = "Twitter User Profiles:\n\n"
        for i, user in enumerate(result["users"], 1):
            formatted += f"--- User {i} ---\n"
            formatted += format_user(user)
            formatted += "\n\n"
        
        return formatted
    except Exception as e:
        return f"Error retrieving user profiles: {str(e)}"

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