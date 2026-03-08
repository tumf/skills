# Python uv Project Templates

Use these as the default starting point when creating the repo requested by this skill.
Adapt names and package paths, but keep the overall shape unless the target repo already has strong conventions.

## Bootstrap commands

```bash
uv init --package my_project
git init
uv add pydantic pydantic-settings
uv add --dev pytest pytest-cov ruff pyright hatch
```

After bootstrap, inspect the generated `pyproject.toml` and add the extra sections below.

## README.md

````md
# my-project

Short project description.

## Setup

```bash
uv sync
uv tool install prek
make install-hooks
```

## Common commands

- `make format`
- `make lint`
- `make typecheck`
- `make test`
- `make coverage`
- `make check`

## Development workflow

1. Sync dependencies with `uv sync`
2. Make changes
3. Run `make check`
4. Run `make coverage` when touching important behavior
5. Commit once hooks and tests pass
````

## LICENSE (MIT)

```text
MIT License

Copyright (c) 2026 YOUR NAME

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## .gitignore

```gitignore
# Python cache and tooling
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.pyright/
.mypy_cache/

# Virtual environments
.venv/
.python-version

# Build artifacts
build/
dist/
*.egg-info/

# Coverage
.coverage
htmlcov/

# OS / editor noise
.DS_Store
.idea/
.vscode/
```

## .editorconfig

```ini
root = true

[*.py]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[Makefile]
indent_style = tab

[*.md]
trim_trailing_whitespace = false
```

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
  "pytest-cov",
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

## src/my_project/settings.py

```python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MY_PROJECT_",
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "my-project"
    log_level: str = "INFO"
    debug: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
```

## src/my_project/logging.py

```python
import logging


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
```

## src/my_project/py.typed

Create an empty file named `src/my_project/py.typed`.

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
.PHONY: test format lint typecheck check coverage hooks install-hooks bump-patch bump-minor bump-major

test:
	uv run pytest

coverage:
	uv run pytest --cov=src/my_project --cov-report=term-missing --cov-report=html

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

## .github/workflows/ci.yml

```yaml
name: ci

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  checks:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v6

      - name: Set up Python
        run: uv python install

      - name: Sync dependencies
        run: uv sync --all-groups

      - name: Lint
        run: make lint

      - name: Typecheck
        run: make typecheck

      - name: Test
        run: make test
```
