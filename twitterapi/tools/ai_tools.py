"""
AI-specific tools for TwitterAPI.io MCP server.

This module contains specialized tool implementations for AI development
trend analysis and influencer monitoring.
"""

from typing import List

from mcp.server.fastmcp import Context

from twitterapi.config import logger
from twitterapi.mcp_server import mcp

@mcp.tool()
async def monitor_ai_influencers(
    influencer_usernames: List[str], 
    ctx: Context,
    days_lookback: int = 7
) -> str:
    """
    Monitor tweets from AI development influencers and analyze engagement.
    
    Args:
        influencer_usernames: List of Twitter usernames to monitor (without @ symbol)
        days_lookback: Number of days to look back (default: 7, max: 30)
        ctx: The MCP context
        
    Returns:
        Formatted AI influencer analysis with engagement metrics
    """
    if days_lookback > 30:
        days_lookback = 30  # Enforce maximum lookback period
    
    if len(influencer_usernames) > 10:
        influencer_usernames = influencer_usernames[:10]  # Limit to 10 influencers
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        # Get all high-engagement tweets from each influencer
        all_results = []
        
        for username in influencer_usernames:
            try:
                result = await twitter_ctx.get_influencer_tweets(username, days_lookback)
                all_results.append(result)
            except Exception as e:
                logger.error(f"Error getting tweets for influencer {username}: {e}")
        
        # Format the results
        formatted = f"AI Influencer Analysis (Past {days_lookback} Days):\n\n"
        
        for result in all_results:
            username = result.get("username", "Unknown")
            high_engagement_tweets = result.get("high_engagement_tweets", [])
            
            formatted += f"## @{username}\n"
            formatted += f"High-engagement tweets: {len(high_engagement_tweets)}\n\n"
            
            for i, tweet in enumerate(high_engagement_tweets[:5], 1):  # Show top 5
                formatted += f"{i}. {tweet['text'][:150]}{'...' if len(tweet['text']) > 150 else ''}\n"
                formatted += f"   Engagement: {tweet.get('engagement_score', 0)} | Posted: {tweet['createdAt']}\n"
                formatted += f"   Likes: {tweet['likeCount']} | Retweets: {tweet['retweetCount']} | Replies: {tweet['replyCount']}\n\n"
        
        if not all_results:
            formatted += "No influencer data could be retrieved.\n"
            
        return formatted
    except Exception as e:
        return f"Error monitoring AI influencers: {str(e)}"

@mcp.tool()
async def analyze_ai_coding_trends(
    influencer_usernames: List[str], 
    ctx: Context,
    days_lookback: int = 7
) -> str:
    """
    Analyze trending topics from AI coding influencers.
    
    Args:
        influencer_usernames: List of Twitter usernames to analyze (without @ symbol)
        days_lookback: Number of days to look back (default: 7, max: 30)
        ctx: The MCP context
        
    Returns:
        Formatted trend analysis of AI coding topics and hashtags
    """
    if days_lookback > 30:
        days_lookback = 30  # Enforce maximum lookback period
    
    if len(influencer_usernames) > 10:
        influencer_usernames = influencer_usernames[:10]  # Limit to 10 influencers
    
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        analysis = await twitter_ctx.analyze_influencer_topics(influencer_usernames, days_lookback)
        
        formatted = f"AI Coding Trend Analysis (Past {days_lookback} Days):\n\n"
        
        # Top hashtags
        formatted += "## Top Hashtags\n"
        for tag, count in analysis.get("top_hashtags", []):
            formatted += f"#{tag}: {count} mentions\n"
        
        formatted += "\n## Trending Topics\n"
        for topic, count in analysis.get("trending_topics", []):
            formatted += f"{topic}: {count} mentions\n"
        
        formatted += f"\nAnalysis based on {analysis.get('total_high_engagement_tweets', 0)} high-engagement tweets "
        formatted += f"from {analysis.get('influencers_analyzed', 0)} influencers\n"
        
        # Influencer-specific stats
        formatted += "\n## Influencer Statistics\n"
        for username, stats in analysis.get("influencer_stats", {}).items():
            formatted += f"@{username}: {stats.get('high_engagement_count', 0)} high-engagement tweets "
            formatted += f"out of {stats.get('total_analyzed', 0)} analyzed\n"
        
        return formatted
    except Exception as e:
        return f"Error analyzing AI coding trends: {str(e)}"

@mcp.tool()
async def search_ai_development_topics(
    query: str, 
    ctx: Context,
    query_type: str = "Latest", 
    count: int = 10
) -> str:
    """
    Search for tweets specifically about AI development topics.
    
    Args:
        query: The AI development search query (can include keywords like 'AI coding', 'ML frameworks', etc.)
        query_type: Type of search, either "Latest" or "Top" (default: "Latest")
        count: Number of results to return (default: 10, max: 50)
        ctx: The MCP context
        
    Returns:
        Formatted search results focused on AI development
    """
    # Enhance the query to focus on AI development content
    ai_terms = ["AI", "artificial intelligence", "machine learning", "ML", "LLM", "deep learning"]
    dev_terms = ["coding", "development", "programming", "framework", "library", "tool"]
    
    # Check if the query already contains AI or dev terms
    has_ai_term = any(term.lower() in query.lower() for term in ai_terms)
    has_dev_term = any(term.lower() in query.lower() for term in dev_terms)
    
    # Enhance query if needed
    enhanced_query = query
    if not has_ai_term:
        enhanced_query = f"{enhanced_query} (AI OR 'artificial intelligence' OR ML)"
    if not has_dev_term:
        enhanced_query = f"{enhanced_query} (coding OR development OR programming)"
    
    # Use the standard search tool with the enhanced query
    twitter_ctx = ctx.request_context.lifespan_context
    try:
        result = await twitter_ctx.search_tweets(enhanced_query, query_type, count)
        
        if not result.get("tweets"):
            return f"No AI development tweets found for query: {query}"
        
        formatted = f"AI Development Search Results for \"{query}\" ({query_type}):\n\n"
        
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
        return f"Error searching AI development topics: {str(e)}"