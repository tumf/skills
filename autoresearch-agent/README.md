# autoresearch-agent

Delegate autoresearch tasks to a headless Claude Code sub-agent process.

Use when the current agent needs to run any autoresearch command (ship, plan, security, debug, fix, scenario, predict, learn) as an autonomous background or foreground subprocess.

## Install

```bash
npx skills add tumf/skills --skill autoresearch-agent
```

## Prerequisites

- `claude` CLI in PATH (or set `CLAUDE_BIN`)
- The [autoresearch](https://github.com/anthropics/claude-code/tree/main/.agent/skills/autoresearch) skill installed in the target project or globally

## Usage

```bash
# Foreground (blocks until done)
scripts/autoresearch ship --auto

# Background via agent-exec (preferred for long runs)
agent-exec run --timeout 3600000 -- scripts/autoresearch fix --guard "npm test"

# Dry-run — verify command before launch
scripts/autoresearch -n ship --auto
```

## Environment variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CLAUDE_BIN` | Path to claude binary | `claude` |
| `CLAUDE_EXTRA_ARGS` | Extra flags for claude | (empty) |
| `AUTORESEARCH_DRY_RUN` | Set `1` to print without executing | `0` |

See [SKILL.md](./SKILL.md) for full workflow documentation and [references/subcommands.md](./references/subcommands.md) for the complete subcommand reference.
