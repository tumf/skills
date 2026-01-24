# Skills.sh

A collection of reusable command-line skills for web scraping, data extraction, and automation tasks.

## Overview

Skills.sh provides ready-to-use scripts and tools that can be integrated into your workflows. Each skill is a self-contained module with its own documentation and scripts.

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

## Installation

Clone this repository:

```bash
git clone https://github.com/tumf/skills.sh.git
cd skills.sh
```

Each skill has its own requirements and setup instructions. See the individual skill documentation for details.

## Project Structure

```
skills.sh/
├── README.md           # This file
├── firecrawl/          # Firecrawl web scraping skill
│   ├── SKILL.md        # Firecrawl documentation
│   └── scripts/        # Python scripts for scraping
└── ...                 # More skills coming soon
```

## Contributing

Contributions are welcome! If you have a useful skill to share:

1. Fork this repository
2. Create a new directory for your skill
3. Add a `SKILL.md` with documentation
4. Include any scripts or code in a `scripts/` subdirectory
5. Update this README.md to list your skill
6. Submit a pull request

## License

MIT License - See individual skills for their specific licenses.

## Links

- Website: https://skills.sh
- Issues: https://github.com/tumf/skills.sh/issues

---

Built with ❤️ for developers who love automation
