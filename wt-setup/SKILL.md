---
name: wt-setup
description: |
  Create and maintain `.wt/setup` bootstrap scripts for git worktree environments.
  The `.wt/setup` script is a repository-local convention executed automatically by
  supporting tools (e.g. wt) when creating new git worktrees. Use when: (1) a project
  needs a `.wt/setup` script, (2) setting up worktree-aware bootstrap for a new repo,
  (3) reviewing or fixing an existing `.wt/setup`, or (4) the user mentions "wt setup",
  "worktree setup", ".wt/setup", or "bootstrap worktree".
---

# wt-setup

Create and maintain `.wt/setup` scripts -- the standard bootstrap entrypoint
executed when a git worktree is created by a supporting tool.

## Background

The [wt](https://github.com/tumf/wt) tool (and other tools that follow the
`.wt/setup` convention) creates git worktrees under
`~/.wt/worktrees/<project>-<name>/`. When a worktree is created, the tool
looks for `.wt/setup` in the repository root and executes it inside the new
worktree directory.

## Convention

### Directory layout

```
.wt/
  AGENTS.md          # Documentation for agents about the .wt/ directory
  setup              # Bootstrap script (executable, committed)
  setup.local        # Local overrides (gitignored)
  worktrees/         # Symlinks to worktrees (gitignored, created by wt)
```

### Execution context

| Item | Value |
|------|-------|
| Working directory | The new worktree root |
| `ROOT_WORKTREE_PATH` | Path to the base repository (source tree) |
| Interpreter | `#!/usr/bin/env bash` (portable) |

### Design rules

1. **Idempotent** -- safe to run multiple times
2. **Non-interactive** -- no prompts; fail fast on missing prerequisites
3. **Fast** -- avoid slow network operations; cache where possible
4. **Portable** -- use `#!/usr/bin/env bash` and standard POSIX tools
5. **Repository-local only** -- tools MUST NOT read user-global setup scripts

## Creating a .wt/setup

### Step 1 -- Detect project type

Inspect the repository to determine what bootstrap actions are needed:

| Indicator | Action |
|-----------|--------|
| `Makefile` with `setup` target | `make setup` |
| `package.json` | `npm install` or `pnpm install` |
| `pyproject.toml` | `uv sync` or `pip install -e .` |
| `Cargo.toml` | `cargo fetch` |
| `go.mod` | `go mod download` |
| `Gemfile` | `bundle install` |
| `.envrc` | `direnv allow` (if available) |

### Step 2 -- Generate the script

Use the generator script or write manually:

```bash
# Using the generator
./wt-setup/scripts/generate.py

# Or manually
mkdir -p .wt
cat > .wt/setup << 'SETUP'
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
SETUP
chmod +x .wt/setup
```

### Step 3 -- Add .wt/setup.local support (optional)

`.wt/setup.local` is gitignored, so it does **not** exist in worktrees.
The script must reference the ROOT (source) repository via `ROOT_WORKTREE_PATH`.

Append to `.wt/setup`:

```bash
# --- Local overrides (from ROOT repo -- .local is gitignored) ---
_local="${ROOT_WORKTREE_PATH:-.}/.wt/setup.local"
if [ -f "$_local" ]; then
  # shellcheck source=/dev/null
  source "$_local"
fi
```

Ensure `.wt/setup.local` is in `.gitignore`.

### Step 4 -- Add AGENTS.md (recommended)

Copy the template to `.wt/AGENTS.md` so AI agents understand the directory:

```bash
cp wt-setup/references/AGENTS.md.template .wt/AGENTS.md
```

Or use the generator with `--agents-md` flag.
The template is at `references/AGENTS.md.template`.

### Step 5 -- Update .gitignore

Add these entries if not present:

```
.wt/setup.local
.wt/worktrees/
```

## Git hooks in worktrees

Worktrees do NOT inherit git hooks from the base repository.
If the base repo uses pre-commit hooks, `.wt/setup` SHOULD re-establish them.

The strategy (in priority order):

1. **pre-commit framework** -- if `.pre-commit-config.yaml` exists, run `pre-commit install`
2. **Husky (Node.js)** -- if `.husky/` exists, run `npx husky install`
3. **Fallback** -- point `core.hooksPath` to the base repo's hooks:
   `git config core.hooksPath "${ROOT_WORKTREE_PATH}/.git/hooks"`

All templates in `references/` include this logic.

## Templates

Template files are in `references/`. Copy one to `.wt/setup` and adjust as needed.

| File | Project type |
|------|-------------|
| `references/setup-make.sh` | Makefile with `setup` target |
| `references/setup-node.sh` | Node.js (npm / pnpm / yarn) |
| `references/setup-python.sh` | Python (uv) |
| `references/setup-rust.sh` | Rust (cargo) |
| `references/setup-multi.sh` | Multi-language / Makefile-first + local overrides |

Example:

```bash
cp wt-setup/references/setup-python.sh .wt/setup
chmod +x .wt/setup
```

## Validation checklist

After creating `.wt/setup`, verify:

- [ ] File is executable (`chmod +x .wt/setup`)
- [ ] Shebang is `#!/usr/bin/env bash`
- [ ] `set -euo pipefail` is present
- [ ] Prerequisite commands are checked before use
- [ ] Script is idempotent (safe to re-run)
- [ ] No interactive prompts
- [ ] `.wt/setup.local` is gitignored
- [ ] `.wt/worktrees/` is gitignored

## Reference

- wt tool: https://github.com/tumf/wt
- Git worktree docs: https://git-scm.com/docs/git-worktree
