# gogcli

Agent skill for Google Workspace and Gmail automation using the `gog` / `gogcli` command-line tool.

This directory contains the skill instructions plus helper scripts and reference docs for setting up OAuth, enabling APIs, and using Google Workspace services from automation.

## Installation

Recommended:

```bash
npx skills add tumf/skills --skill gogcli
```

Alternative: load the skill file directly in your agent configuration:

```jsonc
{
  "instructions": [
    "path/to/gogcli/SKILL.md"
  ]
}
```

## What This Skill Covers

Use this skill when an agent needs to automate or inspect Google Workspace services such as:

- Gmail: search, read, send, label, filter, download attachments
- Calendar: list, search, create, and update events
- Drive: upload, download, organize, and inspect files
- Docs / Sheets / Slides: read, write, and export content
- Contacts, Tasks, Chat, Classroom, Groups, and Keep

The skill is optimized for scriptable workflows, JSON-first output, multi-account usage, and least-privilege authentication.

## Prerequisites

Install the CLI and verify it is available on the machine where the agent runs.

Typical setup paths:

```bash
# Homebrew
brew install steipete/tap/gogcli

# Verify install
which gog || which gogcli
```

You will also need:

- `gcloud` CLI
- A Google account (Gmail or Google Workspace)
- A Google Cloud project with the relevant APIs enabled
- OAuth desktop credentials for the target account(s)

## Included Files

- `gogcli/SKILL.md` — main skill instructions and usage patterns
- `gogcli/references/apis.md` — API/service enablement reference
- `gogcli/references/commands.md` — command reference and examples
- `gogcli/references/troubleshooting.md` — common auth/setup failure modes
- `gogcli/scripts/setup_gcloud_project.sh` — helper to enable required Google APIs
- `gogcli/scripts/validate_credentials.sh` — sanity check for downloaded OAuth client JSON

## Quick Start

1. Set up or select a Google Cloud project.
2. Enable the required APIs.
3. Configure the OAuth consent screen.
4. Create a desktop OAuth client.
5. Add the credentials file to `gog`.
6. Authorize the desired Google account.
7. Test with a harmless read-only command.

Example:

```bash
bash "$SKILL_ROOT/scripts/setup_gcloud_project.sh" PROJECT_ID

gog auth credentials ~/Downloads/client_secret_*.json
gog auth add you@gmail.com

export GOG_ACCOUNT=you@gmail.com
gog gmail labels list
```

## Recommended Safety Pattern

Start with read-only discovery commands before performing writes like sending email, creating calendar events, or mutating Drive files.

Good first checks:

```bash
gog gmail labels list
gog calendar calendars
gog drive ls --max 5
```

Then move to write actions only after the target account, resource IDs, and scopes are confirmed.

## License

MIT
