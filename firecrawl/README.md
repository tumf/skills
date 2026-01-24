# Firecrawl Web Scraping Toolkit

Comprehensive web scraping, crawling, and data extraction toolkit powered by Firecrawl API.

## Features

- **scrape.py**: Extract content from a single URL (fastest, most reliable)
- **search.py**: Search the web and optionally scrape results
- **map.py**: Discover all URLs on a website before deciding what to scrape
- **crawl.py**: Extract content from multiple related pages
- **extract.py**: LLM-powered structured data extraction with JSON schema
- **agent.py**: Autonomous web data gathering - describe what you need, agent finds it

## Installation

### Option 1: Via skills.sh (Recommended for AI Agents)

If you're using an AI agent that supports the skills.sh ecosystem:

```bash
npx skills add tumf/skills --skill firecrawl
```

This automatically installs the skill and makes it available to your AI agent (Claude Code, Cline, Cursor, etc.).

Then set your API key:
```bash
export FIRECRAWL_API_KEY="your-api-key-here"
```

### Option 2: Manual Installation

For standalone use or custom integration:

```bash
# Clone the repository
git clone https://github.com/tumf/skills.git
cd skills/firecrawl

# Install dependencies
pip install firecrawl-py

# Set API key
export FIRECRAWL_API_KEY="your-api-key-here"
```

Get your API key from [Firecrawl](https://firecrawl.dev).

## Quick Start

```bash
# Scrape a webpage
./scripts/scrape.py "https://example.com"

# Search the web
./scripts/search.py "latest AI research papers 2024"

# Discover URLs on a website
./scripts/map.py "https://docs.example.com"
```

## Scripts Reference

### scrape.py - Single Page Scraping

The most powerful and reliable scraper. Use when you know exactly which page contains the information.

```bash
# Basic scrape (returns markdown)
./scripts/scrape.py "https://example.com"

# Get HTML format
./scripts/scrape.py "https://example.com" --format html

# Extract only main content (removes headers, footers, etc.)
./scripts/scrape.py "https://example.com" --only-main

# Combine options
./scripts/scrape.py "https://docs.example.com/api" --format markdown --only-main
```

### search.py - Web Search

Search the web when you don't know which website has the information.

```bash
# Basic search
./scripts/search.py "latest AI research papers 2024"

# Limit results
./scripts/search.py "Python web scraping tutorials" --limit 5

# Search with scraping (get full content)
./scripts/search.py "firecrawl documentation" --limit 3
```

### map.py - URL Discovery

Discover all URLs on a website. Use before deciding what to scrape.

```bash
# Map a website
./scripts/map.py "https://docs.example.com"

# Limit number of URLs
./scripts/map.py "https://example.com" --limit 100

# Search within mapped URLs
./scripts/map.py "https://docs.example.com" --search "authentication"
```

### crawl.py - Multi-Page Crawling

Extract content from multiple related pages. Warning: can be slow and return large results.

```bash
# Basic crawl
./scripts/crawl.py "https://docs.example.com"

# Limit pages
./scripts/crawl.py "https://docs.example.com" --limit 20

# Control crawl depth
./scripts/crawl.py "https://docs.example.com" --limit 10 --depth 2
```

### extract.py - Structured Data Extraction

Extract specific structured data using LLM capabilities.

```bash
# Extract with prompt
./scripts/extract.py "https://example.com/pricing" \
  --prompt "Extract all pricing tiers with their features and prices"

# Extract with JSON schema
./scripts/extract.py "https://example.com/team" \
  --prompt "Extract team member information" \
  --schema '{"type":"object","properties":{"members":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"role":{"type":"string"},"bio":{"type":"string"}}}}}}'

# Extract from multiple URLs
./scripts/extract.py "https://example.com/page1" "https://example.com/page2" \
  --prompt "Extract product information"
```

### agent.py - Autonomous Data Gathering

Autonomous agent that searches, navigates, and extracts data from anywhere on the web.

```bash
# Simple research task
./scripts/agent.py --prompt "Find the founders of Firecrawl and their backgrounds"

# Complex data gathering
./scripts/agent.py --prompt "Find the top 5 AI startups founded in 2024 and their funding amounts"

# Focus on specific URLs
./scripts/agent.py \
  --prompt "Compare the features and pricing" \
  --urls "https://example1.com,https://example2.com"

# With output schema
./scripts/agent.py \
  --prompt "Find recent tech layoffs" \
  --schema '{"type":"object","properties":{"layoffs":{"type":"array","items":{"type":"object","properties":{"company":{"type":"string"},"count":{"type":"number"},"date":{"type":"string"}}}}}}'
```

## Output Format

All scripts output JSON to stdout. Errors are written to stderr.

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message"
}
```

## Usage Examples

### Command Line

```bash
# Quick data extraction
./scripts/scrape.py "https://example.com" > output.md

# Batch processing
for url in $(cat urls.txt); do
  ./scripts/scrape.py "$url"
done

# Pipe to jq for JSON processing
./scripts/search.py "AI news" | jq '.data[].title'
```

### Python Integration

```python
import subprocess
import json

# Scrape a webpage
result = subprocess.run(
    ["./scripts/scrape.py", "https://example.com"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)

if data['success']:
    content = data['data']['markdown']
    print(content)
```

### Shell Script Integration

```bash
#!/bin/bash
# Daily news scraper

URLS=(
  "https://news.ycombinator.com"
  "https://techcrunch.com"
  "https://arstechnica.com"
)

for url in "${URLS[@]}"; do
  echo "Scraping $url..."
  ./scripts/scrape.py "$url" > "data/$(date +%Y%m%d)_$(basename $url).md"
done
```

## Tips

1. **Performance**: Use `scrape` for single pages - it's 500% faster with caching
2. **Discovery**: Use `map` first to find URLs, then `scrape` specific pages
3. **Large sites**: Prefer `map` + `scrape` over `crawl` for better control
4. **Structured data**: Use `extract` with a JSON schema for consistent output
5. **Research**: Use `agent` when you don't know where to find the data

## Environment Variables

- `FIRECRAWL_API_KEY` (required) - Your Firecrawl API key

## Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $FIRECRAWL_API_KEY

# Set API key for current session
export FIRECRAWL_API_KEY="your-key-here"

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export FIRECRAWL_API_KEY="your-key-here"' >> ~/.bashrc
```

### Permission Errors
```bash
# Make scripts executable
chmod +x scripts/*.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade firecrawl-py
```

## Resources

- [Firecrawl Documentation](https://docs.firecrawl.dev)
- [Firecrawl API](https://firecrawl.dev)
- [Get API Key](https://firecrawl.dev)

## License

MIT License
