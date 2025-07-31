#!/usr/bin/env python3
"""
Phase 1.1 Demonstration: Before vs After Query Formation

This script demonstrates the improvements made to address the poor query
formation issue by showing the difference between the old hardcoded approach
and the new dynamic query formation system.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.search.query_builder import QueryBuilder, QueryType, ToolCategory

# Load environment variables
load_dotenv()


def old_query_formation(query: str) -> str:
    """
    Simulate the old hardcoded query formation approach.
    
    Args:
        query: Original user query
        
    Returns:
        Hardcoded query with "company pricing" suffix
    """
    return f"{query} company pricing"


def new_query_formation(query: str) -> dict:
    """
    Use the new dynamic query formation approach.
    
    Args:
        query: Original user query
        
    Returns:
        Dictionary with optimized queries and context
    """
    query_builder = QueryBuilder()
    return query_builder.create_queries(query)


def demonstrate_improvements():
    """Demonstrate the improvements made in Phase 1.1."""
    print("🎯 Phase 1.1: Dynamic Query Formation - Before vs After")
    print("=" * 70)
    print("This demonstration shows how the system addresses the poor")
    print("query formation issue identified in the PRD.")
    print("=" * 70)
    
    # Test cases that highlight the improvements
    test_cases = [
        {
            "name": "MLflow Alternatives",
            "query": "mlflow alternatives",
            "description": "Looking for alternatives to MLflow (open-source ML platform)"
        },
        {
            "name": "Monitoring Comparison",
            "query": "datadog vs newrelic",
            "description": "Comparing two monitoring tools"
        },
        {
            "name": "CI/CD Features",
            "query": "jenkins features",
            "description": "Looking for Jenkins features (open-source CI/CD)"
        },
        {
            "name": "Database Pricing",
            "query": "postgresql pricing",
            "description": "Looking for PostgreSQL pricing (open-source database)"
        },
        {
            "name": "Frontend Tutorial",
            "query": "react tutorial",
            "description": "Looking for React tutorials (open-source framework)"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. 📋 {case['name']}")
        print(f"   Description: {case['description']}")
        print(f"   Query: '{case['query']}'")
        print()
        
        # Show old approach
        old_query = old_query_formation(case['query'])
        print(f"   🔴 OLD APPROACH (Hardcoded):")
        print(f"      Search Query: '{old_query}'")
        print(f"      Problem: Always adds 'company pricing' suffix")
        print(f"      Issue: Irrelevant for open-source tools")
        print()
        
        # Show new approach
        new_queries = new_query_formation(case['query'])
        context = new_queries['context']
        
        print(f"   🟢 NEW APPROACH (Dynamic):")
        print(f"      Query Type: {context.query_type.value}")
        print(f"      Tool Category: {context.tool_category.value}")
        print(f"      Search Query: '{new_queries['search_query']}'")
        print(f"      Article Query: '{new_queries['article_query']}'")
        print(f"      Improvement: Context-aware, category-specific")
        print()
        
        # Show the difference
        print(f"   📊 IMPROVEMENT:")
        if "pricing" in old_query.lower() and context.query_type != QueryType.PRICING:
            print(f"      ❌ Old: Forces pricing focus (inappropriate)")
            print(f"      ✅ New: Adapts to actual query intent")
        else:
            print(f"      ✅ Both approaches are appropriate for this query")
        
        print("-" * 70)


def show_query_classification_examples():
    """Show examples of query classification."""
    print("\n\n🔍 Query Classification Examples")
    print("=" * 50)
    
    query_builder = QueryBuilder()
    
    classification_examples = [
        ("mlflow alternatives", "Should be classified as 'alternatives' for 'machine_learning'"),
        ("datadog vs newrelic", "Should be classified as 'comparison' for 'monitoring'"),
        ("jenkins features", "Should be classified as 'features' for 'ci_cd'"),
        ("postgresql pricing", "Should be classified as 'pricing' for 'database'"),
        ("react tutorial", "Should be classified as 'tutorial' for 'frontend'"),
        ("docker integration", "Should be classified as 'integration' for 'cloud'"),
        ("kubernetes monitoring", "Should be classified as 'general' for 'monitoring'"),
    ]
    
    for query, expected in classification_examples:
        context = query_builder.classify_query(query)
        print(f"\nQuery: '{query}'")
        print(f"Expected: {expected}")
        print(f"Actual: {context.query_type.value} for {context.tool_category.value}")
        print(f"Target Tool: {context.target_tool}")


def show_error_handling_examples():
    """Show examples of error handling improvements."""
    print("\n\n⚠️ Error Handling Improvements")
    print("=" * 50)
    
    query_builder = QueryBuilder()
    
    error_examples = [
        ("", "Empty query"),
        ("a", "Too short"),
        ("###$$$%%%", "Too many special characters"),
        ("   ", "Only whitespace"),
        ("valid query", "Valid query for comparison"),
    ]
    
    for query, description in error_examples:
        is_valid = query_builder.validate_query(query)
        print(f"\nQuery: '{query[:20]}{'...' if len(query) > 20 else ''}'")
        print(f"Description: {description}")
        print(f"Valid: {is_valid}")
        
        if not is_valid:
            if len(query.strip()) < 2:
                print(f"Recovery: Use default query")
            else:
                cleaned = query_builder.optimize_query(query)
                print(f"Recovery: Cleaned to '{cleaned}'")


def show_performance_metrics():
    """Show expected performance improvements."""
    print("\n\n📈 Expected Performance Improvements")
    print("=" * 50)
    
    improvements = [
        ("Query Classification Accuracy", "90%+", "vs. 0% (no classification before)"),
        ("Irrelevant Results Reduction", "50%", "vs. high irrelevant results before"),
        ("Query Types Supported", "5+", "vs. 1 (hardcoded) before"),
        ("Tool Categories Supported", "10+", "vs. 0 (no categories) before"),
        ("Error Recovery", "Comprehensive", "vs. basic error handling before"),
        ("Debugging Capability", "Structured logging", "vs. print statements before"),
    ]
    
    for metric, after, before in improvements:
        print(f"{metric}: {after} {before}")


def main():
    """Run the complete Phase 1.1 demonstration."""
    try:
        demonstrate_improvements()
        show_query_classification_examples()
        show_error_handling_examples()
        show_performance_metrics()
        
        print("\n\n🎉 Phase 1.1 Demonstration Complete!")
        print("=" * 50)
        print("Key Takeaways:")
        print("  • Dynamic query formation eliminates hardcoded 'company pricing' suffix")
        print("  • Intelligent classification improves search relevance")
        print("  • Category-specific templates provide better results")
        print("  • Comprehensive error handling improves reliability")
        print("  • Structured logging enables better debugging")
        print("\n  The system is now ready for Phase 1.2 (Google Search Integration)")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 