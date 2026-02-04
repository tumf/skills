# slack-rs recipes

All examples assume you already authenticated (see `slack-rs auth status`).

## Identify Channels

List channels (public conversations):

```bash
slack-rs api call conversations.list limit=200
```

If you need private channels, ensure your app has appropriate scopes and use the Slack API method options supported by your workspace.

## Read Messages

Fetch recent history for a channel:

```bash
slack-rs api call conversations.history channel=C123456 limit=50
```

## Post a Message

Recommended: set write guard explicitly in shells where you might run commands accidentally.

```bash
export SLACKCLI_ALLOW_WRITE=true
slack-rs api call chat.postMessage channel=C123456 text="Hello from slack-rs"
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
