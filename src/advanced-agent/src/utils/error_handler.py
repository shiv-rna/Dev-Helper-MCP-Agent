"""
Error handling and retry mechanisms for the Developer Tools Agent.

This module provides comprehensive error handling, retry mechanisms,
and graceful degradation for various operations.
"""

import time
import logging
from typing import Callable, Any, Optional, Type, Union, List
from functools import wraps
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)


class SearchError(Exception):
    """Base exception for search-related errors."""
    pass


class QueryError(Exception):
    """Exception for query-related errors."""
    pass


class LLMError(Exception):
    """Exception for LLM-related errors."""
    pass


class ConfigurationError(Exception):
    """Exception for configuration-related errors."""
    pass


class RetryableError(Exception):
    """Exception that indicates an operation should be retried."""
    pass


class NonRetryableError(Exception):
    """Exception that indicates an operation should not be retried."""
    pass


def handle_search_errors(func: Callable) -> Callable:
    """
    Decorator to handle search-related errors with retry logic.
    
    Args:
        func: Function to wrap with error handling
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Search error in {func.__name__}: {str(e)}")
            raise SearchError(f"Search operation failed: {str(e)}") from e
    return wrapper


def handle_query_errors(func: Callable) -> Callable:
    """
    Decorator to handle query-related errors.
    
    Args:
        func: Function to wrap with error handling
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Query error in {func.__name__}: {str(e)}")
            raise QueryError(f"Query operation failed: {str(e)}") from e
    return wrapper


def handle_llm_errors(func: Callable) -> Callable:
    """
    Decorator to handle LLM-related errors with retry logic.
    
    Args:
        func: Function to wrap with error handling
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"LLM error in {func.__name__}: {str(e)}")
            raise LLMError(f"LLM operation failed: {str(e)}") from e
    return wrapper


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception,
    logger: Optional[logging.Logger] = None
) -> Callable:
    """
    Decorator that implements exponential backoff retry logic.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exceptions: Exception types to retry on
        logger: Logger instance for logging retry attempts
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=base_delay, max=max_delay),
            retry=retry_if_exception_type(exceptions),
            before_sleep=before_sleep_log(logger, logging.WARNING) if logger else None
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


class ErrorHandler:
    """
    Centralized error handler for the Developer Tools Agent.
    
    This class provides methods for handling different types of errors
    and implementing appropriate recovery strategies.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def handle_search_failure(self, error: Exception, query: str) -> dict:
        """
        Handle search operation failures.
        
        Args:
            error: The exception that occurred
            query: The search query that failed
            
        Returns:
            Dictionary with error information and fallback strategy
        """
        self.logger.error(f"Search failed for query '{query}': {str(error)}")
        
        # Implement fallback strategy
        if "rate limit" in str(error).lower():
            return {
                "error": "Rate limit exceeded",
                "strategy": "wait_and_retry",
                "wait_time": 60,
                "query": query
            }
        elif "timeout" in str(error).lower():
            return {
                "error": "Search timeout",
                "strategy": "reduce_results",
                "max_results": 2,
                "query": query
            }
        else:
            return {
                "error": "Unknown search error",
                "strategy": "fallback_query",
                "query": f"{query} developer tools"
            }
    
    def handle_query_validation_failure(self, error: Exception, query: str) -> dict:
        """
        Handle query validation failures.
        
        Args:
            error: The exception that occurred
            query: The query that failed validation
            
        Returns:
            Dictionary with error information and recovery strategy
        """
        self.logger.error(f"Query validation failed for '{query}': {str(error)}")
        
        # Implement query recovery strategy
        if len(query.strip()) < 2:
            return {
                "error": "Query too short",
                "strategy": "use_default_query",
                "query": "developer tools"
            }
        else:
            # Clean and optimize the query
            cleaned_query = query.strip()
            return {
                "error": "Query validation failed",
                "strategy": "clean_and_retry",
                "query": cleaned_query
            }
    
    def handle_llm_failure(self, error: Exception, operation: str) -> dict:
        """
        Handle LLM operation failures.
        
        Args:
            error: The exception that occurred
            operation: The LLM operation that failed
            
        Returns:
            Dictionary with error information and recovery strategy
        """
        self.logger.error(f"LLM operation '{operation}' failed: {str(error)}")
        
        if "rate limit" in str(error).lower():
            return {
                "error": "LLM rate limit exceeded",
                "strategy": "wait_and_retry",
                "wait_time": 30,
                "operation": operation
            }
        elif "timeout" in str(error).lower():
            return {
                "error": "LLM timeout",
                "strategy": "reduce_complexity",
                "operation": operation
            }
        else:
            return {
                "error": "LLM operation failed",
                "strategy": "use_fallback",
                "operation": operation
            }
    
    def is_retryable_error(self, error: Exception) -> bool:
        """
        Determine if an error is retryable.
        
        Args:
            error: The exception to check
            
        Returns:
            True if the error is retryable, False otherwise
        """
        retryable_exceptions = (
            ConnectionError,
            TimeoutError,
            RetryableError
        )
        
        error_message = str(error).lower()
        retryable_keywords = [
            "rate limit",
            "timeout",
            "connection",
            "network",
            "temporary",
            "service unavailable"
        ]
        
        # Check if it's a retryable exception type
        if isinstance(error, retryable_exceptions):
            return True
        
        # Check if error message contains retryable keywords
        if any(keyword in error_message for keyword in retryable_keywords):
            return True
        
        return False
    
    def get_error_context(self, error: Exception) -> dict:
        """
        Extract context information from an error.
        
        Args:
            error: The exception to analyze
            
        Returns:
            Dictionary with error context information
        """
        return {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "is_retryable": self.is_retryable_error(error),
            "timestamp": time.time()
        }


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    error_handler: Optional[ErrorHandler] = None,
    **kwargs
) -> Any:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Positional arguments for the function
        default_return: Default value to return on error
        error_handler: Error handler instance
        **kwargs: Keyword arguments for the function
        
    Returns:
        Function result or default_return on error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if error_handler:
            error_handler.logger.error(f"Error in {func.__name__}: {str(e)}")
        return default_return 