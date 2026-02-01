# OpenCode Command Creator

Create custom OpenCode commands with proper structure and configuration.

## Overview

This skill helps you create custom commands for OpenCode that allow you to define reusable prompts and workflows. Commands can include arguments, shell outputs, and file references to build powerful automation.

## Use Cases

- **Repetitive tasks**: Automate common workflows like testing, building, or reviewing
- **Project workflows**: Create project-specific commands for your team
- **Complex operations**: Combine multiple steps into single commands
- **Code generation**: Templates for creating components, files, or features

## Quick Start

### Create a Simple Command

Create `.opencode/commands/test.md`:

```markdown
---
description: Run tests with coverage
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

Use it:
```bash
/test
```

### Create a Command with Arguments

Create `.opencode/commands/component.md`:

```markdown
---
description: Create new React component
agent: code
---

Create a new React component named $ARGUMENTS with TypeScript support.
Include proper typing and basic structure.
```

Use it:
```bash
/component Button
```

## Command Formats

### Markdown Files (Recommended)

**Location:**
- Global: `~/.config/opencode/commands/`
- Project: `.opencode/commands/`

**Structure:**
```markdown
---
description: Command description
agent: agent-name (optional)
model: model-identifier (optional)
subtask: true/false (optional)
---

Your prompt template here.
Use $ARGUMENTS for user input.
Use !`command` for shell output.
Use @file.txt for file content.
```

### JSON Configuration

In `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "command-name": {
      "template": "Your prompt template",
      "description": "Command description",
      "agent": "agent-name",
      "model": "model-identifier",
      "subtask": false
    }
  }
}
```

## Template Features

### 1. Arguments

**All arguments:**
```markdown
Create a component named $ARGUMENTS
```

**Positional arguments:**
```markdown
Create file $1 in directory $2 with content: $3
```

Usage: `/create-file config.json src "{ \"key\": \"value\" }"`

### 2. Shell Command Output

Embed command output with `` !`command` ``:

```markdown
Current test results:
!`npm test`

Analyze these results.
```

### 3. File References

Include file content with `@filename`:

```markdown
Review @src/components/Button.tsx for performance issues.
```

## Configuration Options

| Option | Required | Description |
|--------|----------|-------------|
| `template` | ✅ | Prompt sent to LLM |
| `description` | ❌ | Shown in TUI |
| `agent` | ❌ | Which agent to use |
| `model` | ❌ | Override default model |
| `subtask` | ❌ | Force subagent invocation |

## Examples

### Testing Workflow

`.opencode/commands/test-all.md`:
```markdown
---
description: Run full test suite
agent: build
---

Run tests with coverage:
!`npm test -- --coverage`

Analyze results and suggest improvements.
```

### Code Review

`.opencode/commands/review.md`:
```markdown
---
description: Review recent changes
agent: reviewer
subtask: true
---

Recent commits:
!`git log --oneline -10`

Changed files:
!`git diff --name-only HEAD~5..HEAD`

Review these changes for:
1. Code quality
2. Security issues
3. Performance concerns
```

### Component Generator

`.opencode/commands/new-component.md`:
```markdown
---
description: Generate React component
agent: code
model: anthropic/claude-sonnet-4-5
---

Create a new React component named $1 in directory $2.

Requirements:
- TypeScript with proper types
- Props interface
- Basic styling with CSS modules
- Unit tests with Jest
- Storybook story

Follow project conventions from @docs/component-guide.md
```

### Database Migration

`.opencode/commands/migrate.md`:
```markdown
---
description: Create database migration
---

Create a migration for: $ARGUMENTS

Current schema:
!`cat prisma/schema.prisma`

Generate migration file with:
- Up migration
- Down migration
- Timestamp prefix
```

## Best Practices

### 1. Naming
- Use clear, descriptive names
- Keep names short and memorable
- Use kebab-case for multi-word names

### 2. Organization
- **Global commands** (`~/.config/opencode/commands/`): General utilities
- **Project commands** (`.opencode/commands/`): Project-specific workflows

### 3. Design
- Keep prompts focused and specific
- Use arguments for flexibility
- Include context with shell outputs
- Reference relevant files

### 4. Performance
- Use `subtask: true` for isolated operations
- Choose appropriate models (smaller for simple tasks)
- Limit shell command output

### 5. Maintenance
- Document complex commands
- Test with different inputs
- Version control project commands
- Share useful commands with team

## Common Patterns

### Run and Analyze
```markdown
Run command:
!`npm run build`

Analyze output and fix any errors.
```

### Context from Multiple Files
```markdown
Review these files:
@src/App.tsx
@src/config.ts
@tests/App.test.tsx

Suggest improvements.
```

### Conditional Logic
```markdown
Check build status:
!`npm run build`

If build fails, analyze errors and suggest fixes.
If build succeeds, proceed with deployment checks.
```

### Multi-Step Workflow
```markdown
1. Run linter: !`npm run lint`
2. Run tests: !`npm test`
3. Check types: !`npm run type-check`

Report all issues and suggest fixes in priority order.
```

## Troubleshooting

### Command Not Found
- Check file location (global vs project)
- Verify filename matches command name
- Restart OpenCode to reload commands

### Arguments Not Working
- Ensure `$ARGUMENTS` or `$1, $2...` are in template
- Quote arguments with spaces: `/command "arg with spaces"`

### Shell Command Fails
- Test command in terminal first
- Check command runs from project root
- Verify command is in PATH

### File Reference Not Found
- Use paths relative to project root
- Check file exists
- Verify file permissions

## Integration

### With Agents
```markdown
---
agent: code
---
Generate implementation following @docs/style-guide.md
```

### With Models
```markdown
---
model: anthropic/claude-haiku-4-5
---
Quick lint check: !`npm run lint`
```

### With Subtasks
```markdown
---
subtask: true
---
Isolated analysis without polluting main context.
```

## Resources

- [OpenCode Commands Documentation](https://opencode.ai/docs/commands/)
- [OpenCode Agents](https://opencode.ai/docs/agents/)
- [OpenCode Config](https://opencode.ai/docs/config/)

## License

MIT License - See repository LICENSE file for details.
