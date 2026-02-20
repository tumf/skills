# Contributing (rust-cli)

This skill repository distinguishes between:

- `README.md`: user-facing documentation (what it does, how to use it)
- `CONTRIBUTING.md`: contributor/developer guidance (how to change and maintain it)

## What goes where

Put these in `README.md`:

- Feature overview and intended use
- Installation/prerequisites (if any)
- Quick start and usage examples
- Configuration knobs (env vars, flags)
- Troubleshooting

Put these in `CONTRIBUTING.md`:

- Editing/maintenance workflow
- How to validate changes (lint/tests)
- Release or publishing steps
- Internal conventions and rationale

## Editing guidelines

- Keep markdown readable (prefer ~100 char lines).
- Use fenced code blocks with language tags (e.g. `bash`, `rust`, `json`).
- Prefer short, copy-pastable examples.

## Skill-specific structure

- `rust-cli/SKILL.md`: agent instructions (defaults, workflow patterns, pitfalls)
- `rust-cli/README.md`: user-facing overview and pointers
- `rust-cli/references/`: deeper templates and crate lists

## Updating documentation

When you add or change a recommended pattern:

1. Update `rust-cli/SKILL.md` with the canonical instruction.
2. If it affects users, reflect it in `rust-cli/README.md` (high-level) and/or `rust-cli/references/` (details).
3. Keep contributor-only details (validation/release process) here.
