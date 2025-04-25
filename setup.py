"""
Setup script for twitterapi-mcp package.
This is used for backward compatibility with older pip versions.
"""

from setuptools import setup

# This setup.py exists as a bridge for old pip versions
# Modern installations should use the pyproject.toml file
setup(
    name="twitterapi-mcp",
    version="0.1.0",
    # All other configurations are in pyproject.toml
)