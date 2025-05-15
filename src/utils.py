"""
Utility functions for the Twitter API MCP server.
"""
from typing import Dict, Any, List
import os

def format_tweet(tweet: Dict[str, Any]) -> str:
    """
    Format a tweet for output.
    
    Args:
        tweet: Tweet data dictionary
        
    Returns:
        Formatted tweet as a string
    """
    if not tweet:
        return "Tweet not available"
        
    author = tweet.get("author", {})
    
    formatted = f"Tweet by @{author.get('userName', 'unknown')} ({author.get('name', 'Unknown')}):\n\n"
    formatted += f"{tweet.get('text', 'No content')}\n\n"
    formatted += f"Posted at: {tweet.get('createdAt', 'unknown')}\n"
    formatted += f"Likes: {tweet.get('likeCount', 0)} | "
    formatted += f"Retweets: {tweet.get('retweetCount', 0)} | "
    formatted += f"Replies: {tweet.get('replyCount', 0)}"
    
    # Add hashtags if present
    if tweet.get("entities", {}).get("hashtags"):
        hashtags = [f"#{tag['text']}" for tag in tweet["entities"]["hashtags"]]
        formatted += f"\nHashtags: {' '.join(hashtags)}"
    
    return formatted

def format_tweet_list(tweets: List[Dict[str, Any]]) -> str:
    """
    Format multiple tweets for output.
    
    Args:
        tweets: List of tweet data dictionaries
        
    Returns:
        Formatted tweet list as a string
    """
    if not tweets:
        return "No tweets available"
    
    formatted = f"Tweets ({len(tweets)}):\n\n"
    
    for i, tweet in enumerate(tweets, 1):
        author = tweet.get("author", {})
        formatted += f"{i}. Tweet by @{author.get('userName', 'unknown')} ({author.get('name', 'Unknown')}):\n"
        formatted += f"   {tweet.get('text', 'No content')}\n"
        formatted += f"   Posted at: {tweet.get('createdAt', 'unknown')}\n"
        formatted += f"   Likes: {tweet.get('likeCount', 0)} | "
        formatted += f"Retweets: {tweet.get('retweetCount', 0)} | "
        formatted += f"Replies: {tweet.get('replyCount', 0)}\n\n"
    
    return formatted

def format_user(user: Dict[str, Any]) -> str:
    """
    Format a user profile for output.
    
    Args:
        user: User data dictionary
        
    Returns:
        Formatted user profile as a string
    """
    if not user:
        return "User not available"
        
    formatted = f"Twitter Profile: @{user.get('userName', 'unknown')} ({user.get('name', 'Unknown')})\n\n"
    
    if user.get("description"):
        formatted += f"Bio: {user['description']}\n\n"
    
    if user.get("location"):
        formatted += f"Location: {user['location']}\n"
    
    formatted += f"Followers: {user.get('followers', 0)} | Following: {user.get('following', 0)}\n"
    formatted += f"Tweets: {user.get('statusesCount', 0)} | Media: {user.get('mediaCount', 0)}\n"
    formatted += f"Account created: {user.get('createdAt', 'unknown')}\n"
    
    if user.get("isBlueVerified"):
        formatted += f"✓ Blue Verified\n"
    
    return formatted

def format_trend(trends: List[Dict[str, Any]]) -> str:
    """
    Format trending topics for output.
    
    Args:
        trends: List of trending topic dictionaries
        
    Returns:
        Formatted trends as a string
    """
    if not trends:
        return "No trending topics available"
    
    formatted = "Current Twitter Trends:\n\n"
    
    for i, trend in enumerate(trends, 1):
        formatted += f"{i}. {trend.get('name', 'Unknown')}\n"
        
        # Add tweet volume if available
        if trend.get('tweet_volume'):
            formatted += f"   Tweet volume: {trend['tweet_volume']:,}\n"
            
        # Add description if available
        if trend.get('description'):
            formatted += f"   {trend['description']}\n"
            
        formatted += "\n"
    
    return formatted