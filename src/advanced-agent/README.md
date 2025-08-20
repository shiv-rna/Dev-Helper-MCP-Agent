# Developer Tools Agent - Phase 1.1 Implementation

## Overview

This repository contains the Phase 1.1 implementation of the Developer Tools Agent, which addresses the **poor query formation issue** identified in the PRD. The implementation introduces dynamic query formation with intelligent classification, specialized templates, and comprehensive error handling.

## 🎯 Phase 1.1: Dynamic Query Formation

### Problem Addressed

The original implementation had a critical issue with poor query formation:
- **Location**: `src/firecrawl.py:18`
- **Problem**: Search queries were hardcoded with generic "company pricing" suffix
- **Impact**: 
  - Returns irrelevant results for open-source tools
  - Misses specialized developer tools
  - Poor accuracy for different tool categories

### Solution Implemented

Phase 1.1 implements **Dynamic Query Formation** with the following features:

1. **Intelligent Query Classification**
   - Automatically detects query types (alternatives, comparison, features, pricing, tutorial, integration, general)
   - Identifies tool categories (monitoring, CI/CD, database, cloud, ML, frontend, backend, etc.)
   - Extracts target tools and comparison tools

2. **Specialized Query Templates**
   - Category-specific templates for different tool types
   - Context-aware query optimization
   - Support for 7 query types and 11 tool categories

3. **Query Validation and Optimization**
   - Validates query quality and length
   - Removes stop words and optimizes for search engines
   - Provides fallback strategies for invalid queries

4. **Comprehensive Error Handling**
   - Retry mechanisms with exponential backoff
   - Graceful degradation for failed operations
   - Detailed error logging and recovery strategies

## 🏗️ Architecture

### Current Directory Structure

```
src/
├── workflows/               # Workflow orchestration
│   ├── __init__.py
│   └── developer_tools.py   # Main workflow implementation
├── models/                  # Data models and schemas
│   ├── __init__.py
│   └── schemas.py           # Pydantic models
├── services/                # External service integrations
│   ├── __init__.py
│   ├── firecrawl.py         # Enhanced search service
│   └── serper_search.py     # Serper API integration
├── prompts/                 # Prompt management
│   ├── __init__.py
│   └── developer_tools.py   # Prompt templates
├── search/                  # Search functionality
│   ├── __init__.py
│   └── strategies/
│       ├── __init__.py
│       └── hybrid_search.py # Hybrid search strategy (Firecrawl + Serper)
├── config/                  # Configuration management
│   ├── __init__.py
│   └── settings.py          # Application settings
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── query_builder.py     # Dynamic query formation
│   ├── error_handler.py     # Error handling and retries
│   └── logger.py            # Structured logging
├── analysis/                # Analysis utilities
│   └── __init__.py
└── __init__.py
```

### Key Components

#### 1. QueryBuilder (`src/utils/query_builder.py`)
- **QueryType Enum**: Defines 7 different query types (alternatives, comparison, features, pricing, tutorial, integration, general)
- **ToolCategory Enum**: Defines 11 tool categories (monitoring, CI/CD, database, cloud, machine_learning, frontend, backend, devops, security, testing, general)
- **QueryContext**: Contains classification results and context
- **QueryBuilder Class**: Main class for dynamic query formation with pattern-based classification

#### 2. Settings (`src/config/settings.py`)
- **SearchSettings**: Configuration for search operations (Firecrawl + Serper)
- **LLMSettings**: Configuration for LLM operations (OpenAI)
- **CacheSettings**: Configuration for caching (future use)
- **LoggingSettings**: Configuration for logging

#### 3. Error Handler (`src/utils/error_handler.py`)
- **Custom Exceptions**: SearchError, QueryError, LLMError, etc.
- **Retry Decorators**: Automatic retry with exponential backoff
- **ErrorHandler Class**: Centralized error handling and recovery

#### 4. Logger (`src/utils/logger.py`)
- **StructuredFormatter**: JSON-like log output
- **DevToolsLogger**: Centralized logging with context
- **Performance Tracking**: Operation timing and metrics

#### 5. Hybrid Search (`src/search/strategies/hybrid_search.py`)
- **SearchResult**: Unified search result structure
- **SearchSource**: Enum for different search sources
- **HybridSearchStrategy**: Combines Firecrawl and Serper API

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Required API keys (see Configuration section)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

### Configuration

Create a `.env` file with the following variables:

```bash
# Required
FIRECRAWL_API_KEY=your_firecrawl_api_key
OPENAI_API_KEY=your_openai_api_key

# Optional
SERPER_API_KEY=your_serper_api_key
MAX_SEARCH_RESULTS=5
SEARCH_TIMEOUT=30
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000
LOG_LEVEL=INFO
ENABLE_SERPER_FALLBACK=false
```

### Running the Application

#### Interactive Mode
```bash
uv run main.py
```

#### Test Suite
```bash
uv run python tests/test_phase1_1.py
```

#### Demo Script
```bash
uv run python tests/demo_phase1_1.py
```

## 📊 Features

### Query Classification Examples

| Query | Type | Category | Target Tool |
|-------|------|----------|-------------|
| "mlflow alternatives" | alternatives | machine_learning | mlflow |
| "datadog vs newrelic" | comparison | monitoring | datadog, newrelic |
| "jenkins features" | features | ci_cd | jenkins |
| "postgresql pricing" | pricing | database | postgresql |
| "react tutorial" | tutorial | frontend | react |
| "docker integration" | integration | devops | docker |

### Dynamic Query Templates

The system generates optimized queries based on query type and tool category:

**Alternatives Query (ML Category):**
- Original: "mlflow alternatives"
- Optimized: "mlflow alternatives machine learning AI"

**Comparison Query (Monitoring Category):**
- Original: "datadog vs newrelic"
- Optimized: "datadog vs newrelic comparison features pricing"

**Features Query (CI/CD Category):**
- Original: "jenkins features"
- Optimized: "jenkins features capabilities documentation"

### Error Handling

The system provides comprehensive error handling:

1. **Search Failures**: Automatic fallback to Serper API when configured
2. **LLM Failures**: Retry with exponential backoff
3. **Invalid Queries**: Validation and recovery strategies
4. **Network Issues**: Connection retry mechanisms

## 🧪 Testing

### Test Suite

Run the comprehensive test suite:

```bash
uv run python tests/test_phase1_1.py
```

The test suite covers:
- Query classification accuracy
- Query optimization effectiveness
- Dynamic query formation
- Error handling scenarios
- Configuration validation

### Demo Script

Run the demonstration script to see before/after improvements:

```bash
uv run python tests/demo_phase1_1.py
```

### Manual Testing

Use the interactive application to test queries:

```bash
uv run main.py
```

Available commands:
- `analyze` - Analyze a query without running the full workflow
- `config` - Show current configuration
- `help` - Show help information
- `exit` - Exit the application

## 📈 Performance Improvements

### Before Phase 1.1
- Hardcoded queries with "company pricing" suffix
- No query classification or optimization
- Limited error handling
- Poor results for non-pricing queries

### After Phase 1.1
- **7 query types supported** (alternatives, comparison, features, pricing, tutorial, integration, general)
- **11 tool categories supported** (monitoring, CI/CD, database, cloud, ML, frontend, backend, devops, security, testing, general)
- **Pattern-based query classification** for accurate type detection
- **Hybrid search strategy** combining Firecrawl and Serper API
- **Comprehensive error handling and recovery**
- **Structured logging for debugging**

## 🔮 Future Phases

Phase 1.1 is designed to be compatible with future phases:

### Phase 1.2: Enhanced Serper Integration
- The query builder is ready for enhanced Serper API integration
- Configuration settings already include Serper API settings
- Error handling supports multiple search providers

### Phase 2: Enhanced Tool Discovery
- Query classification provides foundation for better alternative finding
- Tool categories enable specialized discovery strategies
- Error handling supports additional data sources

### Phase 3: Enhanced Prompts
- Query context can be used for prompt selection
- Tool categories enable specialized prompts
- Logging provides data for prompt optimization

## 🐛 Troubleshooting

### Common Issues

1. **Missing API Keys**
   ```
   ValueError: Missing FIRECRAWL_API_KEY in environment variables
   ```
   Solution: Set required environment variables in `.env` file

2. **Query Classification Issues**
   - Check query format and length
   - Use the `analyze` command to debug query processing
   - Review logs for classification details

3. **Search Failures**
   - Check API key validity
   - Review network connectivity
   - Check rate limits and quotas

### Debugging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

Use query analysis:
```bash
uv run main.py
# Enter: analyze
# Enter your query for detailed analysis
```

## 📝 API Reference

### QueryBuilder

```python
from src.utils.query_builder import QueryBuilder

builder = QueryBuilder()

# Classify a query
context = builder.classify_query("mlflow alternatives")

# Create optimized queries
queries = builder.create_queries("mlflow alternatives")

# Validate a query
is_valid = builder.validate_query("mlflow alternatives")
```

### Settings

```python
from src.config.settings import settings

# Access search settings
api_key = settings.search.firecrawl_api_key
max_results = settings.search.max_search_results

# Access LLM settings
model = settings.llm.model_name
temperature = settings.llm.temperature
```

### Logger

```python
from src.utils.logger import logger

# Log with context
logger.info("Operation completed", query="mlflow", results=5)

# Log errors
logger.log_error(error, "operation_name", query="mlflow")
```

## 🤝 Contributing

When contributing to Phase 1.1 or future phases:

1. Follow the existing code structure and patterns
2. Add comprehensive error handling
3. Include structured logging
4. Update tests for new functionality
5. Maintain backward compatibility

## 📄 License

This project is part of the Developer Tools Agent implementation.

---

**Phase 1.1 Status**: ✅ Complete  
**Next Phase**: Phase 1.2 - Enhanced Serper Integration

## 🔍 Current Implementation Status

### ✅ Fully Implemented
- Dynamic Query Builder with 7 query types and 11 tool categories
- Pattern-based query classification system
- Hybrid search strategy (Firecrawl + Serper fallback)
- Comprehensive error handling and retry mechanisms
- Structured logging system
- Configuration management with environment variables
- Main workflow with LangGraph integration
- Test suite and demonstration scripts

### 🔄 Partially Implemented
- Serper API integration (configured but optional fallback)
- Caching system (configured but not yet active)

### 📋 Ready for Future Phases
- Query classification foundation for enhanced tool discovery
- Error handling infrastructure for additional data sources
- Logging system for performance monitoring and optimization
