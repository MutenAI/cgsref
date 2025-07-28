"""Web search tool implementation."""

import json
import logging
import requests
import time
from typing import Dict, Any, Optional

from ..logging.agent_logger import agent_logger

logger = logging.getLogger(__name__)


class WebSearchTool:
    """
    Web search tool using Serper API.
    
    This tool provides web search capabilities for agents.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"
    
    async def search(
        self,
        query: str,
        num_results: int = 10,
        location: str = "us"
    ) -> str:
        """
        Perform a web search using the Serper API.

        Args:
            query: Search query string
            num_results: Number of results to return (1-100)
            location: Location for localized results (us, it, etc.)

        Returns:
            JSON string with search results
        """
        start_time = time.time()

        logger.info(f"🌐 WEB SEARCH: Searching for '{query}' (max {num_results} results)")

        if not self.api_key:
            error_msg = "SERPER_API_KEY not configured"
            logger.error(f"❌ WEB SEARCH ERROR: {error_msg}")
            return json.dumps({
                "error": error_msg,
                "results": []
            })

        payload = {
            "q": query,
            "num": min(num_results, 100),
            "gl": location,
            "hl": "en",
            "type": "search"
        }

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            logger.info(f"🔍 WEB SEARCH: Making API request to Serper...")
            logger.debug(f"🔍 WEB SEARCH: Payload: {json.dumps(payload, indent=2)}")

            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )

            logger.debug(f"🔍 WEB SEARCH: Response status: {response.status_code}")
            response.raise_for_status()

            result = response.json()
            duration_ms = (time.time() - start_time) * 1000

            # Format results for better readability
            organic_results = result.get("organic", [])
            formatted_results = {
                "searchParameters": result.get("searchParameters", {}),
                "organic": organic_results,
                "answerBox": result.get("answerBox"),
                "knowledgeGraph": result.get("knowledgeGraph"),
                "total_results": len(organic_results)
            }

            logger.info(f"✅ WEB SEARCH SUCCESS: Found {len(organic_results)} results in {duration_ms:.2f}ms")

            # Log top results for debugging
            for i, res in enumerate(organic_results[:3]):
                logger.debug(f"📄 Result {i+1}: {res.get('title', 'No title')} - {res.get('link', 'No link')}")

            return json.dumps(formatted_results, indent=2)

        except requests.exceptions.Timeout:
            duration_ms = (time.time() - start_time) * 1000
            error_msg = f"Serper API request timed out after {duration_ms:.2f}ms"
            logger.error(f"⏰ WEB SEARCH TIMEOUT: {error_msg}")
            return json.dumps({
                "error": error_msg,
                "results": []
            })
        except requests.exceptions.RequestException as e:
            duration_ms = (time.time() - start_time) * 1000
            error_msg = f"HTTP error in web search: {str(e)}"
            logger.error(f"🌐 WEB SEARCH HTTP ERROR: {error_msg} ({duration_ms:.2f}ms)")
            return json.dumps({
                "error": error_msg,
                "results": []
            })
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            error_msg = f"Unexpected error in web search: {str(e)}"
            logger.error(f"❌ WEB SEARCH ERROR: {error_msg} ({duration_ms:.2f}ms)")
            return json.dumps({
                "error": error_msg,
                "results": []
            })
    
    async def search_financial_content(
        self, 
        topic: str, 
        exclude_topics: str = "crypto,day_trading"
    ) -> str:
        """
        Search for current financial content with specific focus.
        
        Args:
            topic: Topic focus for the search
            exclude_topics: Topics to exclude (comma-separated)
            
        Returns:
            Formatted financial content analysis
        """
        logger.info(f"Searching for financial content with topic: {topic}")
        
        # Build specific search queries for financial content
        search_queries = [
            f"financial news investment trends this week 2025 {topic}",
            f"market analysis earnings reports last 7 days {topic}",
            f"economic indicators policy changes recent {topic}",
            f"IPO acquisitions merger announcements 2025 {topic}",
            f"inflation interest rates fed policy this month {topic}"
        ]
        
        # Exclude unwanted topics
        exclude_list = [t.strip().lower() for t in exclude_topics.split(",") if t.strip()]
        for query_idx, query in enumerate(search_queries):
            for exclude_topic in exclude_list:
                search_queries[query_idx] += f" -{exclude_topic}"
        
        all_content = []
        
        for query in search_queries:
            try:
                search_results = await self.search(query, num_results=5)
                search_data = json.loads(search_results)
                organic_results = search_data.get("organic", [])
                
                for result in organic_results[:3]:  # Top 3 per query
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    link = result.get("link", "")
                    
                    if title and snippet:
                        # Check if we should exclude this content
                        content_text = f"{title} {snippet}".lower()
                        should_exclude = any(
                            exclude_topic in content_text 
                            for exclude_topic in exclude_list
                        )
                        
                        if not should_exclude:
                            all_content.append({
                                "title": title,
                                "summary": snippet,
                                "url": link,
                                "relevance_score": len([
                                    word for word in topic.lower().split() 
                                    if word in content_text
                                ])
                            })
                            
            except Exception as e:
                logger.warning(f"Search error for query '{query}': {str(e)}")
                continue
        
        # Sort by relevance and take the best
        all_content.sort(key=lambda x: x["relevance_score"], reverse=True)
        top_content = all_content[:10]
        
        if not top_content:
            return f"""# Financial Content Analysis
**Topic Focus**: {topic}
**Analysis Date**: {self._get_current_date()}

## ⚠️ Limited Results Found

No relevant financial content found matching the specified criteria.
This may indicate very specific topic requirements or limited recent content.

**Recommendation**: Broaden the topic focus or try alternative search approaches.
"""
        
        # Generate structured summary with real content
        return self._format_financial_summary(topic, top_content)
    
    def _format_financial_summary(self, topic: str, content: list) -> str:
        """Format financial content into structured summary."""
        from datetime import datetime
        
        summary = f"""# Financial Content Analysis
**Topic Focus**: {topic}
**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Relevant Articles Found**: {len(content)}

## 📰 CURRENT FINANCIAL INSIGHTS

"""
        
        # Categorize content
        market_news = []
        earnings_news = []
        policy_news = []
        general_news = []
        
        for item in content:
            title_lower = item["title"].lower()
            if any(keyword in title_lower for keyword in ["earnings", "revenue", "profit", "quarterly"]):
                earnings_news.append(item)
            elif any(keyword in title_lower for keyword in ["fed", "interest", "inflation", "policy", "rate"]):
                policy_news.append(item)
            elif any(keyword in title_lower for keyword in ["market", "stock", "trading", "index"]):
                market_news.append(item)
            else:
                general_news.append(item)
        
        # Build structured output
        if earnings_news:
            summary += "### 💰 EARNINGS & CORPORATE PERFORMANCE\n\n"
            for item in earnings_news[:3]:
                summary += f"**{item['title']}**\n"
                summary += f"{item['summary']}\n"
                summary += f"[Read More]({item['url']})\n\n"
        
        if policy_news:
            summary += "### 🏛️ ECONOMIC POLICY & INDICATORS\n\n"
            for item in policy_news[:3]:
                summary += f"**{item['title']}**\n"
                summary += f"{item['summary']}\n"
                summary += f"[Read More]({item['url']})\n\n"
        
        if market_news:
            summary += "### 📈 MARKET TRENDS & ANALYSIS\n\n"
            for item in market_news[:3]:
                summary += f"**{item['title']}**\n"
                summary += f"{item['summary']}\n"
                summary += f"[Read More]({item['url']})\n\n"
        
        if general_news:
            summary += "### 📊 GENERAL FINANCIAL NEWS\n\n"
            for item in general_news[:2]:
                summary += f"**{item['title']}**\n"
                summary += f"{item['summary']}\n"
                summary += f"[Read More]({item['url']})\n\n"
        
        summary += f"""## 🎯 KEY TAKEAWAYS FOR CONTENT CREATION

**Trending Topics Identified:**
- {len(earnings_news)} earnings-related stories
- {len(policy_news)} policy/economic indicator updates  
- {len(market_news)} market trend analyses
- {len(general_news)} other financial developments

**Content Opportunities:**
- Create educational explainers around current earnings trends
- Develop Gen Z-focused analysis of policy changes
- Use current market movements as teaching moments
- Connect financial news to practical money management tips

**Brand Integration:**
Focus on how these developments affect young investors and their financial planning decisions.
Use these insights to create empowering, educational content that builds financial confidence.
"""
        
        return summary
    
    def _get_current_date(self) -> str:
        """Get current date formatted for display."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M')
