# agentic-cli-design

Agent skill for designing and reviewing CLI tools that LLM/AI agents can operate safely and reliably.

This directory contains *skill documentation* (guidance + checklists + templates). It does not ship a CLI binary and does not include executable scripts.

## Installation

Recommended (skills.sh):

```bash
npx skills add tumf/skills --skill agentic-cli-design
```

Alternative: load the skill file directly in your agent configuration:

```jsonc
{
  "instructions": [
    "path/to/agentic-cli-design/SKILL.md"
  ]
}
```

## How To Use The Skill

Once loaded, ask your agent to apply the framework to your CLI or spec.

Example requests:

```text
Review this CLI's output/exit codes for agent compatibility and propose changes.
Design an agent-friendly command structure for this tool (list/get/create/delete).
Create a JSON output schema and error vocabulary for these commands.
Add an introspection command (commands/schema/help) and document it.
```

## What's Included

- `agentic-cli-design/SKILL.md` - Main skill instructions and when to use it
- `agentic-cli-design/references/scorecard.md` - Review checklist you can run against an existing CLI
- `agentic-cli-design/references/templates.md` - Copy/paste templates (JSON responses, exit codes, introspection, auth)
- `agentic-cli-design/references/anti-patterns.md` - Common failure modes that break agent workflows
- `agentic-cli-design/references/principles.md` - Deeper reference material backing the framework

## Notes

- This skill is most effective when paired with real CLI examples (help output, sample stdout/stderr, failure cases) or a concrete command list.
- Use structured output (`--json`) and stable schemas whenever possible so agents can parse results deterministically.

## License

MIT

---

**Last Updated**: February 5, 2026
