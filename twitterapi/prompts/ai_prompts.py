"""
AI development prompts for TwitterAPI.io MCP server.

This module contains prompt templates for AI development trend analysis
and influencer monitoring.
"""

from typing import List

from mcp.server.fastmcp.prompts import base

from twitterapi.config import DEFAULT_AI_INFLUENCERS
from twitterapi.mcp_server import mcp

@mcp.prompt()
def analyze_ai_coding_influencers(influencers: str = ",".join(DEFAULT_AI_INFLUENCERS[:5])) -> List[base.Message]:
    """
    Analyze AI coding influencers and their recent tweets.
    
    Args:
        influencers: Comma-separated list of Twitter usernames to analyze (without @ symbol)
        
    Returns:
        List of messages for the prompt template
    """
    # Split the influencers string into a list
    influencer_list = [name.strip() for name in influencers.split(",")]
    
    return [
        base.UserMessage("I need a comprehensive analysis of recent tweets and trends from top AI coding influencers."),
        base.UserMessage("Please analyze the following influencers to identify key AI development trends, tools, and topics they're discussing:"),
        base.AssistantMessage("I'll analyze these AI influencers for you. Let me gather their recent tweets and identify trending topics."),
        base.UserMessage("Use the 'monitor_ai_influencers' tool to collect the data."),
        base.UserMessage(f"Here's the list of influencers to analyze: {influencers}")
    ]

@mcp.prompt()
def ai_development_trend_analysis(days: int = 7, influencers: str = ",".join(DEFAULT_AI_INFLUENCERS)) -> List[base.Message]:
    """
    Perform a trend analysis on AI development topics from Twitter.
    
    Args:
        days: Number of days to look back (1-30)
        influencers: Comma-separated list of Twitter usernames to analyze (without @ symbol)
        
    Returns:
        List of messages for the prompt template
    """
    # Split the influencers string into a list
    influencer_list = [name.strip() for name in influencers.split(",")]
    
    # Ensure days is within bounds
    days = max(1, min(30, days))
    
    return [
        base.UserMessage(f"I need a trend analysis of AI coding and development discussions on Twitter from the past {days} days."),
        base.UserMessage("Please identify emerging topics, technologies, and discussions in the AI development community."),
        base.UserMessage("Focus on technical trends that would be relevant for developers looking to improve their AI workflows."),
        base.AssistantMessage("I'll analyze recent AI development trends on Twitter for you. Let me collect and analyze the data."),
        base.UserMessage("Use the appropriate tools to gather AI coding trend data from Twitter influencers."),
        base.UserMessage(f"Please analyze these influencers: {influencers}")
    ]

@mcp.prompt()
def research_ai_development_topic(topic: str) -> List[base.Message]:
    """
    Research a specific AI development topic on Twitter.
    
    Args:
        topic: The AI development topic to research (e.g., "LLM fine-tuning", "AI coding assistants")
        
    Returns:
        List of messages for the prompt template
    """
    return [
        base.UserMessage(f"I need to research the latest discussions and advancements in {topic} on Twitter."),
        base.UserMessage("Please find the most relevant and insightful tweets about this topic from AI developers and researchers."),
        base.UserMessage("Focus on technical details, new approaches, and practical developer insights rather than general news."),
        base.AssistantMessage(f"I'll research the latest Twitter discussions about {topic} for you, focusing on technical insights from AI developers."),
        base.UserMessage(f"Use the 'search_ai_development_topics' tool to search for content related to {topic}."),
        base.UserMessage("After collecting the tweets, please analyze them to identify key insights, emerging patterns, and notable expert opinions on this topic.")
    ]

@mcp.prompt()
def create_ai_development_post_ideas(topic: str, influencers: str = ",".join(DEFAULT_AI_INFLUENCERS[:3])) -> List[base.Message]:
    """
    Generate ideas for AI development content based on Twitter trends.
    
    Args:
        topic: The AI development topic to focus on
        influencers: Comma-separated list of Twitter usernames to analyze (without @ symbol)
        
    Returns:
        List of messages for the prompt template
    """
    # Split the influencers string into a list
    influencer_list = [name.strip() for name in influencers.split(",")]
    
    return [
        base.UserMessage(f"I need to create engaging Twitter content about {topic} for an AI development audience."),
        base.UserMessage("Please analyze current discussions on this topic and suggest post ideas that would be valuable for AI developers."),
        base.UserMessage(f"Examine what influential accounts like {influencers} are saying about this topic."),
        base.AssistantMessage(f"I'll help generate AI development content ideas about {topic} based on current Twitter trends."),
        base.UserMessage("Use the appropriate tools to research this topic on Twitter and analyze related trends."),
        base.UserMessage("Suggest tweet formats that include technical insights, code tips, or workflow improvements that would be valuable to AI developers.")
    ]