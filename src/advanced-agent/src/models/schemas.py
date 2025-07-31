"""
This module defines the data models used by the advanced agent for structured outputs.
It uses Pydantic for data validation and serialization.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel # Allows to validate data structures

class CompanyAnalysis(BaseModel):
    """Structured output for LLM company analysis focused on developer tools."""
    pricing_model: str # Free, Freemium, Paid, Enterprise, Unknown
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    description: str = ""
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []


class CompanyInfo(BaseModel):
    """Structured output for LLM company information."""
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    competitors: List[str] = []
    # Developer specific fields
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    developer_experience_rating: Optional[str] = None # e.g., "Excellent", "Good", "Average", "Poor"


class ResearchState(BaseModel):
    """State for the research agent."""
    query: str
    extracted_tools: List[str] = [] #Tools extracted from the articles
    companies: List[CompanyInfo] = [] # Companies identified in the research
    search_results: List[Dict[str, Any]] = [] # Raw search results
    analysis: Optional[str] = None # Analysis of the research findings

