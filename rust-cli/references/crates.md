# Rust CLI crate selection guide

Use these as defaults unless the existing repository has a different established stack.

## Core

- `clap` (derive): CLI parsing, help text, subcommands.
- `anyhow`: ergonomic error propagation in binaries.
- `thiserror`: typed errors (especially for libraries that the CLI calls).
- `tracing` + `tracing-subscriber`: structured diagnostics; keep logs on stderr.
- `serde` + `serde_json`: input/output schemas and machine-readable JSON.

## IO / OS / UX

- `camino`: UTF-8 path types (when you want to avoid OS-string edge cases).
- `walkdir`: directory traversal.
- `globset`: include/exclude patterns.
- `indicatif`: progress bars (send to stderr; disable in `--json` mode).
- `owo-colors` (or `anstyle`): optional colored stderr output.

## Networking / Async (only if needed)

- `reqwest`: HTTP client.
- `tokio`: async runtime.
- `url`: URL parsing.

## Testing

- `assert_cmd`: run the compiled binary in tests.
- `predicates`: ergonomic assertions on output.
- `insta`: snapshot testing (useful for JSON output schemas).
- `tempfile`: temporary files/dirs.

## Configuration

- `figment` or `config`: layered config (env + file + defaults).
- `dotenvy`: local dev env files (avoid relying on this in production).
- `directories`: cross-platform user/project directories. Note: `ProjectDirs` follows OS conventions (macOS uses Application Support). If you need an explicit XDG layout on macOS, use `BaseDirs` + `$XDG_CONFIG_HOME`/`$XDG_DATA_HOME`; avoid reading `HOME` directly.
