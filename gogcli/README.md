# gogcli

Agent skill for Google Workspace automation using the `gog` CLI from `steipete/gogcli`.

This skill is aligned to the upstream project README and focuses on safe, scriptable usage for agents.

## Installation

See `gogcli/references/installation.md`.

## What This Skill Covers

Use this skill whenever an agent needs to automate or inspect Google services from the terminal, especially in scriptable or multi-step workflows such as:

- Gmail: search, read, send, labels, drafts, filters, tracking, watch webhooks
- Calendar: list/search/create/update/delete events, invitations, free/busy, team calendars
- Drive: list/search/upload/download/share/organize files and shared drives
- Docs / Sheets / Slides: create, copy, export, and structured edits
- Contacts / People / Tasks
- Chat, Classroom, Forms, Apps Script
- Groups, Admin, Keep for Google Workspace environments
- Multi-account auth, named OAuth clients, service accounts, command allowlists

The skill is optimized for JSON-first automation, multiple accounts, flexible auth, and least-privilege access.

## Prerequisites

See `gogcli/references/installation.md`, `gogcli/references/oauth.md`, and `gogcli/references/apis.md`.

## Included Files

- `gogcli/SKILL.md` — main skill instructions and usage patterns
- `gogcli/references/installation.md` — installation and bootstrap reference
- `gogcli/references/oauth.md` — OAuth and authentication reference
- `gogcli/references/apis.md` — API/service enablement reference
- `gogcli/references/commands.md` — command reference and examples
- `gogcli/references/troubleshooting.md` — common auth/setup failure modes
- `gogcli/scripts/setup_gcloud_project.sh` — helper to enable Google APIs
- `gogcli/scripts/validate_credentials.sh` — sanity check for downloaded OAuth client JSON

## Quick Start

1. Follow `gogcli/references/installation.md`.
2. Follow `gogcli/references/oauth.md`.
3. Test with a harmless read-only command.

Example:

```bash
gog auth credentials ~/Downloads/client_secret_*.json
gog auth add you@gmail.com

gog auth list
export GOG_ACCOUNT=you@gmail.com
gog gmail labels list
```

Use `gog auth list` to verify which accounts are authenticated. `gog auth status` is only for the currently selected account context.

## Recommended Safety Pattern

Start with read-only discovery commands before performing writes like sending email, creating calendar events, or mutating Drive files.

Good first checks:

```bash
gog auth status
gog gmail labels list
gog calendar calendars
gog drive ls --max 5
```

Then move to write actions only after the target account, resource IDs, and scopes are confirmed.

## License

MIT
