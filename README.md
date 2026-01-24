# Skills

A collection of skills for AI coding agents and command-line automation.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

### firecrawl

Web scraping, crawling, and data extraction powered by Firecrawl API.

**Use when:**
- Extracting content from web pages
- Searching and scraping the web
- Discovering URLs on websites
- Crawling multiple pages
- Extracting structured data with JSON schemas
- Autonomously gathering data from the web

**Tools included:**
- `scrape.py` - Single page scraping (fastest, most reliable)
- `search.py` - Web search with optional scraping
- `map.py` - URL discovery before scraping
- `crawl.py` - Multi-page content extraction
- `extract.py` - LLM-powered structured data extraction
- `agent.py` - Autonomous web data gathering

**[→ Documentation](./firecrawl/README.md)**

---

*More skills coming soon...*

## Installation

```bash
npx skills add tumf/skills --skill <skill-name>
```

Example:
```bash
npx skills add tumf/skills --skill firecrawl
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**

```
Scrape the content from https://example.com
```

```
Search the web for "latest AI research papers"
```

```
Extract pricing information from this webpage
```

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `README.md` - Full documentation
- `scripts/` - Executable scripts (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
