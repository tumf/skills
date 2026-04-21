# Troubleshooting gogcli Setup

## Common Issues and Solutions

### "Access blocked" or unverified app during OAuth

**Cause**: The OAuth app is in testing and your account is not listed as a test user.

**Solution**:
1. Open branding: https://console.cloud.google.com/auth/branding
2. Open audience: https://console.cloud.google.com/auth/audience
3. Add your Google account as a test user
4. Retry `gog auth add ...`

### "No OAuth client credentials stored"

**Cause**: You have not stored a Desktop OAuth client JSON in `gog` yet.

**Solution**:
1. Download the Desktop OAuth client JSON from https://console.cloud.google.com/auth/clients
2. Validate it if needed:
   ```bash
   bash "$SKILL_ROOT/scripts/validate_credentials.sh" ~/Downloads/client_secret_*.json
   ```
3. Register it:
   ```bash
   gog auth credentials ~/Downloads/client_secret_*.json
   ```

### "Invalid client credentials"

**Cause**: Wrong file type, malformed JSON, or a corrupted download.

**Solution**:
1. Re-download the credentials file
2. Ensure it is a **Desktop app** OAuth client
3. Validate with the helper script

### "API not enabled"

**Cause**: The target Google API is not enabled in the Cloud project used by your OAuth client.

**Solution**:
```bash
bash "$SKILL_ROOT/scripts/setup_gcloud_project.sh" PROJECT_ID
```

Or enable the required API directly in Cloud Console.

### "403 insufficient permissions"

**Cause**: Missing OAuth scopes or token was created with narrower access than the command requires.

**Solution**:
```bash
# Broad user services
gog auth add user@gmail.com --services user --force-consent

# Or a targeted re-auth
gog auth add user@gmail.com --services gmail,calendar --force-consent

# Examples of explicit narrow scopes
gog auth add user@gmail.com --services drive --drive-scope readonly
gog auth add user@gmail.com --services gmail --gmail-scope readonly
```

### Refresh token not updated after adding scopes

**Cause**: Google may not reissue a refresh token unless consent is forced.

**Solution**:
```bash
gog auth add user@gmail.com --services sheets --force-consent
```

### Headless / remote machine cannot complete browser auth

**Cause**: No local browser or callback cannot reach the machine.

**Solution**:
Use one of these flows:

```bash
# Manual flow
gog auth add you@gmail.com --services user --manual

# Two-step remote flow
gog auth add you@gmail.com --services user --remote --step 1
gog auth add you@gmail.com --services user --remote --step 2 --auth-url 'http://127.0.0.1:<port>/oauth2/callback?code=...&state=...'

# Reverse proxy / tunnel callback
gog auth add you@gmail.com --listen-addr 0.0.0.0:8080 --redirect-host gog.example.com
```

### Keychain prompts repeatedly on macOS

**Cause**: macOS Keychain treats different binary paths as different apps.

**Solutions**:
1. Use a stable `gog` binary path
2. Force keychain backend:
   ```bash
   export GOG_KEYRING_BACKEND=keychain
   ```
3. Or switch to encrypted file backend:
   ```bash
   gog auth keyring file
   export GOG_KEYRING_PASSWORD='...'
   ```

### Workspace service account commands fail

**Cause**: Domain-wide delegation is incomplete, wrong scopes are allowlisted, or the account is not configured.

**Check**:
1. Service account exists and has domain-wide delegation enabled
2. Required scopes are allowlisted in Admin Console
3. The key is registered in `gog`

```bash
gog auth service-account set you@yourdomain.com --key ~/Downloads/service-account.json
gog --account you@yourdomain.com auth status
gog auth list
```

### Keep / Admin / Groups not working on consumer Gmail

**Cause**: These commands depend on Google Workspace capabilities.

**Solution**:
- Use a Workspace account where required
- For Keep/Admin, configure service account + domain-wide delegation
- For Groups, enable Cloud Identity API and grant the needed scope

### Gmail watch webhook issues

**Cause**: Pub/Sub push auth, callback routing, or Gmail history timing.

**Checks**:
```bash
gog gmail watch status
gog gmail watch renew
gog gmail history --since <historyId>
```

Notes:
- `watch serve --fetch-delay` defaults to `3s` upstream and helps avoid Gmail History indexing races.
- `watch serve --exclude-labels` defaults to `SPAM,TRASH`.
- See upstream watch docs: https://github.com/steipete/gogcli/blob/main/docs/watch.md

## Safe verification commands

After setup, verify with harmless reads first:

```bash
gog auth list
gog auth status
gog gmail labels list
gog calendar calendars
gog drive ls --max 5
```

If `gog auth status` looks unauthenticated, confirm with `gog auth list` first. `status` is about the active account context, not the full authenticated-account inventory.

## Getting Help

- GitHub Issues: https://github.com/steipete/gogcli/issues
- Upstream README: https://github.com/steipete/gogcli/blob/main/README.md
- Upstream auth clients doc: https://github.com/steipete/gogcli/blob/main/docs/auth-clients.md
- Upstream watch doc: https://github.com/steipete/gogcli/blob/main/docs/watch.md
