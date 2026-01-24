# Clawdbot Configuration Examples

Practical configuration examples for common use cases.

## Table of Contents

- [Minimal Setup](#minimal-setup)
- [Single User WhatsApp Bot](#single-user-whatsapp-bot)
- [Multi-Channel Setup](#multi-channel-setup)
- [Remote Gateway with Tailscale](#remote-gateway-with-tailscale)
- [Sandboxed Agent](#sandboxed-agent)
- [Multi-Agent Routing](#multi-agent-routing)
- [Skills Management](#skills-management)
- [Self-Chat Mode (Group Control)](#self-chat-mode-group-control)
- [Modular Config with Includes](#modular-config-with-includes)
- [Development Setup](#development-setup)

## Minimal Setup

Basic configuration to get started:

```jsonc
{
  // Required: agent workspace
  "agents": {
    "defaults": {
      "workspace": "~/Projects/my-agent-workspace"
    }
  },
  
  // Recommended: restrict WhatsApp access
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123"]
    }
  }
}
```

**Setup commands**:
```bash
# Initialize workspace
clawdbot setup

# Pair WhatsApp
clawdbot channels login

# Start gateway
clawdbot gateway
```

## Single User WhatsApp Bot

Personal assistant with enhanced privacy:

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Documents/ClauwdWorkspace",
      "model": "anthropic/claude-sonnet-4",
      "blockStreamingDefault": "on"
    }
  },
  
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123"],
      
      // Disable group participation
      "groups": {
        "*": { 
          "enabled": false 
        }
      }
    }
  },
  
  "skills": {
    // Only load specific bundled skills
    "allowBundled": ["gemini", "peekaboo", "browser"],
    
    "entries": {
      "gemini": {
        "enabled": true,
        "apiKey": "${GEMINI_API_KEY}"
      }
    }
  },
  
  "tools": {
    "exec": {
      // Require approval for all commands
      "security": "ask"
    }
  }
}
```

## Multi-Channel Setup

Bot available on WhatsApp, Telegram, and Discord:

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Clawdbot/workspace",
      "model": "anthropic/claude-sonnet-4"
    }
  },
  
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123", "+15555550124"]
    },
    
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "allowFrom": ["alice", "bob"]
    },
    
    "discord": {
      "enabled": true,
      "botToken": "${DISCORD_BOT_TOKEN}",
      "allowFrom": ["123456789012345678", "234567890123456789"]
    }
  },
  
  "messages": {
    "groupChat": {
      // Custom mention patterns for all channels
      "mentionPatterns": ["@clawd", "hey clawd"]
    }
  }
}
```

**Setup**:
```bash
# Set tokens in environment
export TELEGRAM_BOT_TOKEN="your-telegram-token"
export DISCORD_BOT_TOKEN="your-discord-token"

# Start gateway
clawdbot gateway
```

## Remote Gateway with Tailscale

Access gateway over Tailscale network:

```jsonc
{
  "gateway": {
    "port": 18789,
    "bind": "tailnet",  // Listen on Tailscale IP
    
    "auth": {
      "token": "${GATEWAY_AUTH_TOKEN}"  // Required for non-loopback
    },
    
    "canvasHost": {
      "port": 18793,
      "enabled": true
    }
  },
  
  "agents": {
    "defaults": {
      "workspace": "~/Clawdbot/workspace"
    }
  },
  
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123"]
    }
  }
}
```

**Generate token**:
```bash
clawdbot doctor --generate-gateway-token
```

**Start gateway**:
```bash
clawdbot gateway --bind tailnet --token $GATEWAY_AUTH_TOKEN
```

**Connect from remote**:
```bash
# On client machine
export CLAWDBOT_GATEWAY_URL="ws://gateway-hostname.tailnet-name.ts.net:18789"
export CLAWDBOT_GATEWAY_TOKEN="your-token"

clawdbot tui
```

## Sandboxed Agent

Run agent in isolated Docker container:

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Clawdbot/workspace",
      "model": "anthropic/claude-sonnet-4",
      
      "sandbox": {
        "enabled": true,
        "workspaceRoot": "~/.clawdbot/workspaces",
        
        "docker": {
          "image": "clawdbot/sandbox:latest",
          
          // Install dependencies in container
          "setupCommand": "apt-get update && apt-get install -y python3-pip nodejs npm && pip3 install ruff black && npm install -g typescript",
          
          // Pass through API keys
          "env": {
            "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
            "GEMINI_API_KEY": "${GEMINI_API_KEY}"
          },
          
          // Resource limits
          "memory": "2g",
          "cpus": "2"
        }
      }
    }
  },
  
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123"]
    }
  }
}
```

**Build custom sandbox image**:
```dockerfile
FROM clawdbot/sandbox:latest

RUN apt-get update && \
    apt-get install -y python3-pip nodejs npm && \
    pip3 install ruff black mypy && \
    npm install -g typescript eslint prettier

WORKDIR /workspace
```

```bash
docker build -t my-clawdbot-sandbox .
```

Update config to use custom image:
```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "image": "my-clawdbot-sandbox"
        }
      }
    }
  }
}
```

## Multi-Agent Routing

Route different users/channels to specialized agents:

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Clawdbot/main-workspace",
      "model": "anthropic/claude-sonnet-4"
    },
    
    "list": [
      {
        "id": "code-reviewer",
        "workspace": "~/Clawdbot/reviewer-workspace",
        "model": "anthropic/claude-sonnet-4",
        "routes": [
          { "channel": "telegram", "peer": "alice" }
        ],
        "tools": {
          "write": false,
          "edit": false,
          "exec": { "security": "deny" }
        }
      },
      
      {
        "id": "data-analyst",
        "workspace": "~/Clawdbot/analyst-workspace",
        "model": "openai/gpt-4",
        "routes": [
          { "channel": "discord", "peer": "123456789012345678" }
        ]
      }
    ]
  },
  
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}"
    },
    
    "discord": {
      "enabled": true,
      "botToken": "${DISCORD_BOT_TOKEN}"
    },
    
    "whatsapp": {
      "allowFrom": ["+15555550123"]
    }
  }
}
```

## Skills Management

Advanced skills configuration:

```jsonc
{
  "skills": {
    // Only load specific bundled skills
    "allowBundled": ["gemini", "browser", "peekaboo"],
    
    // Additional skill directories
    "load": {
      "extraDirs": [
        "~/Projects/custom-skills/skills",
        "~/Documents/Company/clawdbot-skills"
      ],
      "watch": true,
      "watchDebounceMs": 250
    },
    
    // Installation preferences
    "install": {
      "preferBrew": true,
      "nodeManager": "pnpm"
    },
    
    // Per-skill configuration
    "entries": {
      "gemini": {
        "enabled": true,
        "apiKey": "${GEMINI_API_KEY}",
        "env": {
          "GEMINI_MODEL": "gemini-pro"
        }
      },
      
      "nano-banana-pro": {
        "enabled": true,
        "apiKey": "${GEMINI_API_KEY}",
        "config": {
          "endpoint": "https://generativelanguage.googleapis.com/v1beta",
          "model": "gemini-3-pro-image"
        }
      },
      
      "browser": {
        "enabled": true
      },
      
      // Disable specific bundled skill
      "sag": {
        "enabled": false
      }
    }
  },
  
  "agents": {
    "defaults": {
      "workspace": "~/Clawdbot/workspace"
    }
  }
}
```

## Self-Chat Mode (Group Control)

Control gateway via special self-chat:

```jsonc
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123"],
      
      // Regular groups require mention
      "groups": {
        "*": { 
          "requireMention": true 
        },
        
        // Special control group (use group JID)
        "120363012345678@g.us": {
          "requireMention": false,
          "enabled": true
        }
      }
    }
  },
  
  "messages": {
    "groupChat": {
      "mentionPatterns": ["@clawd", "hey clawd", "/clawd"]
    }
  }
}
```

**Usage**: Send commands to control group without mentions:
```
/activation always
/model anthropic/claude-sonnet-4
/status
```

## Modular Config with Includes

Split configuration into multiple files:

**Main config** (`~/.clawdbot/clawdbot.json`):
```jsonc
{
  "$include": [
    "~/.clawdbot/config/agents.json",
    "~/.clawdbot/config/channels.json",
    "~/.clawdbot/config/skills.json"
  ],
  
  "gateway": {
    "port": 18789,
    "auth": {
      "token": "${GATEWAY_AUTH_TOKEN}"
    }
  }
}
```

**Agents config** (`~/.clawdbot/config/agents.json`):
```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Clawdbot/workspace",
      "model": "anthropic/claude-sonnet-4",
      "blockStreamingDefault": "on"
    }
  }
}
```

**Channels config** (`~/.clawdbot/config/channels.json`):
```jsonc
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123"]
    },
    
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}"
    }
  }
}
```

**Skills config** (`~/.clawdbot/config/skills.json`):
```jsonc
{
  "skills": {
    "allowBundled": ["gemini", "browser"],
    
    "entries": {
      "gemini": {
        "enabled": true,
        "apiKey": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

**Benefits**:
- Easier to manage
- Team can share base configs
- Override specific parts per environment

## Development Setup

Local development with hot reload:

```jsonc
{
  "agents": {
    "defaults": {
      "workspace": "~/Projects/clawdbot-dev/workspace",
      "model": "anthropic/claude-sonnet-4"
    }
  },
  
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+15555550123"]
    }
  },
  
  "skills": {
    // Load skills from development directory
    "load": {
      "extraDirs": [
        "~/Projects/my-skills/skills"
      ],
      "watch": true,  // Hot reload on changes
      "watchDebounceMs": 250
    },
    
    // Allow all bundled skills for testing
    "allowBundled": null
  },
  
  "tools": {
    "exec": {
      "security": "allow"  // Auto-approve for dev
    }
  },
  
  "logging": {
    "level": "debug",
    "console": true,
    "file": "~/.clawdbot/logs/dev.log"
  },
  
  "gateway": {
    "port": 19789  // Non-default port for dev instance
  }
}
```

**Multi-instance development**:
```bash
# Terminal 1: Production instance
clawdbot gateway

# Terminal 2: Development instance
CLAWDBOT_CONFIG_PATH=~/.clawdbot/dev.json \
CLAWDBOT_STATE_DIR=~/.clawdbot-dev \
clawdbot gateway --port 19789
```

## Testing Configuration

Validate and inspect configuration:

```bash
# Validate config syntax
clawdbot configure --validate

# Show effective configuration
clawdbot configure --show

# Check gateway status
clawdbot status

# Deep health check
clawdbot doctor

# Test specific skill
clawdbot skills list
```

## Environment Variables

Set API keys and tokens:

```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
export TELEGRAM_BOT_TOKEN="..."
export DISCORD_BOT_TOKEN="..."
export GATEWAY_AUTH_TOKEN="..."
```

Or use config file:
```jsonc
{
  "env": {
    "vars": {
      "ANTHROPIC_API_KEY": "sk-ant-...",
      "GEMINI_API_KEY": "..."
    }
  }
}
```

## Common Patterns

### Owner-Only Bot

```jsonc
{
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123"],
      "groups": { "*": { "enabled": false } }
    }
  }
}
```

### Team Bot with Allowlist

```jsonc
{
  "channels": {
    "whatsapp": {
      "allowFrom": [
        "+15555550123",  // Alice
        "+15555550124",  // Bob
        "+15555550125"   // Charlie
      ]
    }
  }
}
```

### Read-Only Agent (Review Mode)

```jsonc
{
  "tools": {
    "write": false,
    "edit": false,
    "exec": { "security": "deny" }
  }
}
```

### Cost-Conscious Setup

```jsonc
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-haiku-4",  // Cheaper model
      "models": {
        "primary": "anthropic/claude-haiku-4",
        "fallback": []  // No fallback
      }
    }
  }
}
```
