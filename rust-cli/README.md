# rust-cli

Build maintainable Rust CLI programs with a consistent, automation-friendly structure.

## What This Skill Covers

- clap-based argument parsing (derive)
- English help output (`-h`/`--help`) and meaningful per-subcommand help
- anyhow-based error handling (fail fast)
- tracing-based diagnostics (stderr)
- JSON output mode and stdout/stderr separation
- predictable exit codes
- choosing a unique binary/command name (avoid crates.io and common system collisions)
- integration tests for the CLI binary
- git hooks with `prek` (pre-commit / pre-push)
- XDG filesystem layout: config in `~/.config/{app_name}`, non-git-managed data in `~/.local/share/{app_name}`

## Example Trigger Phrases

- "Create a Rust CLI with clap, JSON output mode, and good exit codes."
- "Add a --json flag and ensure stdout is machine-readable and logs go to stderr."
- "Set up prek hooks to run cargo fmt/clippy/test."
- "Write integration tests for this Rust CLI using assert_cmd."

## References

- `rust-cli/references/crates.md`
- `rust-cli/references/templates.md`
- Companion skill for agent-operated CLIs: [agentic-cli-design](https://github.com/tumf/skills/tree/main/agentic-cli-design)

## Troubleshooting

### Cross-platform testing pitfalls

**Home directory override (Windows limitation):**

On Windows, `directories::BaseDirs` uses Win32 API directly and **cannot be overridden by environment variables** (`HOME` or `USERPROFILE`). Unix/Linux/macOS read `$HOME` and can be overridden.

**Solutions:**
- Mark tests as `#[cfg(not(target_os = "windows"))]` when testing HOME override
- Use dependency injection: accept explicit paths instead of calling `BaseDirs` internally
- Add `windows-latest` to CI matrix to catch issues early

**Other common issues:**
- `std::env::temp_dir()` and `std::env::current_exe()` also use OS API (not overridable)
- Path separators, line endings, executable extensions differ between platforms
- Always use `std::path::Path` and `tempfile` crate for portability

See `SKILL.md` for detailed patterns and examples.

### Flaky tests with time-based cleanup

If you store timestamps as Unix seconds and compute cleanup cutoffs using `SystemTime::now()`, tests can flake across platforms.
A common pattern is:

- `record()` inserts `created_at = now_secs()`
- `cleanup_old_entries(0)` computes `cutoff = now_secs()` a moment later
- `DELETE ... WHERE created_at < cutoff` can delete the freshly inserted row

Stabilize tests by avoiding the boundary:

```rust
std::thread::sleep(std::time::Duration::from_millis(10));
let deleted = ledger.cleanup_old_entries(1).unwrap();
assert_eq!(deleted, 0);
```

If `days = 0` is meant to be a no-op (keep everything), implement that semantic explicitly (and test it).
