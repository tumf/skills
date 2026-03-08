# python-uv-project

Opinionated skill for bootstrapping generic Python projects with `uv`, git, `prek`, Makefile-based quality targets, Pydantic models, coverage, CI, and Hatch version bumps.

## What This Skill Covers

- `uv init`-based project creation
- git repository bootstrap
- `pytest`, `ruff`, and `pyright` wired through `Makefile`
- `pytest-cov` and `make coverage`
- `prek` hooks for `pre-commit` and `pre-push`
- strict Pydantic-first data modeling
- repo baseline files: `README.md`, MIT `LICENSE`, `.gitignore`, `.editorconfig`
- `settings.py`, `py.typed`, and `__about__.py` scaffolding
- minimal GitHub Actions CI running Make targets
- Hatch version bump targets: `bump-patch`, `bump-minor`, `bump-major`

## Example Trigger Phrases

- "Create a new Python project with uv, git, ruff, pyright, pytest, and prek."
- "Standardize this Python repo around Makefile targets for test/format/lint/typecheck."
- "Bootstrap a Python package with strict Pydantic models and Hatch version bumps."
- "Set up a uv-based Python repo the way tumf likes it."
- "Create a generic Python repo with MIT license, CI, coverage, and solid defaults."

## References

- `python-uv-project/references/templates.md`
