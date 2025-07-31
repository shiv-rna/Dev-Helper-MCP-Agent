"""
Enhanced workflow for the Developer Tools Agent with dynamic query formation.

This module implements the main workflow with improved query processing,
better error handling, and integration with the new query builder system.
"""

from typing import Any, Dict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from ..models import ResearchState, CompanyInfo, CompanyAnalysis
from ..services import FirecrawlService
from ..prompts import DeveloperToolsPrompts
from ..search.query_builder import QueryBuilder
from ..config.settings import settings
from ..utils.error_handler import handle_llm_errors, LLMError, ErrorHandler
from ..utils.logger import logger


class Workflow:
    """
    Enhanced workflow with dynamic query formation and improved error handling.
    
    This class addresses the poor query formation issue by:
    1. Using intelligent query builders for different query types
    2. Implementing comprehensive error handling and retry mechanisms
    3. Providing fallback strategies for failed operations
    4. Adding detailed logging for debugging and monitoring
    """
    
    def __init__(self):
        """Initialize the workflow with enhanced components."""
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(
            model=settings.llm.model_name,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens
        )
        self.prompts = DeveloperToolsPrompts()
        self.query_builder = QueryBuilder()
        self.error_handler = ErrorHandler(logger)
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Build the enhanced workflow graph."""
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)

        graph.set_entry_point("extract_tools")
        graph.add_edge(start_key="extract_tools", end_key="research")
        graph.add_edge(start_key="research", end_key="analyze")
        graph.add_edge(start_key="analyze", end_key=END)
        return graph.compile()

    def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        """
        Enhanced tool extraction step with dynamic query formation.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with extracted tools
        """
        logger.log_query_processing(
            query=state.query,
            query_type="tool_extraction"
        )
        
        print(f"🔍 Finding articles about: {state.query}")

        # Use query builder to create optimized article query
        query_info = self.query_builder.create_queries(state.query)
        article_query = query_info['article_query']
        
        logger.info(
            "Using optimized article query",
            original_query=state.query,
            optimized_query=article_query
        )

        try:
            # Use the new search_articles method
            search_results = self.firecrawl.search_articles(query=state.query, num_results=3)
        except Exception as e:
            logger.log_error(e, "article_search", query=state.query)
            # Fallback to original method
            search_results = self.firecrawl.search_company(query=article_query, num_results=3)

        all_content = ""
        for result in search_results:
            url = result.get("url", "")
            try:
                scraped = self.firecrawl.scrape_company_page(url=url)
                if scraped and hasattr(scraped, 'markdown'):
                    all_content += scraped.markdown[:1500] + "\n\n"
            except Exception as e:
                logger.log_error(e, "page_scraping", url=url)
                continue

        if not all_content.strip():
            logger.warning("No content extracted from search results", query=state.query)
            return {"extracted_tools": []}

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(query=state.query, content=all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            tool_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            
            logger.log_llm_operation(
                operation="tool_extraction",
                model=settings.llm.model_name,
                tools_extracted=len(tool_names)
            )
            
            print(f"🔧 Extracted tools: {', '.join(tool_names[:5])}")
            return {"extracted_tools": tool_names}
            
        except Exception as e:
            logger.log_error(e, "tool_extraction_llm", query=state.query)
            print(f"❌ Error extracting tools: {e}")
            return {"extracted_tools": []}

    @handle_llm_errors
    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        """
        Enhanced company content analysis with better error handling.
        
        Args:
            company_name: Name of the company/tool
            content: Content to analyze
            
        Returns:
            Structured analysis of the company content
            
        Raises:
            LLMError: If LLM analysis fails
        """
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name=company_name, content=content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            
            logger.log_llm_operation(
                operation="company_analysis",
                model=settings.llm.model_name,
                company_name=company_name
            )
            
            print(f"📊 Analysis for {company_name} completed!")
            return analysis
            
        except Exception as e:
            logger.log_error(e, "company_analysis", company_name=company_name)
            raise LLMError(f"Analysis failed for {company_name}: {str(e)}") from e

    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        """
        Enhanced research step with improved error handling and fallback strategies.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with researched companies
        """
        extracted_tools = getattr(state, "extracted_tools", [])
        
        if not extracted_tools:
            logger.warning("No tools extracted, falling back to direct search", query=state.query)
            print("⚠️ No tools extracted, Falling back to direct search.")
            
            try:
                search_results = self.firecrawl.search_with_fallback(query=state.query, num_results=4)
                tool_names = [
                    result.get("metadata", {}).get("title", "Unknown")
                    for result in search_results
                ]
            except Exception as e:
                logger.log_error(e, "fallback_search", query=state.query)
                tool_names = [state.query]  # Use original query as fallback
        else:
            tool_names = extracted_tools[:2]
        
        print(f"🔬 Researching specific tools: {', '.join(tool_names)}")

        companies = []

        for tool_name in tool_names:
            try:
                # Use optimized search query for tool research
                query_info = self.query_builder.create_queries(tool_name)
                search_query = f"{tool_name} official site"
                
                tool_search_results = self.firecrawl.search_company(query=search_query, num_results=1)
                
            except Exception as e:
                logger.log_error(e, "tool_search", tool_name=tool_name)
                continue

            if tool_search_results:
                result = tool_search_results[0]
                url = result.get("url", "")
                
                company = CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown", ""),
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                try:
                    scraped = self.firecrawl.scrape_company_page(url=url)
                    if scraped and hasattr(scraped, 'markdown'):
                        content = scraped.markdown[:2500]  # Limit to 2500 characters
                        analysis = self._analyze_company_content(company_name=company.name, content=content)
                        
                        company.pricing_model = analysis.pricing_model
                        company.is_open_source = analysis.is_open_source
                        company.tech_stack = analysis.tech_stack
                        company.description = analysis.description
                        company.api_available = analysis.api_available
                        company.language_support = analysis.language_support
                        company.integration_capabilities = analysis.integration_capabilities
                        
                except Exception as e:
                    logger.log_error(e, "company_analysis", tool_name=tool_name)
                    # Continue with basic company info

                companies.append(company)

        logger.info(
            "Research step completed",
            tools_researched=len(tool_names),
            companies_found=len(companies)
        )
        
        print(f"🏢 Found {len(companies)} companies/tools in research step.")
        return {"companies": companies}

    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        """
        Enhanced analysis step with improved error handling.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with analysis results
        """
        print("📝 Generating recommendations based on research findings...")

        company_data = [
            company.json() for company in state.companies
        ]

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATION_SYSTEM),
            HumanMessage(content=self.prompts.recommendation_user(query=state.query, company_data=company_data))
        ]

        try:
            response = self.llm.invoke(messages)
            
            logger.log_llm_operation(
                operation="recommendation_generation",
                model=settings.llm.model_name,
                companies_analyzed=len(state.companies)
            )
            
            print("✅ Recommendations generated successfully.")
            return {"analysis": response.content}
            
        except Exception as e:
            logger.log_error(e, "recommendation_generation", query=state.query)
            print(f"❌ Error generating recommendations: {e}")
            return {"analysis": "Failed to generate recommendations."}
        
    def run(self, query: str) -> ResearchState:
        """
        Run the enhanced workflow with improved error handling and logging.
        
        Args:
            query: User query to process
            
        Returns:
            Final research state with results
        """
        logger.info("Starting workflow execution", query=query)
        
        try:
            initial_state = ResearchState(query=query)
            final_state = self.workflow.invoke(initial_state)
            
            logger.info(
                "Workflow completed successfully",
                query=query,
                tools_extracted=len(final_state.get("extracted_tools", [])),
                companies_researched=len(final_state.get("companies", []))
            )
            
            print("🚀 Workflow completed successfully.")
            return ResearchState(**final_state)
            
        except Exception as e:
            logger.log_error(e, "workflow_execution", query=query)
            print(f"❌ Workflow failed: {e}")
            # Return a minimal state with error information
            return ResearchState(
                query=query,
                extracted_tools=[],
                companies=[],
                analysis=f"Workflow failed: {str(e)}"
            )
    
    def get_query_analysis(self, query: str) -> Dict[str, Any]:
        """
        Get detailed analysis of a query for debugging and optimization.
        
        Args:
            query: The user query to analyze
            
        Returns:
            Dictionary with query analysis information
        """
        return self.firecrawl.get_query_analysis(query)
    
        





