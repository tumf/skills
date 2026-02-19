# Troubleshooting gogcli Setup

## Common Issues and Solutions

### "Access blocked: app has not completed Google verification process"

**Cause**: User is not added as test user in OAuth consent screen.

**Solution**:
1. Open OAuth consent screen: https://console.cloud.google.com/apis/credentials/consent
2. Scroll to "Test users" section
3. Click "ADD USERS"
4. Add your Gmail address
5. Save and retry authentication

### "API not enabled"

**Cause**: Required API not enabled for the project.

**Solution**:
```bash
# Enable specific API
gcloud services enable gmail.googleapis.com --project=PROJECT_ID

# Or use setup script
bash "$SKILL_ROOT/scripts/setup_gcloud_project.sh" PROJECT_ID
```

### "No OAuth client credentials stored"

**Cause**: OAuth client credentials not registered with gog.

**Solution**:
1. Download credentials JSON from Google Cloud Console
2. Validate: `bash "$SKILL_ROOT/scripts/validate_credentials.sh" ~/Downloads/client_secret_*.json`
3. Register: `gog auth credentials ~/Downloads/client_secret_*.json`

### "Invalid client credentials"

**Cause**: Wrong credentials file format or corrupted download.

**Solution**:
1. Re-download credentials from Console
2. Ensure file type is "Desktop app"
3. Validate with script: `bash "$SKILL_ROOT/scripts/validate_credentials.sh" FILE`

### "Token refresh failed"

**Cause**: Revoked or expired refresh token.

**Solution**:
```bash
# Re-authenticate with force consent
gog auth add user@gmail.com --force-consent
```

### "Keychain prompts on macOS"

**Cause**: Different binary paths treated as different apps by Keychain.

**Solutions**:
1. Use stable binary path (recommended)
2. Switch to file backend: `gog auth keyring file`
3. Set password env: `export GOG_KEYRING_PASSWORD=...`

### "403 Insufficient Permission"

**Cause**: Missing required OAuth scopes.

**Solution**:
```bash
# Re-authenticate with all services
gog auth add user@gmail.com --services user --force-consent

# Or specific service
gog auth add user@gmail.com --services gmail,calendar --force-consent
```

### "Project quota exceeded"

**Cause**: Too many API requests.

**Solutions**:
1. Check quota in Cloud Console: https://console.cloud.google.com/apis/dashboard
2. Request quota increase if needed
3. Use different OAuth client for different accounts

## Testing Authentication

After setup, verify with these commands:

```bash
# List accounts
gog auth list

# Check auth status
gog auth status

# Test Gmail access
gog gmail labels list

# Test Calendar access
gog calendar calendars

# Test Drive access
gog drive ls --max 5
```

## Getting Help

- GitHub Issues: https://github.com/steipete/gogcli/issues
- Documentation: https://github.com/steipete/gogcli/blob/main/README.md
- Auth documentation: See `docs/auth-clients.md` in repository
