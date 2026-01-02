# ESG in Real Estate Weekly Monitor

An automated agent to scan, analyze, and synthesize everything happening in ESG + Real Estate each week.

## What It Does

This agent runs weekly to:
1. **Scan** multiple source categories (news, regulations, research, industry reports)
2. **Analyze** content through Claude for relevance and importance
3. **Synthesize** findings into a structured digest
4. **Track** themes and developments over time in a local database

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     WEEKLY SCHEDULER                            │
│              (cron job / GitHub Actions / manual)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  News Sources        │  Regulatory Bodies   │  Research/Reports │
│  ─────────────────   │  ─────────────────   │  ──────────────── │
│  • Reuters ESG       │  • EU Taxonomy/SFDR  │  • GRESB          │
│  • Bloomberg Green   │  • SEC Climate       │  • CRREM          │
│  • PropertyWeek      │  • FCA/TPT           │  • JLL Research   │
│  • CoStar/GlobeSt    │  • ISSB/IFRS         │  • CBRE/Savills   │
│  • IPE Real Assets   │  • Local authorities │  • Academic (SSRN)│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE PROCESSING LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│  1. Relevance filtering (ESG + RE focus)                        │
│  2. Theme extraction and categorization                         │
│  3. Importance scoring                                          │
│  4. Cross-source synthesis                                      │
│  5. Actionability assessment (research/teaching/Plinthos)       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       OUTPUT LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Weekly Digest (Markdown/DOCX)                                  │
│  • Executive Summary                                            │
│  • News Highlights                                              │
│  • Regulatory Updates                                           │
│  • Research & Reports                                           │
│  • Market Developments                                          │
│  • Implications (by audience)                                   │
│  ──────────────────────────────────────────────────────────────│
│  Database Update (SQLite)                                       │
│  • Theme tracking                                               │
│  • Source citations                                             │
│  • Historical trends                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Source Categories

### 1. News & Media
| Source | Focus | Method |
|--------|-------|--------|
| Reuters Sustainable Business | Global ESG news | Web search |
| Bloomberg Green | Climate finance | Web search |
| PropertyWeek | UK property | RSS/Search |
| CoStar/GlobeSt | US commercial RE | Web search |
| IPE Real Assets | Institutional RE | Web search |
| Estates Gazette | UK property | Web search |

### 2. Regulatory Bodies
| Source | Jurisdiction | Key Topics |
|--------|--------------|------------|
| European Commission | EU | Taxonomy, SFDR, CSRD, EPBD |
| SEC | US | Climate disclosure rules |
| FCA/TPT | UK | Transition plans, SDR |
| ISSB/IFRS | Global | Sustainability standards |

### 3. Industry Bodies & Research
| Source | Type | Focus |
|--------|------|-------|
| GRESB | Benchmark | RE sustainability scores |
| CRREM | Tool | Carbon risk modeling |
| ULI | Association | Best practices |
| RICS | Professional body | Standards, guidance |
| BBP (Better Buildings Partnership) | Coalition | UK commercial |

### 4. Academic & Think Tanks
| Source | Type |
|--------|------|
| SSRN | Working papers |
| MSCI Research | Market analysis |
| Carbon Trust | Technical guidance |
| World Green Building Council | Global standards |

## Usage

### Option 1: Run via Claude Code (Recommended)

```bash
# Navigate to agent directory
cd esg-re-monitor

# Run the weekly monitor
python run_monitor.py

# Or with specific date range
python run_monitor.py --start 2025-12-26 --end 2026-01-02
```

### Option 2: Run via Claude.ai

Upload this folder as a skill, then ask:
> "Run my ESG real estate weekly monitor and create a digest"

### Option 3: Schedule Automatically

Add to crontab (runs every Sunday at 8am):
```bash
0 8 * * 0 cd /path/to/esg-re-monitor && python run_monitor.py >> logs/monitor.log 2>&1
```

Or use GitHub Actions (see `.github/workflows/weekly-monitor.yml`).

## Output Structure

The weekly digest follows this structure:

1. **Executive Summary** (150 words)
   - Top 3-5 developments
   - Key theme of the week
   
2. **News Highlights** (400 words)
   - Major announcements
   - Market movements
   - Company initiatives
   
3. **Regulatory Updates** (300 words)
   - New/proposed regulations
   - Compliance deadlines
   - Guidance releases
   
4. **Research & Reports** (300 words)
   - New studies/white papers
   - Data releases
   - Benchmark updates
   
5. **Market Developments** (300 words)
   - Green finance deals
   - Portfolio transactions
   - Technology/PropTech
   
6. **Implications** (200 words)
   - For investors
   - For asset managers
   - For Plinthos clients

## Customization

Edit `config.py` to:
- Add/remove sources
- Adjust search queries
- Change output format
- Configure database location
- Set relevance thresholds

## File Structure

```
esg-re-monitor/
├── README.md                 # This file
├── config.py                 # Configuration settings
├── run_monitor.py            # Main entry point
├── sources/
│   ├── __init__.py
│   ├── news.py               # News source handlers
│   ├── regulatory.py         # Regulatory source handlers
│   └── research.py           # Research source handlers
├── processing/
│   ├── __init__.py
│   ├── analyzer.py           # Claude-based analysis
│   └── synthesizer.py        # Digest generation
├── database/
│   ├── __init__.py
│   ├── models.py             # Database models
│   └── tracker.py            # Theme/source tracking
├── templates/
│   ├── weekly_digest.md      # Digest template
│   └── analysis_prompt.txt   # Claude prompt template
├── outputs/                  # Generated digests
└── data/
    └── esg_monitor.db        # SQLite database
```
