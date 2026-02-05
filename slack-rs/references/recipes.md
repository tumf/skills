# slack-rs recipes

All examples assume you already authenticated (see `slack-rs auth status`).

These recipes are written for slack-rs v0.1.32+.

## Token Store (Keyring vs File)

By default, slack-rs uses the OS keyring/keychain.

If your environment does not have a working keyring (CI, containers, headless machines), use the file backend:

```bash
export SLACKRS_TOKEN_STORE=file
```

Security note: `~/.config/slack-rs/tokens.json` contains OAuth tokens/secrets. Treat it as a secret.

## Bot vs User Token

If your Slack app has both bot and user tokens, choose the default token type per profile:

```bash
slack-rs config set my-workspace --token-type user
slack-rs config set my-workspace --token-type bot
```

## Profile Management

List profiles:

```bash
slack-rs auth list
```

Show auth status for a profile:

```bash
slack-rs auth status my-workspace
```

Login (interactive / uses saved config when present):

```bash
slack-rs auth login my-workspace
```

Remote/SSH environments (recommended):

```bash
slack-rs auth login my-workspace --client-id 123456789012.1234567890123 --cloudflared
```

Rename a profile:

```bash
slack-rs auth rename old-name new-name
```

Logout (removes profile + deletes credentials from keyring):

```bash
slack-rs auth logout my-workspace
```

## OAuth Config (Per Profile)

Show saved OAuth config:

```bash
slack-rs config oauth show my-workspace
```

Set OAuth config (client secret is stored in keyring):

```bash
slack-rs config oauth set my-workspace \
  --client-id 123456789012.1234567890123 \
  --redirect-uri http://127.0.0.1:8765/callback \
  --scopes "chat:write,users:read,channels:read"
```

Delete OAuth config:

```bash
slack-rs config oauth delete my-workspace
```

## Identify Channels

List conversations (public + private depending on token/scopes):

Preferred (convenience command):

```bash
slack-rs conv list
```

Search conversations by name:

```bash
slack-rs conv search <pattern>
```

Raw API equivalent:

```bash
slack-rs api call conversations.list limit=200
```

If you need private channels, ensure your app has appropriate scopes and use the Slack API method options supported by your workspace.

## Read Messages

Fetch recent history for a channel:

Preferred:

```bash
slack-rs conv history C123456 limit=50
```

Raw API equivalent:

```bash
slack-rs api call conversations.history channel=C123456 limit=50
```

## Post a Message

Recommended: set write guard explicitly in shells where you might run commands accidentally.

```bash
export SLACKCLI_ALLOW_WRITE=true
slack-rs api call chat.postMessage channel=C123456 text="Hello from slack-rs"
```

Convenience command:

```bash
export SLACKCLI_ALLOW_WRITE=true
slack-rs msg post C123456 "Hello from slack-rs"
```

Disable writes by default:

```bash
export SLACKCLI_ALLOW_WRITE=false
```

Thread reply:

```bash
export SLACKCLI_ALLOW_WRITE=true
slack-rs api call chat.postMessage channel=C123456 thread_ts=1234567890.123 text="Reply in thread"
```

## User Lookup

Get info for a user ID:

```bash
slack-rs api call users.info user=U123456
```

Search by email (requires the right scopes):

```bash
slack-rs api call users.lookupByEmail email=user@example.com
```

## Search

Search messages (requires `search:read`):

```bash
slack-rs api call search.messages query="from:alice has:link" count=20
```

## Output Format

By default, slack-rs wraps responses in a unified envelope:

```json
{
  "meta": {"method": "...", "command": "...", "token_type": "..."},
  "response": {"ok": true, "...": "..."}
}
```

To get the raw Slack Web API response (without the envelope), use `--raw`:

```bash
slack-rs api call conversations.list --raw
```

## Profile Backup / Migration

Export/import profiles using encrypted files. Treat export files as secrets (they contain access tokens and may include client secrets).

Prompt for passphrase (recommended):

```bash
slack-rs auth export --profile my-workspace --out my-workspace.enc --passphrase-prompt
slack-rs auth import --profile my-workspace --in my-workspace.enc --passphrase-prompt
```

Export/import all profiles:

```bash
slack-rs auth export --all --out all-profiles.enc --passphrase-prompt
slack-rs auth import --all --in all-profiles.enc --passphrase-prompt
```

Non-interactive automation:

```bash
export SLACKRS_KEYRING_PASSWORD="strong-passphrase"
slack-rs auth export --profile my-workspace --out backup.enc --yes
slack-rs auth import --profile my-workspace --in backup.enc
```
