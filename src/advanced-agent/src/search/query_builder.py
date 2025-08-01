"""
Dynamic Query Builder for intelligent search query formation.

This module implements query classification and specialized query templates
to improve search accuracy and relevance for different types of developer tool queries.
"""

from typing import List, Dict, Optional, Literal
from enum import Enum
import re
from dataclasses import dataclass


class QueryType(Enum):
    """Enumeration of different query types for classification."""
    ALTERNATIVES = "alternatives"
    COMPARISON = "comparison"
    FEATURES = "features"
    PRICING = "pricing"
    TUTORIAL = "tutorial"
    INTEGRATION = "integration"
    GENERAL = "general"


class ToolCategory(Enum):
    """Enumeration of different tool categories."""
    MONITORING = "monitoring"
    CI_CD = "ci_cd"
    DATABASE = "database"
    CLOUD = "cloud"
    MACHINE_LEARNING = "machine_learning"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DEVOPS = "devops"
    SECURITY = "security"
    TESTING = "testing"
    GENERAL = "general"


@dataclass
class QueryContext:
    """Context information for query building."""
    query_type: QueryType
    tool_category: ToolCategory
    original_query: str
    target_tool: Optional[str] = None
    comparison_tools: Optional[List[str]] = None


class QueryBuilder:
    """
    Dynamic query builder that creates intelligent search queries based on query type and context.
    
    This class addresses the poor query formation issue by:
    1. Classifying queries into different types
    2. Identifying tool categories
    3. Generating specialized query templates
    4. Validating and optimizing queries
    """
    
    def __init__(self):
        # Query type patterns for classification
        self.query_patterns = {
            QueryType.ALTERNATIVES: [
                r'\b(alternatives?|replacement|substitute|instead of|similar to)\b',
                r'\bvs\b|\bversus\b',
                r'\bcompare\b',
                r'\bother\b.*\btools?\b'
            ],
            QueryType.COMPARISON: [
                r'\bcompare\b',
                r'\bvs\b|\bversus\b',
                r'\bdifference\b',
                r'\bwhich.*better\b'
            ],
            QueryType.FEATURES: [
                r'\bfeatures?\b',
                r'\bcapabilities?\b',
                r'\bwhat.*can.*do\b',
                r'\bfunctionality\b'
            ],
            QueryType.PRICING: [
                r'\bpricing\b',
                r'\bcost\b',
                r'\bprice\b',
                r'\bfree\b',
                r'\bpaid\b'
            ],
            QueryType.TUTORIAL: [
                r'\btutorial\b',
                r'\bhow.*to\b',
                r'\bguide\b',
                r'\bgetting.*started\b'
            ],
            QueryType.INTEGRATION: [
                r'\bintegration\b',
                r'\bapi\b',
                r'\bsdk\b',
                r'\bconnect\b'
            ]
        }
        
        # Tool category patterns
        self.category_patterns = {
            ToolCategory.MONITORING: [
                r'\bmonitoring\b', r'\blogging\b', r'\banalytics\b', r'\bobservability\b',
                r'\bdatadog\b', r'\bnewrelic\b', r'\bgrafana\b', r'\bprometheus\b'
            ],
            ToolCategory.CI_CD: [
                r'\bci\b', r'\bcd\b', r'\bcontinuous\b', r'\bdeployment\b', r'\bjenkins\b',
                r'\bgithub.*actions\b', r'\bgitlab\b', r'\bcircleci\b', r'\btravis\b'
            ],
            ToolCategory.DATABASE: [
                r'\bdatabase\b', r'\bpostgresql\b', r'\bmysql\b', r'\bmongodb\b',
                r'\bredis\b', r'\belasticsearch\b', r'\bclickhouse\b'
            ],
            ToolCategory.CLOUD: [
                r'\baws\b', r'\bazure\b', r'\bgcp\b', r'\bcloud\b', r'\bkubernetes\b',
                r'\bdocker\b', r'\bterraform\b', r'\bansible\b'
            ],
            ToolCategory.MACHINE_LEARNING: [
                r'\bml\b', r'\bmachine.*learning\b', r'\bai\b', r'\bartificial.*intelligence\b',
                r'\btensorflow\b', r'\bpytorch\b', r'\bscikit.*learn\b', r'\bmlflow\b'
            ],
            ToolCategory.FRONTEND: [
                r'\bfrontend\b', r'\breact\b', r'\bvue\b', r'\bangular\b', r'\bui\b',
                r'\bux\b', r'\bdesign\b', r'\bcomponent\b'
            ],
            ToolCategory.BACKEND: [
                r'\bbackend\b', r'\bapi\b', r'\bserver\b', r'\bnode\b', r'\bdjango\b',
                r'\bflask\b', r'\bfastapi\b', r'\bspring\b'
            ],
            ToolCategory.DEVOPS: [
                r'\bdevops\b', r'\bdeployment\b', r'\borchestration\b', r'\bcontainer\b',
                r'\bkubernetes\b', r'\bdocker\b', r'\bhelm\b'
            ],
            ToolCategory.SECURITY: [
                r'\bsecurity\b', r'\bauthentication\b', r'\bauthorization\b', r'\bencryption\b',
                r'\bvault\b', r'\bkeycloak\b', r'\boauth\b'
            ],
            ToolCategory.TESTING: [
                r'\btesting\b', r'\btest\b', r'\bqa\b', r'\bquality\b', r'\bcypress\b',
                r'\bselenium\b', r'\bjest\b', r'\bpytest\b'
            ]
        }
        
        # Specialized query templates for different query types and categories
        self.query_templates = {
            QueryType.ALTERNATIVES: {
                ToolCategory.MONITORING: "{tool} alternatives monitoring logging observability",
                ToolCategory.CI_CD: "{tool} alternatives CI CD pipeline deployment",
                ToolCategory.DATABASE: "{tool} alternatives database management",
                ToolCategory.CLOUD: "{tool} alternatives cloud infrastructure",
                ToolCategory.MACHINE_LEARNING: "{tool} alternatives machine learning AI",
                ToolCategory.FRONTEND: "{tool} alternatives frontend framework UI",
                ToolCategory.BACKEND: "{tool} alternatives backend API framework",
                ToolCategory.DEVOPS: "{tool} alternatives devops deployment",
                ToolCategory.SECURITY: "{tool} alternatives security authentication",
                ToolCategory.TESTING: "{tool} alternatives testing framework",
                ToolCategory.GENERAL: "{tool} alternatives similar tools"
            },
            QueryType.COMPARISON: {
                ToolCategory.GENERAL: "{tool1} vs {tool2} comparison features pricing"
            },
            QueryType.FEATURES: {
                ToolCategory.GENERAL: "{tool} features capabilities documentation"
            },
            QueryType.PRICING: {
                ToolCategory.GENERAL: "{tool} pricing cost plans pricing model"
            },
            QueryType.TUTORIAL: {
                ToolCategory.GENERAL: "{tool} tutorial getting started guide documentation"
            },
            QueryType.INTEGRATION: {
                ToolCategory.GENERAL: "{tool} integration API SDK documentation"
            },
            QueryType.GENERAL: {
                ToolCategory.GENERAL: "{tool} developer tools software"
            }
        }
    
    def classify_query(self, query: str) -> QueryContext:
        """
        Classify the query type and identify tool category.
        
        Args:
            query: The original user query
            
        Returns:
            QueryContext object with classification results
        """
        query_lower = query.lower()
        
        # Classify query type
        query_type = QueryType.GENERAL
        for qtype, patterns in self.query_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    query_type = qtype
                    break
            if query_type != QueryType.GENERAL:
                break
        
        # Identify tool category
        tool_category = ToolCategory.GENERAL
        for category, patterns in self.category_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    tool_category = category
                    break
            if tool_category != ToolCategory.GENERAL:
                break
        
        # Extract target tool name
        target_tool = self._extract_tool_name(query)
        
        # Extract comparison tools for comparison queries
        comparison_tools = None
        if query_type == QueryType.COMPARISON:
            comparison_tools = self._extract_comparison_tools(query)
        
        return QueryContext(
            query_type=query_type,
            tool_category=tool_category,
            original_query=query,
            target_tool=target_tool,
            comparison_tools=comparison_tools
        )
    
    def _extract_tool_name(self, query: str) -> Optional[str]:
        """
        Extract the main tool name from the query.
        
        Args:
            query: The user query
            
        Returns:
            Extracted tool name or None
        """
        # Remove common query words
        query_clean = re.sub(r'\b(alternatives?|vs|versus|compare|features?|pricing|tutorial|guide|how|to|best|top|review)\b', '', query.lower())
        query_clean = re.sub(r'\s+', ' ', query_clean).strip()
        
        # For now, return the cleaned query as the tool name
        # In a more sophisticated implementation, this could use NLP to extract proper nouns
        return query_clean if query_clean else None
    
    def _extract_comparison_tools(self, query: str) -> Optional[List[str]]:
        """
        Extract tool names for comparison queries.
        
        Args:
            query: The user query
            
        Returns:
            List of tool names to compare or None
        """
        # Simple extraction for "tool1 vs tool2" format
        vs_pattern = r'(\w+(?:\s+\w+)*)\s+(?:vs|versus)\s+(\w+(?:\s+\w+)*)'
        match = re.search(vs_pattern, query, re.IGNORECASE)
        
        if match:
            return [match.group(1).strip(), match.group(2).strip()]
        
        return None
    
    def build_search_query(self, context: QueryContext) -> str:
        """
        Build an optimized search query based on the query context.
        
        Args:
            context: QueryContext object with classification results
            
        Returns:
            Optimized search query string
        """
        if not context.target_tool:
            return context.original_query
        
        # Get the appropriate template
        templates = self.query_templates.get(context.query_type, {})
        template = templates.get(context.tool_category, templates.get(ToolCategory.GENERAL, "{tool}"))
        
        # Fill the template
        if context.query_type == QueryType.COMPARISON and context.comparison_tools:
            if len(context.comparison_tools) >= 2:
                return template.format(
                    tool1=context.comparison_tools[0],
                    tool2=context.comparison_tools[1]
                )
        
        return template.format(tool=context.target_tool)
    
    def build_article_query(self, context: QueryContext) -> str:
        """
        Build a query for finding articles about the tool/topic.
        
        Args:
            context: QueryContext object with classification results
            
        Returns:
            Article search query string
        """
        if not context.target_tool:
            return f"{context.original_query} developer tools comparison"
        
        base_query = context.target_tool
        
        if context.query_type == QueryType.ALTERNATIVES:
            return f"{base_query} alternatives comparison best tools"
        elif context.query_type == QueryType.COMPARISON:
            return f"{base_query} comparison review analysis"
        elif context.query_type == QueryType.FEATURES:
            return f"{base_query} features capabilities review"
        elif context.query_type == QueryType.PRICING:
            return f"{base_query} pricing cost analysis"
        else:
            return f"{base_query} developer tools software review"
    
    def validate_query(self, query: str) -> bool:
        """
        Validate if the query is well-formed and suitable for search.
        
        Args:
            query: The search query to validate
            
        Returns:
            True if query is valid, False otherwise
        """
        if not query or len(query.strip()) < 2:
            return False
        
        # Check for excessive special characters
        special_char_ratio = len(re.findall(r'[^\w\s]', query)) / len(query)
        if special_char_ratio > 0.3:
            return False
        
        return True
    
    def optimize_query(self, query: str) -> str:
        """
        Optimize the query for better search results.
        
        Args:
            query: The original query
            
        Returns:
            Optimized query string
        """
        # Remove excessive whitespace
        query = re.sub(r'\s+', ' ', query).strip()
        
        # Remove common stop words that don't add value to search
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = query.split()
        optimized_words = [word for word in words if word.lower() not in stop_words]
        
        return ' '.join(optimized_words) if optimized_words else query
    
    def create_queries(self, original_query: str) -> Dict[str, str]:
        """
        Create multiple optimized queries for different search purposes.
        
        Args:
            original_query: The original user query
            
        Returns:
            Dictionary containing different types of queries
        """
        context = self.classify_query(original_query)
        
        search_query = self.build_search_query(context)
        article_query = self.build_article_query(context)
        
        # Optimize queries
        search_query = self.optimize_query(search_query)
        article_query = self.optimize_query(article_query)
        
        return {
            'search_query': search_query,
            'article_query': article_query,
            'context': context
        } 