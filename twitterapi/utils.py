"""
Utility functions for TwitterAPI.io MCP server.

This module provides helper functions for loading environment variables,
handling common formatting tasks, and other shared utilities.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from .env files.
    
    Looks for .env files in the following order:
    1. twitterapi/.env (package-level)
    2. ./.env (project root)
    """
    # Path to the directory containing this file
    base_dir = Path(__file__).parent.absolute()
    
    # Try loading from package-level .env first
    env_file = base_dir / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        return True
    
    # Try loading from project root .env
    root_env = base_dir.parent / '.env'
    if root_env.exists():
        load_dotenv(root_env)
        return True
    
    return False

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