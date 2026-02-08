# Skills

A collection of skills for AI coding agents.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Installation

```bash
npx skills add tumf/skills
```

## Available Skills

### firecrawl

Web scraping and data extraction toolkit.

[Documentation](./firecrawl/README.md)

### clawdbot-config

Comprehensive Clawdbot configuration and skills system management skill.

[Documentation](./clawdbot-config/README.md)

### opencode-command-creator

Create custom OpenCode commands with proper structure and configuration.

[Documentation](./opencode-command-creator/README.md)

### opencode-agent-creator

Create specialized OpenCode agents with proper configuration for primary agents and subagents.

[Documentation](./opencode-agent-creator/README.md)

### slack-rs

Slack Web API automation via the slack-rs CLI (Rust).

[Documentation](./slack-rs/README.md)

### rust-cli

General guidance and templates for building Rust CLI programs (clap/anyhow/tracing/serde_json), including prek-based git hooks.

[Documentation](./rust-cli/README.md)

---

*More skills coming soon...*

## Usage

Skills are available once installed. Use the skill name in your request.

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `README.md` - Full documentation
- `scripts/` - Executable scripts (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
