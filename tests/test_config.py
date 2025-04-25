import pytest
import os
from unittest.mock import patch

from twitterapi.config import get_env_var, logger

def test_get_env_var_exists():
    """Test retrieving an existing environment variable"""
    with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        assert get_env_var("TEST_VAR") == "test_value"

def test_get_env_var_default():
    """Test retrieving a non-existent variable with default"""
    with patch.dict(os.environ, {}, clear=True):
        assert get_env_var("NON_EXISTENT", default="default_value") == "default_value"

def test_get_env_var_required_missing():
    """Test retrieving a required but missing variable raises ValueError"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            get_env_var("REQUIRED_VAR", required=True)

def test_get_env_var_required_exists():
    """Test retrieving a required and existing variable"""
    with patch.dict(os.environ, {"REQUIRED_VAR": "exists"}):
        assert get_env_var("REQUIRED_VAR", required=True) == "exists"

def test_get_env_var_empty_string():
    """Test retrieving an empty string environment variable"""
    with patch.dict(os.environ, {"EMPTY_VAR": ""}):
        assert get_env_var("EMPTY_VAR") == ""
        # Empty string should still satisfy required=True
        assert get_env_var("EMPTY_VAR", required=True) == ""
        # Default should not override an empty string
        assert get_env_var("EMPTY_VAR", default="default") == ""