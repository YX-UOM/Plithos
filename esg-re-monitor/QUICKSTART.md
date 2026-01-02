# Quick Start Guide: ESG Real Estate Monitor

## Overview

This agent automates your weekly ESG in Real Estate monitoring. It scans news, regulatory updates, research, and market developments, then synthesizes everything into a structured digest.

## Three Ways to Run

### Option A: Claude Code (Recommended for You)

This is the simplest approach - just ask Claude to run it.

**Setup:**
```bash
# Download this folder to your machine
# Navigate to it in Claude Code
cd esg-re-monitor
```

**Run:**
Simply ask Claude:
```
Run the ESG real estate weekly monitor and create a digest for this week
```

Or step by step:
```
1. "Search for ESG real estate news from the past 7 days"
2. "Now search for regulatory updates on EU taxonomy and UK MEES"
3. "Search for GRESB and green building research"
4. "Analyze all the results and identify top themes"
5. "Generate a weekly digest and save it"
```

---

### Option B: Standalone Script with API

Run independently using the Anthropic API with web search.

**Setup:**
```bash
cd esg-re-monitor

# Install dependencies
pip install anthropic httpx python-docx

# Set API key
export ANTHROPIC_API_KEY=your_key_here
```

**Run:**
```bash
# Run for past 7 days
python run_api_monitor.py

# Run for past 14 days
python run_api_monitor.py --days 14
```

**Schedule with cron:**
```bash
# Add to crontab (runs every Sunday at 8am)
crontab -e
0 8 * * 0 cd /path/to/esg-re-monitor && python run_api_monitor.py >> logs/monitor.log 2>&1
```

---

### Option C: GitHub Actions (Automated)

Fully automated weekly runs with results saved to your repository.

**Setup:**
1. Fork/copy this repo to your GitHub
2. Add `ANTHROPIC_API_KEY` to repository secrets
3. Enable GitHub Actions

The workflow runs every Sunday at 8am UTC. You can also trigger manually.

---

## Customizing Sources

Edit `config.py` to adjust:

```python
# Add your own search queries
SEARCH_QUERIES = {
    "news": [
        "your custom query here",
        # ...
    ],
    # Add new categories
    "your_category": [
        "query 1",
        "query 2",
    ]
}
```

### Suggested Additional Queries for Your Work

**For Plinthos (ESG Consulting):**
```python
"ESG reporting real estate requirements",
"carbon accounting buildings",
"scope 3 emissions real estate",
"net zero pathway property",
```

**For Teaching (Advanced RE Finance):**
```python
"green premium real estate research",
"ESG fund performance property",
"climate risk property valuation",
"sustainable real estate returns",
```

**For Academic Research:**
```python
"machine learning carbon emissions prediction",
"AI ESG reporting",
"corporate climate strategy real estate",
```

---

## Output Structure

Each weekly digest includes:

| Section | Content | Words |
|---------|---------|-------|
| Executive Summary | Top developments, key theme | 150 |
| News Highlights | Major announcements, market moves | 400 |
| Regulatory Updates | Policy changes, compliance deadlines | 300 |
| Research & Reports | Studies, benchmark data | 300 |
| Market Developments | Deals, PropTech, transactions | 300 |
| Implications | For investors, managers, consultants | 200 |

---

## Database & Tracking

The monitor maintains a SQLite database (`data/esg_monitor.db`) that tracks:

- All weekly digests
- Theme frequency over time
- Source citations
- Key statistics mentioned

Query historical data:
```python
import sqlite3
conn = sqlite3.connect("data/esg_monitor.db")

# Get all digests
cursor = conn.execute("SELECT week_ending, content FROM digests")
for row in cursor:
    print(row[0])
```

---

## Integration Ideas

### Feed into Newsletter

The digest output can directly feed your Substack/LinkedIn content:
1. Run monitor each Sunday
2. Review and edit the digest
3. Publish key sections to your channels

### Combine with Slow Investor Skill

Run both monitors together:
1. ESG Real Estate Monitor (this tool)
2. Slow Investor (your existing investment newsletter analysis)
3. Cross-reference themes appearing in both

### Support Plinthos Client Work

Use the digest to:
- Stay current on regulatory changes affecting clients
- Identify new advisory opportunities
- Prepare client briefings on emerging requirements

---

## Troubleshooting

**API errors:**
- Check `ANTHROPIC_API_KEY` is set correctly
- Verify API access includes web search capability

**Empty results:**
- Try broader search queries
- Check date range isn't too narrow

**Missing sections:**
- Some weeks may have less activity in certain categories
- The digest will note when categories have limited content

---

## Files in This Package

```
esg-re-monitor/
├── README.md                      # Full documentation
├── QUICKSTART.md                  # This file
├── config.py                      # Configuration & search queries
├── run_monitor.py                 # Main script (framework)
├── run_claude_code_monitor.py     # Claude Code version
├── run_api_monitor.py             # Standalone API version
├── mcp_server.py                  # MCP server version
├── templates/
│   └── analysis_prompt.md         # Analysis framework
├── .github/workflows/
│   └── weekly-monitor.yml         # GitHub Actions automation
├── outputs/                       # Generated digests
└── data/
    └── esg_monitor.db            # SQLite database
```

---

## Next Steps

1. **Start simple**: Use Claude Code to run a single search category
2. **Expand**: Add all categories once comfortable
3. **Customize**: Adjust queries for your specific focus areas
4. **Automate**: Set up GitHub Actions or cron for hands-free operation
5. **Integrate**: Connect outputs to your newsletter and Plinthos workflows

Questions? Just ask Claude in Claude Code!
