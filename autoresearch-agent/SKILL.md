---
name: autoresearch-agent
description: >
  Delegate autoresearch tasks to a headless Claude Code sub-agent process.
  Use when the current agent needs to run any autoresearch command
  (autoresearch, ship, plan, security, debug, fix, scenario, predict, learn)
  as an autonomous background or foreground subprocess via `claude --dangerously-skip-permissions -p`.
  Ideal for long-running autonomous loops, overnight improvement runs,
  CI/CD pipeline integration, and fire-and-forget shipping workflows.
  Triggers on: "run autoresearch in background", "headless autoresearch",
  "delegate autoresearch", "spawn autoresearch", "autoresearch sub-agent",
  "autoresearch agent", or any request to run autoresearch non-interactively.
---

# autoresearch-agent

Spawn autoresearch as a headless Claude Code subprocess. The wrapper script
`scripts/autoresearch` translates CLI subcommands into
`claude --dangerously-skip-permissions -p "/autoresearch:<sub> <flags>"`.

## Prerequisites

- `claude` CLI in PATH (or set `CLAUDE_BIN`)
- The autoresearch skill installed in the target project or globally
  (`~/.claude/skills/autoresearch/`)

## Quick reference

```bash
# Foreground (blocks until done)
scripts/autoresearch ship --auto

# Background via agent-exec (preferred for long runs)
agent-exec run --timeout 3600000 -- scripts/autoresearch fix --guard "npm test"
```

## Execution modes

### 1. Foreground — short tasks (<5 min)

Run directly when the result is needed immediately:

```bash
scripts/autoresearch ship --checklist-only
scripts/autoresearch plan "Reduce bundle size"
```

### 2. Background via agent-exec — long tasks (>5 min)

If `agent-exec` is available, prefer it for any run that may exceed 5 minutes.
This keeps the calling agent responsive.

```bash
# Launch
agent-exec run \
  --cwd "$(pwd)" \
  --timeout 7200000 \
  -- scripts/autoresearch security --fail-on critical

# Check progress
agent-exec status <JOB_ID>
agent-exec tail --tail-lines 50 <JOB_ID>

# Wait for completion
agent-exec wait <JOB_ID>
```

Add `--notify-file results.ndjson` to get a completion event written when done.

### 3. Dry-run — verify command before launch

```bash
scripts/autoresearch -n ship --auto
# prints: + claude --dangerously-skip-permissions -p '/autoresearch:ship --auto'
```

## Workflow

1. **Determine subcommand and flags** from the user request
2. **Check estimated duration** — short (<5 min) → foreground; long → agent-exec
3. **Verify prerequisites** — `which claude`, skill installed
4. **Launch** — foreground exec or `agent-exec run`
5. **Monitor** (background only) — `agent-exec tail` / `status`
6. **Report results** back to the user

## Subcommands

See `references/subcommands.md` for the full subcommand table with flags.

| Subcommand | Typical duration | Recommended mode |
|------------|-----------------|------------------|
| `ship --auto` | 2-10 min | foreground |
| `ship --checklist-only` | <1 min | foreground |
| `plan` | 1-3 min | foreground |
| `security` | 10-60 min | agent-exec |
| `debug` | 10-60 min | agent-exec |
| `fix` | 5-30 min | agent-exec |
| `scenario` | 5-30 min | agent-exec |
| `predict` | 3-10 min | foreground or agent-exec |
| `learn` | 5-30 min | agent-exec |
| (base loop) | unbounded | agent-exec with `--timeout` |

## Environment variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CLAUDE_BIN` | Path to claude binary | `claude` |
| `CLAUDE_EXTRA_ARGS` | Extra flags for claude (e.g. `--model sonnet`) | (empty) |
| `AUTORESEARCH_DRY_RUN` | Set `1` to print command without executing | `0` |

## Error handling

- If `claude` is not found, the script exits with a clear error message.
- If the autoresearch skill is not installed, claude will report an unknown command.
  Fix: install the skill per the autoresearch README.
- If agent-exec is unavailable, fall back to direct foreground execution
  and warn the user that long runs will block.

## Examples

```bash
# Ship a PR headlessly
scripts/autoresearch ship --auto

# Run 25 iterations of test coverage improvement in background
agent-exec run --timeout 3600000 \
  -- scripts/autoresearch "Goal: coverage to 90%" --iterations 25

# Security audit with CI gate
agent-exec run --timeout 7200000 \
  -- scripts/autoresearch security --fail-on critical --iterations 15

# Debug then fix pipeline
agent-exec run --timeout 1800000 \
  -- scripts/autoresearch debug --scope "src/**/*.ts" --iterations 10
# ... after completion:
agent-exec run --timeout 1800000 \
  -- scripts/autoresearch fix --from-debug --iterations 20
```
