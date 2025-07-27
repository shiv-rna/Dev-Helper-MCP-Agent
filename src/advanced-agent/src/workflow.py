from typing import Any, Dict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .models import ResearchState, CompanyInfo, CompanyAnalysis
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts

class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.prompts = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)

        graph.set_entry_point("extract_tools")
        graph.add_edge(start_key= "extract_tools", end_key= "research")
        graph.add_edge(start_key= "research", end_key= "analyze")
        graph.add_edge(start_key= "analyze", end_key= END)
        return graph.compile()

        

    def _extract_tools_step(self, state:ResearchState) -> Dict[str, Any]:
        print(f"🔍 Finding articles about: {state.query}")

        article_query = f"{state.query} tools comparison best alternatives"
        search_results = self.firecrawl.search_company(query=article_query, num_results=3)

        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_company_page(url=url)
            if scraped:
                all_content += scraped.markdown[:1500] + "\n\n"

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
            print(f"🔧 Extracted tools: {', '.join(tool_names[:5])}")
            return {"extracted_tools": tool_names}
            # Langgraph will handle the state update automatically
        except Exception as e:
            print(f"❌ Error extracting tools: {e}")
            return {"extracted_tools": []}

    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        # LLM to output structured analysis of the company content 
        # This is most important learning step from this code workflow
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name=company_name, content=content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            print(f"📊 Analysis for {company_name} completed !")
            return analysis
        except Exception as e:
            print(f"❌ Error analyzing company content: {e}")
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Analysis failed",
                api_available=None,
                language_support=[],
                integration_capabilities=[]
            )

    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_tools = getattr(state, "extracted_tools", [])
        if not extracted_tools:
            print("⚠️ No tools extracted, Falling back to direct search.")
            search_results = self.firecrawl.search_company(query=state.query, num_results=4)
            tool_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            tool_names = extracted_tools[:2]
        
        print(f"🔬 Researching specific tools: {', '.join(tool_names)}")

        companies = []

        for tool_name in tool_names:
            try:
                tool_search_results = self.firecrawl.search_company(query= tool_name + " official site ", num_results=1)
            except Exception as e:
                print(f"❌ Error searching for tool {tool_name}: {e}")
                continue

            if tool_search_results:
                result = tool_search_results.data[0]
                url = result.get("url", "")
                
                company=CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown", ""), # This description of the site url
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                scraped = self.firecrawl.scrape_company_page(url=url)
                if scraped:
                    content = scraped.markdown[:2500]  # Limit to 2500 characters
                    analysis = self._analyze_company_content(company_name=company.name, content=content)
                    
                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities

                companies.append(company)

        print(f"🏢 Found {len(companies)} companies/tools in research step.")
        return {"companies": companies}

    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
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
            print("✅ Recommendations generated successfully.")
            return {"analysis": response.content}
        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            return {"analysis": "Failed to generate recommendations."}
        
    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        print("🚀 Workflow completed successfully.")
        return ResearchState(**final_state)  # Convert to ResearchState for consistency
    
        





