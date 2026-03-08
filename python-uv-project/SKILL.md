---
name: python-uv-project
description: |
  Scaffold opinionated Python projects with uv as the package/project manager and `uv init` as the bootstrap step.
  Use when creating or standardizing a Python repository that should include: git initialization, Makefile-driven
  `test`/`format`/`lint`/`typecheck` workflows, `prek` git hooks, strict typed data models with Pydantic, and
  Hatch-based semantic version bumps via `make bump-patch`, `make bump-minor`, and `make bump-major`.
---

# python-uv-project - Opinionated Python Project Bootstrap

Build a modern Python repo around `uv`, fast local automation, and predictable quality gates.
Prefer current stable releases and avoid unnecessary version pin micromanagement unless the user asks for it.

## Default stack

- Bootstrap with `uv init`, then keep dependency management in `uv`.
- Initialize git immediately and make the repo ready for normal commit flow.
- Use a `src/` layout for packages.
- Use `pytest` for tests.
- Use `ruff` for formatting and linting.
- Use `pyright` for type checking.
- Use `pydantic` (and `pydantic-settings` when config/env modeling is needed) for strict data contracts.
- Use `hatch` for version bump operations.
- Drive routine developer commands through `Makefile` targets: `test`, `format`, `lint`, `typecheck`.

## Workflow

### 1. Scaffold with uv

Create the project with `uv init` rather than hand-writing `pyproject.toml`.
Prefer package mode for reusable libraries and service code:

```bash
uv init --package <project-name>
```

Then add the default toolchain with `uv add` / `uv add --dev`.
Keep the initial setup non-interactive and scriptable.

### 2. Normalize project layout

- Keep package code under `src/<package_name>/`.
- Add `tests/` for pytest.
- Add a small version module when needed for Hatch version management.
- Add `.gitignore` entries appropriate for Python, `.venv/`, caches, and build artifacts.

If the generated layout is close but not fully aligned, update it rather than replacing `uv` defaults wholesale.

### 3. Configure quality tooling

Add the development dependencies through `uv` and wire them into `pyproject.toml`.

Recommended dev tools:

- `pytest`
- `ruff`
- `pyright`
- `hatch`
- `pydantic`
- `pydantic-settings` when the app has config models

Use current stable releases by default. Do not invent exact version pins unless the repo already pins tools consistently.

### 4. Add Makefile entry points

Every project created with this skill should expose these targets at minimum:

- `make test`
- `make format`
- `make lint`
- `make typecheck`
- `make bump-patch`
- `make bump-minor`
- `make bump-major`

Prefer `uv run ...` inside Make targets so the project-local environment is always used.
Use the template in `python-uv-project/references/templates.md`.

### 5. Install prek hooks

Use `prek` for git hooks.
Recommended split:

- `pre-commit`: `make format` and `make lint`
- `pre-push`: `make typecheck` and `make test`

Keep hooks fast on commit and comprehensive on push.
Use a local-hook configuration that shells out to Make targets instead of duplicating commands.

### 6. Make Pydantic the source of truth for data

When the project touches structured data, configs, request/response models, or file-backed schemas:

- model them with `pydantic.BaseModel`
- validate inputs at boundaries
- prefer explicit field types over `dict[str, Any]`
- set stricter model config when appropriate (`extra="forbid"`, frozen models, validation on assignment, etc.)
- centralize environment/config parsing in dedicated settings models

Do not leave loosely typed config parsing or ad hoc JSON validation in place if Pydantic can express it cleanly.

### 7. Set up Hatch version bumps

Use Hatch for release version changes and expose it via Make.
The user specifically wants:

- `make bump-patch`
- `make bump-minor`
- `make bump-major`

Prefer a simple, explicit Hatch configuration that updates one canonical version source.
If the repo uses a package module such as `src/<package_name>/__about__.py`, point Hatch there.
If the repo already manages version directly in `pyproject.toml`, keep the approach consistent.

### 8. Verify the scaffold

After generating or refactoring the project, run the full local workflow:

```bash
make format
make lint
make typecheck
make test
```

If hooks were added, also install them and ensure `prek run --all-files` passes.

## Implementation notes

- Prefer `uv sync` / `uv run` instead of raw virtualenv activation instructions.
- Keep commands agent-friendly and non-interactive.
- Preserve existing repository conventions when modifying an already-started project.
- If CI is requested, mirror the same Make targets rather than re-specifying tool commands in multiple places.

## References

- Copy/paste bootstrap snippets: `python-uv-project/references/templates.md`
