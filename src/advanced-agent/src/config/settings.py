"""
Configuration settings for the Developer Tools Agent.

This module manages all configuration settings, environment variables,
and provides a centralized way to access application settings.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class SearchSettings:
    """Settings related to search functionality."""
    firecrawl_api_key: str
    google_api_key: Optional[str] = None
    google_engine_id: Optional[str] = None
    max_search_results: int = 5
    search_timeout: int = 30
    enable_google_search: bool = False


@dataclass
class LLMSettings:
    """Settings related to LLM functionality."""
    openai_api_key: str
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.1
    max_tokens: int = 2000


@dataclass
class CacheSettings:
    """Settings related to caching functionality."""
    enable_caching: bool = False
    redis_url: Optional[str] = None
    cache_ttl: int = 3600  # 1 hour


@dataclass
class LoggingSettings:
    """Settings related to logging functionality."""
    log_level: str = "INFO"
    enable_structured_logging: bool = True


class Settings:
    """
    Centralized settings manager for the Developer Tools Agent.
    
    This class provides a single point of access to all configuration
    settings and ensures proper validation of required environment variables.
    """
    
    def __init__(self):
        self._validate_required_env_vars()
        
        self.search = SearchSettings(
            firecrawl_api_key=self._get_required_env("FIRECRAWL_API_KEY"),
            google_api_key=os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY"),
            google_engine_id=os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID"),
            max_search_results=int(os.getenv("MAX_SEARCH_RESULTS", "5")),
            search_timeout=int(os.getenv("SEARCH_TIMEOUT", "30")),
            enable_google_search=bool(os.getenv("ENABLE_GOOGLE_SEARCH", "false").lower() == "true")
        )
        
        self.llm = LLMSettings(
            openai_api_key=self._get_required_env("OPENAI_API_KEY"),
            model_name=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000"))
        )
        
        self.cache = CacheSettings(
            enable_caching=bool(os.getenv("ENABLE_CACHING", "false").lower() == "true"),
            redis_url=os.getenv("REDIS_URL"),
            cache_ttl=int(os.getenv("CACHE_TTL", "3600"))
        )
        
        self.logging = LoggingSettings(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            enable_structured_logging=bool(os.getenv("ENABLE_STRUCTURED_LOGGING", "true").lower() == "true")
        )
    
    def _get_required_env(self, key: str) -> str:
        """
        Get a required environment variable.
        
        Args:
            key: Environment variable name
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If the environment variable is not set
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def _validate_required_env_vars(self) -> None:
        """
        Validate that all required environment variables are set.
        
        Raises:
            ValueError: If any required environment variable is missing
        """
        required_vars = ["FIRECRAWL_API_KEY", "OPENAI_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def is_google_search_enabled(self) -> bool:
        """
        Check if Google search is enabled and properly configured.
        
        Returns:
            True if Google search is enabled and configured, False otherwise
        """
        return (
            self.search.enable_google_search and
            self.search.google_api_key is not None and
            self.search.google_engine_id is not None
        )
    
    def is_caching_enabled(self) -> bool:
        """
        Check if caching is enabled and properly configured.
        
        Returns:
            True if caching is enabled and configured, False otherwise
        """
        return self.cache.enable_caching and self.cache.redis_url is not None
    
    def get_search_config(self) -> dict:
        """
        Get search configuration as a dictionary.
        
        Returns:
            Dictionary containing search configuration
        """
        return {
            "firecrawl_api_key": self.search.firecrawl_api_key,
            "google_api_key": self.search.google_api_key,
            "google_engine_id": self.search.google_engine_id,
            "max_search_results": self.search.max_search_results,
            "search_timeout": self.search.search_timeout,
            "enable_google_search": self.search.enable_google_search
        }
    
    def get_llm_config(self) -> dict:
        """
        Get LLM configuration as a dictionary.
        
        Returns:
            Dictionary containing LLM configuration
        """
        return {
            "openai_api_key": self.llm.openai_api_key,
            "model_name": self.llm.model_name,
            "temperature": self.llm.temperature,
            "max_tokens": self.llm.max_tokens
        }


# Global settings instance
settings = Settings() 