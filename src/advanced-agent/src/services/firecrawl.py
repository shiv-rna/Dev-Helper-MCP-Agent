"""
Enhanced Firecrawl service with dynamic query formation and error handling.

This module provides an improved search service that addresses the poor query
formation issue by using intelligent query builders and comprehensive error handling.
"""

import os
from typing import List, Dict, Any, Optional
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

from ..search.query_builder import QueryBuilder
from ..config.settings import settings
from ..utils.error_handler import handle_search_errors, SearchError
from ..utils.logger import logger

load_dotenv()


class FirecrawlService:
    """
    Enhanced Firecrawl service with dynamic query formation.
    
    This class addresses the poor query formation issue by:
    1. Using intelligent query builders based on query type
    2. Implementing comprehensive error handling
    3. Providing fallback strategies for failed searches
    """
    
    def __init__(self):
        """
        Initialize the Firecrawl service with configuration and query builder.
        
        Raises:
            ValueError: If FIRECRAWL_API_KEY is not set
        """
        api_key = settings.search.firecrawl_api_key
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY in environment variables.")
        
        self.app = FirecrawlApp(api_key=api_key)
        self.query_builder = QueryBuilder()
        self.logger = logger
    
    @handle_search_errors
    def search_company(self, query: str, num_results: int = None) -> List[Dict[str, Any]]:
        """
        Search for company/tool information using dynamic query formation.
        
        Args:
            query: The original user query
            num_results: Number of results to return (defaults to config setting)
            
        Returns:
            List of search results
            
        Raises:
            SearchError: If search operation fails
        """
        if num_results is None:
            num_results = settings.search.max_search_results
        
        # Use query builder to create optimized search query
        query_info = self.query_builder.create_queries(query)
        search_query = query_info['search_query']
        
        self.logger.log_query_processing(
            query=query,
            query_type=query_info['context'].query_type.value,
            optimized_query=search_query
        )
        
        try:
            result = self.app.search(
                query=search_query,
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            
            self.logger.log_search_operation(
                query=search_query,
                results_count=len(result.data) if result and result.data else 0
            )
            
            return result.data if result else []
            
        except Exception as e:
            self.logger.log_error(e, "search_company", query=search_query)
            raise SearchError(f"Search failed for query '{search_query}': {str(e)}") from e
    
    @handle_search_errors
    def search_articles(self, query: str, num_results: int = None) -> List[Dict[str, Any]]:
        """
        Search for articles about tools/topics using optimized article queries.
        
        Args:
            query: The original user query
            num_results: Number of results to return (defaults to config setting)
            
        Returns:
            List of article search results
            
        Raises:
            SearchError: If search operation fails
        """
        if num_results is None:
            num_results = settings.search.max_search_results
        
        # Use query builder to create optimized article query
        query_info = self.query_builder.create_queries(query)
        article_query = query_info['article_query']
        
        self.logger.log_query_processing(
            query=query,
            query_type="article_search",
            optimized_query=article_query
        )
        
        try:
            result = self.app.search(
                query=article_query,
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            
            self.logger.log_search_operation(
                query=article_query,
                results_count=len(result.data) if result and result.data else 0
            )
            
            return result.data if result else []
            
        except Exception as e:
            self.logger.log_error(e, "search_articles", query=article_query)
            raise SearchError(f"Article search failed for query '{article_query}': {str(e)}") from e
    
    @handle_search_errors
    def scrape_company_page(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape content from a company/tool website.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Scraped content or None if scraping fails
            
        Raises:
            SearchError: If scraping operation fails
        """
        try:
            result = self.app.scrape_url(
                url=url,
                formats=["markdown"]
            )
            
            self.logger.info(
                "Page scraping completed",
                url=url,
                content_length=len(result.markdown) if result and result.markdown else 0
            )
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, "scrape_company_page", url=url)
            raise SearchError(f"Scraping failed for URL '{url}': {str(e)}") from e
    
    def search_with_fallback(self, query: str, num_results: int = None) -> List[Dict[str, Any]]:
        """
        Search with fallback strategies for better reliability.
        
        Args:
            query: The original user query
            num_results: Number of results to return
            
        Returns:
            List of search results (may be from fallback strategy)
        """
        try:
            # Try primary search
            return self.search_company(query, num_results)
        except SearchError as e:
            self.logger.warning(
                "Primary search failed, trying fallback",
                original_query=query,
                error=str(e)
            )
            
            # Fallback: try with simplified query
            try:
                simplified_query = self.query_builder.optimize_query(query)
                return self.search_company(simplified_query, num_results)
            except SearchError:
                self.logger.error(
                    "Fallback search also failed",
                    query=query,
                    simplified_query=simplified_query
                )
                return []
    
    def get_query_analysis(self, query: str) -> Dict[str, Any]:
        """
        Get analysis of the query for debugging and optimization.
        
        Args:
            query: The user query to analyze
            
        Returns:
            Dictionary with query analysis information
        """
        query_info = self.query_builder.create_queries(query)
        context = query_info['context']
        
        return {
            "original_query": query,
            "optimized_search_query": query_info['search_query'],
            "optimized_article_query": query_info['article_query'],
            "query_type": context.query_type.value,
            "tool_category": context.tool_category.value,
            "target_tool": context.target_tool,
            "comparison_tools": context.comparison_tools,
            "is_valid": self.query_builder.validate_query(query)
        }