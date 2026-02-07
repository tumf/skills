# slack-rs (skill)

Agent skill for Slack Web API automation using the `slack-rs` CLI.

This directory contains the skill documentation only (no bundled scripts/binaries). The `slack-rs` CLI is a separate project:

- https://github.com/tumf/slack-rs

## What You Get

- `slack-rs/SKILL.md`: agent instructions for using `slack-rs`
- `slack-rs/references/recipes.md`: copy/paste recipes

## Install The Skill

Recommended:

```bash
npx skills add tumf/skills --skill slack-rs
```

Alternative: load the skill file directly in your agent config:

```jsonc
{
  "instructions": ["path/to/slack-rs/SKILL.md"]
}
```

## Prerequisites

Install the `slack-rs` CLI on the machine where the agent runs.

This skill assumes recent versions of `slack-rs` (v0.1.40+):

```bash
slack-rs --version
slack-rs --help
```

Tip: `slack-rs` supports machine-readable introspection:

```bash
slack-rs commands --json
slack-rs conv list --help --json
slack-rs schema --command msg.post --output json-schema
```

## Using The Skill

Once the skill is loaded, the agent will run `slack-rs` commands directly.

Prefer convenience commands when possible:

```bash
slack-rs conv list
slack-rs conv search <pattern>
slack-rs conv history <channel_id>

slack-rs msg post <channel_id> "Hello"
```

For anything else, use the generic method runner:

```bash
slack-rs api call <method> [params...]
```

## Credentials And Storage

`slack-rs` stores profiles, OAuth config, and tokens under `~/.config/slack-rs/`. Treat this directory as a secret.

For backup/migration, refer to:

```bash
slack-rs auth export --help
slack-rs auth import --help
```

## Write Safety Guard

Many Slack methods write data (posting, updating, deleting, reactions). In automation shells, set:

```bash
export SLACKCLI_ALLOW_WRITE=false
```

Enable writes only when you intend to change Slack:

```bash
export SLACKCLI_ALLOW_WRITE=true
```
