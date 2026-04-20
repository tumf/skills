# OAuth and Authentication Reference

This reference collects first-time authentication details for `gog`.

## 1. Create OAuth credentials

Create a Desktop OAuth client in Google Cloud Console:

1. Open credentials: https://console.cloud.google.com/apis/credentials
2. Create a project: https://console.cloud.google.com/projectcreate
3. Enable the APIs you need. Common ones:
   - Gmail API: https://console.cloud.google.com/apis/api/gmail.googleapis.com
   - Google Calendar API: https://console.cloud.google.com/apis/api/calendar-json.googleapis.com
   - Google Drive API: https://console.cloud.google.com/apis/api/drive.googleapis.com
   - Google Docs API: https://console.cloud.google.com/apis/api/docs.googleapis.com
   - Google Sheets API: https://console.cloud.google.com/apis/api/sheets.googleapis.com
   - Google Slides API: https://console.cloud.google.com/apis/api/slides.googleapis.com
   - People API: https://console.cloud.google.com/apis/api/people.googleapis.com
   - Google Tasks API: https://console.cloud.google.com/apis/api/tasks.googleapis.com
   - Google Chat API: https://console.cloud.google.com/apis/api/chat.googleapis.com
   - Google Classroom API: https://console.cloud.google.com/apis/api/classroom.googleapis.com
   - Google Forms API: https://console.cloud.google.com/apis/api/forms.googleapis.com
   - Apps Script API: https://console.cloud.google.com/apis/api/script.googleapis.com
   - Cloud Identity API: https://console.cloud.google.com/apis/api/cloudidentity.googleapis.com
   - Admin SDK API: https://console.cloud.google.com/apis/api/admin.googleapis.com
   - Google Keep API: https://console.cloud.google.com/apis/api/keep.googleapis.com
4. Configure OAuth branding: https://console.cloud.google.com/auth/branding
5. If the app is in testing, add test users: https://console.cloud.google.com/auth/audience
6. Create a Desktop OAuth client: https://console.cloud.google.com/auth/clients

Helpful local scripts:

```bash
bash "$SKILL_ROOT/scripts/setup_gcloud_project.sh" PROJECT_ID
bash "$SKILL_ROOT/scripts/validate_credentials.sh" ~/Downloads/client_secret_*.json
```

## 2. Store credentials

```bash
gog auth credentials ~/Downloads/client_secret_*.json
```

For multiple OAuth clients/projects:

```bash
gog --client work auth credentials ~/Downloads/work-client.json
gog auth credentials list
```

## 3. Authorize account

### Standard browser flow

```bash
gog auth add you@gmail.com
```

### Manual flow for headless / remote hosts

```bash
gog auth add you@gmail.com --services user --manual
```

### Split remote flow

```bash
gog auth add you@gmail.com --services user --remote --step 1
gog auth add you@gmail.com --services user --remote --step 2 --auth-url 'http://127.0.0.1:<port>/oauth2/callback?code=...&state=...'
```

### Proxy / tunnel callback flow

```bash
gog auth add you@gmail.com --listen-addr 0.0.0.0:8080 --redirect-host gog.example.com
```

### Direct access token mode

```bash
gog --access-token "$(gcloud auth print-access-token)" gmail labels list
```

## 4. Test auth safely

```bash
export GOG_ACCOUNT=you@gmail.com
gog auth status
gog gmail labels list
gog calendar calendars
gog drive ls --max 5
```

## Multiple accounts

```bash
gog gmail search 'newer_than:7d' --account you@gmail.com
export GOG_ACCOUNT=you@gmail.com

gog auth alias set work work@company.com
gog gmail search 'newer_than:7d' --account work
```

## Multiple OAuth clients

```bash
gog --client work auth credentials ~/Downloads/work.json
gog --client work auth add you@company.com
gog --client work auth credentials ~/Downloads/work.json --domain example.com
```

See upstream details: https://github.com/steipete/gogcli/blob/main/docs/auth-clients.md

## Keyring backends

```bash
gog auth keyring
gog auth keyring keychain
gog auth keyring file
```

For non-interactive file backend runs:

```bash
export GOG_KEYRING_PASSWORD='...'
```

## Least-privilege scopes

```bash
gog auth add you@gmail.com --services drive,calendar --readonly
gog auth add you@gmail.com --services drive --drive-scope readonly
gog auth add you@gmail.com --services gmail --gmail-scope readonly
```

If scopes changed and refresh token is not reissued:

```bash
gog auth add you@gmail.com --services user --force-consent
```

## Workspace service accounts

For Google Workspace environments:

1. Create a service account in Google Cloud.
2. Enable domain-wide delegation.
3. Allowlist required scopes in Admin Console.
4. Configure the account in `gog`.

```bash
gog auth service-account set you@yourdomain.com --key ~/Downloads/service-account.json
gog --account you@yourdomain.com auth status
```

Notes:

- Keep is Workspace-only and expects service account + domain-wide delegation.
- Admin commands also require Workspace service-account setup.
- Groups requires Cloud Identity API and Workspace permissions.
