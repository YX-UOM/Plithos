#!/usr/bin/env python3
"""
ESG Monitor - Standalone API Version

This version uses the Anthropic API directly with web search tool enabled.
Can be run standalone, via cron, or in GitHub Actions.

Requirements:
    pip install anthropic httpx python-docx

Environment:
    ANTHROPIC_API_KEY=your_api_key

Usage:
    python run_api_monitor.py
    python run_api_monitor.py --days 14
"""

import argparse
import json
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Please install anthropic: pip install anthropic")
    exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path("outputs")
DATABASE_PATH = Path("data/esg_monitor.db")

SEARCH_QUERIES = {
    "news": [
        "ESG real estate news",
        "sustainable buildings news", 
        "net zero buildings real estate",
        "green real estate investment",
        "building decarbonization",
    ],
    "regulatory": [
        "EU taxonomy real estate",
        "CSRD real estate reporting",
        "UK MEES regulations",
        "SEC climate disclosure buildings",
        "ISSB sustainability standards",
    ],
    "research": [
        "GRESB real estate results",
        "green building certification statistics",
        "ESG property valuation study",
        "carbon risk real estate report",
    ],
    "market": [
        "green bond real estate",
        "sustainable REIT news",
        "PropTech sustainability",
        "green building transaction",
    ],
}

THEMES = [
    "carbon_emissions",
    "energy_efficiency",
    "climate_risk", 
    "regulation_compliance",
    "green_finance",
    "certification_ratings",
    "proptech_innovation",
]

# =============================================================================
# ANTHROPIC CLIENT WITH WEB SEARCH
# =============================================================================

def create_client():
    """Create Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable required")
    return anthropic.Anthropic(api_key=api_key)


def search_with_claude(client, query: str, context: str = "") -> dict:
    """
    Use Claude with web search to find ESG real estate content.
    """
    
    system_prompt = """You are an ESG real estate research assistant. 
    Your task is to search for and collect relevant news, research, and regulatory updates
    about ESG (Environmental, Social, Governance) topics in the real estate sector.
    
    Focus on:
    - Carbon emissions and net zero targets
    - Energy efficiency regulations
    - Climate risk and stranded assets
    - ESG reporting requirements (CSRD, SFDR, etc.)
    - Green finance and sustainable investment
    - Building certifications (BREEAM, LEED, GRESB)
    - PropTech innovations for sustainability
    
    When searching, prioritize:
    - Recent content (past 7 days)
    - Reputable sources (Reuters, Bloomberg, property press, regulatory bodies)
    - Actionable information for investors and asset managers
    """
    
    user_prompt = f"""Search for: {query}

    {context}
    
    Find relevant articles from the past week. For each result, extract:
    1. Title
    2. Source/publication
    3. URL
    4. Key insight (1-2 sentences)
    5. Relevance score (0-1) for ESG in real estate
    
    Return results as JSON array."""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        system=system_prompt
    )
    
    return response


def analyze_results(client, all_results: list) -> dict:
    """
    Analyze collected results and prepare digest content.
    """
    
    analysis_prompt = f"""Analyze these ESG real estate search results from the past week:

{json.dumps(all_results, indent=2)}

Provide a structured analysis:

1. **Top Stories** (5 most important items):
   - Title, source, URL
   - Why it matters (2-3 sentences)
   - Theme category

2. **Theme Summary**:
   For each theme that appears, list count and key highlights:
   - carbon_emissions
   - energy_efficiency
   - climate_risk
   - regulation_compliance
   - green_finance
   - certification_ratings
   - proptech_innovation

3. **Regulatory Alerts**:
   Any compliance deadlines or new requirements

4. **Key Statistics**:
   Notable numbers/data points mentioned

5. **Geographic Distribution**:
   Breakdown by UK, EU, US, Global

Return as structured JSON."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": analysis_prompt}
        ]
    )
    
    return response


def generate_digest(client, analysis: str, week_start: str, week_end: str) -> str:
    """
    Generate the final weekly digest.
    """
    
    digest_prompt = f"""Based on this analysis of ESG real estate news from {week_start} to {week_end}:

{analysis}

Generate a professional weekly digest with these sections:

# ESG in Real Estate Weekly Digest
## {week_start} - {week_end}

## Executive Summary
(150 words - top developments and key theme of the week)

## 📰 News Highlights  
(400 words - major announcements, market movements, company initiatives)

## 📋 Regulatory Updates
(300 words - new/proposed regulations, compliance deadlines, guidance)

## 📊 Research & Reports
(300 words - new studies, data releases, benchmark updates)

## 💹 Market Developments
(300 words - green finance deals, transactions, PropTech)

## 🎯 Implications

### For Investors
(Key implications for real estate investors)

### For Asset Managers
(Key implications for property/asset managers)

### For ESG Consultants
(Key implications for ESG reporting and advisory - consider Plinthos-type services)

## Sources
(List all sources cited with links)

Write in a professional but accessible tone. Include specific data points where available.
Make implications actionable and concrete."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        messages=[
            {"role": "user", "content": digest_prompt}
        ]
    )
    
    # Extract text from response
    digest_text = ""
    for block in response.content:
        if hasattr(block, 'text'):
            digest_text += block.text
    
    return digest_text


# =============================================================================
# DATABASE
# =============================================================================

def init_database():
    """Initialize SQLite database."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS digests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_ending TEXT UNIQUE,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def save_to_database(week_ending: str, content: str):
    """Save digest to database."""
    init_database()
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO digests (week_ending, content)
        VALUES (?, ?)
    """, (week_ending, content))
    
    conn.commit()
    conn.close()


# =============================================================================
# MAIN WORKFLOW
# =============================================================================

def run_monitor(days_back: int = 7):
    """Run the complete monitoring workflow."""
    
    print("=" * 60)
    print("ESG in Real Estate Weekly Monitor (API Version)")
    print("=" * 60)
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    week_start = start_date.strftime("%B %d")
    week_end = end_date.strftime("%B %d, %Y")
    week_ending_str = end_date.strftime("%Y-%m-%d")
    
    print(f"Period: {week_start} - {week_end}")
    print("-" * 60)
    
    # Initialize client
    client = create_client()
    
    # Step 1: Search all categories
    print("\n[1/3] Searching sources...")
    all_results = []
    
    for category, queries in SEARCH_QUERIES.items():
        print(f"  Category: {category}")
        for query in queries:
            print(f"    Searching: {query}")
            try:
                result = search_with_claude(
                    client, 
                    query,
                    f"Looking for content from the past {days_back} days."
                )
                all_results.append({
                    "category": category,
                    "query": query,
                    "response": str(result.content)
                })
            except Exception as e:
                print(f"    Error: {e}")
    
    # Step 2: Analyze results
    print("\n[2/3] Analyzing results...")
    analysis_response = analyze_results(client, all_results)
    analysis_text = ""
    for block in analysis_response.content:
        if hasattr(block, 'text'):
            analysis_text += block.text
    
    # Step 3: Generate digest
    print("\n[3/3] Generating digest...")
    digest = generate_digest(client, analysis_text, week_start, week_end)
    
    # Save outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save markdown
    md_path = OUTPUT_DIR / f"esg_re_digest_{week_ending_str}.md"
    md_path.write_text(digest)
    print(f"\nSaved: {md_path}")
    
    # Save to database
    save_to_database(week_ending_str, digest)
    print(f"Database updated: {DATABASE_PATH}")
    
    print("\n" + "=" * 60)
    print("Monitor complete!")
    print("=" * 60)
    
    return str(md_path)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ESG Real Estate Weekly Monitor (API Version)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to look back (default: 7)"
    )
    
    args = parser.parse_args()
    run_monitor(args.days)


if __name__ == "__main__":
    main()
