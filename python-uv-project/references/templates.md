# Python uv Project Templates

Use these as the default starting point when creating the repo requested by this skill.
Adapt names and package paths, but keep the overall shape unless the target repo already has strong conventions.

## Bootstrap commands

```bash
uv init --package my_project
git init
uv add pydantic pydantic-settings
uv add --dev pytest ruff pyright hatch
```

After bootstrap, inspect the generated `pyproject.toml` and add the extra sections below.

## pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Short project description"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "pydantic",
  "pydantic-settings",
]

[dependency-groups]
dev = [
  "hatch",
  "pyright",
  "pytest",
  "ruff",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.version]
path = "src/my_project/__about__.py"

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.pyright]
include = ["src", "tests"]
typeCheckingMode = "strict"
venvPath = "."
venv = ".venv"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
```

If the project does not need environment-backed settings, omit `pydantic-settings`.

## src/my_project/__about__.py

```python
__version__ = "0.1.0"
```

## src/my_project/models.py

```python
from pydantic import BaseModel, ConfigDict


class ExampleRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    enabled: bool = True
```

## tests/test_models.py

```python
import pytest
from pydantic import ValidationError

from my_project.models import ExampleRecord


def test_example_record_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ExampleRecord(id="1", name="demo", unknown=True)
```

## Makefile

```makefile
.PHONY: test format lint typecheck check hooks install-hooks bump-patch bump-minor bump-major

test:
	uv run pytest

format:
	uv run ruff format .

lint:
	uv run ruff check .

typecheck:
	uv run pyright

check: format lint typecheck test

hooks:
	uv tool run prek run --all-files

install-hooks:
	uv tool run prek install --install-hooks --hook-type pre-commit --hook-type pre-push

bump-patch:
	uv run hatch version patch

bump-minor:
	uv run hatch version minor

bump-major:
	uv run hatch version major
```

If the user wants hook installation to work without `uv tool run`, add a repo-specific bootstrap target that installs `prek` first.

## prek.toml

```toml
default_install_hook_types = ["pre-commit", "pre-push"]

[[repos]]
repo = "local"

hooks = [
  {
    id = "format",
    name = "make format",
    language = "system",
    entry = "make format",
    pass_filenames = false,
    always_run = true,
    stages = ["pre-commit"],
  },
  {
    id = "lint",
    name = "make lint",
    language = "system",
    entry = "make lint",
    pass_filenames = false,
    always_run = true,
    stages = ["pre-commit"],
  },
  {
    id = "typecheck",
    name = "make typecheck",
    language = "system",
    entry = "make typecheck",
    pass_filenames = false,
    always_run = true,
    stages = ["pre-push"],
  },
  {
    id = "test",
    name = "make test",
    language = "system",
    entry = "make test",
    pass_filenames = false,
    always_run = true,
    stages = ["pre-push"],
  },
]
```

## Suggested bootstrap sequence

```bash
uv sync
uv tool install prek
make install-hooks
make check
git add .
git commit -m "Initial project scaffold"
```
