# Installation and Setup Reference

This reference collects installation and bootstrap details for the upstream `steipete/gogcli` CLI.

## Install gogcli

### Homebrew

```bash
brew install gogcli
```

### Arch Linux

```bash
yay -S gogcli
```

### Build from source

```bash
git clone https://github.com/steipete/gogcli.git
cd gogcli
make
./bin/gog --help
```

Useful help commands:

```bash
gog --help
gog <group> --help
GOG_HELP=full gog --help
gog --version
```

## Install this skill

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

## Prerequisites

You will typically need:

- A Google account (Gmail or Google Workspace)
- A Google Cloud project with the relevant APIs enabled
- OAuth Desktop client credentials for the target account(s)
- For Workspace-only admin / keep / some groups flows, domain-wide delegation where required

## Initial setup flow

1. Create a Google Cloud project.
2. Enable the APIs you need.
3. Configure OAuth branding / audience.
4. Create a Desktop OAuth client.
5. Store credentials in `gog`.
6. Authorize the desired account.
7. Verify with read-only commands.

## Helpful local scripts

```bash
bash "$SKILL_ROOT/scripts/setup_gcloud_project.sh" PROJECT_ID
bash "$SKILL_ROOT/scripts/validate_credentials.sh" ~/Downloads/client_secret_*.json
```
