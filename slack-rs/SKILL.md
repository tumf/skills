---
name: slack-rs
description: |
  Slack Web API automation via the slack-rs CLI (Rust). Use when you need to authenticate to Slack via OAuth (PKCE), manage multiple workspace profiles securely, call arbitrary Slack Web API methods (e.g. chat.postMessage, conversations.list, users.info), or run safe scripted Slack operations from the terminal. Includes profile export/import (encrypted) and write-safety guard via SLACKCLI_ALLOW_WRITE.
---

# slack-rs - Slack Web API CLI (Rust)

Use `slack-rs` to interact with Slack workspaces using your own OAuth credentials. It supports multiple profiles (workspaces/apps), stores sensitive secrets in the OS keyring, and can call any Slack Web API method.

## Install

Build from source:

```bash
git clone https://github.com/tumf/slack-rs.git
cd slack-rs
cargo build --release
./target/release/slack-rs --help
```

Or install from a local checkout:

```bash
cargo install --path .
```

## OAuth Setup (One-time per Slack App)

Create a Slack app and configure OAuth:

1. Go to https://api.slack.com/apps and create an app.
2. Under "OAuth & Permissions" add Redirect URL:

   - `http://127.0.0.1:8765/callback`

3. Add required "User Token Scopes" for your use case.
4. Copy your Client ID and Client Secret.

Recommended: store OAuth config per profile (client secret is stored in keyring).

```bash
slack-rs config oauth set my-workspace \
  --client-id 123456789012.1234567890123 \
  --redirect-uri http://127.0.0.1:8765/callback \
  --scopes "chat:write,users:read,channels:read"
```

If supported by your version, use `--scopes "all"` for a broad preset.

## Authenticate (Per profile)

```bash
slack-rs auth login my-workspace
slack-rs auth status my-workspace
slack-rs auth list
```

During login, the CLI opens a browser for OAuth authorization and stores:

- Profile metadata in `~/.config/slack-rs/profiles.json`
- Access tokens and client secrets in the OS keyring

## Make API Calls

Use generic API calls for anything supported by Slack Web API:

```bash
slack-rs api call users.info user=U123456
slack-rs api call conversations.list limit=200
slack-rs api call conversations.history channel=C123456 limit=50
slack-rs api call chat.postMessage channel=C123456 text="Hello from slack-rs"
```

For more copy/pasteable recipes, see `slack-rs/references/recipes.md`.

## Safe Defaults for Write Operations

Many Slack methods are write operations (posting, updating, deleting, reactions). Use the guard in environments where writes are risky:

```bash
export SLACKCLI_ALLOW_WRITE=false
```

Re-enable explicitly when you intend to write:

```bash
export SLACKCLI_ALLOW_WRITE=true
```

## Profile Backup / Migration

Export/import profiles using encrypted files (treat as secrets):

```bash
# Prompt for passphrase (recommended)
slack-rs auth export --all --out all-profiles.enc --passphrase-prompt
slack-rs auth import --all --in all-profiles.enc --passphrase-prompt
```

Non-interactive automation:

```bash
export SLACKRS_KEYRING_PASSWORD="strong-passphrase"
slack-rs auth export --profile my-workspace --out backup.enc --yes
slack-rs auth import --profile my-workspace --in backup.enc
```

## Troubleshooting

- Keyring errors: consult the upstream repo's `KEYRING_FIX.md`.
- Remote environments: use a tunnel (ngrok/cloudflared) and set your profile redirect URI accordingly.
