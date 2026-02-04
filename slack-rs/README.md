# slack-rs

Slack Web API automation via the `slack-rs` CLI (Rust): multi-account OAuth (PKCE), secure keyring storage, generic Slack Web API calls, and convenient profile management.

## Install

```bash
git clone https://github.com/tumf/slack-rs.git
cd slack-rs
cargo build --release
./target/release/slack-rs --help
```

## Quick Start

1. Create a Slack app: https://api.slack.com/apps
2. Add redirect URL: `http://127.0.0.1:8765/callback`
3. Set OAuth config:

```bash
slack-rs config oauth set my-workspace \
  --client-id 123456789012.1234567890123 \
  --redirect-uri http://127.0.0.1:8765/callback \
  --scopes "chat:write,users:read,channels:read"
```

4. Login:

```bash
slack-rs auth login my-workspace
```

5. Call Slack Web API:

```bash
slack-rs api call conversations.list limit=200
slack-rs api call chat.postMessage channel=C123456 text="Hello"
```

## Safety

Disable writes by default:

```bash
export SLACKCLI_ALLOW_WRITE=false
```

## Recipes

See `slack-rs/references/recipes.md`.

## Links

- Upstream: https://github.com/tumf/slack-rs
- Slack Web API: https://api.slack.com/web
