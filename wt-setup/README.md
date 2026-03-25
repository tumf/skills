# wt-setup

Create and maintain `.wt/setup` bootstrap scripts for git worktree environments.

## Features

- Auto-detect project type and generate appropriate `.wt/setup` scripts
- Templates for Node.js, Python (uv), Rust, Go, and Makefile-first projects
- Support for `.wt/setup.local` local overrides
- `.wt/AGENTS.md` generation for AI agent awareness
- Idempotent, non-interactive, fast bootstrap convention

## Installation

### Prerequisites

- Python 3.10+
- git

### Setup

```bash
chmod +x wt-setup/scripts/generate.py
```

## Quick Start

```bash
# Run from a project root to generate .wt/setup
./wt-setup/scripts/generate.py
```

## Usage

### Generator Script

The `generate.py` script inspects the current directory and creates an
appropriate `.wt/setup` script.

```bash
# Generate with auto-detection
./wt-setup/scripts/generate.py

# Specify project type explicitly
./wt-setup/scripts/generate.py --type node

# Include AGENTS.md
./wt-setup/scripts/generate.py --agents-md

# Dry run (print to stdout without writing)
./wt-setup/scripts/generate.py --dry-run
```

### Supported Project Types

| Type | Detection | Bootstrap Command |
|------|-----------|-------------------|
| `make` | `Makefile` with `setup` target | `make setup` |
| `node` | `package.json` | `npm ci` / `pnpm install` / `yarn install` |
| `python` | `pyproject.toml` | `uv sync` / `pip install -e .` |
| `rust` | `Cargo.toml` | `cargo fetch` |
| `go` | `go.mod` | `go mod download` |
| `ruby` | `Gemfile` | `bundle install` |

### Manual Creation

If you prefer to write `.wt/setup` manually, follow these conventions:

1. Use `#!/usr/bin/env bash` shebang
2. Add `set -euo pipefail`
3. Check prerequisites with `command -v`
4. Keep it idempotent and non-interactive

## Examples

### Example 1: Auto-detect and generate

```bash
cd my-project
./path/to/wt-setup/scripts/generate.py
```

**Output:**

```json
{
  "success": true,
  "data": {
    "detected_type": "node",
    "package_manager": "pnpm",
    "files_created": [".wt/setup"],
    "files_modified": [".gitignore"]
  }
}
```

### Example 2: Generate with all extras

```bash
./wt-setup/scripts/generate.py --agents-md --dry-run
```

This previews all files that would be created without writing them.

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `WT_SETUP_TYPE` | Override auto-detection | (auto) |

## Tips & Best Practices

- Always check prerequisites before running commands
- Prefer `--frozen-lockfile` / `npm ci` for reproducible installs
- `.wt/setup.local` is gitignored and won't exist in worktrees -- source it
  via `ROOT_WORKTREE_PATH` (e.g. `"${ROOT_WORKTREE_PATH:-.}/.wt/setup.local"`)
- Keep `.wt/setup` fast -- avoid building the full project

## Troubleshooting

### `.wt/setup` is not executable

```bash
chmod +x .wt/setup
git update-index --chmod=+x .wt/setup
```

### Setup fails in worktree but works in main repo

Check that paths are relative, not absolute. Use `ROOT_WORKTREE_PATH`
environment variable to reference the base repository if needed.

### `.wt/setup.local` is committed by accident

Add it to `.gitignore` and remove from tracking:

```bash
echo ".wt/setup.local" >> .gitignore
git rm --cached .wt/setup.local
```

## License

MIT License
