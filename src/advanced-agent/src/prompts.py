"""
This module contains prompts for analyzing developer tools and their impact on software development.
It includes prompts for extracting tool names and analyzing company information relevant to developers.
"""


class DeveloperToolsPrompts:
    """Collection of prompts for analyzing developer tools and their impact on software development."""

    # Tool Extraction Prompt
    TOOL_EXTRACTION_SYSTEM = """You are a tech researcher. Extract specific tool, library, platform, or service names from articles.
                            Focus on actual products/tools that developers can use, not general concepts or features."""
    
    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""
        Query: {query}
        Article Content: {content}

        Extract a list of specific tool/service names mentioned in this content that are relevant to "{query}".

        Rules:
        - Only inclue actual product/tool names, not generic terms or concepts.
        - Focus on tools that developers can use directly use/implement.
        - Include both open source and commercial tools.
        - Limit to the 5 most relevant tools.
        - Return jus the tool names, one per line, no descriptions

        Example format:
        Tool 1
        Tool 2
        Tool 3
        """
    
    # Company/Tool Analysis Prompt
    TOOL_ANALYSIS_SYSTEM = """You are analyzing developer tools and programming technologies. 
                            Focus on extracting information relevant to programmers and software developers. 
                            Pay special attention to programming languages, frameworks, APIs, SDKs, and development workflows."""
    
    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        return f"""
        Company/Tool: {company_name}
        Website Content: {content[:2500]}

        Analyze this content from a developer's perspective and provide:
        - pricing_model: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown"
        - is_open_source: true if open source, false if proprietary, null if unclear
        - tech_stack: List of programming languages, frameworks, databases, APIs, or technologies supported/used
        - description: Brief 1-sentence description focusing on what this tool does for developers
        - api_available: true if REST API, GraphQL, SDK, or programmatic access is mentioned
        - language_support: List of programming languages explicitly supported (e.g., Python, JavaScript, Go, etc.)
        - integration_capabilities: List of tools/platforms it integrates with (e.g., GitHub, VS Code, Docker, AWS, etc.)

        Focus on developer-relevant features like APIs, SDKs, language support, integrations, and development workflows.
        """
    
    # Recommendation Prompts
    RECOMMENDATION_SYSTEM = """You are a senior software engineer providing quick, concise tech recommendations. 
                            Keep responses brief and actionable - maximum 3-4 sentences total."""

    @staticmethod
    def recommendation_user(query: str, company_data: str) -> str:
        return f"""
        Developer Query: {query}
        Tools/Technology Analyzed: {company_data}

        Provide a brief recommendation (3-4 sentences max) covering:
        - Which tool is best and why
        - Key cost/pricing consideration
        - Main technical advantage

        Be concise and direct - no long explanations needed.
        """
