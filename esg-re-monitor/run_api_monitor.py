#!/usr/bin/env python3
"""
ESG Monitor - Minimal Version (Rate-Limit Safe)
Only 3 searches with 60-second delays between calls.
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import anthropic

OUTPUT_DIR = Path("outputs")
DELAY = 60  # seconds between API calls

def main():
    print("=" * 50)
    print("ESG Real Estate Weekly Monitor")
    print("=" * 50)
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    week_start = start_date.strftime("%B %d")
    week_end = end_date.strftime("%B %d, %Y")
    date_str = end_date.strftime("%Y-%m-%d")
    
    print(f"Period: {week_start} - {week_end}")
    print(f"Delay between calls: {DELAY}s")
    
    # Initialize client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Single comprehensive search
    print("\n[1/2] Searching for ESG real estate news...")
    
    search_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{
            "role": "user",
            "content": """Search for ESG real estate news from the past week.

Find the top 10 most important stories covering:
- Carbon emissions and net zero buildings
- Energy efficiency regulations (MEES, EPC)
- Climate risk and stranded assets
- ESG reporting (CSRD, SFDR, taxonomy)
- Green finance and sustainable investment
- Building certifications (BREEAM, LEED, GRESB)

For each story provide: title, source, URL, and key insight."""
        }]
    )
    
    # Extract search results
    search_text = ""
    for block in search_response.content:
        if hasattr(block, 'text'):
            search_text += block.text
    
    print("  ✓ Search complete")
    print(f"\n  Waiting {DELAY}s before generating digest...")
    time.sleep(DELAY)
    
    # Generate digest
    print("\n[2/2] Generating digest...")
    
    digest_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Based on these search results about ESG in real estate:

{search_text}

Create a weekly digest for {week_start} - {week_end} with:

# ESG in Real Estate Weekly Digest
## {week_start} - {week_end}

## Executive Summary
(Top 3-5 developments, 100 words)

## News Highlights
(Key announcements and market news)

## Regulatory Updates
(Policy changes, compliance deadlines)

## Market Developments
(Green finance, transactions, PropTech)

## Implications

### For Investors
(Investment implications)

### For Asset Managers  
(Operational implications)

### For ESG Consultants
(Advisory implications for Plinthos-type services)

## Sources
(List all sources with URLs)

Be concise and professional."""
        }]
    )
    
    # Extract digest
    digest = ""
    for block in digest_response.content:
        if hasattr(block, 'text'):
            digest += block.text
    
    print("  ✓ Digest generated")
    
    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"esg_re_digest_{date_str}.md"
    output_path.write_text(digest)
    
    print(f"\n✓ Saved: {output_path}")
    print("=" * 50)
    print("Complete!")

if __name__ == "__main__":
    main()
