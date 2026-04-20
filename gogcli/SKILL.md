---
name: gogcli
description: Fast, script-friendly CLI for Google services via `gog`. Use this skill whenever the user needs to work with Gmail, Google Calendar, Drive, Docs, Sheets, Slides, Forms, Apps Script, Contacts, Tasks, People, Chat, Classroom, Groups, Admin, or Keep from the terminal, especially for Google Workspace automation, account setup, OAuth/client configuration, service accounts, domain-wide delegation, or JSON/scriptable workflows. Prefer this skill even when the user does not mention `gog` explicitly but is clearly trying to automate or inspect Google services from a CLI or agent workflow.
---

# gogcli - Google in your terminal

## Overview

`gog` is a script-friendly CLI for Google services with JSON-first output, multiple accounts, and flexible authentication. This skill is for agents that need to inspect or automate Google Workspace and Gmail workflows safely.

Core areas:

- Gmail: search, read, send, drafts, labels, filters, watch webhooks, tracking
- Calendar: events, invites, team calendars, free/busy, conflicts, special event types
- Drive: list/search/upload/download/share/move/delete, shared drives
- Docs / Slides / Sheets: create, copy, export, update, formatting helpers
- Contacts / People / Tasks
- Chat, Classroom, Forms, Apps Script
- Groups, Admin, Keep in Workspace environments

## Installation

See `references/installation.md`.

## Authentication Quick Start

For first-time setup, see `references/oauth.md` and `references/apis.md`.

Minimal happy path:

```bash
gog auth credentials ~/Downloads/client_secret_*.json
gog auth add you@gmail.com

export GOG_ACCOUNT=you@gmail.com
gog auth status
gog gmail labels list
```

## Authentication Model

`gog` supports:

- Multiple accounts via `--account` / `GOG_ACCOUNT`
- Account aliases via `gog auth alias ...`
- Multiple OAuth clients via `--client` / `GOG_CLIENT`
- Keyring backends: `auto`, `keychain`, `file`
- Least-privilege auth with `--readonly`, `--drive-scope`, `--gmail-scope`
- Workspace service accounts with domain-wide delegation

See details in `references/oauth.md`.

## Workspace service accounts

For Workspace-only flows such as Keep or Admin, verify service-account configuration before acting.

Quick check:

```bash
gog --account you@yourdomain.com auth status
```

See full setup in `references/oauth.md`.

## Output and automation conventions

- Default output is human-readable.
- Use `--json` for machine-readable scripting.
- Use `--plain` for stable TSV-like output.
- Human hints/progress go to stderr.
- Prefer read-only discovery before mutating commands.

Recommended preflight pattern:

```bash
gog auth status --json
gog gmail labels list --json
gog calendar calendars --json
gog drive ls --max 5 --json
```

## Common command patterns

See `references/commands.md`.

## Agent guidance

- First confirm the target account with `gog auth status` or explicit `--account`.
- Use `--json` whenever downstream parsing matters.
- Prefer the smallest scope set that can accomplish the task.
- For Workspace-only commands, verify service-account/domain-wide-delegation status first.
- For Gmail watch/tracking flows, verify external webhook URLs and auth before enabling writes.
- Do not assume consumer Gmail accounts can use Chat, Admin, Groups, or Keep service-account flows.

## References

- Upstream repo: https://github.com/steipete/gogcli
- Upstream auth clients doc: https://github.com/steipete/gogcli/blob/main/docs/auth-clients.md
- Upstream Gmail watch doc: https://github.com/steipete/gogcli/blob/main/docs/watch.md
- Local references: `references/installation.md`, `references/oauth.md`, `references/apis.md`, `references/commands.md`, `references/troubleshooting.md`
