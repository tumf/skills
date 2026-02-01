# OpenCode Agent Examples

This directory contains example agent configurations demonstrating different use cases and patterns.

## Available Examples

### Primary Agents

#### debug.md
**Purpose**: Systematic debugging and issue investigation  
**Key Features**:
- Read-only with bash access
- Low temperature (0.2) for focused analysis
- Edit permission requires confirmation
- Methodical debugging approach

**Usage**: Switch to debug agent with Tab key when investigating issues

### Subagents

#### code-reviewer.md
**Purpose**: Code review without making changes  
**Key Features**:
- Read-only (no write/edit)
- Git commands allowed for inspection
- Low temperature (0.1) for consistent analysis
- Focus on quality, bugs, performance, security

**Usage**: `@code-reviewer please review src/components/Button.tsx`

#### docs-writer.md
**Purpose**: Technical documentation creation  
**Key Features**:
- Full file operations
- No bash access
- Medium temperature (0.3) for clear writing
- Structured documentation approach

**Usage**: `@docs-writer create API documentation for the user service`

#### security-auditor.md
**Purpose**: Security vulnerability identification  
**Key Features**:
- Read-only (no write/edit/bash)
- Low temperature (0.1) for thorough analysis
- Comprehensive security checklist
- Severity-based reporting

**Usage**: `@security-auditor audit the authentication module`

## Installation

Copy any example to your agents directory:

```bash
# Global
cp examples/code-reviewer.md ~/.config/opencode/agents/

# Project-specific
cp examples/security-auditor.md .opencode/agents/
```

## Customization

Each example can be customized by modifying:

1. **Model**: Change to faster/cheaper or more capable models
2. **Temperature**: Adjust creativity vs. consistency
3. **Tools**: Enable/disable specific capabilities
4. **Permissions**: Fine-tune approval requirements
5. **Prompt**: Customize guidelines and behavior

## Creating Your Own

Use these examples as templates:

1. Copy an example that's closest to your needs
2. Rename the file (filename = agent name)
3. Update the `description` to match your use case
4. Modify the system prompt
5. Adjust tools and permissions
6. Test with `@your-agent-name` or Tab (for primary agents)

## Common Patterns

### Read-Only Analysis Agent
```yaml
tools:
  write: false
  edit: false
permission:
  bash:
    "*": deny
```

### Investigation Agent
```yaml
tools:
  write: false
permission:
  bash:
    "*": allow
  edit: ask
```

### Documentation Agent
```yaml
tools:
  bash: false
temperature: 0.3-0.5
```

### High-Precision Agent
```yaml
temperature: 0.1-0.2
model: anthropic/claude-sonnet-4-20250514
```

## Tips

- **Start restrictive**: Add permissions later if needed
- **Test incrementally**: Try with simple tasks first
- **Iterate prompts**: Refine based on actual outputs
- **Use appropriate temperatures**: Lower for analysis, higher for creativity
- **Name clearly**: Agent names should indicate their purpose

## Resources

- [OpenCode Agents Docs](https://opencode.ai/docs/agents/)
- [Agent Configuration](https://opencode.ai/docs/config/)
- [Model Selection](https://opencode.ai/docs/models)
- [Tool Reference](https://opencode.ai/docs/tools)
