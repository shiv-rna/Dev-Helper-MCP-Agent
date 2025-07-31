"""
Structured logging for the Developer Tools Agent.

This module provides structured logging capabilities with different
log levels and formats for better debugging and monitoring.
"""

import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter for structured logging output.
    
    This formatter provides consistent, structured log output
    that is easy to parse and analyze.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record with structured output.
        
        Args:
            record: The log record to format
            
        Returns:
            Formatted log string
        """
        # Create structured log entry
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        # Format as JSON-like string for readability
        formatted_parts = []
        for key, value in log_entry.items():
            if isinstance(value, str):
                formatted_parts.append(f"{key}='{value}'")
            else:
                formatted_parts.append(f"{key}={value}")
        
        return " | ".join(formatted_parts)


class DevToolsLogger:
    """
    Centralized logger for the Developer Tools Agent.
    
    This class provides a unified logging interface with different
    log levels and structured output capabilities.
    """
    
    def __init__(self, name: str = "dev_tools_agent", level: str = "INFO"):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = StructuredFormatter()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """
        Log a debug message.
        
        Args:
            message: The message to log
            **kwargs: Additional context fields
        """
        self._log_with_extra(logging.DEBUG, message, kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """
        Log an info message.
        
        Args:
            message: The message to log
            **kwargs: Additional context fields
        """
        self._log_with_extra(logging.INFO, message, kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """
        Log a warning message.
        
        Args:
            message: The message to log
            **kwargs: Additional context fields
        """
        self._log_with_extra(logging.WARNING, message, kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """
        Log an error message.
        
        Args:
            message: The message to log
            **kwargs: Additional context fields
        """
        self._log_with_extra(logging.ERROR, message, kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """
        Log a critical message.
        
        Args:
            message: The message to log
            **kwargs: Additional context fields
        """
        self._log_with_extra(logging.CRITICAL, message, kwargs)
    
    def _log_with_extra(self, level: int, message: str, extra_fields: Dict[str, Any]) -> None:
        """
        Log a message with extra fields.
        
        Args:
            level: Log level
            message: The message to log
            extra_fields: Additional context fields
        """
        if extra_fields:
            # Create a custom log record with extra fields
            record = self.logger.makeRecord(
                self.logger.name,
                level,
                "",
                0,
                message,
                (),
                None
            )
            record.extra_fields = extra_fields
            self.logger.handle(record)
        else:
            self.logger.log(level, message)
    
    def log_query_processing(self, query: str, query_type: str, **kwargs: Any) -> None:
        """
        Log query processing information.
        
        Args:
            query: The user query
            query_type: Type of query (alternatives, comparison, etc.)
            **kwargs: Additional context fields
        """
        self.info(
            "Processing query",
            query=query,
            query_type=query_type,
            **kwargs
        )
    
    def log_search_operation(self, query: str, results_count: int, **kwargs: Any) -> None:
        """
        Log search operation information.
        
        Args:
            query: The search query
            results_count: Number of results returned
            **kwargs: Additional context fields
        """
        self.info(
            "Search operation completed",
            query=query,
            results_count=results_count,
            **kwargs
        )
    
    def log_llm_operation(self, operation: str, model: str, **kwargs: Any) -> None:
        """
        Log LLM operation information.
        
        Args:
            operation: The LLM operation (extraction, analysis, etc.)
            model: The LLM model used
            **kwargs: Additional context fields
        """
        self.info(
            "LLM operation completed",
            operation=operation,
            model=model,
            **kwargs
        )
    
    def log_error(self, error: Exception, context: str, **kwargs: Any) -> None:
        """
        Log error information with context.
        
        Args:
            error: The exception that occurred
            context: Context where the error occurred
            **kwargs: Additional context fields
        """
        self.error(
            f"Error in {context}: {str(error)}",
            error_type=type(error).__name__,
            context=context,
            **kwargs
        )
    
    def log_performance(self, operation: str, duration: float, **kwargs: Any) -> None:
        """
        Log performance metrics.
        
        Args:
            operation: The operation being measured
            duration: Duration in seconds
            **kwargs: Additional context fields
        """
        self.info(
            "Performance metric",
            operation=operation,
            duration_seconds=duration,
            **kwargs
        )


def get_logger(name: str = "dev_tools_agent", level: str = "INFO") -> DevToolsLogger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        level: Log level
        
    Returns:
        DevToolsLogger instance
    """
    return DevToolsLogger(name, level)


# Global logger instance
logger = get_logger() 