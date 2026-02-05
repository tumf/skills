# slack-rs

Agent skill for Slack Web API automation using the `slack-rs` CLI tool (Rust).

## Overview

This skill enables AI agents to interact with Slack workspaces via OAuth-authenticated API calls. It uses the `slack-rs` CLI tool to securely manage multiple workspace profiles and execute any Slack Web API method.

### Key Features

- OAuth authentication with PKCE flow (including cloudflared-based remote login)
- Multiple workspace profile management
- Secure token storage using OS keyring
- Profile import/export with encryption
- Generic API access: call any Slack Web API method
- Write operation safety guard via environment variable
- Smart retry logic with exponential backoff

## Prerequisites

Before using this skill, you must have the `slack-rs` CLI tool installed on your system.

### Install slack-rs CLI

Install from crates.io (recommended):

```bash
cargo install slack-rs
```

Or build from source:

```bash
git clone https://github.com/tumf/slack-rs.git
cd slack-rs
cargo build --release
# Binary available at: target/release/slack-rs
```

Or install from local source:

```bash
git clone https://github.com/tumf/slack-rs.git
cd slack-rs
cargo install --path .
```

Verify installation:

```bash
slack-rs --version
```

## Skill Installation

To enable this skill for AI agents, add the skill directory to your agent's configuration:

### OpenCode / Claude

Add to `.opencode/config.jsonc` or `~/.config/opencode/config.jsonc`:

```jsonc
{
  "instructions": [
    "path/to/slack-rs/SKILL.md"
  ]
}
```

Or use the skill loader:

```bash
# In an agent conversation
Load the slack-rs skill
```

### AgentSkills Format

This skill follows the [AgentSkills](https://agentskills.io/) format:

- `SKILL.md` - Agent instructions (YAML frontmatter + usage docs)
- `README.md` - This file (user-facing documentation)
- No `scripts/` directory (uses `slack-rs` CLI directly)

## Setup for First Use

After installing the `slack-rs` CLI tool, you need to set up OAuth credentials for your Slack workspace(s).

### 1. Create a Slack App

1. Go to https://api.slack.com/apps
2. Click "Create New App"
3. In "Basic Information" -> "App Credentials", note your Client ID and Client Secret

### 2. Set Up OAuth Credentials

#### Quick Setup: App Manifest + Cloudflared (Recommended)

The most recommended login flow is to install `cloudflared` and use `--cloudflared`.
In this mode, `slack-rs auth login` generates a Slack App Manifest for you (and copies it to your clipboard, best effort).

Intended flow:

1. Create a Slack app and get credentials:
   - Go to https://api.slack.com/apps
   - Create an app
   - In "Basic Information" -> "App Credentials", copy your client ID and client secret
2. Install cloudflared:
   - https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
3. Start login with `--cloudflared`:

```bash
slack-rs auth login my-workspace --client-id 123456789012.1234567890123 --cloudflared
# You'll be prompted for the client secret (hidden)
# A manifest YAML is generated, saved, and copied to clipboard
```

4. Paste the generated YAML into Slack:
   - In your Slack app settings, open "App Manifest"
   - Paste the generated YAML (from clipboard or `~/.config/slack-rs/<profile>_manifest.yml`)
   - Apply the changes
5. Return to the terminal and press Enter:
   - The CLI opens your browser
   - Click "Allow"
   - The CLI exchanges the code for tokens and saves them securely

Scope flags:

- `--bot-scopes <scopes>`: comma-separated list or `all`
- `--user-scopes <scopes>`: comma-separated list or `all`

Common scopes:

- `chat:write` - post messages
- `users:read` - view users
- `channels:read` - list public channels
- `files:read` - access files
- `search:read` - search workspace content
- `reactions:write` - add/remove reactions

Full list: https://api.slack.com/scopes

#### Manual Setup (Alternative)

If you prefer manual configuration:

1. Go to https://api.slack.com/apps and create an app
2. In "OAuth & Permissions", add redirect URL: `http://127.0.0.1:8765/callback`
3. Add required scopes under "User Token Scopes"
4. Copy client ID and client secret from "Basic Information" -> "App Credentials"

#### Providing Credentials

Option A: save OAuth config to a profile (recommended for most users):

```bash
slack-rs config oauth set my-workspace \
  --client-id 123456789012.1234567890123 \
  --redirect-uri http://127.0.0.1:8765/callback \
  --scopes "chat:write,users:read,channels:read"

slack-rs auth login my-workspace
```

Option B: provide during login (one-time use):

```bash
slack-rs auth login my-workspace --client-id 123456789012.1234567890123
```

Option C: interactive prompts:

```bash
slack-rs auth login my-workspace
```

### 2. Authenticate

During login, the CLI opens a browser for OAuth authorization and stores:

- Profile metadata in `~/.config/slack-rs/profiles.json`
- Access tokens and client secrets in the OS keyring

Remote/SSH environments: the recommended flow is `slack-rs auth login ... --cloudflared`.

ngrok status: the `--ngrok` flag exists in the CLI help, but ngrok tunnel automation is not implemented in v0.1.6.

### 3. Verify Authentication

Check auth status:

```bash
slack-rs auth status my-workspace
```

List all profiles:

```bash
slack-rs auth list
```

## Usage with AI Agents

Once the skill is loaded, the agent can:

- Call any Slack Web API method
- Manage multiple workspace profiles
- Search messages, users, and channels
- Post messages and upload files
- Manage channels and conversations

Example agent prompts:

```
"Search for messages containing 'deployment' in the #engineering channel"
"Post a message to #general saying the build is complete"
"List all public channels in my workspace"
"Get information about user U123456"
```

The agent will use `slack-rs api call` commands under the hood.

## Configuration

### Environment Variables

Only the following environment variables are supported by the current implementation. OAuth client credentials are configured via `slack-rs config oauth set` (not environment variables).

| Variable | Description | Default | Use Case |
|----------|-------------|---------|----------|
| `SLACKCLI_ALLOW_WRITE` | Control write operations (post/update/delete messages). Values: `true`, `1`, `yes` (allow) or `false`, `0`, `no` (deny) | `true` | Safety in production environments |
| `SLACKRS_KEYRING_PASSWORD` | Passphrase for encrypting/decrypting export files. Alternative to `--passphrase-prompt`. | - | Automated backup/restore |
| `SLACK_OAUTH_BASE_URL` | Custom OAuth base URL for testing or private Slack installations. | `https://slack.com` | Testing, enterprise Slack |

### Write Operation Protection

Write operations are controlled by `SLACKCLI_ALLOW_WRITE`:

```bash
export SLACKCLI_ALLOW_WRITE=false
slack-rs api call chat.postMessage channel=C123456 text="Hello"  # denied

export SLACKCLI_ALLOW_WRITE=true
slack-rs api call chat.postMessage channel=C123456 text="Hello"  # allowed
```

## API Examples

Generic API calls (the agent will use these patterns):

```bash
# Get user information
slack-rs api call users.info user=U123456

# List conversations
slack-rs api call conversations.list limit=200

# Get channel history
slack-rs api call conversations.history channel=C123456 limit=50

# Post a message
slack-rs api call chat.postMessage channel=C123456 text="Hello from slack-rs"

# Search messages
slack-rs api call search.messages query="deployment" count=50
```

For more recipes, see `references/recipes.md` in the slack-rs repository.

## Safety Features

### Write Protection

For safety in production environments, control write operations with:

```bash
export SLACKCLI_ALLOW_WRITE=false  # Deny all write operations
```

Re-enable when needed:

```bash
export SLACKCLI_ALLOW_WRITE=true  # Allow write operations (default)
```

## Troubleshooting

- **Keyring errors**: Consult the upstream repo's `KEYRING_FIX.md`
- **Remote/SSH environments**: Use `--cloudflared` flag during login, or set up a tunnel (ngrok) and configure redirect URI accordingly
- **Token expiration**: Run `slack-rs auth status <profile>` to check; re-login with `slack-rs auth login <profile>` if needed

## Links

- **slack-rs CLI tool**: https://github.com/tumf/slack-rs
- **Slack Web API**: https://api.slack.com/web
- **AgentSkills format**: https://agentskills.io/

## License

MIT - See LICENSE file in the slack-rs repository
