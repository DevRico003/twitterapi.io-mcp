"""
TwitterAPI.io client module.

This module contains the TwitterAPIContext class which handles all
interactions with the TwitterAPI.io service.
"""

import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple

import httpx

from twitterapi.config import logger, BASE_URL, CACHE_TTL

@dataclass
class TwitterAPIContext:
    """
    Client for interacting with the TwitterAPI.io service.

    This class handles all API calls to TwitterAPI.io, including authentication,
    request formatting, and response parsing. It includes caching for
    expensive or frequently accessed data.

    Attributes:
        api_key: API key for TwitterAPI.io authentication
        client: httpx.AsyncClient for making HTTP requests
        base_url: Base URL for the TwitterAPI.io API
        influencer_cache: Cache for influencer data
        cache_timeout: Cache timeout in seconds
    """
    api_key: str
    client: httpx.AsyncClient
    base_url: str = BASE_URL

    # Cache for influencer data to reduce API calls
    # influencer_cache removed for neutrality
    cache_timeout: int = CACHE_TTL

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
        logger.info(f"Fetching tweet: {tweet_id}")
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
        logger.info(f"Fetching user: {username}")
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
        logger.info(f"Fetching tweets for user: {username}")
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
        logger.info(f"Fetching followers for user: {username}")
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
        logger.info(f"Fetching following for user: {username}")
        response = await self.client.get(
            f"{self.base_url}/twitter/user/followings",
            headers={"x-api-key": self.api_key},
            params={"userName": username, "count": count}
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
        logger.info(f"Fetching replies for tweet: {tweet_id}")
        response = await self.client.get(
            f"{self.base_url}/twitter/tweet/replies",
            headers={"x-api-key": self.api_key},
            params={"tweetId": tweet_id, "count": count}
        )
        response.raise_for_status()
        return response.json()

    async def get_tweet_retweeters(self, tweet_id: str, count: int = 10) -> Dict[str, Any]:
        """
        Get users who retweeted a tweet.

        Args:
            tweet_id: The ID of the tweet
            count: Number of retweeters to retrieve

        Returns:
            Retweeters data as a dictionary

        Raises:
            httpx.HTTPError: If the API request fails
        """
        logger.info(f"Fetching retweeters for tweet: {tweet_id}")
        response = await self.client.get(
            f"{self.base_url}/twitter/tweet/retweeters",
            headers={"x-api-key": self.api_key},
            params={"tweetId": tweet_id, "count": count}
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
        logger.info(f"Searching tweets: {query}")
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