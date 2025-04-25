import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
from pathlib import Path

from twitterapi.utils import load_environment, format_tweet, format_user

# Test load_environment
def test_load_environment_package_level():
    """Test loading environment from package-level .env"""
    with patch('pathlib.Path.exists') as mock_exists, \
         patch('twitterapi.utils.load_dotenv') as mock_load_dotenv:
        
        # Mock the package-level .env file exists
        mock_exists.return_value = True
        
        result = load_environment()
        
        assert result is True
        mock_load_dotenv.assert_called_once()

def test_load_environment_root_level():
    """Test loading environment from root-level .env"""
    with patch('pathlib.Path.exists') as mock_exists, \
         patch('twitterapi.utils.load_dotenv') as mock_load_dotenv:
        
        # Mock the package-level .env doesn't exist but root-level does
        mock_exists.side_effect = [False, True]
        
        result = load_environment()
        
        assert result is True
        mock_load_dotenv.assert_called_once()

def test_load_environment_not_found():
    """Test when no .env files are found"""
    with patch('pathlib.Path.exists') as mock_exists, \
         patch('twitterapi.utils.load_dotenv') as mock_load_dotenv:
        
        # Mock no .env files exist
        mock_exists.return_value = False
        
        result = load_environment()
        
        assert result is False
        mock_load_dotenv.assert_not_called()

# Test format_tweet
def test_format_tweet_complete():
    """Test formatting a complete tweet"""
    tweet = {
        "text": "Test tweet",
        "author": {"userName": "testuser", "name": "Test User"},
        "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
        "likeCount": 10,
        "retweetCount": 5,
        "replyCount": 2,
        "entities": {
            "hashtags": [
                {"text": "AI"},
                {"text": "Python"}
            ]
        }
    }
    
    result = format_tweet(tweet)
    
    assert "Tweet by @testuser (Test User)" in result
    assert "Test tweet" in result
    assert "Likes: 10 | Retweets: 5 | Replies: 2" in result
    assert "Hashtags: #AI #Python" in result

def test_format_tweet_minimal():
    """Test formatting a tweet with minimal data"""
    tweet = {
        "text": "Test tweet",
        "author": {"userName": "testuser"},
        "likeCount": 0
    }
    
    result = format_tweet(tweet)
    
    assert "Tweet by @testuser" in result
    assert "Test tweet" in result
    assert "Likes: 0 | Retweets: 0 | Replies: 0" in result
    assert "Hashtags:" not in result

def test_format_tweet_empty():
    """Test formatting an empty tweet"""
    result = format_tweet({})
    assert "Tweet not available" == result

def test_format_tweet_none():
    """Test formatting a None tweet"""
    result = format_tweet(None)
    assert "Tweet not available" in result

# Test format_user
def test_format_user_complete():
    """Test formatting a complete user profile"""
    user = {
        "userName": "testuser",
        "name": "Test User",
        "description": "Test bio",
        "location": "Test Location",
        "followers": 100,
        "following": 50,
        "statusesCount": 500,
        "mediaCount": 20,
        "createdAt": "Wed Apr 25 10:00:00 +0000 2025",
        "isBlueVerified": True
    }
    
    result = format_user(user)
    
    assert "Twitter Profile: @testuser (Test User)" in result
    assert "Bio: Test bio" in result
    assert "Location: Test Location" in result
    assert "Followers: 100 | Following: 50" in result
    assert "Tweets: 500 | Media: 20" in result
    assert "✓ Blue Verified" in result

def test_format_user_minimal():
    """Test formatting a user profile with minimal data"""
    user = {
        "userName": "testuser",
        "name": "Test User"
    }
    
    result = format_user(user)
    
    assert "Twitter Profile: @testuser (Test User)" in result
    assert "Bio:" not in result
    assert "Location:" not in result
    assert "Followers: 0 | Following: 0" in result
    assert "Tweets: 0 | Media: 0" in result
    assert "✓ Blue Verified" not in result

def test_format_user_empty():
    """Test formatting an empty user profile"""
    result = format_user({})
    assert "User not available" == result

def test_format_user_none():
    """Test formatting a None user profile"""
    result = format_user(None)
    assert "User not available" in result