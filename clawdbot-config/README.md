# clawdbot-config

Comprehensive Clawdbot configuration and skills system management skill.

## Installation

```bash
npx skills add tumf/clawdbot-config
```

Or with specific agents:

```bash
npx add-skill tumf/clawdbot-config -a opencode -a claude-code -a clawdbot
```

## Supported Agents

| Agent | Project Path | Global Path |
|-------|--------------|-------------|
| Clawdbot | `skills/` | `~/.clawdbot/skills/` |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Codex | `.codex/skills/` | `~/.codex/skills/` |

And 20+ more agents supported by [add-skill](https://github.com/vercel-labs/add-skill).

## What's Included

- **SKILL.md** - Main skill instructions for Clawdbot configuration
- **references/config-schema.md** - Complete configuration schema
- **references/config-examples.md** - Practical configuration examples
- **references/skills-system.md** - Skills system documentation
- **references/repomix-output.xml** - Full documentation archive (370+ files)

## Features

- Initial Clawdbot setup and configuration
- Skills creation with AgentSkills-compatible YAML frontmatter
- Channel configuration (WhatsApp, Telegram, Discord, iMessage, etc.)
- Gateway and remote access setup
- Multi-agent routing
- Troubleshooting guides

## Compatibility

| Component | Version |
|-----------|---------|
| Clawdbot | 1.x |
| skills CLI | 1.0.18+ |
| add-skill CLI | Latest |

## License

MIT

---

**Last Updated**: January 24, 2026
