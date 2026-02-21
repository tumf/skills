# oss-publish

Skill for making a project ready to publish as open source and to cut releases reliably.

## What You Get

- `oss-publish/SKILL.md`: agent instructions
- `oss-publish/references/checklist.md`: preflight checklists
- `oss-publish/references/templates.md`: copy/paste templates for common policy files
- `oss-publish/references/readme.md`: README.md writing guide + copy/paste template

## Install The Skill

Recommended:

```bash
npx skills add tumf/skills --skill oss-publish
```

Alternative: load directly from the directory:

```jsonc
{
  "instructions": ["path/to/oss-publish/SKILL.md"]
}
```

## Example Trigger Phrases

- "Open source this repo and prepare the standard files."
- "Cut a release with tags and release notes, safely."
- "Add SECURITY.md and a vulnerability reporting process."
- "Set up CI matrix across Linux/macOS/Windows and add pre-commit checks."
