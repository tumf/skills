#!/usr/bin/env bash
set -euo pipefail

# --- Detect package manager ---
if [ -f "pnpm-lock.yaml" ]; then
  pnpm install --frozen-lockfile
elif [ -f "yarn.lock" ]; then
  yarn install --frozen-lockfile
elif [ -f "package-lock.json" ]; then
  npm ci
else
  npm install
fi

# --- Environment ---
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
  cp .env.example .env
  echo "info: created .env from .env.example -- edit as needed"
fi

# --- Git hooks (worktrees don't inherit hooks from the base repo) ---
if [ -f ".pre-commit-config.yaml" ] && command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
elif [ -f ".husky/install.mjs" ] || [ -d ".husky/_" ]; then
  npx husky install 2>/dev/null || true
elif [ -n "${ROOT_WORKTREE_PATH:-}" ] && [ -d "${ROOT_WORKTREE_PATH}/.git/hooks" ]; then
  git config core.hooksPath "${ROOT_WORKTREE_PATH}/.git/hooks"
fi
