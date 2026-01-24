# Skills

A collection of reusable command-line tools for web scraping, data extraction, and automation tasks.

## Overview

This repository provides ready-to-use scripts and tools that can be used in multiple ways:
- **Standalone tools**: Use the scripts directly from the command line
- **Integration**: Import into your own projects and workflows
- **Automation**: Integrate into shell scripts, cron jobs, or CI/CD pipelines

Each tool is self-contained with its own documentation and executable scripts.

## Installation

### Install Specific Skills (AI Agents)

```bash
# Install a specific skill
npx skills add tumf/skills --skill <skill-name>
```

```bash
npx skills add tumf/skills
```

### Clone Repository

```bash
# Clone entire repository
git clone https://github.com/tumf/skills.git
cd skills

# Navigate to specific skill and follow its README
cd <skill-name>
cat README.md
```

## Available Skills

### 🔥 [Firecrawl](./firecrawl) - Web Scraping Toolkit

Comprehensive web scraping, crawling, and data extraction powered by Firecrawl API.

**Tools**: scrape, search, map, crawl, extract, agent  
**Installation**: `npx skills add tumf/skills --skill firecrawl`

**[📖 Documentation](./firecrawl/README.md)**

---

*More skills coming soon...*

## General Usage

Each skill is self-contained with its own scripts and documentation. After installation:

### Command Line

```bash
# Navigate to skill directory
cd <skill-name>

# View documentation
cat README.md

# Run scripts
./scripts/<script-name>.py [arguments]
```

### Python Integration

```python
import subprocess
import json

# Call any skill script
result = subprocess.run(
    ["./path/to/skill/scripts/script.py", "arg1"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
```

### Automation & CI/CD

```bash
# Cron jobs, shell scripts, GitHub Actions, etc.
cd /path/to/skills/<skill-name>
./scripts/<script>.py [args]
```

## Repository Structure

```
skills/
├── README.md                # This file - collection overview
├── LICENSE                  # MIT License
│
├── <skill-name>/           # Each skill is self-contained
│   ├── README.md           # Skill documentation
│   ├── SKILL.md            # AI agent metadata (optional)
│   ├── scripts/            # Executable scripts
│   ├── references/         # Additional docs (optional)
│   └── assets/             # Templates, configs (optional)
│
└── firecrawl/              # Example: Firecrawl web scraping
    ├── README.md
    ├── SKILL.md
    └── scripts/
        ├── scrape.py
        ├── search.py
        └── ...
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
