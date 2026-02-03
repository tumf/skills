#!/bin/bash
# Setup Google Cloud project for gogcli with required APIs

set -e

PROJECT_ID="${1:-}"
if [ -z "$PROJECT_ID" ]; then
	echo "Usage: $0 <project-id>"
	exit 1
fi

echo "=== Setting up Google Cloud project for gogcli ==="
echo "Project ID: $PROJECT_ID"
echo ""

# Set active project
echo "1. Setting active project..."
gcloud config set project "$PROJECT_ID"

# Enable required APIs
echo ""
echo "2. Enabling required APIs..."
gcloud services enable \
	gmail.googleapis.com \
	calendar-json.googleapis.com \
	drive.googleapis.com \
	people.googleapis.com \
	tasks.googleapis.com \
	sheets.googleapis.com \
	cloudidentity.googleapis.com \
	chat.googleapis.com \
	classroom.googleapis.com \
	--project="$PROJECT_ID"

echo ""
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure OAuth consent screen:"
echo "   https://console.cloud.google.com/apis/credentials/consent?project=$PROJECT_ID"
echo ""
echo "2. Create OAuth client:"
echo "   https://console.cloud.google.com/apis/credentials/oauthclient?project=$PROJECT_ID"
