#!/usr/bin/env python3
"""
ESG Monitor - Standalone API Version (Rate-Limit Safe)

This version includes delays between API calls to avoid rate limits.
"""

import argparse
import json
import os
import sqlite3
import time
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

# Reduced queries to stay within rate limits
SEARCH_QUERIES = {
    "news": [
        "ESG real estate news this week",
        "net zero buildings news",
    ],
    "regulatory": [
        "EU taxonomy CSRD real estate 2025",
        "UK MEES building regulations",
    ],
    "research": [
        "GRESB real estate sustainability",
    ],
    "market": [
        "green bond real estate investment",
    ],
}

# Delay between API calls (seconds)
API_DELAY = 15

# =============================================================================
# ANTHROPIC CLIENT
# =============================================================================

def create_client():
    """Create Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable required")
    return anthropic.Anthropic(api_key=api_key)


def search_with_claude(client, query: str) -> dict:
    """Use Claude with web search to find ESG real estate content."""
    
    print(f"    Waiting {API_DELAY}s before search...")
    time.sleep(API_DELAY)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {
                "role": "user", 
                "content": f"""Search for: {query}

Find 3-5 relevant articles from the past week about ESG in real estate.
For each result, provide:
1. Title
2. Source
3. URL  
4. Key insight (1-2 sentences)

Focus on: carbon emissions, energy efficiency, climate risk, regulations, green finance, certifications, PropTech."""
            }
        ]
    )
    
    return response


def analyze_results(client, all_results: list) -> str:
    """Analyze collected results."""
    
    print(f"  Waiting {API_DELAY}s before analysis...")
    time.sleep(API_DELAY)
    
    # Summarize results for analysis
    results_summary = []
    for r in all_results:
        if r.get("response"):
            results_summary.append(f"Category: {r['category']}\nQuery: {r['query']}\nResults: {r['response'][:2000]}")
    
    results_text = "\n\n---\n\n".join(results_summary)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze these ESG real estate search results and identify:

1. Top 5 most important stories
2. Key themes (carbon, energy, regulation, finance, etc.)
3. Any regulatory deadlines or alerts
4. Geographic breakdown (UK, EU, US, Global)

Results:
{results_text}

Provide a structured summary."""
            }
        ]
    )
    
    # Extract text
    analysis = ""
    for block in response.content:
        if hasattr(block, 'text'):
            analysis += block.text
    
    return analysis


def generate_digest(client, analysis: str, week_start: str, week_end: str) -> str:
    """Generate the weekly digest."""
    
    print(f"  Waiting {API_DELAY}s before generating digest...")
    time.sleep(API_DELAY)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": f"""Create a weekly ESG Real Estate digest for {week_start} - {week_end}.

Based on this analysis:
{analysis}

Use this format:

# ESG in Real Estate Weekly Digest
## {week_start} - {week_end}

## Executive Summary
(Top 3-5 developments in 150 words)

## News Highlights
(Major announcements and market movements)

## Regulatory Updates
(Policy changes and compliance deadlines)

## Research & Reports
(New studies and data)

## Market Developments
(Deals, PropTech, transactions)

## Implications

### For Investors
(Key investment implications)

### For Asset Managers
(Operational implications)

### For ESG Consultants
(Advisory and reporting implications)

## Sources
(List sources with links)

Write professionally but accessibly. Include specific data where available."""
            }
        ]
    )
    
    digest = ""
    for block in response.content:
        if hasattr(block, 'text'):
            digest += block.text
    
    return digest


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
    """Run the monitoring workflow with rate limit protection."""
    
    print("=" * 60)
    print("ESG in Real Estate Weekly Monitor")
    print("=" * 60)
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    week_start = start_date.strftime("%B %d")
    week_end = end_date.strftime("%B %d, %Y")
    week_ending_str = end_date.strftime("%Y-%m-%d")
    
    print(f"Period: {week_start} - {week_end}")
    print(f"API delay between calls: {API_DELAY} seconds")
    print("-" * 60)
    
    # Initialize client
    client = create_client()
    
    # Step 1: Search (with delays)
    print("\n[1/3] Searching sources...")
    all_results = []
    
    for category, queries in SEARCH_QUERIES.items():
        print(f"  Category: {category}")
        for query in queries:
            print(f"    Searching: {query}")
            try:
                result = search_with_claude(client, query)
                
                # Extract text from response
                response_text = ""
                for block in result.content:
                    if hasattr(block, 'text'):
                        response_text += block.text
                
                all_results.append({
                    "category": category,
                    "query": query,
                    "response": response_text
                })
                print(f"    ✓ Got results")
                
            except Exception as e:
                print(f"    ✗ Error: {e}")
                all_results.append({
                    "category": category,
                    "query": query,
                    "response": f"Error: {str(e)}"
                })
    
    # Step 2: Analyze
    print("\n[2/3] Analyzing results...")
    analysis = analyze_results(client, all_results)
    print("  ✓ Analysis complete")
    
    # Step 3: Generate digest
    print("\n[3/3] Generating digest...")
    digest = generate_digest(client, analysis, week_start, week_end)
    print("  ✓ Digest generated")
    
    # Save outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    md_path = OUTPUT_DIR / f"esg_re_digest_{week_ending_str}.md"
    md_path.write_text(digest)
    print(f"\nSaved: {md_path}")
    
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
    parser = argparse.ArgumentParser(description="ESG Real Estate Weekly Monitor")
    parser.add_argument("--days", type=int, default=7, help="Days to look back")
    args = parser.parse_args()
    run_monitor(args.days)


if __name__ == "__main__":
    main()
