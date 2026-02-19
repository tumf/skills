# openclaw-agent-creator

Create and maintain OpenClaw agent workspaces (bootstrap files + memory layout).

## What this skill is for

Use this skill when you want to:

- Create a new OpenClaw workspace (or an additional profile workspace)
- Seed bootstrap files with a clean separation of concerns
- Adopt a durable, file-based memory system (daily logs + curated long-term memory)
- Back up a workspace with git without committing secrets

This skill is based on the "Memory as Documentation" approach: memory and behavior live in editable Markdown files.

## Workspace layout (recommended)

OpenClaw expects a workspace directory (default: `~/.openclaw/workspace`). A practical minimal layout:

```
<workspace>/
  AGENTS.md
  SOUL.md
  USER.md
  IDENTITY.md
  TOOLS.md
  MEMORY.md            # optional
  memory/
    YYYY-MM-DD.md
```

Tip: if you want multiple workspaces, prefer profiles.

- Set `OPENCLAW_PROFILE=myprofile` when launching OpenClaw.
- The default workspace becomes `~/.openclaw/workspace-myprofile`.

If OpenClaw is installed, `openclaw setup --workspace <path>` can seed missing defaults without overwriting existing files.

## Bootstrap file responsibilities

- `IDENTITY.md`: who the agent is (stable metadata)
- `SOUL.md`: how the agent behaves (values, boundaries)
- `USER.md`: who the user is + preferences
- `AGENTS.md`: workflow, safety bar, and memory policy
- `TOOLS.md`: local environment notes and dangerous command guardrails (guidance only)

Memory:

- `memory/YYYY-MM-DD.md`: daily log (append-only)
- `MEMORY.md`: curated long-term memory (keep it small)

## Scripts

All scripts print JSON to stdout.

### Initialize a workspace

```bash
python3 "$SKILL_ROOT/scripts/init_workspace.py" \
  --workspace "$HOME/.openclaw/workspace-myprofile" \
  --agent-name "Claw" \
  --agent-vibe "sharp, concise, helpful" \
  --agent-emoji ":lobster:" \
  --user-name "tumf" \
  --user-language "Japanese" \
  --create-today-log
```

By default, the script also creates a starter `.gitignore` to reduce the chance of committing secrets.
Disable with `--no-gitignore`.

### Promote KEEP lines into long-term memory

```bash
python3 "$SKILL_ROOT/scripts/promote_keep.py" \
  --daily "$HOME/.openclaw/workspace/memory/2026-02-19.md" \
  --memory "$HOME/.openclaw/workspace/MEMORY.md"
```

## Notes

- Do not commit secrets to the workspace.
- Keep bootstrap files short; large files may be truncated when injected into context.
