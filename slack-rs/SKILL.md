---
name: slack-rs
description: |
  Slack Web API automation via the slack-rs CLI (Rust). Use when you need to authenticate to Slack via OAuth (PKCE), manage multiple workspace profiles securely, call arbitrary Slack Web API methods (e.g. chat.postMessage, conversations.list, users.info), and run safe scripted Slack operations from the terminal. Includes optional cloudflared-based remote login, encrypted profile export/import, and write-safety guard via SLACKCLI_ALLOW_WRITE.
---

# slack-rs - Slack Web API CLI (Rust)

Use `slack-rs` to interact with Slack workspaces using your own OAuth credentials. It supports multiple profiles (workspaces/apps), stores sensitive secrets in the OS keyring, and can call any Slack Web API method.

## Install

Install from crates.io (recommended):

```bash
cargo install slack-rs
```

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

Create a Slack app and configure OAuth.

Recommended login flow (especially for remote/SSH environments): use `--cloudflared`.
In this mode, `slack-rs auth login` generates a Slack App Manifest YAML for you (and copies it to clipboard, best effort).

1. Go to https://api.slack.com/apps and create an app.
2. Copy your Client ID and Client Secret from "Basic Information" -> "App Credentials".
3. Either:

   - Use the manifest flow (`--cloudflared`) and paste the generated YAML into Slack, or
   - Configure OAuth manually (alternative):

     - Under "OAuth & Permissions", add redirect URL: `http://127.0.0.1:8765/callback`
     - Add required "User Token Scopes" for your use case

Recommended: store OAuth config per profile (client secret is stored in keyring).

```bash
slack-rs config oauth set my-workspace \
  --client-id 123456789012.1234567890123 \
  --redirect-uri http://127.0.0.1:8765/callback \
  --scopes "chat:write,users:read,channels:read"
```

If supported by your version, use `--scopes "all"` for a broad preset.

Common scopes:

- `chat:write` - post messages
- `users:read` - view users
- `channels:read` - list public channels
- `search:read` - search workspace content
- `reactions:write` - add/remove reactions

Full list: https://api.slack.com/scopes

## Authenticate (Per profile)

```bash
slack-rs auth login my-workspace
slack-rs auth status my-workspace
slack-rs auth list
```

Remote/SSH environments (recommended):

```bash
slack-rs auth login my-workspace --client-id 123456789012.1234567890123 --cloudflared
```

Note: the `--ngrok` flag exists in the CLI help, but ngrok tunnel automation is not implemented in v0.1.6.

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

## Configuration

Only the following environment variables are supported by the current implementation:

- `SLACKCLI_ALLOW_WRITE`: allow/deny write operations (default: allowed)
- `SLACKRS_KEYRING_PASSWORD`: passphrase for encrypting/decrypting export files (automation)
- `SLACK_OAUTH_BASE_URL`: custom OAuth base URL (testing/enterprise Slack)

## Troubleshooting

- Keyring errors: consult the upstream repo's `KEYRING_FIX.md`.
- Remote environments: use a tunnel (ngrok/cloudflared) and set your profile redirect URI accordingly.

## Useful Commands

Profile management:

```bash
slack-rs auth list
slack-rs auth status <profile>
slack-rs auth rename <old> <new>
slack-rs auth logout <profile>
```

OAuth config management:

```bash
slack-rs config oauth show <profile>
slack-rs config oauth delete <profile>
```
