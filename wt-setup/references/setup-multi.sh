#!/usr/bin/env bash
set -euo pipefail

# --- Prerequisites ---
for cmd in make git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "error: $cmd not found" >&2
    exit 1
  fi
done

# --- Bootstrap ---
make setup

# --- Git hooks (worktrees don't inherit hooks from the base repo) ---
if [ -f ".pre-commit-config.yaml" ] && command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
elif [ -n "${ROOT_WORKTREE_PATH:-}" ] && [ -d "${ROOT_WORKTREE_PATH}/.git/hooks" ]; then
  git config core.hooksPath "${ROOT_WORKTREE_PATH}/.git/hooks"
fi

# --- Local overrides (from ROOT repo -- .local is gitignored) ---
_local="${ROOT_WORKTREE_PATH:-.}/.wt/setup.local"
if [ -f "$_local" ]; then
  # shellcheck source=/dev/null
  source "$_local"
fi
