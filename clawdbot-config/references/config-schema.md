# Clawdbot Configuration Schema

Complete reference for `~/.clawdbot/clawdbot.json` configuration options.

## Table of Contents

- [File Location](#file-location)
- [Format](#format)
- [Top-Level Structure](#top-level-structure)
- [Agents Configuration](#agents-configuration)
- [Skills Configuration](#skills-configuration)
- [Channels Configuration](#channels-configuration)
- [Gateway Configuration](#gateway-configuration)
- [Tools Configuration](#tools-configuration)
- [Providers Configuration](#providers-configuration)
- [Environment Variables](#environment-variables)

## File Location

**Primary config**: `~/.clawdbot/clawdbot.json`

**Alternative paths**:
- Set via `CLAWDBOT_CONFIG_PATH` environment variable
- Per-instance: `CLAWDBOT_STATE_DIR` for multi-instance setups

## Format

- **File format**: JSONC (JSON with Comments)
- **Schema validation**: Strict validation enabled by default
- **Includes support**: Use `$include` for modular configs

## Top-Level Structure

```jsonc
{
  // Agent runtime configuration
  "agents": { /* ... */ },
  
  // Skills system configuration
  "skills": { /* ... */ },
  
  // Channel integrations (WhatsApp, Telegram, etc.)
  "channels": { /* ... */ },
  
  // Gateway server configuration
  "gateway": { /* ... */ },
  
  // Tool behavior and permissions
  "tools": { /* ... */ },
  
  // Model provider settings
  "providers": { /* ... */ },
  
  // Environment and shell settings
  "env": { /* ... */ },
  
  // Logging configuration
  "logging": { /* ... */ }
}
```

## Agents Configuration

Controls the embedded agent runtime (derived from p-mono).

### Basic Structure

```jsonc
{
  "agents": {
    "defaults": {
      // Required: agent workspace directory
      "workspace": "~/Projects/my-agent-workspace",
      
      // Model configuration
      "model": "anthropic/claude-sonnet-4",
      "models": {
        "primary": "anthropic/claude-sonnet-4",
        "fallback": ["anthropic/claude-sonnet-3-5"]
      },
      
      // Session configuration
      "sessionStore": "~/.clawdbot/agents/default/sessions",
      
      // Streaming and chunking
      "blockStreamingDefault": "off",  // "off" | "on"
      "blockStreamingBreak": "text_end",  // "text_end" | "message_end"
      "blockStreamingChunk": [800, 1200],  // [min, max] characters
      "blockStreamingCoalesce": true,
      
      // Sandbox configuration
      "sandbox": {
        "enabled": false,
        "workspaceRoot": "~/.clawdbot/workspaces",
        "docker": {
          "image": "clawdbot/sandbox:latest",
          "setupCommand": "apt-get update && apt-get install -y python3-pip",
          "env": {
            "GEMINI_API_KEY": "${GEMINI_API_KEY}"
          }
        }
      }
    }
  }
}
```

### Agent Workspace

The workspace is the **only** working directory for agent tools and context.

**Bootstrap files** (injected on first turn):
- `AGENTS.md` - Operating instructions and memory
- `SOUL.md` - Persona, boundaries, tone
- `TOOLS.md` - User-maintained tool notes
- `BOOTSTRAP.md` - One-time first-run ritual (deleted after)
- `IDENTITY.md` - Agent name/vibe/emoji
- `USER.md` - User profile and preferences

**Skip bootstrap creation**:
```jsonc
{
  "agent": {
    "skipBootstrap": true
  }
}
```

### Model References

Format: `provider/model` (split on first `/`)

**Examples**:
- `anthropic/claude-sonnet-4`
- `openai/gpt-4`
- `openrouter/moonshotai/kimi-k2` (includes provider for nested paths)

## Skills Configuration

See [Skills System Reference](./skills-system.md) for complete details.

### Quick Reference

```jsonc
{
  "skills": {
    // Optional: allowlist for bundled skills only
    "allowBundled": ["gemini", "peekaboo"],
    
    // Loading configuration
    "load": {
      "extraDirs": [
        "~/Projects/agent-scripts/skills",
        "~/Projects/oss/some-skill-pack/skills"
      ],
      "watch": true,
      "watchDebounceMs": 250
    },
    
    // Installation preferences
    "install": {
      "preferBrew": true,
      "nodeManager": "npm"  // npm | pnpm | yarn | bun
    },
    
    // Per-skill overrides
    "entries": {
      "nano-banana-pro": {
        "enabled": true,
        "apiKey": "GEMINI_KEY_HERE",
        "env": {
          "GEMINI_API_KEY": "GEMINI_KEY_HERE"
        }
      },
      "peekaboo": { "enabled": true },
      "sag": { "enabled": false }
    }
  }
}
```

## Channels Configuration

### WhatsApp

```jsonc
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123"],  // Strongly recommended
      "groups": {
        "*": { 
          "requireMention": true 
        }
      }
    }
  }
}
```

### Telegram

```jsonc
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "allowFrom": ["username1", "username2"]
    }
  }
}
```

### Discord

```jsonc
{
  "channels": {
    "discord": {
      "enabled": true,
      "botToken": "${DISCORD_BOT_TOKEN}",
      "allowFrom": ["user_id_1", "user_id_2"]
    }
  }
}
```

### iMessage (macOS only)

```jsonc
{
  "channels": {
    "imessage": {
      "enabled": true,
      "cliPath": "/opt/homebrew/bin/imsg",
      "dbPath": "~/Library/Messages/chat.db"
    }
  }
}
```

## Gateway Configuration

### Basic Gateway Settings

```jsonc
{
  "gateway": {
    // WebSocket server
    "port": 18789,
    "host": "127.0.0.1",  // Loopback only (recommended)
    "bind": "loopback",  // "loopback" | "tailnet" | "lan"
    
    // Authentication (required for non-loopback)
    "auth": {
      "token": "your-secure-token-here"
    },
    
    // Canvas host (HTTP file server)
    "canvasHost": {
      "port": 18793,
      "enabled": true
    }
  }
}
```

### Remote Access

For **Tailnet access**:
```bash
clawdbot gateway --bind tailnet --token YOUR_TOKEN
```

For **SSH tunneling**:
```bash
ssh -L 18789:localhost:18789 user@remote-host
```

## Tools Configuration

### Exec Tool

```jsonc
{
  "tools": {
    "exec": {
      "enabled": true,
      "security": "ask",  // "allow" | "ask" | "deny"
      "applyPatch": true  // Enable apply_patch tool
    }
  }
}
```

### Browser Tool

```jsonc
{
  "tools": {
    "browser": {
      "enabled": true,
      "profilePath": "~/.clawdbot/browser-profile",
      "browserPath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    }
  }
}
```

## Providers Configuration

### Anthropic

```jsonc
{
  "providers": {
    "anthropic": {
      "apiKey": "${ANTHROPIC_API_KEY}",
      "options": {
        "timeout": 600000,
        "setCacheKey": true
      }
    }
  }
}
```

### OpenAI

```jsonc
{
  "providers": {
    "openai": {
      "apiKey": "${OPENAI_API_KEY}",
      "organization": "${OPENAI_ORG_ID}"
    }
  }
}
```

### OpenRouter

```jsonc
{
  "providers": {
    "openrouter": {
      "apiKey": "${OPENROUTER_API_KEY}",
      "baseUrl": "https://openrouter.ai/api/v1"
    }
  }
}
```

## Environment Variables

### Shell Environment Import

```jsonc
{
  "env": {
    "shellEnv": {
      "enabled": true,  // Import from login shell
      "timeout": 5000
    }
  }
}
```

### Direct Environment Variables

```jsonc
{
  "env": {
    "vars": {
      "ANTHROPIC_API_KEY": "sk-ant-...",
      "OPENAI_API_KEY": "sk-..."
    }
  }
}
```

## Logging Configuration

```jsonc
{
  "logging": {
    "level": "info",  // "debug" | "info" | "warn" | "error"
    "file": "~/.clawdbot/logs/gateway.log",
    "console": true
  }
}
```

## Config Includes ($include)

Modular configuration using includes:

```jsonc
{
  "$include": [
    "~/.clawdbot/config/agents.json",
    "~/.clawdbot/config/channels.json"
  ],
  
  // Local overrides
  "gateway": {
    "port": 18789
  }
}
```

**Merge behavior**: Later configs override earlier ones for conflicting keys.

**Nested includes**: Supported, resolved recursively.

**Error handling**: Missing include files cause startup failure (by design).

## Minimal Recommended Config

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Projects/my-agent-workspace"
    }
  },
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123"]
    }
  }
}
```

## Configuration Validation

Run validation:
```bash
clawdbot configure --validate
```

Check current config:
```bash
clawdbot status
clawdbot configure --show
```
