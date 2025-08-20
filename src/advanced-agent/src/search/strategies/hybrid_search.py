"""
Hybrid search strategy combining Firecrawl and Serper API.

This module implements a hybrid search approach that uses Firecrawl as the primary
search engine and Serper API as a fallback for comprehensive results, particularly
for alternatives queries.
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

from ...services.firecrawl import FirecrawlService
from ...services.serper_search import SerperService, SerperSearchResult
from ...utils.query_builder import QueryBuilder
from ...config.settings import settings
from ...utils.error_handler import handle_search_errors, SearchError
from ...utils.logger import logger


class SearchSource(Enum):
    """Enumeration of search sources."""
    FIRECRAWL = "firecrawl"
    SERPER = "serper"
    HYBRID = "hybrid"


@dataclass
class SearchResult:
    """Unified search result from any source."""
    title: str
    url: str
    content: str
    source: SearchSource
    relevance_score: float = 0.0
    position: int = 0


class HybridSearchStrategy:
    """
    Hybrid search strategy combining Firecrawl and Serper API.
    
    This class provides:
    1. Primary search using Firecrawl for detailed content
    2. Fallback to Serper API for alternatives and comparisons
    3. Result ranking and deduplication
    4. Cost-effective search with comprehensive coverage
    """
    
    def __init__(self):
        """Initialize the hybrid search strategy."""
        self.firecrawl = FirecrawlService()
        self.serper = SerperService() if settings.is_serper_fallback_enabled() else None
        self.query_builder = QueryBuilder()
        self.logger = logger
    
    def search(self, query: str, num_results: int = None) -> List[SearchResult]:
        """
        Perform hybrid search using both Firecrawl and Serper.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of unified search results
        """
        if num_results is None:
            num_results = settings.search.max_search_results
        
        # Analyze query to determine search strategy
        query_info = self.query_builder.create_queries(query)
        query_type = query_info['context'].query_type.value
        
        self.logger.info(
            "Starting hybrid search",
            query=query,
            query_type=query_type,
            serper_available=bool(self.serper)
        )
        
        results = []
        
        # Primary search with Firecrawl
        try:
            firecrawl_results = self._search_firecrawl(query, query_info, num_results)
            results.extend(firecrawl_results)
            self.logger.info(
                "Firecrawl search completed",
                results_count=len(firecrawl_results)
            )
        except Exception as e:
            self.logger.log_error(e, "firecrawl_search", query=query)
        
        # Fallback to Serper for alternatives or if Firecrawl fails
        if self._should_use_serper_fallback(query_type, len(results)):
            try:
                serper_results = self._search_serper(query, query_info, num_results)
                results.extend(serper_results)
                self.logger.info(
                    "Serper fallback completed",
                    results_count=len(serper_results)
                )
            except Exception as e:
                self.logger.log_error(e, "serper_fallback", query=query)
        
        # Rank and deduplicate results
        ranked_results = self._rank_and_deduplicate(results)
        
        self.logger.info(
            "Hybrid search completed",
            total_results=len(ranked_results),
            firecrawl_count=len([r for r in ranked_results if r.source == SearchSource.FIRECRAWL]),
            serper_count=len([r for r in ranked_results if r.source == SearchSource.SERPER])
        )
        
        return ranked_results[:num_results]
    
    def _search_firecrawl(self, query: str, query_info: Dict[str, Any], num_results: int) -> List[SearchResult]:
        """Search using Firecrawl service."""
        search_query = query_info['search_query']
        
        try:
            firecrawl_data = self.firecrawl.search_company(search_query, num_results)
            
            results = []
            for i, item in enumerate(firecrawl_data):
                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    content=item.get("content", ""),
                    source=SearchSource.FIRECRAWL,
                    position=i + 1
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.log_error(e, "firecrawl_search", query=search_query)
            return []
    
    def _search_serper(self, query: str, query_info: Dict[str, Any], num_results: int) -> List[SearchResult]:
        """Search using Serper API."""
        if not self.serper:
            return []
        
        search_query = query_info['search_query']
        
        try:
            serper_data = self.serper.search(search_query, num_results)
            
            results = []
            for serper_result in serper_data:
                result = SearchResult(
                    title=serper_result.title,
                    url=serper_result.link,
                    content=serper_result.snippet,
                    source=SearchSource.SERPER,
                    position=serper_result.position
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.log_error(e, "serper_search", query=search_query)
            return []
    
    def _should_use_serper_fallback(self, query_type: str, current_results: int) -> bool:
        """
        Determine if Serper fallback should be used.
        
        Args:
            query_type: Type of query (alternatives, comparison, etc.)
            current_results: Number of results from primary search
            
        Returns:
            True if Serper fallback should be used
        """
        # Always use Serper for alternatives queries
        if query_type == "alternatives":
            return True
        
        # Use Serper if primary search returned few results
        if current_results < 3:
            return True
        
        # Use Serper for comparison queries
        if query_type == "comparison":
            return True
        
        return False
    
    def _rank_and_deduplicate(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        Rank and deduplicate search results.
        
        Args:
            results: List of search results
            
        Returns:
            Ranked and deduplicated results
        """
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        # Calculate relevance scores
        for result in unique_results:
            result.relevance_score = self._calculate_relevance_score(result)
        
        # Sort by relevance score (higher is better)
        ranked_results = sorted(
            unique_results,
            key=lambda x: (x.relevance_score, -x.position),
            reverse=True
        )
        
        return ranked_results
    
    def _calculate_relevance_score(self, result: SearchResult) -> float:
        """
        Calculate relevance score for a search result.
        
        Args:
            result: Search result to score
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.0
        
        # Base score from position (earlier results are better)
        if result.position <= 3:
            score += 0.3
        elif result.position <= 5:
            score += 0.2
        else:
            score += 0.1
        
        # Source preference (Firecrawl typically has better content)
        if result.source == SearchSource.FIRECRAWL:
            score += 0.2
        
        # Content quality score
        content_length = len(result.content)
        if content_length > 500:
            score += 0.3
        elif content_length > 200:
            score += 0.2
        else:
            score += 0.1
        
        # Title quality score
        title_length = len(result.title)
        if 10 <= title_length <= 100:
            score += 0.2
        else:
            score += 0.1
        
        return min(score, 1.0)
    
    def search_alternatives(self, tool_name: str, num_results: int = 8) -> List[SearchResult]:
        """
        Search for alternatives to a specific tool.
        
        Args:
            tool_name: Name of the tool to find alternatives for
            num_results: Number of results to return
            
        Returns:
            List of alternative tools
        """
        query = f"{tool_name} alternatives"
        return self.search(query, num_results)
    
    def search_comparison(self, tool1: str, tool2: str, num_results: int = 8) -> List[SearchResult]:
        """
        Search for comparison between two tools.
        
        Args:
            tool1: First tool name
            tool2: Second tool name
            num_results: Number of results to return
            
        Returns:
            List of comparison results
        """
        query = f"{tool1} vs {tool2}"
        return self.search(query, num_results) 