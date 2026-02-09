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

## Flaky tests: time-based cutoffs (SystemTime + second precision)

If you store timestamps as Unix seconds (`i64`) and compute a cleanup cutoff using `SystemTime::now()`, tests can become flaky across platforms.
This often passes on Linux/macOS and fails on Windows due to timing/resolution differences.

Typical failure mode (SQLite example):

- `record()` inserts `created_at = now_secs()` (e.g. `1707408142`).
- a moment later, `cleanup_old_entries(0)` computes `cutoff = now_secs()` (e.g. `1707408143`).
- SQL uses `WHERE created_at < cutoff` which matches the freshly inserted row (`1707408142 < 1707408143`).

Recommended fixes (pick one that matches intended semantics):

- **Tests:** avoid boundary conditions; use a large margin (e.g. `cleanup_old_entries(1)` instead of `0`), and optionally insert a small sleep between operations to avoid same-second edges.
- **Implementation:** define `days <= 0` semantics explicitly (often a no-op), or inject a clock so tests can be deterministic. If you keep second-precision storage, be careful with `<` vs `<=` and how you define "older than N days".

Example test adjustment (stable across platforms):

```rust
#[test]
fn test_cleanup_old_entries() {
    let (ledger, _temp) = create_test_ledger();

    ledger
        .record("test-1", "hash-1", "tweet-1", "success")
        .unwrap();

    // Ensure the cutoff is not computed in the exact same instant.
    std::thread::sleep(std::time::Duration::from_millis(10));

    // Use a safe margin: a fresh entry should not be deleted.
    let deleted = ledger.cleanup_old_entries(1).unwrap();
    assert_eq!(deleted, 0);

    let entry = ledger.lookup("test-1").unwrap();
    assert!(entry.is_some());
}
```

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
