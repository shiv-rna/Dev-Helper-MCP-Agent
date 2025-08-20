"""
Serper API service for enhanced search integration.

This module provides a Serper API integration as a fallback to Firecrawl
for comprehensive search results, particularly for alternatives queries.
"""

import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from ..config.settings import settings
from ..utils.error_handler import handle_search_errors, SearchError
from ..utils.logger import logger


@dataclass
class SerperSearchResult:
    """Structured result from Serper API search."""
    title: str
    link: str
    snippet: str
    position: int
    source: str = "serper"


class SerperService:
    """
    Serper API service for web search functionality.
    
    This service provides:
    1. Web search capabilities as fallback to Firecrawl
    2. Structured result formatting
    3. Error handling and retry mechanisms
    4. Cost-effective search for alternatives queries
    """
    
    def __init__(self):
        """
        Initialize the Serper service.
        
        Raises:
            ValueError: If SERPER_API_KEY is not set
        """
        self.api_key = settings.search.serper_api_key
        if not self.api_key:
            raise ValueError("Missing SERPER_API_KEY in environment variables.")
        
        self.base_url = "https://google.serper.dev/search"
        self.logger = logger
    
    @handle_search_errors
    def search(self, query: str, num_results: int = 10) -> List[SerperSearchResult]:
        """
        Perform a web search using Serper API.
        
        Args:
            query: Search query string
            num_results: Number of results to return (max 10 for free tier)
            
        Returns:
            List of structured search results
            
        Raises:
            SearchError: If search operation fails
        """
        if num_results > 10:
            num_results = 10  # Serper free tier limit
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": num_results
        }
        
        try:
            self.logger.info(
                "Performing Serper search",
                query=query,
                num_results=num_results
            )
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=settings.search.search_timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract organic results
            organic_results = data.get("organic", [])
            
            results = []
            for i, result in enumerate(organic_results[:num_results]):
                serper_result = SerperSearchResult(
                    title=result.get("title", ""),
                    link=result.get("link", ""),
                    snippet=result.get("snippet", ""),
                    position=i + 1
                )
                results.append(serper_result)
            
            self.logger.info(
                "Serper search completed",
                query=query,
                results_count=len(results)
            )
            
            return results
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(e, "serper_search", query=query)
            raise SearchError(f"Serper search failed for query '{query}': {str(e)}") from e
        except Exception as e:
            self.logger.log_error(e, "serper_search", query=query)
            raise SearchError(f"Unexpected error in Serper search: {str(e)}") from e
    
    def search_alternatives(self, tool_name: str, num_results: int = 8) -> List[SerperSearchResult]:
        """
        Search for alternatives to a specific tool.
        
        Args:
            tool_name: Name of the tool to find alternatives for
            num_results: Number of results to return
            
        Returns:
            List of alternative tools
        """
        query = f"{tool_name} alternatives best"
        return self.search(query, num_results)
    
    def search_comparison(self, tool1: str, tool2: str, num_results: int = 8) -> List[SerperSearchResult]:
        """
        Search for comparison between two tools.
        
        Args:
            tool1: First tool name
            tool2: Second tool name
            num_results: Number of results to return
            
        Returns:
            List of comparison results
        """
        query = f"{tool1} vs {tool2} comparison"
        return self.search(query, num_results)
    
    def is_available(self) -> bool:
        """
        Check if Serper service is available.
        
        Returns:
            True if API key is configured, False otherwise
        """
        return bool(self.api_key) 