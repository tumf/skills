# Clawdbot Skills System

Complete guide to Clawdbot's AgentSkills-compatible skill system.

## Table of Contents

- [Overview](#overview)
- [Skill Locations and Precedence](#skill-locations-and-precedence)
- [Skill Format](#skill-format)
- [Skill Metadata (Gating)](#skill-metadata-gating)
- [Per-Skill Configuration](#per-skill-configuration)
- [Environment Injection](#environment-injection)
- [Installer Specifications](#installer-specifications)
- [Skills in Sandboxed Agents](#skills-in-sandboxed-agents)
- [Skills Watcher](#skills-watcher)
- [Token Impact](#token-impact)
- [ClawdHub Registry](#clawdhub-registry)

## Overview

Clawdbot uses **AgentSkills-compatible** skill folders to teach agents how to use tools. Each skill is a directory containing `SKILL.md` with YAML frontmatter and instructions.

**Key Features**:
- Bundled skills (shipped with install)
- Managed/local skills (`~/.clawdbot/skills`)
- Workspace skills (`<workspace>/skills`)
- Load-time filtering based on environment, config, and binary presence
- Plugin-provided skills

## Skill Locations and Precedence

Skills are loaded from **three** locations:

1. **Bundled skills**: Shipped with npm package or Clawdbot.app
2. **Managed/local skills**: `~/.clawdbot/skills`
3. **Workspace skills**: `<workspace>/skills`

**Precedence** (highest to lowest):
```
<workspace>/skills → ~/.clawdbot/skills → bundled skills
```

**Additional folders** (lowest precedence):
```jsonc
{
  "skills": {
    "load": {
      "extraDirs": [
        "~/Projects/agent-scripts/skills",
        "~/Projects/oss/some-skill-pack/skills"
      ]
    }
  }
}
```

## Skill Format

### Directory Structure

```
skill-name/
├── SKILL.md           (required)
├── scripts/           (optional)
├── references/        (optional)
└── assets/            (optional)
```

### SKILL.md Format

**Required YAML frontmatter**:

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
---

# Instructions

Use this skill when...

## Quick Start

...
```

**Optional frontmatter keys**:

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups
homepage: https://github.com/example/gemini-cli
user-invocable: true
disable-model-invocation: false
command-dispatch: tool
command-tool: gemini_execute
command-arg-mode: raw
metadata: {"clawdbot":{"emoji":"♊️","requires":{"bins":["gemini"]}}}
---
```

**Frontmatter fields**:
- `name` (required): Skill identifier
- `description` (required): When and how to use this skill
- `homepage`: URL for skill documentation
- `user-invocable`: Expose as user slash command (default: `true`)
- `disable-model-invocation`: Exclude from model prompt (default: `false`)
- `command-dispatch`: Set to `"tool"` for direct tool invocation
- `command-tool`: Tool name for dispatch
- `command-arg-mode`: Argument handling mode (default: `"raw"`)
- `metadata`: Single-line JSON object for gating and installation

### Using SKILL_ROOT in Instructions

Reference the skill folder path via `SKILL_ROOT`:

```markdown
Run the script:
```bash
python3 "$SKILL_ROOT/scripts/process.py"
```
```

## Skill Metadata (Gating)

Skills are **filtered at load time** using `metadata.clawdbot`:

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
metadata: {"clawdbot":{"requires":{"bins":["uv"],"env":["GEMINI_API_KEY"],"config":["browser.enabled"]},"primaryEnv":"GEMINI_API_KEY"}}
---
```

### Metadata Fields

**`metadata.clawdbot` structure**:

```jsonc
{
  "clawdbot": {
    // Always include this skill (skip other gates)
    "always": true,
    
    // Optional emoji for macOS Skills UI
    "emoji": "♊️",
    
    // Optional homepage URL
    "homepage": "https://example.com",
    
    // Platform filtering
    "os": ["darwin", "linux", "win32"],
    
    // Requirements (all must be met)
    "requires": {
      // All binaries must exist on PATH
      "bins": ["uv", "python3"],
      
      // At least one binary must exist
      "anyBins": ["npm", "pnpm", "yarn"],
      
      // Environment variables (or config values)
      "env": ["GEMINI_API_KEY"],
      
      // Config paths must be truthy
      "config": ["browser.enabled", "tools.exec.enabled"]
    },
    
    // Primary environment variable for this skill
    "primaryEnv": "GEMINI_API_KEY",
    
    // Installation specifications (for macOS Skills UI)
    "install": [
      {
        "id": "brew",
        "kind": "brew",
        "formula": "gemini-cli",
        "bins": ["gemini"],
        "label": "Install Gemini CLI (brew)"
      }
    ],
    
    // Skill configuration key (defaults to skill name)
    "skillKey": "custom-config-key"
  }
}
```

### Gating Rules

**Binary requirements** (`requires.bins`):
- Checked on **host** at skill load time
- For sandboxed agents, binary must also exist **inside container**
- Use `agents.defaults.sandbox.docker.setupCommand` for installation

**Environment requirements** (`requires.env`):
- Env var must exist OR be provided in `skills.entries.<name>.env`

**Config requirements** (`requires.config`):
- Config paths must be truthy in `~/.clawdbot/clawdbot.json`

**Platform requirements** (`os`):
- Only load on specified platforms (`darwin`, `linux`, `win32`)

## Per-Skill Configuration

Configure individual skills in `~/.clawdbot/clawdbot.json`:

```jsonc
{
  "skills": {
    "entries": {
      "nano-banana-pro": {
        // Enable/disable skill
        "enabled": true,
        
        // Primary API key (uses metadata.clawdbot.primaryEnv)
        "apiKey": "GEMINI_KEY_HERE",
        
        // Environment variables
        "env": {
          "GEMINI_API_KEY": "GEMINI_KEY_HERE",
          "GEMINI_ENDPOINT": "https://api.example.com"
        },
        
        // Custom configuration
        "config": {
          "endpoint": "https://example.invalid",
          "model": "nano-pro"
        }
      },
      
      "peekaboo": { "enabled": true },
      "sag": { "enabled": false }
    }
  }
}
```

**Configuration keys**:
- Use skill `name` by default
- If skill defines `metadata.clawdbot.skillKey`, use that instead

**Bundled skill allowlist**:
```jsonc
{
  "skills": {
    "allowBundled": ["gemini", "peekaboo"]
  }
}
```

## Environment Injection

**Per agent run** (scoped, not global):

1. Read skill metadata
2. Apply `skills.entries.<key>.env` or `skills.entries.<key>.apiKey`
3. Build system prompt with eligible skills
4. Restore original environment after run

**Injected only if** the variable isn't already set in `process.env`.

## Installer Specifications

Skills can declare installation methods in `metadata.clawdbot.install`:

### Brew Installer

```jsonc
{
  "id": "brew",
  "kind": "brew",
  "formula": "gemini-cli",
  "bins": ["gemini"],
  "label": "Install Gemini CLI (brew)",
  "os": ["darwin"]
}
```

### Node Package Installer

```jsonc
{
  "id": "npm",
  "kind": "node",
  "package": "typescript",
  "global": true,
  "bins": ["tsc"],
  "label": "Install TypeScript (npm)"
}
```

**Node manager preference**:
```jsonc
{
  "skills": {
    "install": {
      "nodeManager": "pnpm"  // npm | pnpm | yarn | bun
    }
  }
}
```

### Go Package Installer

```jsonc
{
  "id": "go-tool",
  "kind": "go",
  "package": "github.com/example/tool",
  "bins": ["tool"],
  "label": "Install Tool (go install)"
}
```

**Auto-install Go**: If `go` is missing and `brew` is available, gateway installs Go via Homebrew first.

### UV Package Installer

```jsonc
{
  "id": "uv-package",
  "kind": "uv",
  "package": "ruff",
  "bins": ["ruff"],
  "label": "Install Ruff (uv)"
}
```

### Download Installer

```jsonc
{
  "id": "binary-download",
  "kind": "download",
  "url": "https://github.com/example/tool/releases/download/v1.0.0/tool-linux-x64.tar.gz",
  "archive": "tar.gz",
  "extract": true,
  "stripComponents": 1,
  "targetDir": "~/.clawdbot/tools/tool",
  "bins": ["tool"],
  "label": "Download Tool Binary",
  "os": ["linux"]
}
```

### Multiple Installers

Gateway picks a **single** preferred option:
1. Brew (if available)
2. Node (if available)
3. Download (lists all options)

## Skills in Sandboxed Agents

**Important**: Sandboxed agents run inside Docker containers.

**Binary requirements**:
- Must exist on host at load time
- Must exist inside container at runtime
- Install via `setupCommand`:

```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "setupCommand": "apt-get update && apt-get install -y python3-pip && pip3 install summarize"
        }
      }
    }
  }
}
```

**Environment variables**:
- Global `skills.entries.<skill>.env` applies to **host** runs only
- For sandboxed runs, use `agents.defaults.sandbox.docker.env`:

```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "env": {
            "GEMINI_API_KEY": "${GEMINI_API_KEY}",
            "OPENAI_API_KEY": "${OPENAI_API_KEY}"
          }
        }
      }
    }
  }
}
```

## Skills Watcher

Auto-refresh skills when `SKILL.md` files change:

```jsonc
{
  "skills": {
    "load": {
      "watch": true,
      "watchDebounceMs": 250
    }
  }
}
```

**Behavior**:
- Skills snapshot is created when session starts
- Watcher bumps snapshot on changes (hot reload)
- Refreshed list picked up on next agent turn

## Token Impact

Skills are injected as compact XML in the system prompt:

**Base overhead** (when ≥1 skill): 195 characters

**Per skill**: 97 characters + length of:
- XML-escaped `<name>`
- XML-escaped `<description>`
- XML-escaped `<location>`

**Formula** (characters):
```
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

**Rough estimate**: ~4 chars/token → **~24 tokens per skill** + field lengths

## ClawdHub Registry

Browse and install community skills:

**Website**: https://clawdhub.com

**CLI commands**:
```bash
# Install skill into workspace
clawdhub install <skill-slug>

# Update all installed skills
clawdhub update --all

# Sync (scan + publish updates)
clawdhub sync --all
```

**Default install location**: `./skills` (or configured workspace)

## Remote macOS Nodes

**Linux gateway + macOS node**:

If a macOS node is connected with `system.run` allowed, Clawdbot treats macOS-only skills as eligible when:
1. Required binaries are present on the node
2. Node reports command support

**Agent invocation**: Use `nodes` tool (typically `nodes.run`)

**Caveat**: Skills remain visible if node goes offline; invocations may fail until reconnection.

## Multi-Agent Skills

**Per-agent skills**: `<workspace>/skills` (agent-specific)

**Shared skills**: `~/.clawdbot/skills` (visible to all agents)

**Shared folders**: `skills.load.extraDirs` (lowest precedence)

**Precedence per agent**:
```
agent-workspace/skills → ~/.clawdbot/skills → extraDirs → bundled
```

## Plugin Skills

Plugins can ship skills by listing `skills` directories in `clawdbot.plugin.json`:

```jsonc
{
  "name": "my-plugin",
  "skills": ["./skills"]
}
```

**Loading**: Plugin skills load when plugin is enabled

**Gating**: Use `metadata.clawdbot.requires.config` on plugin's config entry

**Precedence**: Participate in normal precedence rules

## Common Patterns

### API Integration Skill

```markdown
---
name: myapi
description: Interact with MyAPI service for data retrieval and updates
metadata: {"clawdbot":{"requires":{"env":["MYAPI_KEY"]},"primaryEnv":"MYAPI_KEY"}}
---

# MyAPI Integration

Authenticate using the MYAPI_KEY environment variable.

## Quick Start

\`\`\`python
import os
import requests

api_key = os.environ['MYAPI_KEY']
response = requests.get('https://api.example.com/data', 
                        headers={'Authorization': f'Bearer {api_key}'})
\`\`\`

## Endpoints

See [API Reference](./references/api.md) for complete documentation.
```

### CLI Tool Skill

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups
metadata: {"clawdbot":{"emoji":"♊️","requires":{"bins":["gemini"]},"install":[{"id":"brew","kind":"brew","formula":"gemini-cli","bins":["gemini"],"label":"Install Gemini CLI (brew)"}]}}
---

# Gemini CLI

## Usage

\`\`\`bash
# Ask a question
gemini "What is the capital of France?"

# Search Google
gemini --search "latest TypeScript features"
\`\`\`

## Installation

Install via Homebrew:
\`\`\`bash
brew install gemini-cli
\`\`\`
```

### Multi-Platform Skill

```markdown
---
name: screenshot
description: Capture screen or window screenshots
metadata: {"clawdbot":{"os":["darwin","linux"],"requires":{"anyBins":["screencapture","import","scrot"]}}}
---

# Screenshot Tool

Platform-specific commands:

- macOS: Use `screencapture`
- Linux: Use `import` (ImageMagick) or `scrot`

## macOS

\`\`\`bash
screencapture -x ~/Desktop/screenshot.png
\`\`\`

## Linux

\`\`\`bash
import ~/screenshot.png
# or
scrot ~/screenshot.png
\`\`\`
```
