---
name: oss-publish
description: |
  Open source publication and release hygiene for repositories and CLIs (language-agnostic): choose and add LICENSE,
  prepare README/CONTRIBUTING/SECURITY/CODE_OF_CONDUCT, standardize versioning/tags/releases and release notes,
  set up CI matrices, quality gates (pre-commit/pre-push), and safe-by-default automation/bootstrapping.
  Use when preparing a project to be published publicly (GitHub/GitLab), cutting a release, or standardizing repo
  tooling across languages.
---

# oss-publish - OSS Publication And Release Hygiene

Focus: make a repository publishable and releasable with minimal ambiguity.
Prefer safe-by-default, non-interactive, repeatable steps.

## Baseline Repo Artifacts

Add these at repo root (or confirm they exist and are correct):

- `LICENSE` (pick one; do not invent a custom license)
- `README.md` (project intent, quick start, examples)
- `CONTRIBUTING.md` (how to contribute; local dev workflow)
- `CODE_OF_CONDUCT.md` (community expectations; adopt a standard template)
- `SECURITY.md` (vulnerability reporting process)
- Optional: `SUPPORT.md` (where to ask questions)

If the project is a CLI/tool, also ensure:

- `--help` is stable and in English
- docs include examples for both humans and automation

## Release Discipline (Language-Agnostic)

- Use semantic versioning (SemVer) unless the ecosystem dictates otherwise.
- Treat releases as immutable:
  - tag the release commit
  - generate release notes from commits/CHANGELOG
  - attach artifacts (if you distribute binaries)

Pre-release checklist (minimum):

1) working tree clean
2) tests + lint/format pass
3) documentation updated (README, examples)
4) version bumped + tagged
5) release notes produced

For a concrete checklist and file templates, see:

- `oss-publish/references/checklist.md`
- `oss-publish/references/templates.md`
- `oss-publish/references/readme.md`

## Quality Gates (Local + CI)

Prefer a split between fast and slow checks:

- `pre-commit`: format + lint (fast)
- `pre-push` (or CI only): full test suite (slower)

Use `pre-commit` or `prek` (compatible alternative) depending on repo conventions.

## CI Policy (Cross-Platform)

If the project is intended to be cross-platform, include a CI matrix:

- `ubuntu-latest`
- `macos-latest`
- `windows-latest`

Set `fail-fast: false` so one platform failure does not hide others.

## Stable Bootstrap Entry Point

Prefer a single, predictable setup command usable by humans and automation:

- Provide an executable `.wt/setup` that runs `make setup` (or equivalent)
- Keep it idempotent and non-interactive

## Naming And Collisions

- Pick a unique repo and command/binary name.
- Avoid collisions with common system commands and common package names.
- If the name is generic, add an org/team prefix.

## Filesystem Layout (XDG)

If the project stores user config/data:

- Config: `$XDG_CONFIG_HOME/{app}` (fallback `~/.config/{app}`)
- Data/state/artifacts (non-git-managed): `$XDG_DATA_HOME/{app}` (fallback `~/.local/share/{app}`)

Avoid OS-specific special cases unless the ecosystem requires it.

## Related Skills

- `agentic-cli-design`: deep guidance for agent/automation-friendly CLIs (JSON mode, exit codes, non-interactive)
- `rust-cli`: Rust-specific CLI implementation patterns (clap/anyhow/tracing/serde_json, cargo-release)
