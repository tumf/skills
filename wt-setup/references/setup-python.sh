#!/usr/bin/env bash
set -euo pipefail

# --- Prerequisites ---
if ! command -v uv >/dev/null 2>&1; then
  echo "error: uv not found -- install from https://docs.astral.sh/uv/" >&2
  exit 1
fi

# --- Bootstrap ---
uv sync

# --- Git hooks (worktrees don't inherit hooks from the base repo) ---
if [ -f ".pre-commit-config.yaml" ] && command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
elif [ -n "${ROOT_WORKTREE_PATH:-}" ] && [ -d "${ROOT_WORKTREE_PATH}/.git/hooks" ]; then
  git config core.hooksPath "${ROOT_WORKTREE_PATH}/.git/hooks"
fi
