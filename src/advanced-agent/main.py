"""
Enhanced main application for the Developer Tools Agent with Phase 1.1 features.

This module demonstrates the improved query formation capabilities and
provides a user-friendly interface for testing the enhanced functionality.
"""

import io
import sys
import json
from dotenv import load_dotenv
from datetime import datetime
from src.workflows import Workflow
from src.search.query_builder import QueryBuilder
from src.config.settings import settings
from src.utils.logger import logger

load_dotenv()


def save_output_to_file(content: str, extension="txt"):
    """
    Save output content to a timestamped file.
    
    Args:
        content: Content to save
        extension: File extension
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"developer_tools_output_{timestamp}.{extension}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n📝 Output saved to {filename}")


def analyze_query(query: str) -> dict:
    """
    Analyze a query using the new query builder.
    
    Args:
        query: User query to analyze
        
    Returns:
        Dictionary with query analysis information
    """
    query_builder = QueryBuilder()
    return query_builder.create_queries(query)


def display_query_analysis(query: str):
    """
    Display detailed analysis of a query.
    
    Args:
        query: User query to analyze
    """
    print(f"\n🔍 Query Analysis for: '{query}'")
    print("=" * 50)
    
    try:
        analysis = analyze_query(query)
        context = analysis['context']
        
        print(f"📋 Query Type: {context.query_type.value}")
        print(f"🏷️  Tool Category: {context.tool_category.value}")
        print(f"🎯 Target Tool: {context.target_tool or 'None'}")
        
        if context.comparison_tools:
            print(f"⚖️  Comparison Tools: {', '.join(context.comparison_tools)}")
        
        print(f"\n🔧 Optimized Queries:")
        print(f"  Search: '{analysis['search_query']}'")
        print(f"  Article: '{analysis['article_query']}'")
        
        print(f"\n✅ Query Valid: {QueryBuilder().validate_query(query)}")
        
    except Exception as e:
        logger.log_error(e, "query_analysis", query=query)
        print(f"❌ Query analysis failed: {e}")


def main():
    """
    Main application with enhanced Phase 1.1 features.
    
    This function provides an interactive interface for testing the
    improved query formation and analysis capabilities.
    """
    workflow = Workflow()
    print("🐧 Developer Tools Agent - Phase 1.1 🐧")
    print("Enhanced with Dynamic Query Formation")
    print("=" * 50)

    while True:
        query = input("\n✒️  Developer Tools Query: ").strip()
        
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        
        if query.lower() == "analyze":
            # Special command to analyze the last query
            print("Please enter a query to analyze:")
            analyze_query_input = input("Query: ").strip()
            if analyze_query_input:
                display_query_analysis(analyze_query_input)
            continue
        
        if query.lower() == "config":
            # Display configuration information
            print("\n⚙️ Configuration:")
            print(f"  Firecrawl API Key: {'Set' if settings.search.firecrawl_api_key else 'Not Set'}")
            print(f"  OpenAI API Key: {'Set' if settings.llm.openai_api_key else 'Not Set'}")
            print(f"  Max Search Results: {settings.search.max_search_results}")
            print(f"  LLM Model: {settings.llm.model_name}")
            print(f"  Log Level: {settings.logging.log_level}")
            continue
        
        if query.lower() == "help":
            # Display help information
            print("\n📖 Available Commands:")
            print("  analyze - Analyze a query without running the full workflow")
            print("  config  - Show current configuration")
            print("  help    - Show this help message")
            print("  exit    - Exit the application")
            print("\n📝 Query Examples:")
            print("  mlflow alternatives")
            print("  datadog vs newrelic")
            print("  jenkins features")
            print("  postgresql pricing")
            print("  react tutorial")
            continue

        if query:
            # Show query analysis before processing
            print(f"\n🔍 Analyzing query: '{query}'")
            display_query_analysis(query)
            
            # Ask user if they want to proceed
            proceed = input("\n🚀 Proceed with workflow? (y/n): ").strip().lower()
            if proceed not in ['y', 'yes']:
                print("⏭️  Skipping workflow execution")
                continue
            
            buffer = io.StringIO()
            sys.stdout = buffer  # Redirect stdout

            try:
                logger.info("Starting workflow execution", query=query)
                result = workflow.run(query)
                
                print(f"\n📊 Results for: {query}")
                print("=" * 60)

                for i, company in enumerate(result.companies, start=1):
                    print(f"\n{i}. 🏢 {company.name}")
                    print(f"   🌐 Website: {company.website}")
                    print(f"   💰 Pricing: {company.pricing_model}")
                    print(f"   📖 Open Source: {company.is_open_source}")

                    if company.tech_stack:
                        print(f"   🛠️  Tech Stack: {', '.join(company.tech_stack[:5])}")

                    if company.language_support:
                        print(
                            f"   💻 Language Support: {', '.join(company.language_support[:5])}"
                        )

                    if company.api_available is not None:
                        api_status = (
                            "✅ Available" if company.api_available else "❌ Not Available"
                        )
                        print(f"   🔌 API: {api_status}")

                    if company.integration_capabilities:
                        print(
                            f"   🔗 Integrations: {', '.join(company.integration_capabilities[:4])}"
                        )

                    if company.description and company.description != "Analysis failed":
                        print(f"   📝 Description: {company.description}")

                    print()

                if result.analysis:
                    print(f"Developer Recommendations:")
                    print("-" * 40)
                    print(result.analysis)

                logger.info(
                    "Workflow completed successfully",
                    query=query,
                    companies_found=len(result.companies)
                )

            except Exception as e:
                logger.log_error(e, "main_workflow", query=query)
                print(f"❌ Workflow failed: {e}")
                print("Please check your configuration and try again.")

            sys.stdout = sys.__stdout__  # Reset stdout
            output = buffer.getvalue()
            save_output_to_file(output)  # Save to file
            print(output)  # Also print to console


if __name__ == "__main__":
    main()
