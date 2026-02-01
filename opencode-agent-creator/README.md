# OpenCode Agent Creator

A skill for creating specialized OpenCode agents with proper configuration.

## Overview

This skill provides comprehensive guidance for creating OpenCode agents - specialized AI assistants configured for specific tasks and workflows. Agents can be primary (user-facing) or subagents (invoked for specialized tasks).

## Features

- **Agent Types**: Primary agents and subagents with different use cases
- **Configuration Formats**: Markdown files (recommended) and JSON configuration
- **Flexible Permissions**: Granular control over tool access and operations
- **Model Selection**: Override default models per agent
- **Temperature Control**: Fine-tune creativity vs. determinism
- **Tool Management**: Enable/disable specific tools per agent

## Quick Start

### Create an Agent Interactively

```bash
opencode agent create
```

### Manual Creation

1. Create a markdown file in `~/.config/opencode/agents/` or `.opencode/agents/`
2. Add YAML frontmatter with configuration
3. Write the system prompt below the frontmatter

**Example: `code-reviewer.md`**

```markdown
---
description: Reviews code for best practices and potential issues
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
---

You are a code reviewer. Focus on security, performance, and maintainability.
```

## Agent Types

### Primary Agents
- Main assistants you interact with directly
- Switch between them using **Tab** key
- Examples: Build (full development), Plan (analysis only)

### Subagents
- Specialized for specific tasks
- Invoked by `@mention` or automatically by primary agents
- Examples: General (multi-step tasks), Explore (codebase search)

## Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `description` | string | Brief description of agent's purpose (required) |
| `mode` | string | `primary`, `subagent`, or `all` (default: `all`) |
| `model` | string | Override default model (format: `provider/model-id`) |
| `temperature` | number | Control randomness (0.0-1.0) |
| `maxSteps` | number | Maximum agentic iterations |
| `tools` | object | Enable/disable specific tools |
| `permission` | object | Control operation approval requirements |
| `hidden` | boolean | Hide subagent from autocomplete |
| `disable` | boolean | Disable the agent |

## Permission Levels

- **`allow`**: No approval required
- **`ask`**: Prompt user before action
- **`deny`**: Completely disable

## Temperature Guidelines

- **0.0-0.2**: Focused and deterministic (code analysis, planning)
- **0.3-0.5**: Balanced (general development)
- **0.6-1.0**: Creative (brainstorming, exploration)

## Example Agents

### Documentation Writer

```markdown
---
description: Writes and maintains project documentation
mode: subagent
tools:
  bash: false
---

You are a technical writer. Create clear, comprehensive documentation.
```

### Security Auditor

```markdown
---
description: Performs security audits and identifies vulnerabilities
mode: subagent
tools:
  write: false
  edit: false
---

You are a security expert. Identify potential security issues.
```

### Debug Agent

```markdown
---
description: Focused debugging with investigation tools
mode: primary
temperature: 0.2
tools:
  write: false
permission:
  edit: ask
---

You are a debugging specialist. Systematically investigate issues.
```

## Usage

### Using Primary Agents
- Press **Tab** to cycle through available primary agents
- Agent name appears in the CLI prompt

### Using Subagents
- **Manual**: Type `@agent-name your message`
- **Automatic**: Primary agents invoke them based on descriptions
- **Navigate sessions**: `<Leader>+Right/Left` to switch between parent/child sessions

## Best Practices

1. ✅ Use clear, descriptive agent names
2. ✅ Write focused system prompts for specific tasks
3. ✅ Restrict tools to only what's needed
4. ✅ Use `ask` permission for risky operations
5. ✅ Set appropriate temperature for the task
6. ✅ Store reusable agents globally, project-specific agents locally
7. ✅ Test agents thoroughly before committing

## File Locations

- **Global agents**: `~/.config/opencode/agents/`
- **Project agents**: `.opencode/agents/`
- **Global config**: `~/.config/opencode/opencode.jsonc`
- **Project config**: `.opencode/opencode.jsonc` or `./opencode.jsonc`

## Requirements

- OpenCode CLI installed
- Access to LLM providers (Anthropic, OpenAI, etc.)
- Proper API keys configured

## Related Documentation

- [OpenCode Agents Documentation](https://opencode.ai/docs/agents/)
- [OpenCode Configuration](https://opencode.ai/docs/config/)
- [OpenCode Tools](https://opencode.ai/docs/tools)
- [OpenCode Permissions](https://opencode.ai/docs/permissions)

## License

MIT License - See LICENSE file for details
