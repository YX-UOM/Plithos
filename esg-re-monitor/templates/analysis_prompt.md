# ESG Real Estate Analysis Framework

Use this framework to analyze collected content for the weekly digest.

## Step 1: Content Filtering

For each item collected, determine:

**Relevance Score (0-1)**
- 1.0: Directly about ESG in real estate (e.g., "GRESB releases 2025 benchmark results")
- 0.8: Highly relevant (e.g., "EU finalizes building energy directive")
- 0.6: Moderately relevant (e.g., "Carbon pricing impacts commercial sectors")
- 0.4: Tangentially relevant (e.g., "Climate finance trends")
- Below 0.4: Exclude

**Exclude items that are:**
- Purely promotional without news value
- Duplicate coverage of the same story
- Opinion pieces without factual content
- More than 2 weeks old

## Step 2: Theme Classification

Assign each item to ONE primary theme:

| Theme | Keywords | Example |
|-------|----------|---------|
| carbon_emissions | carbon, emissions, GHG, scope 1/2/3, embodied carbon, net zero | "Building sector emissions reach new high" |
| energy_efficiency | energy performance, EPC, MEES, retrofit, heat pump | "UK tightens EPC requirements" |
| climate_risk | climate risk, stranded assets, CRREM, flood, heat stress | "Climate risk modeling for portfolios" |
| regulation_compliance | taxonomy, SFDR, CSRD, TCFD, disclosure, compliance | "CSRD implementation guidance released" |
| green_finance | green bond, sustainable loan, ESG fund, green premium | "Record green bond issuance in RE" |
| certification_ratings | BREEAM, LEED, GRESB, NABERS, certification | "GRESB average scores increase" |
| proptech_innovation | PropTech, smart building, IoT, AI, digital twin | "AI-powered building optimization" |

## Step 3: Importance Scoring

**HIGH importance** - Include in executive summary:
- New regulations or policy announcements
- Major benchmark releases (GRESB, CRREM updates)
- Large transactions (>$500M) with ESG angle
- Industry-changing technology announcements
- Deadline reminders (<3 months out)

**MEDIUM importance** - Include in relevant section:
- Research reports and studies
- Company sustainability initiatives
- Market trend data
- Regional policy developments
- New certification achievements

**LOW importance** - Include if space permits:
- Conference announcements
- Minor company news
- Opinion/thought leadership
- Local/regional stories without broader implications

## Step 4: Geographic Tagging

Tag each item with scope:
- **UK**: England, Scotland, Wales, Northern Ireland specific
- **EU**: European Union policy/markets
- **US**: United States specific
- **APAC**: Asia-Pacific region
- **Global**: Multi-region or worldwide scope

## Step 5: Synthesis Questions

For the executive summary, answer:
1. What is THE most important development this week?
2. What themes are gaining momentum?
3. What should readers do differently based on this week's news?

For implications sections, consider:

**Investors:**
- How does this affect asset valuations?
- What due diligence questions arise?
- Are there new risk factors to consider?
- What opportunities emerge?

**Asset Managers:**
- What operational changes are needed?
- What capex implications exist?
- How should tenant engagement change?
- What reporting requirements apply?

**ESG Consultants (Plinthos angle):**
- What new advisory opportunities arise?
- What frameworks or methodologies need updating?
- What client questions will this generate?
- How does this affect reporting requirements?

## Output Format

Structure your analysis as:

```json
{
  "week_ending": "2026-01-02",
  "items_analyzed": 45,
  "items_included": 23,
  
  "top_stories": [
    {
      "title": "...",
      "source": "...",
      "url": "...",
      "summary": "...",
      "theme": "...",
      "importance": "high"
    }
  ],
  
  "by_theme": {
    "carbon_emissions": {
      "count": 5,
      "highlights": ["...", "..."]
    },
    // ... other themes
  },
  
  "regulatory_alerts": [
    {
      "title": "...",
      "deadline": "2026-03-01",
      "action_required": "..."
    }
  ],
  
  "key_statistics": [
    {"metric": "...", "value": "...", "source": "..."}
  ]
}
```
