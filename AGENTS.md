# Agent Development Guidelines

This is a collection of skills for AI coding agents following the [Agent Skills](https://agentskills.io/) format.

## Repository Structure

```
skills/
├── README.md              # Main documentation
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
└── {skill-name}/         # Individual skill directories
    ├── SKILL.md          # Agent instructions (YAML frontmatter + docs)
    ├── README.md         # Full documentation for users
    └── scripts/          # Executable Python scripts
```

## Quick Commands

```bash
# Make scripts executable
chmod +x {skill}/scripts/*.py

# Run a script
./{skill}/scripts/{script-name}.py [arguments]

# Example
./firecrawl/scripts/scrape.py "https://example.com"
```

## Detailed Guidelines

For specific development guidelines, see:
- [Python Style Guide](.agent/python-style.md) - Script structure, formatting, error handling
- [Documentation Standards](.agent/documentation.md) - SKILL.md and README.md formats
- [Development Workflow](.agent/workflow.md) - Creating skills, Git workflow
- [Project Standards](.agent/standards.md) - JSON output, environment variables, licensing
