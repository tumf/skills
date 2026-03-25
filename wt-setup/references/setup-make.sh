#!/usr/bin/env bash
set -euo pipefail

# --- Prerequisites ---
if ! command -v make >/dev/null 2>&1; then
  echo "error: make not found" >&2
  exit 1
fi

# --- Bootstrap ---
make setup

# --- Git hooks (worktrees don't inherit hooks from the base repo) ---
if [ -f ".pre-commit-config.yaml" ] && command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
elif [ -n "${ROOT_WORKTREE_PATH:-}" ] && [ -d "${ROOT_WORKTREE_PATH}/.git/hooks" ]; then
  git config core.hooksPath "${ROOT_WORKTREE_PATH}/.git/hooks"
fi
