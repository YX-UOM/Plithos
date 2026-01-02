"""
ESG in Real Estate Monitor - Configuration

Customize sources, search queries, and output settings here.
"""

from datetime import datetime, timedelta

# =============================================================================
# SEARCH QUERIES
# =============================================================================

# Core search queries for web search
# These are combined with time filters to get weekly results

SEARCH_QUERIES = {
    "news": [
        # General ESG + RE
        "ESG real estate news",
        "sustainable buildings news",
        "green real estate investment",
        "net zero buildings news",
        
        # Climate & Carbon
        "real estate carbon emissions",
        "building decarbonization news",
        "embodied carbon construction",
        "CRREM carbon risk real estate",
        
        # Energy
        "building energy efficiency regulations",
        "MEES energy performance",
        "heat pump commercial buildings",
        "renewable energy real estate",
        
        # Finance & Investment
        "green bonds real estate",
        "sustainable real estate investment",
        "ESG property fund",
        "climate risk real estate investment",
        
        # Specific regions
        "UK net zero buildings",
        "EU building regulations energy",
        "US commercial building emissions",
    ],
    
    "regulatory": [
        # EU
        "EU taxonomy real estate",
        "SFDR property funds",
        "CSRD real estate reporting",
        "EPBD building directive",
        "EU green building standards",
        
        # UK
        "UK MEES regulations",
        "UK net zero buildings policy",
        "FCA sustainability disclosure",
        "TPT transition plan taskforce",
        
        # US
        "SEC climate disclosure real estate",
        "US building emissions regulations",
        "Local Law 97 New York",
        
        # Global
        "ISSB sustainability standards",
        "TCFD real estate",
        "GHG protocol buildings",
    ],
    
    "research": [
        # Benchmarks & Data
        "GRESB results 2025",
        "green building certification statistics",
        "carbon risk real estate study",
        
        # Academic
        "ESG real estate performance research",
        "green premium real estate study",
        "climate risk property valuation",
        
        # Industry reports
        "JLL sustainability report",
        "CBRE ESG research",
        "Savills net zero report",
        "Knight Frank sustainability",
    ],
    
    "market": [
        # Transactions & Deals
        "green real estate transaction",
        "sustainable property acquisition",
        "ESG REIT news",
        
        # PropTech
        "PropTech sustainability",
        "building analytics ESG",
        "smart building energy management",
        
        # Certification
        "BREEAM certification news",
        "LEED building news",
        "NABERS rating",
        "EPC rating news",
    ],
}

# =============================================================================
# SOURCES TO MONITOR
# =============================================================================

# Direct URLs to check (via web_fetch)
DIRECT_SOURCES = {
    "regulatory": [
        {
            "name": "EU Sustainable Finance",
            "url": "https://finance.ec.europa.eu/sustainable-finance_en",
            "frequency": "weekly",
        },
        {
            "name": "FCA Sustainability",
            "url": "https://www.fca.org.uk/firms/climate-change-and-sustainable-finance",
            "frequency": "weekly",
        },
    ],
    "industry": [
        {
            "name": "GRESB Insights",
            "url": "https://www.gresb.com/nl-en/insights/",
            "frequency": "weekly",
        },
        {
            "name": "ULI Knowledge Finder",
            "url": "https://knowledge.uli.org/",
            "frequency": "weekly",
        },
    ],
}

# RSS feeds (if implementing RSS parsing)
RSS_FEEDS = [
    # Add RSS feed URLs here if you want to implement RSS parsing
    # {"name": "Property Week", "url": "..."},
]

# =============================================================================
# THEME CATEGORIES
# =============================================================================

# Used for classifying and tracking content
THEME_CATEGORIES = {
    "carbon_emissions": [
        "carbon", "emissions", "GHG", "greenhouse gas", "scope 1", "scope 2", 
        "scope 3", "embodied carbon", "operational carbon", "net zero",
        "decarbonization", "decarbonisation"
    ],
    "energy_efficiency": [
        "energy efficiency", "energy performance", "EPC", "MEES", "heat pump",
        "insulation", "retrofit", "energy consumption", "renewable energy",
        "solar", "electricity"
    ],
    "climate_risk": [
        "climate risk", "physical risk", "transition risk", "stranded assets",
        "CRREM", "flood risk", "heat stress", "climate adaptation", "resilience"
    ],
    "regulation_compliance": [
        "regulation", "compliance", "taxonomy", "SFDR", "CSRD", "TCFD", "ISSB",
        "disclosure", "reporting", "mandatory", "legislation"
    ],
    "green_finance": [
        "green bond", "sustainable finance", "ESG investing", "impact investing",
        "green loan", "sustainability-linked", "green premium", "brown discount"
    ],
    "certification_ratings": [
        "BREEAM", "LEED", "NABERS", "GRESB", "certification", "rating",
        "benchmark", "assessment", "performance"
    ],
    "proptech_innovation": [
        "PropTech", "smart building", "IoT", "sensors", "analytics", "AI",
        "digital twin", "building management", "automation"
    ],
    "social_governance": [
        "social impact", "tenant wellbeing", "health", "community",
        "governance", "diversity", "stakeholder", "just transition"
    ],
}

# =============================================================================
# ANALYSIS SETTINGS
# =============================================================================

# Claude model to use for analysis
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Relevance threshold (0-1) for including items
RELEVANCE_THRESHOLD = 0.6

# Maximum items to include per category in digest
MAX_ITEMS_PER_CATEGORY = 5

# =============================================================================
# OUTPUT SETTINGS
# =============================================================================

# Output directory for digests
OUTPUT_DIR = "outputs"

# Database location
DATABASE_PATH = "data/esg_monitor.db"

# Output format options: "markdown", "docx", "both"
OUTPUT_FORMAT = "both"

# =============================================================================
# TIME SETTINGS
# =============================================================================

def get_date_range(days_back: int = 7):
    """Get date range for weekly monitoring."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date

def format_date_for_search(date: datetime) -> str:
    """Format date for search queries."""
    return date.strftime("%Y-%m-%d")

# =============================================================================
# AUDIENCE-SPECIFIC PROMPTS
# =============================================================================

# For generating implications sections
AUDIENCE_PROMPTS = {
    "investors": """
        What are the implications for real estate investors?
        Consider: risk assessment, valuation impacts, due diligence requirements,
        portfolio strategy, regulatory compliance costs, green premium opportunities.
    """,
    "asset_managers": """
        What are the implications for asset/property managers?
        Consider: operational changes, capex requirements, tenant engagement,
        certification pathways, reporting obligations, technology adoption.
    """,
    "plinthos_clients": """
        What are the implications for ESG reporting consultants and their clients?
        Consider: new reporting requirements, data collection needs, framework updates,
        client advisory opportunities, tool/methodology changes.
    """,
}
