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

from twitterapi.config import logger, BASE_URL, CACHE_TTL, AI_TOPICS

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
    influencer_cache: Dict[str, Tuple[float, Dict]] = field(default_factory=dict)
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
        
    async def get_influencer_tweets(self, username: str, days_lookback: int = 7, count: int = 20) -> Dict[str, Any]:
        """
        Get recent tweets from an influencer with engagement metrics.
        
        This method includes caching to reduce API calls for frequently
        accessed influencer data.
        
        Args:
            username: Twitter username to analyze
            days_lookback: Number of days to look back for content
            count: Maximum number of tweets to retrieve
            
        Returns:
            Dictionary with influencer tweets and engagement metrics
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        logger.info(f"Fetching influencer tweets for: {username}")
        
        # Check cache first
        cache_key = f"influencer_{username}"
        if cache_key in self.influencer_cache:
            cache_time, cache_data = self.influencer_cache[cache_key]
            if (time.time() - cache_time) < self.cache_timeout:
                logger.info(f"Using cached data for influencer: {username}")
                return cache_data
        
        # Get recent tweets with high count to cover the lookback period
        result = await self.get_user_tweets(username, count=count)
        
        # Filter for engagement metrics and recency
        if "tweets" in result:
            cutoff_date = datetime.now() - timedelta(days=days_lookback)
            
            # Process tweets to include engagement metrics
            high_engagement_tweets = []
            for tweet in result["tweets"]:
                # Parse the date (assuming Twitter API format)
                try:
                    tweet_date = datetime.strptime(tweet["createdAt"], "%a %b %d %H:%M:%S %z %Y")
                    
                    # Check if within lookback period
                    if tweet_date > cutoff_date:
                        # Add engagement score
                        tweet["engagement_score"] = (
                            tweet.get("likeCount", 0) * 1 + 
                            tweet.get("retweetCount", 0) * 2 + 
                            tweet.get("replyCount", 0) * 3 +
                            tweet.get("quoteCount", 0) * 2
                        )
                        high_engagement_tweets.append(tweet)
                except Exception as e:
                    logger.warning(f"Error parsing tweet date: {e}")
                    continue
            
            # Sort by engagement score
            high_engagement_tweets.sort(key=lambda x: x.get("engagement_score", 0), reverse=True)
            
            # Create response with engagement-focused data
            response = {
                "username": username,
                "high_engagement_tweets": high_engagement_tweets[:10],  # Top 10 by engagement
                "total_analyzed": len(result["tweets"]),
                "lookback_days": days_lookback
            }
            
            # Cache the results
            self.influencer_cache[cache_key] = (time.time(), response)
            
            return response
        
        return {"username": username, "high_engagement_tweets": [], "error": "No tweets found"}
        
    async def analyze_influencer_topics(self, usernames: List[str], days_lookback: int = 7) -> Dict[str, Any]:
        """
        Analyze trending topics from a list of influencers.
        
        Args:
            usernames: List of Twitter usernames to analyze
            days_lookback: Number of days to look back for content
            
        Returns:
            Dictionary with trending topics and hashtag analysis
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        logger.info(f"Analyzing trending topics from influencers: {usernames}")
        
        all_tweets = []
        influencer_data = {}
        
        # Collect tweets from all influencers
        for username in usernames:
            try:
                user_data = await self.get_influencer_tweets(username, days_lookback)
                influencer_data[username] = {
                    "high_engagement_count": len(user_data.get("high_engagement_tweets", [])),
                    "total_analyzed": user_data.get("total_analyzed", 0)
                }
                
                all_tweets.extend(user_data.get("high_engagement_tweets", []))
            except Exception as e:
                logger.error(f"Error analyzing influencer {username}: {e}")
                continue
        
        # Extract hashtags and topics
        hashtags = {}
        topics = {}
        
        for tweet in all_tweets:
            # Extract hashtags
            if "entities" in tweet and "hashtags" in tweet["entities"]:
                for tag in tweet["entities"]["hashtags"]:
                    tag_text = tag["text"].lower()
                    hashtags[tag_text] = hashtags.get(tag_text, 0) + 1
            
            # Simple topic extraction from text
            if "text" in tweet:
                words = tweet["text"].lower().split()
                for topic in AI_TOPICS:
                    if topic in words:
                        topics[topic] = topics.get(topic, 0) + 1
        
        # Sort hashtags and topics by frequency
        sorted_hashtags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "influencers_analyzed": len(usernames),
            "total_high_engagement_tweets": len(all_tweets),
            "top_hashtags": sorted_hashtags[:10],
            "trending_topics": sorted_topics[:10],
            "influencer_stats": influencer_data
        }