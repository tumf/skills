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
