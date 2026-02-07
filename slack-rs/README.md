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

This skill assumes recent versions of `slack-rs` (v0.1.40+). Verify your installation:

```bash
slack-rs --version
slack-rs --help  # Check available commands and flags
```

Tip: `slack-rs` supports machine-readable introspection via `commands --json`, `<cmd> --help --json`, and `schema --command <cmd> --output json-schema`.

## Using The Skill

Once the skill is loaded, the agent will use the `slack-rs` CLI under the hood, typically via `slack-rs api call`.

Examples:

```text
List public channels in my workspace
Search for messages containing "deployment" in #engineering
Post "build is complete" to #general
```

More recipes:

- `slack-rs/references/recipes.md`
