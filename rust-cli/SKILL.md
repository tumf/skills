---
name: rust-cli
description: |
  General guidance for building Rust CLI programs (clap/anyhow/tracing/serde_json), with
  agent-friendly patterns: JSON output mode, stdout/stderr separation, predictable exit codes,
  and a practical git-hooks setup using prek.
---

# rust-cli - Build Maintainable Rust CLIs

Use this skill when you need to design or implement a Rust CLI with production-grade ergonomics and automation.

## Defaults (Agent-Friendly)

- CLI parsing: `clap` derive.
- Error handling: `anyhow` (or `thiserror` for library-style errors).
- Logging/diagnostics: `tracing` + `tracing-subscriber` (write logs to stderr).
- Structured output: `serde` + `serde_json`.

## Help output

- `-h` and `--help` must display help text in English.
- Do not disable clap help flags; ensure `--help` works at every level (root command and each subcommand).
- If you have subcommands, set `about` and `long_about` (English) on the top-level command and each subcommand so `mycli sub --help` is meaningful.

## Command/Binary Naming

- Prefer a unique command name; check crates.io and common package managers.
- Avoid reserved/common names (and collisions with typical system commands).
- If the name is generic, consider a prefix (e.g., org/team) to reduce conflicts.

## Filesystem layout (XDG)

Assume `~/.config` is user-managed under git.

- Config files: `~/.config/{app_name}` (XDG: `$XDG_CONFIG_HOME/{app_name}`).
- Non-git-managed data (runtime/cache/state/artifacts): `~/.local/share/{app_name}` (XDG: `$XDG_DATA_HOME/{app_name}`).

- macOS: still use the XDG-style `.config` / `.local/share` layout; do not use `~/Library/Application Support/`.
- Precedence: `$XDG_CONFIG_HOME` / `$XDG_DATA_HOME` first; then `~/.config` / `~/.local/share`.

When enforcing this layout, prefer `directories::BaseDirs` (for `home_dir()`) + XDG env vars; `directories::ProjectDirs` follows OS conventions.

## Cross-platform environment

- Do not assume OS-specific environment variables like `HOME` for cross-platform support.
- Background: this may work on Linux/macOS but Windows may not set the same environment variables.
- Team principle: environment-dependent values must be obtained via the Rust stdlib or well-established crates to abstract OS differences.
- Practice: unify home directory retrieval via `directories::BaseDirs` (and `directories::ProjectDirs` for app-scoped config/cache/data paths).

## CI policy

- When changing filesystem/env-path/config discovery code, always include `windows-latest` in a CI matrix to catch issues early.

## Companion Skill: agentic-cli-design

If this CLI will be operated by AI agents and/or automation, also consult the `agentic-cli-design` skill.
Borrow these concepts: machine-readable output, non-interactive operation, idempotent commands, safe-by-default behavior, observability, and introspection.

## Workflow

1) Define the CLI surface area (subcommands, flags, required args) and keep it stable.
2) Implement a "JSON output mode" (e.g. `--json`) that prints ONLY machine-readable JSON to stdout.
3) Always send logs and progress to stderr; keep stdout reserved for the command result.
4) Use explicit exit codes:
   - `0`: success
   - `1`: expected failures (validation errors, missing resource, etc.)
   - `2`: CLI usage errors (typically handled by clap)
5) Add tests that execute the binary and assert:
   - exit code
   - stdout schema/content (especially in `--json` mode)
   - stderr contains diagnostics (but not required for correctness)
6) Automate quality gates with git hooks. `prek` is a good approach for fast, compatible pre-commit/pre-push hooks.

## Templates

- Crate selection: `rust-cli/references/crates.md`
- Copy/paste scaffolding (Cargo.toml, main.rs, tests, prek config): `rust-cli/references/templates.md`
