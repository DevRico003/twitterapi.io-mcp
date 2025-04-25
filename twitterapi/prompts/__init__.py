"""
Prompts package for TwitterAPI.io MCP server.

This package contains all the prompt implementations for the MCP server.
"""

# Import and re-export all prompts
from twitterapi.prompts.ai_prompts import (
    analyze_ai_coding_influencers,
    ai_development_trend_analysis,
    research_ai_development_topic,
    create_ai_development_post_ideas
)

__all__ = [
    'analyze_ai_coding_influencers',
    'ai_development_trend_analysis',
    'research_ai_development_topic',
    'create_ai_development_post_ideas'
]