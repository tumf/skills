# Templates

These are minimal, standard templates. Customize to fit the project.

## SECURITY.md

```markdown
# Security Policy

## Reporting a Vulnerability

Please report security issues privately.

- Preferred contact: <email or issue template>
- What to include: affected version, reproduction steps, impact assessment

We will acknowledge receipt within a reasonable timeframe.
```

## CODE_OF_CONDUCT.md

Prefer adopting a well-known template (e.g. Contributor Covenant) rather than inventing a custom policy.

If you use Contributor Covenant, include:

- version number
- enforcement contact

## CONTRIBUTING.md (skeleton)

```markdown
# Contributing

Thanks for contributing!

## Development setup

1. Clone the repo
2. Run the bootstrap script:

   ```bash
   ./.wt/setup
   ```

## Running checks

Describe the expected commands (format, lint, test).

## Submitting changes

- Keep changes focused
- Add tests when applicable
- Describe why the change is needed
```

## .wt/setup (repo bootstrap script)

Create an executable script at `.wt/setup` and keep it as the one stable entrypoint for bootstrapping.
This should be safe to run repeatedly and should avoid interactive prompts.

```bash
#!/usr/bin/env bash
set -euo pipefail

if ! command -v make >/dev/null 2>&1; then
  echo "error: make not found" >&2
  exit 1
fi

make setup
```

Make it executable:

```bash
chmod +x .wt/setup
```
