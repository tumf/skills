#!/usr/bin/env python3
"""Initialize an OpenClaw workspace with bootstrap files.

This script creates a workspace directory and seeds common OpenClaw bootstrap files:
AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md, MEMORY.md (optional), and memory/YYYY-MM-DD.md.

All output is JSON on stdout.

Examples:
  python3 init_workspace.py \
    --workspace "$HOME/.openclaw/workspace-myprofile" \
    --agent-name "Claw" \
    --agent-vibe "sharp, concise, helpful" \
    --agent-emoji ":lobster:" \
    --user-name "tumf" \
    --user-language "Japanese" \
    --create-today-log
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class InitResult:
    workspace: str
    created_dirs: list[str]
    created_files: list[str]
    skipped_files: list[str]


def _write_file(path: Path, content: str, *, overwrite: bool) -> tuple[bool, str]:
    """Write content to path.

    Returns:
      (created_or_overwritten, status)
        status is one of: created, overwritten, skipped
    """
    if path.exists() and not overwrite:
        return False, "skipped"

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and overwrite:
        path.write_text(content, encoding="utf-8")
        return True, "overwritten"

    path.write_text(content, encoding="utf-8")
    return True, "created"


def _agents_md() -> str:
    return """# Operating Instructions

## Workflow

1. Investigate: understand current state before proposing changes.
2. Propose: explain the plan and tradeoffs before executing.
3. Execute: make the change carefully, keeping scope small.
4. Verify: report results and provide next steps.

## Memory Policy

- Durable decisions, constraints, and lessons go to MEMORY.md.
- Daily running context goes to memory/YYYY-MM-DD.md.
- If the user says "remember this", write it down (do not keep it in RAM).

## Safety Bar

- Treat destructive operations as risky (deletes, overwrites, force pushes).
- Prefer dry-runs and explicit confirmations for irreversible actions.
"""


def _soul_md() -> str:
    return """# Core Values

- Prefer simple solutions over complex ones.
- Ask clarifying questions when assumptions would change the outcome.
- Optimize for safety and reversibility.

# Boundaries

- Do not modify production systems without explicit user instruction.
- Do not store secrets in the workspace.
- In shared/group contexts, do not output private information.
"""


def _user_md(user_name: str, user_language: str) -> str:
    user_name = user_name.strip() or "(unknown)"
    user_language = user_language.strip() or "(unspecified)"
    return f"""# User Profile

- Name: {user_name}
- Language: {user_language} (code/commands can be English)

# Output Preferences

- Keep responses concise and actionable.
- Use checklists for multi-step tasks.
"""


def _identity_md(agent_name: str, agent_vibe: str, agent_emoji: str) -> str:
    agent_name = agent_name.strip() or "Claw"
    agent_vibe = agent_vibe.strip() or "sharp, concise, helpful"
    agent_emoji = agent_emoji.strip() or ":lobster:"
    return f"""- **Name:** {agent_name}
- **Creature:** AI assistant
- **Vibe:** {agent_vibe}
- **Emoji:** {agent_emoji}
- **Avatar:** (optional) avatars/<file>
"""


def _tools_md() -> str:
    shell = os.environ.get("SHELL", "(unknown)")
    return f"""# Local Environment

- OS: (fill in)
- Shell: {shell}

# Dangerous Commands

Ask for confirmation before running:

- `rm -rf` (recursive delete)
- `git push --force` (force push)
- `docker system prune` (delete unused Docker data)

# Notes

- This file is guidance only. It does not define which tools exist.
"""


def _gitignore() -> str:
    return """# OpenClaw workspace

# OS
.DS_Store

# Secrets (never commit)
.env
**/*.key
**/*.pem
**/secrets*
**/*credential*

# Optional: editor/tooling
.vscode/
.idea/
"""


def _memory_md() -> str:
    return """# Long-term Memory

## Decisions

- (date): (decision) - (why)

## Lessons

- (lesson)

## Durable Facts

- (fact)
"""


def _daily_md(today: date) -> str:
    return f"""# {today.isoformat()}

## Log

- (notes)

## KEEP

- KEEP: (durable note to promote into MEMORY.md)
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize an OpenClaw workspace with bootstrap files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s --workspace ~/.openclaw/workspace-myprofile --agent-name Claw --create-today-log
  %(prog)s --workspace ./workspace --overwrite
""",
    )
    parser.add_argument(
        "--workspace",
        required=True,
        help="Workspace directory to create/seed",
    )
    parser.add_argument(
        "--agent-name", default="Claw", help="Agent name for IDENTITY.md"
    )
    parser.add_argument(
        "--agent-vibe",
        default="sharp, concise, helpful",
        help="Agent vibe for IDENTITY.md",
    )
    parser.add_argument(
        "--agent-emoji",
        default=":lobster:",
        help="Agent emoji for IDENTITY.md (ASCII is fine, e.g. :lobster:)",
    )
    parser.add_argument("--user-name", default="", help="User name for USER.md")
    parser.add_argument("--user-language", default="", help="User language for USER.md")
    parser.add_argument(
        "--with-memory",
        action="store_true",
        help="Create MEMORY.md if missing",
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Do not create .gitignore (default: create if missing)",
    )
    parser.add_argument(
        "--create-today-log",
        action="store_true",
        help="Create memory/YYYY-MM-DD.md for today if missing",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files (default: never overwrite)",
    )

    args = parser.parse_args()

    try:
        workspace = Path(os.path.expanduser(args.workspace)).resolve()

        created_dirs: list[str] = []
        created_files: list[str] = []
        skipped_files: list[str] = []

        if not workspace.exists():
            workspace.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(workspace))

        files: dict[str, str] = {
            "AGENTS.md": _agents_md(),
            "SOUL.md": _soul_md(),
            "USER.md": _user_md(args.user_name, args.user_language),
            "IDENTITY.md": _identity_md(
                args.agent_name, args.agent_vibe, args.agent_emoji
            ),
            "TOOLS.md": _tools_md(),
        }
        if args.with_memory:
            files["MEMORY.md"] = _memory_md()

        for rel, content in files.items():
            p = workspace / rel
            wrote, status = _write_file(p, content, overwrite=args.overwrite)
            if status in {"created", "overwritten"}:
                created_files.append(str(p))
            else:
                skipped_files.append(str(p))

        if not args.no_gitignore:
            p = workspace / ".gitignore"
            wrote, status = _write_file(p, _gitignore(), overwrite=args.overwrite)
            if status in {"created", "overwritten"}:
                created_files.append(str(p))
            else:
                skipped_files.append(str(p))

        if args.create_today_log:
            mem_dir = workspace / "memory"
            if not mem_dir.exists():
                mem_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(mem_dir))

            today = date.today()
            daily_path = mem_dir / f"{today.isoformat()}.md"
            wrote, status = _write_file(
                daily_path, _daily_md(today), overwrite=args.overwrite
            )
            if status in {"created", "overwritten"}:
                created_files.append(str(daily_path))
            else:
                skipped_files.append(str(daily_path))

        result = InitResult(
            workspace=str(workspace),
            created_dirs=created_dirs,
            created_files=created_files,
            skipped_files=skipped_files,
        )
        print(
            json.dumps(
                {
                    "success": True,
                    "result": {
                        "workspace": result.workspace,
                        "created_dirs": result.created_dirs,
                        "created_files": result.created_files,
                        "skipped_files": result.skipped_files,
                    },
                },
                indent=2,
                default=str,
            )
        )
        return 0
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
