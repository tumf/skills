# Skills

A collection of reusable command-line tools and skills for web scraping, data extraction, and automation tasks.

## Overview

This repository provides ready-to-use scripts and tools that can be used in multiple ways:
- **Standalone tools**: Use the scripts directly from the command line
- **AI Agent skills**: Install via [skills.sh](https://skills.sh) for AI agents like Claude Code, Cline, Cursor, etc.
- **Integration**: Import into your own projects and workflows

Each skill is self-contained with its own documentation and executable scripts.

## Installation

### Standalone Use

Clone this repository and use the scripts directly:

```bash
git clone https://github.com/tumf/skills.git
cd skills

# Install dependencies for the skill you want to use
cd firecrawl
pip install firecrawl-py

# Set up environment variables
export FIRECRAWL_API_KEY="your-api-key-here"

# Use the scripts
./scripts/scrape.py "https://example.com"
```

### AI Agent Integration (Optional)

If you're using an AI agent that supports [skills.sh](https://skills.sh), you can install skills directly:

```bash
npx skills add https://github.com/tumf/skills --skill firecrawl
```

This works with Claude Code, Cline, Cursor, ClawdBot, GitHub Copilot, and other compatible agents.

## Available Skills

### 🔥 [Firecrawl](./firecrawl)

Comprehensive web scraping, crawling, and data extraction toolkit powered by Firecrawl API.

**Features:**
- **scrape**: Extract content from a single URL (fastest, most reliable)
- **search**: Search the web and optionally scrape results
- **map**: Discover all URLs on a website before deciding what to scrape
- **crawl**: Extract content from multiple related pages
- **extract**: LLM-powered structured data extraction with JSON schema
- **agent**: Autonomous web data gathering - describe what you need, agent finds it

**Quick Start:**
```bash
# Install dependencies
pip install firecrawl-py

# Set API key
export FIRECRAWL_API_KEY="your-api-key-here"

# Scrape a webpage
./firecrawl/scripts/scrape.py "https://example.com"
```

[View Firecrawl Documentation](./firecrawl/SKILL.md)

## Usage Modes

### 1. Command Line Tools

Use scripts directly from your terminal for automation, scripting, or manual tasks:

```bash
# Quick data extraction
./firecrawl/scripts/scrape.py "https://example.com" > output.md

# Integrate into shell scripts
for url in $(cat urls.txt); do
  ./firecrawl/scripts/scrape.py "$url"
done
```

### 2. Python Integration

Import and use in your Python projects:

```python
import subprocess
import json

result = subprocess.run(
    ["./firecrawl/scripts/scrape.py", "https://example.com"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
```

### 3. AI Agent Skills

Compatible with AI agents supporting the [skills.sh](https://skills.sh) standard:
- Claude Code
- Cline  
- Cursor
- ClawdBot
- GitHub Copilot
- And more...

## Repository Structure

Each skill is organized as a self-contained module:

```
skills/
├── README.md                # This file
└── firecrawl/              # Firecrawl skill
    ├── SKILL.md            # Skill metadata and instructions
    └── scripts/            # Executable Python scripts
        ├── scrape.py       # Single page scraping
        ├── search.py       # Web search
        ├── map.py          # URL discovery
        ├── crawl.py        # Multi-page crawling
        ├── extract.py      # Structured data extraction
        └── agent.py        # Autonomous data gathering
```

## Adding New Skills/Tools

Want to add your own skill or tool? Follow this structure:

1. **Create a directory** for your skill (e.g., `my-tool/`)

2. **Add executable scripts** in a `scripts/` subdirectory:
   - Make scripts executable (`chmod +x`)
   - Include a shebang line (`#!/usr/bin/env python3`)
   - Output JSON to stdout for easy parsing
   - Write errors to stderr

3. **Create SKILL.md documentation** with:
   - YAML frontmatter with `name` and `description`
   - Installation instructions
   - Usage examples
   - API reference

4. **Optional additions**:
   - `references/` - Extended documentation
   - `assets/` - Templates, config files, etc.
   - `tests/` - Unit tests for your scripts

**Note**: Skills are compatible with the [Agent Skills specification](https://agentskills.io/) for use with AI agents, but can also be used standalone.

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create your skill following the structure above
3. Update this README.md to list your skill
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
