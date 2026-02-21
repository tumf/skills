# Templates

These are copy/paste starting points. Keep stdout strictly for the command result.
Send logs, progress, and diagnostics to stderr.

## Cargo.toml (binary)

```toml
[package]
name = "mycli"
version = "0.1.0"
edition = "2021"

[dependencies]
anyhow = "1"
clap = { version = "4", features = ["derive"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "fmt"] }

[dev-dependencies]
assert_cmd = "2"
predicates = "3"
serde_json = "1"
```

## src/main.rs (scaffold)

```rust
use anyhow::Context;
use clap::Parser;
use serde_json::json;
use std::process::ExitCode;

#[derive(Debug, Parser)]
#[command(name = "mycli")]
struct Args {
    /// Emit machine-readable JSON to stdout.
    #[arg(long)]
    json: bool,

    /// Control log verbosity (stderr). Examples: "info", "debug", "warn".
    #[arg(long, default_value = "info")]
    log: String,
}

fn init_tracing(level: &str) {
    // Keep diagnostics on stderr. In JSON output mode, stdout must remain clean.
    let filter = tracing_subscriber::EnvFilter::try_new(level)
        .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info"));

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .with_writer(std::io::stderr)
        .with_target(false)
        .with_level(true)
        .compact()
        .init();
}

fn main() -> ExitCode {
    let args = Args::parse();
    init_tracing(&args.log);

    match run(&args) {
        Ok(value) => {
            // stdout: command result only
            if args.json {
                println!("{}", json!({ "ok": true, "result": value }));
            } else {
                println!("{value}");
            }
            ExitCode::SUCCESS
        }
        Err(err) => {
            // In `--json` mode, stdout must always be machine-readable (both success and error).
            // Keep logs/diagnostics on stderr.
            if args.json {
                // stdout: machine-readable error payload
                println!(
                    "{}",
                    json!({ "ok": false, "error": { "message": err.to_string() } })
                );
            } else {
                // stderr: human-readable diagnostics
                eprintln!("error: {err:#}");
            }
            ExitCode::from(1)
        }
    }
}

fn run(_args: &Args) -> anyhow::Result<String> {
    // Replace with your actual logic.
    // Use .context(...) at boundaries so failures are actionable.
    let value = "hello".to_string();
    Ok(value).context("computing greeting")
}
```

## clap help (English + per-subcommand help)

```rust
use clap::{Parser, Subcommand};

#[derive(Debug, Parser)]
#[command(
    name = "mycli",
    about = "Do useful things from the terminal.",
    long_about = "Do useful things from the terminal.\n\nUse subcommands to perform actions."
)]
struct Cli {
    #[command(subcommand)]
    cmd: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    /// Print a greeting.
    #[command(about = "Print a greeting.", long_about = "Print a greeting to stdout.")]
    Hello {
        /// Name to greet.
        name: String,
    },
}
```

## tests/cli.rs (integration test)

```rust
use assert_cmd::Command;
use serde_json::Value;

#[test]
fn json_mode_is_machine_readable() {
    let mut cmd = Command::cargo_bin(env!("CARGO_PKG_NAME")).unwrap();
    let output = cmd.arg("--json").assert().success().get_output().clone();

    let stdout = String::from_utf8(output.stdout).unwrap();
    let v: Value = serde_json::from_str(&stdout).unwrap();

    assert_eq!(v["ok"], true);
    assert!(v.get("result").is_some());
}
```

## XDG paths (config vs non-git-managed data)

Add:

```toml
# Cargo.toml
directories = "5"
```

Use (home dir):

```rust
use directories::BaseDirs;
use std::path::PathBuf;

fn home_dir() -> PathBuf {
    BaseDirs::new()
        .expect("failed to determine base directories")
        .home_dir()
        .to_path_buf()
}

// Note: do not read `HOME` directly; it is not reliably set across platforms.
```

Use (explicit XDG layout):

```rust
use directories::BaseDirs;
use std::env;
use std::path::PathBuf;

fn xdg_app_dirs(app_name: &str) -> (PathBuf, PathBuf) {
    let home = BaseDirs::new()
        .expect("failed to determine base directories")
        .home_dir()
        .to_path_buf();

    let config_home = env::var_os("XDG_CONFIG_HOME")
        .map(PathBuf::from)
        .unwrap_or_else(|| home.join(".config"));

    let data_home = env::var_os("XDG_DATA_HOME")
        .map(PathBuf::from)
        .unwrap_or_else(|| home.join(".local").join("share"));

    let app_config_dir = config_home.join(app_name);
    let app_data_dir = data_home.join(app_name);

    (app_config_dir, app_data_dir)
}

// Note: `directories::ProjectDirs` follows platform conventions (e.g. macOS Application Support).
// Do not use it when you need to enforce an XDG layout on macOS.
```

## GitHub Actions (CI matrix incl. Windows)

```yaml
name: ci

on:
  push:
  pull_request:

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo test --all
```

## Git hooks / pre-commit (prek)

`prek` is a fast, Rust-based, compatible alternative to `pre-commit`. It supports TOML configs (`prek.toml`) and
`pre-commit` YAML configs (`.pre-commit-config.yaml`). It also supports multiple git hook types via `prek install --hook-type ...`.

Recommended split:

- `pre-commit`: quick checks (format + lint)
- `pre-push`: slower checks (tests)

Create `prek.toml` at the repository root:

```toml
# prek.toml
# Config file name is "prek.toml" (TOML) or ".pre-commit-config.yaml" (YAML).

# Install both hook scripts by default when running `prek install`.
default_install_hook_types = ["pre-commit", "pre-push"]

[[repos]]
repo = "local"

hooks = [
  {
    id = "cargo-fmt-check",
    name = "cargo fmt --check",
    language = "system",
    entry = "cargo fmt --all -- --check",
    pass_filenames = false,
    always_run = true,
    stages = ["pre-commit"],
  },
  {
    id = "cargo-clippy",
    name = "cargo clippy -D warnings",
    language = "system",
    entry = "cargo clippy --all-targets --all-features -- -D warnings",
    pass_filenames = false,
    always_run = true,
    stages = ["pre-commit"],
  },
  {
    id = "cargo-test",
    name = "cargo test",
    language = "system",
    entry = "cargo test",
    pass_filenames = false,
    always_run = true,
    stages = ["pre-push"],
  },
]
```

Install hooks (non-interactive):

```bash
prek install --install-hooks
```

Notes:

- If you do not set `default_install_hook_types`, `prek install` defaults to installing `pre-commit` only.
- Alternatively, you can explicitly choose hook types:

```bash
prek install --install-hooks --hook-type pre-commit --hook-type pre-push
```

## Makefile (common Rust CLI targets)

This is a copy/paste Makefile you can adapt per-repo.
It is safe-by-default for publish: `make publish` requires `PUBLISH=1`.

```makefile
# Makefile for a Rust CLI project

.PHONY: build help install release test clean fmt lint check setup pre-commit pre-commit-hooks \
        bump-patch bump-minor bump-major publish publish-dry-run

# Default target
build:
	@echo "Building debug version..."
	cargo build

help:
	@echo "Available targets:"
	@echo "  make (default)         - Build debug version"
	@echo "  make build             - Build debug version"
	@echo "  make install           - Install the binary to ~/.cargo/bin"
	@echo "  make release           - Build optimized release version"
	@echo "  make test              - Run all tests"
	@echo "  make clean             - Clean build artifacts"
	@echo "  make fmt               - Format code with rustfmt"
	@echo "  make lint              - Run clippy linter"
	@echo "  make check             - Run fmt, lint, and test"
	@echo "  make setup             - Setup development environment"
	@echo "  make pre-commit         - Run prek on all files"
	@echo "  make pre-commit-hooks  - Install git pre-commit hooks"
	@echo "  make bump-patch        - Bump patch version + tag (no publish)"
	@echo "  make bump-minor        - Bump minor version + tag (no publish)"
	@echo "  make bump-major        - Bump major version + tag (no publish)"
	@echo "  make publish-dry-run    - Verify publish packaging (no upload)"
	@echo "  make publish           - Publish to crates.io (requires PUBLISH=1)"

install:
	@echo "Installing from local checkout..."
	cargo install --path .

release:
	@echo "Building release version..."
	cargo build --release

test:
	@echo "Running tests..."
	cargo test --verbose

clean:
	@echo "Cleaning build artifacts..."
	cargo clean

fmt:
	@echo "Formatting code..."
	cargo fmt

lint:
	@echo "Running clippy..."
	cargo clippy -- -D warnings

check: fmt lint test
	@echo "All checks passed!"

setup: pre-commit-hooks
	@echo "Setting up development environment..."
	@command -v rustfmt >/dev/null 2>&1 || rustup component add rustfmt
	@command -v clippy >/dev/null 2>&1 || rustup component add clippy
	@command -v cargo-release >/dev/null 2>&1 || cargo install cargo-release
	@echo "Development environment setup complete!"

pre-commit:
	@set -e; \
	if command -v prek >/dev/null 2>&1; then PREK=prek; \
	elif [ -x "$$HOME/.local/bin/prek" ]; then PREK="$$HOME/.local/bin/prek"; \
	else \
		echo "prek not found. Run 'make pre-commit-hooks' to install it."; \
		exit 1; \
	fi; \
	"$$PREK" run --all-files

pre-commit-hooks:
	@set -e; \
	echo "Installing pre-commit hooks (prek)..."; \
	if command -v prek >/dev/null 2>&1; then PREK=prek; \
	elif [ -x "$$HOME/.local/bin/prek" ]; then PREK="$$HOME/.local/bin/prek"; \
	else \
		echo "prek not found. Installing to $$HOME/.local/bin..."; \
		mkdir -p "$$HOME/.local/bin"; \
		curl -LsSf https://github.com/j178/prek/releases/latest/download/prek-installer.sh | sh; \
		PREK="$$HOME/.local/bin/prek"; \
	fi; \
	"$$PREK" install --overwrite --hook-type pre-commit; \
	echo "Pre-commit hook installed. Run 'make pre-commit' to verify."

# Version bumps + tag creation (no publish)
bump-patch:
	@echo "Bumping patch version (no publish)..."
	@cargo release patch --execute --no-confirm --no-publish

bump-minor:
	@echo "Bumping minor version (no publish)..."
	@cargo release minor --execute --no-confirm --no-publish

bump-major:
	@echo "Bumping major version (no publish)..."
	@cargo release major --execute --no-confirm --no-publish

publish-dry-run:
	@echo "Running cargo publish --dry-run..."
	cargo publish --dry-run

publish:
	@set -e; \
	if [ "$(PUBLISH)" != "1" ]; then \
		echo "Refusing to publish. Re-run with: make publish PUBLISH=1"; \
		exit 1; \
	fi; \
	echo "Publishing to crates.io..."; \
	cargo publish
```

## Repo bootstrap entrypoint (.wt/setup)

For language-agnostic bootstrap script patterns (idempotent, non-interactive), see:

- `oss-publish/references/templates.md`
