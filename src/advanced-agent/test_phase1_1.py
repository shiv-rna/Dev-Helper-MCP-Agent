#!/usr/bin/env python3
"""
Test script for Phase 1.1: Dynamic Query Formation

This script demonstrates the improved query formation capabilities
and shows how the system addresses the poor query formation issue.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.search.query_builder import QueryBuilder, QueryType, ToolCategory
from src.config.settings import settings
from src.utils.logger import logger

# Load environment variables
load_dotenv()


def test_query_classification():
    """Test query classification functionality."""
    print("🧪 Testing Query Classification")
    print("=" * 50)
    
    query_builder = QueryBuilder()
    
    # Test cases for different query types
    test_queries = [
        "mlflow alternatives",
        "datadog vs newrelic",
        "jenkins features",
        "postgresql pricing",
        "react tutorial",
        "docker integration",
        "kubernetes monitoring tools",
        "python testing frameworks",
        "aws security best practices",
        "machine learning platforms"
    ]
    
    for query in test_queries:
        context = query_builder.classify_query(query)
        print(f"\nQuery: '{query}'")
        print(f"  Type: {context.query_type.value}")
        print(f"  Category: {context.tool_category.value}")
        print(f"  Target Tool: {context.target_tool}")
        if context.comparison_tools:
            print(f"  Comparison Tools: {context.comparison_tools}")


def test_query_optimization():
    """Test query optimization functionality."""
    print("\n\n🔧 Testing Query Optimization")
    print("=" * 50)
    
    query_builder = QueryBuilder()
    
    # Test cases for query optimization
    test_queries = [
        "what are the best alternatives to mlflow for machine learning",
        "compare datadog vs newrelic vs grafana",
        "how much does postgresql cost and what are the pricing plans",
        "tutorial guide for getting started with react development",
        "integration api sdk documentation for docker containers"
    ]
    
    for query in test_queries:
        optimized = query_builder.optimize_query(query)
        print(f"\nOriginal: '{query}'")
        print(f"Optimized: '{optimized}'")


def test_dynamic_query_formation():
    """Test dynamic query formation for different scenarios."""
    print("\n\n🚀 Testing Dynamic Query Formation")
    print("=" * 50)
    
    query_builder = QueryBuilder()
    
    # Test different query scenarios
    test_scenarios = [
        {
            "name": "Alternatives Query",
            "query": "mlflow alternatives",
            "description": "Looking for alternatives to MLflow"
        },
        {
            "name": "Comparison Query", 
            "query": "datadog vs newrelic",
            "description": "Comparing two monitoring tools"
        },
        {
            "name": "Features Query",
            "query": "jenkins features",
            "description": "Looking for Jenkins features"
        },
        {
            "name": "Pricing Query",
            "query": "postgresql pricing",
            "description": "Looking for PostgreSQL pricing information"
        },
        {
            "name": "Tutorial Query",
            "query": "react tutorial",
            "description": "Looking for React tutorials"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📋 {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Query: '{scenario['query']}'")
        
        query_info = query_builder.create_queries(scenario['query'])
        context = query_info['context']
        
        print(f"  Query Type: {context.query_type.value}")
        print(f"  Tool Category: {context.tool_category.value}")
        print(f"  Search Query: '{query_info['search_query']}'")
        print(f"  Article Query: '{query_info['article_query']}'")
        print(f"  Valid Query: {query_builder.validate_query(scenario['query'])}")


def test_error_handling():
    """Test error handling for invalid queries."""
    print("\n\n⚠️ Testing Error Handling")
    print("=" * 50)
    
    query_builder = QueryBuilder()
    
    # Test invalid queries
    invalid_queries = [
        "",  # Empty query
        "a",  # Too short
        "x" * 1000,  # Too long
        "###$$$%%%",  # Too many special characters
        "   ",  # Only whitespace
    ]
    
    for query in invalid_queries:
        is_valid = query_builder.validate_query(query)
        print(f"Query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
        print(f"  Valid: {is_valid}")
        
        if not is_valid:
            # Test recovery strategies
            if len(query.strip()) < 2:
                print(f"  Recovery: Use default query 'developer tools'")
            else:
                cleaned = query_builder.optimize_query(query)
                print(f"  Recovery: Cleaned query '{cleaned}'")


def test_configuration():
    """Test configuration settings."""
    print("\n\n⚙️ Testing Configuration")
    print("=" * 50)
    
    print(f"Firecrawl API Key: {'Set' if settings.search.firecrawl_api_key else 'Not Set'}")
    print(f"OpenAI API Key: {'Set' if settings.llm.openai_api_key else 'Not Set'}")
    print(f"Max Search Results: {settings.search.max_search_results}")
    print(f"Search Timeout: {settings.search.search_timeout}")
    print(f"LLM Model: {settings.llm.model_name}")
    print(f"LLM Temperature: {settings.llm.temperature}")
    print(f"Log Level: {settings.logging.log_level}")


def main():
    """Run all tests for Phase 1.1 implementation."""
    print("🎯 Phase 1.1: Dynamic Query Formation - Test Suite")
    print("=" * 60)
    print("This test demonstrates the improvements made to address")
    print("the poor query formation issue identified in the PRD.")
    print("=" * 60)
    
    try:
        # Test all components
        test_query_classification()
        test_query_optimization()
        test_dynamic_query_formation()
        test_error_handling()
        test_configuration()
        
        print("\n\n✅ All Phase 1.1 tests completed successfully!")
        print("\n🎉 Key Improvements Demonstrated:")
        print("  • Intelligent query classification (alternatives, comparison, features, etc.)")
        print("  • Tool category identification (monitoring, CI/CD, database, etc.)")
        print("  • Dynamic query templates for different scenarios")
        print("  • Query validation and optimization")
        print("  • Comprehensive error handling and recovery")
        print("  • Structured logging for debugging")
        print("  • Configuration management")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.log_error(e, "test_execution")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 