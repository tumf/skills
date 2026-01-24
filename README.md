# Skills

A collection of reusable command-line tools for web scraping, data extraction, and automation tasks.

## Overview

This repository provides ready-to-use scripts and tools that can be used in multiple ways:
- **Standalone tools**: Use the scripts directly from the command line
- **Integration**: Import into your own projects and workflows
- **Automation**: Integrate into shell scripts, cron jobs, or CI/CD pipelines

Each tool is self-contained with its own documentation and executable scripts.

## Installation

### Quick Install (AI Agents)

```bash
npx skills add tumf/skills --skill firecrawl
```

### Manual Installation

```bash
git clone https://github.com/tumf/skills.git
cd skills/firecrawl

# Install dependencies
pip install firecrawl-py

# Set up environment variables
export FIRECRAWL_API_KEY="your-api-key-here"

# Use the scripts
./scripts/scrape.py "https://example.com"
```

## Available Tools

### 🔥 [Firecrawl](./firecrawl)

Comprehensive web scraping, crawling, and data extraction toolkit powered by Firecrawl API.

**6 Tools Included:**
- `scrape.py` - Single page scraping (fastest)
- `search.py` - Web search and scraping
- `map.py` - URL discovery
- `crawl.py` - Multi-page crawling
- `extract.py` - Structured data extraction with JSON schema
- `agent.py` - Autonomous web data gathering

**Quick Start:**
```bash
# Install
npx skills add tumf/skills --skill firecrawl
# or manually: pip install firecrawl-py

# Set API key
export FIRECRAWL_API_KEY="your-api-key-here"

# Use
./firecrawl/scripts/scrape.py "https://example.com"
```

**[📖 Full Documentation](./firecrawl/README.md)** | [SKILL.md](./firecrawl/SKILL.md)

## Usage Examples

### Command Line

Use scripts directly from your terminal:

```bash
# Quick data extraction
./firecrawl/scripts/scrape.py "https://example.com" > output.md

# Batch processing
for url in $(cat urls.txt); do
  ./firecrawl/scripts/scrape.py "$url"
done

# Pipe to other tools
./firecrawl/scripts/search.py "AI news" | jq '.data'
```

### Python Integration

Use in your Python projects:

```python
import subprocess
import json

# Call script and parse JSON output
result = subprocess.run(
    ["./firecrawl/scripts/scrape.py", "https://example.com"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)

# Process the scraped data
if data['success']:
    content = data['data']['markdown']
    print(content)
```

### Automation & CI/CD

Integrate into automated workflows:

```bash
# Cron job for daily scraping
0 9 * * * cd /path/to/skills/firecrawl && ./scripts/scrape.py "https://example.com" >> /var/log/scrape.log

# GitHub Actions
- name: Scrape website
  run: |
    cd firecrawl
    ./scripts/scrape.py "https://example.com" > data.md
```

## Repository Structure

Each tool is organized as a self-contained module:

```
skills/
├── README.md                # This file
└── firecrawl/              # Firecrawl web scraping toolkit
    ├── README.md           # Full documentation and usage guide
    ├── SKILL.md            # Skill metadata (for AI agents)
    └── scripts/            # Executable Python scripts
        ├── scrape.py       # Single page scraping
        ├── search.py       # Web search
        ├── map.py          # URL discovery
        ├── crawl.py        # Multi-page crawling
        ├── extract.py      # Structured data extraction
        └── agent.py        # Autonomous data gathering
```

## Adding New Tools

Want to add your own tool? Follow this structure:

1. **Create a directory** for your tool (e.g., `my-tool/`)

2. **Add executable scripts** in a `scripts/` subdirectory:
   - Make scripts executable (`chmod +x`)
   - Include a shebang line (`#!/usr/bin/env python3`)
   - Output JSON to stdout for easy parsing
   - Write errors to stderr

3. **Create documentation**:
   - `README.md` - Full documentation with installation, usage, examples
   - `SKILL.md` (optional) - For AI agent compatibility with YAML frontmatter

4. **Optional additions**:
   - `references/` - Extended documentation
   - `assets/` - Templates, config files, etc.
   - `tests/` - Unit tests for your scripts

## Contributing

Contributions are welcome! To add a new tool:

1. Fork this repository
2. Create your tool following the structure above
3. Update this README.md to list your tool
4. Submit a pull request

## Resources

- [GitHub Repository](https://github.com/tumf/skills)
- [Report Issues](https://github.com/tumf/skills/issues)

**For AI Agent users**:
- [skills.sh](https://skills.sh) - Agent Skills Directory  
- [Agent Skills Specification](https://agentskills.io/)

## License

MIT License - See individual skills for their specific licenses.

---

💡 Use as standalone tools or integrate with [skills.sh](https://skills.sh) compatible AI agents
