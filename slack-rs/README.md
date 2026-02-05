# slack-rs (skill)

Agent skill for Slack Web API automation using the `slack-rs` CLI.

This directory contains the *skill* documentation. The `slack-rs` CLI is a separate project with its own README.

slack-rs CLI repository:

- https://github.com/tumf/slack-rs

## What You Get

- A skill file (`SKILL.md`) that teaches an agent how to use `slack-rs`
- A set of usage patterns and safety notes (no bundled scripts/binaries)

## Install the skill

Recommended:

```bash
npx skills add tumf/skills --skill slack-rs
```

Alternative: load the skill file directly in your agent config:

```jsonc
{
  "instructions": [
    "path/to/slack-rs/SKILL.md"
  ]
}
```

## Prerequisites

You must install the `slack-rs` CLI on the machine where the agent runs.

Verify:

```bash
slack-rs --version
```

Recommended: use slack-rs v0.1.32+.

## Using The Skill

Once the skill is loaded, the agent will use the `slack-rs` CLI under the hood.

In slack-rs v0.1.32+, prefer the convenience commands when possible:

```bash
slack-rs conv list
slack-rs conv search <pattern>
slack-rs conv history <channel_id>
```

For anything else, use the generic method runner:

```bash
slack-rs api call <method> [params...]
```

### Token Store (Keyring vs File)

By default, slack-rs uses the OS keyring/keychain. In CI/containers or environments without a working keyring, use the file backend:

```bash
export SLACKRS_TOKEN_STORE=file
```

Note: `~/.config/slack-rs/tokens.json` contains OAuth tokens/secrets. Treat it as a secret.

### Bot vs User Token

If your app has both bot and user tokens, select the default token type per profile:

```bash
slack-rs config set <profile> --token-type user
slack-rs config set <profile> --token-type bot
```

Confirm:

```bash
slack-rs auth status <profile>
```

Examples:

```text
List public channels in my workspace
Search for messages containing "deployment" in #engineering
Post "build is complete" to #general
```

More recipes:

- `slack-rs/references/recipes.md`
