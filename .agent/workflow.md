# Development Workflow

## Creating a New Skill

Follow these steps to add a new skill to the repository:

### 1. Create Directory Structure

```bash
# Create skill directory (use kebab-case)
mkdir {skill-name}

# Create scripts directory
mkdir {skill-name}/scripts
```

### 2. Create Core Files

Each skill needs these files:

| File | Purpose | Required |
|------|---------|----------|
| `SKILL.md` | Agent instructions with YAML frontmatter | Yes |
| `README.md` | User-facing documentation | Yes |
| `scripts/*.py` | Executable Python scripts | Yes |

### 3. Write SKILL.md

```yaml
---
name: skill-name
description: |
  Clear description of what the skill does
  and when to use it.
---

# Skill Name

[Installation, usage, examples]
```

See [Documentation Standards](documentation.md) for format details.

### 4. Write README.md

Include all required sections:
- Features
- Installation
- Quick Start
- Usage Reference
- Examples
- Troubleshooting

See [Documentation Standards](documentation.md) for template.

### 5. Create Scripts

```bash
# Create executable Python script
touch {skill-name}/scripts/{script-name}.py
chmod +x {skill-name}/scripts/{script-name}.py
```

Follow [Python Style Guide](python-style.md) for script structure.

### 6. Test Scripts

```bash
# Test help output
./{skill-name}/scripts/{script-name}.py --help

# Test with minimal arguments
./{skill-name}/scripts/{script-name}.py "test-input"

# Test error handling (e.g., missing API key)
unset API_KEY_NAME
./{skill-name}/scripts/{script-name}.py "test-input"
```

### 7. Update Main README

Add your skill to the "Available Skills" section in the root `README.md`.

### 8. Verify File Permissions

```bash
# Ensure all scripts are executable
chmod +x {skill-name}/scripts/*.py

# Verify
ls -la {skill-name}/scripts/
```

## Git Workflow

### Commit Message Format

Use conventional commits:

```
type: description

[optional body]
```

| Type | Usage | Example |
|------|-------|---------|
| `feat:` | New feature/skill | `feat: add web scraping skill` |
| `fix:` | Bug fix | `fix: handle missing API key gracefully` |
| `docs:` | Documentation only | `docs: update README examples` |
| `chore:` | Maintenance | `chore: update dependencies` |
| `refactor:` | Code restructuring | `refactor: simplify error handling` |
| `test:` | Add/update tests | `test: add integration tests` |

### Standard Workflow

```bash
# Check status
git status

# Add files
git add .

# Commit with descriptive message
git commit -m "feat: add new skill for X"

# Push to remote
git push
```

### Branch Strategy

For this repository:
- Work directly on `main` for simple changes
- Create feature branches for complex work: `feature/skill-name`
- Merge via pull request for review

```bash
# Create feature branch
git checkout -b feature/new-skill

# Make changes, commit
git add .
git commit -m "feat: add new skill"

# Push branch
git push -u origin feature/new-skill

# Create PR on GitHub
```

## File Permissions

All Python scripts **must** be executable:

```bash
# Make single script executable
chmod +x scripts/script-name.py

# Make all scripts in directory executable
chmod +x scripts/*.py

# Verify permissions
ls -la scripts/
# Should show: -rwxr-xr-x
```

## Testing Checklist

Before committing a new skill:

```
[ ] Scripts are executable (chmod +x)
[ ] Scripts run without errors
[ ] --help flag works for all scripts
[ ] Error handling tested (missing env vars, bad input)
[ ] JSON output is properly formatted
[ ] SKILL.md has correct YAML frontmatter
[ ] README.md includes all required sections
[ ] Examples in README are tested and work
[ ] Main README.md updated with new skill
[ ] Git commit message follows convention
```

## Environment Setup

### Python Dependencies

Install per-skill dependencies as needed:

```bash
# For firecrawl skill
pip install firecrawl-py

# For other skills
pip install package-name
```

### Environment Variables

Never commit sensitive data. Use environment variables:

```bash
# Set for current session
export FIRECRAWL_API_KEY="your-key"

# Add to .env file (never commit)
echo 'FIRECRAWL_API_KEY="your-key"' >> .env

# Load .env file
source .env
```

Document all required environment variables in the skill's README.md.

## Code Review Guidelines

When reviewing new skills:

1. **File structure** - Correct directories and file names?
2. **Documentation** - SKILL.md and README.md complete?
3. **Code style** - Follows [Python Style Guide](python-style.md)?
4. **Error handling** - Proper JSON output on errors?
5. **Testing** - Scripts tested and working?
6. **Permissions** - Scripts executable?
7. **Security** - No hardcoded secrets?

## Common Issues

### Scripts Not Executable

**Problem:** `Permission denied` when running script

**Solution:**
```bash
chmod +x {skill}/scripts/*.py
```

### Import Errors

**Problem:** `ModuleNotFoundError`

**Solution:**
```bash
pip install required-package
```

### Missing Environment Variables

**Problem:** Script fails with "environment variable not set"

**Solution:**
```bash
export VARIABLE_NAME="value"
# Or add to .env file
```

### JSON Output Errors

**Problem:** `Object of type X is not JSON serializable`

**Solution:**
```python
# Use default=str in json.dumps()
json.dumps(data, indent=2, default=str)
```
