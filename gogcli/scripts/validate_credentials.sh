#!/bin/bash
# Validate gogcli OAuth credentials JSON file

set -e

CREDS_FILE="${1:-}"
if [ -z "$CREDS_FILE" ]; then
	echo "Usage: $0 <credentials.json>"
	exit 1
fi

if [ ! -f "$CREDS_FILE" ]; then
	echo "Error: File not found: $CREDS_FILE"
	exit 1
fi

echo "=== Validating credentials file ==="
echo "File: $CREDS_FILE"
echo ""

# Check if it's valid JSON
if ! jq empty "$CREDS_FILE" 2>/dev/null; then
	echo "❌ Error: Invalid JSON format"
	exit 1
fi

# Check for required fields
REQUIRED_FIELDS=(
	".installed.client_id"
	".installed.client_secret"
	".installed.project_id"
	".installed.auth_uri"
	".installed.token_uri"
)

for field in "${REQUIRED_FIELDS[@]}"; do
	if ! jq -e "$field" "$CREDS_FILE" >/dev/null 2>&1; then
		echo "❌ Error: Missing required field: $field"
		exit 1
	fi
done

# Extract and display key information
CLIENT_ID=$(jq -r '.installed.client_id' "$CREDS_FILE")
PROJECT_ID=$(jq -r '.installed.project_id' "$CREDS_FILE")

echo "✅ Credentials file is valid"
echo ""
echo "Project ID: $PROJECT_ID"
echo "Client ID: $CLIENT_ID"
echo ""
echo "Ready to register with gog:"
echo "  gog auth credentials $CREDS_FILE"
