# gogcli Commands Reference

## Table of Contents

- [Authentication](#authentication)
- [Gmail](#gmail)
- [Calendar](#calendar)
- [Drive](#drive)
- [Contacts](#contacts)
- [Tasks](#tasks)
- [Sheets](#sheets)
- [Docs](#docs)
- [Slides](#slides)
- [Chat](#chat)
- [Classroom](#classroom)
- [Groups](#groups)
- [Keep](#keep)
- [People](#people)
- [Time](#time)

## Authentication

### Setup and Account Management

```bash
# Store OAuth client credentials
gog auth credentials <path>

# Store named OAuth client for Workspace
gog --client work auth credentials <path>

# List stored OAuth clients
gog auth credentials list

# Authorize account
gog auth add <email>

# Authorize with specific services
gog auth add <email> --services drive,calendar

# Authorize with read-only scopes
gog auth add <email> --services drive,calendar --readonly

# Force re-consent (when adding new scopes)
gog auth add <email> --services sheets --force-consent

# List accounts
gog auth list

# Verify tokens are valid
gog auth list --check

# Show current auth state
gog auth status

# List available services and scopes
gog auth services

# Remove account
gog auth remove <email>
```

### Service Accounts (Workspace only)

```bash
# Configure service account for domain-wide delegation
gog auth service-account set <email> --key <path>

# Check service account status
gog auth service-account status <email>

# Remove service account
gog auth service-account unset <email>
```

### Keyring Management

```bash
# Show current keyring backend
gog auth keyring

# Set keyring backend
gog auth keyring file
gog auth keyring keychain
gog auth keyring auto
```

### Account Aliases

```bash
# Set alias
gog auth alias set work work@company.com

# List aliases
gog auth alias list

# Remove alias
gog auth alias unset work
```

## Gmail

### Search and Read

```bash
# Search threads
gog gmail search 'newer_than:7d' --max 10
gog gmail search 'is:unread' --max 20
gog gmail search 'from:alice@example.com' --max 5

# Search messages (one row per email)
gog gmail messages search 'newer_than:7d' --max 10
gog gmail messages search 'has:attachment' --max 10 --include-body

# Get thread details
gog gmail thread get <threadId>
gog gmail thread get <threadId> --download
gog gmail thread get <threadId> --download --out-dir ./attachments

# Get message
gog gmail get <messageId>
gog gmail get <messageId> --format metadata

# Get attachment
gog gmail attachment <messageId> <attachmentId>
gog gmail attachment <messageId> <attachmentId> --out ./file.bin

# Get Gmail web URL
gog gmail url <threadId>
```

### Send and Compose

```bash
# Send email (plain text)
gog gmail send --to a@b.com --subject "Hello" --body "Message"

# Send email (HTML)
gog gmail send --to a@b.com --subject "Hello" \
  --body "Plain fallback" \
  --body-html "<p>HTML content</p>"

# Send with body from file
gog gmail send --to a@b.com --subject "Hello" --body-file ./msg.txt

# Send with body from stdin
cat message.txt | gog gmail send --to a@b.com --subject "Hello" --body-file -

# Send with tracking (requires setup)
gog gmail send --to a@b.com --subject "Hello" \
  --body-html "<p>Hi!</p>" --track
```

### Drafts

```bash
# List drafts
gog gmail drafts list

# Create draft
gog gmail drafts create --subject "Draft" --body "Content"
gog gmail drafts create --to a@b.com --subject "Draft" --body "Content"

# Update draft
gog gmail drafts update <draftId> --subject "Updated" --body "New content"

# Send draft
gog gmail drafts send <draftId>
```

### Labels

```bash
# List labels
gog gmail labels list

# Get label details (includes message counts)
gog gmail labels get INBOX --json

# Create label
gog gmail labels create "My Label"

# Modify thread labels
gog gmail thread modify <threadId> --add STARRED --remove INBOX
gog gmail labels modify <threadId> --add STARRED --remove INBOX
```

### Batch Operations

```bash
# Batch delete
gog gmail batch delete <msgId1> <msgId2>

# Batch modify labels
gog gmail batch modify <msgId1> <msgId2> --add STARRED --remove INBOX
```

### Filters

```bash
# List filters
gog gmail filters list

# Create filter
gog gmail filters create --from 'noreply@example.com' --add-label 'Notifications'

# Delete filter
gog gmail filters delete <filterId>
```

### Settings

```bash
# Auto-forwarding
gog gmail autoforward get
gog gmail autoforward enable --email forward@example.com
gog gmail autoforward disable

# Forwarding addresses
gog gmail forwarding list
gog gmail forwarding add --email forward@example.com

# Send-as
gog gmail sendas list
gog gmail sendas create --email alias@example.com

# Vacation responder
gog gmail vacation get
gog gmail vacation enable --subject "OOO" --message "..."
gog gmail vacation disable

# Delegation (Workspace)
gog gmail delegates list
gog gmail delegates add --email delegate@example.com
gog gmail delegates remove --email delegate@example.com
```

### Watch (Pub/Sub Push)

```bash
# Start watching
gog gmail watch start --topic projects/<p>/topics/<t> --label INBOX

# Serve webhook endpoint
gog gmail watch serve --bind 127.0.0.1 --token <shared> \
  --hook-url http://127.0.0.1:18789/hooks/agent

# Get history since historyId
gog gmail history --since <historyId>
```

### Email Tracking

```bash
# Setup tracking (per-account)
gog gmail track setup --worker-url https://gog-email-tracker.<acct>.workers.dev

# Check opens
gog gmail track opens <tracking_id>
gog gmail track opens --to recipient@example.com

# View status
gog gmail track status
```

## Calendar

### Calendars

```bash
# List calendars
gog calendar calendars

# Access control rules
gog calendar acl <calendarId>

# Available colors
gog calendar colors

# Current time
gog calendar time --timezone America/New_York

# List workspace users
gog calendar users
```

### Events

```bash
# List events with time filters
gog calendar events <calendarId> --today
gog calendar events <calendarId> --tomorrow
gog calendar events <calendarId> --week
gog calendar events <calendarId> --days 3
gog calendar events <calendarId> --from today --to friday
gog calendar events <calendarId> --from 2025-01-01T00:00:00Z --to 2025-01-08T00:00:00Z

# Include weekday columns
gog calendar events <calendarId> --today --weekday

# All calendars
gog calendar events --all

# Get specific event
gog calendar event <calendarId> <eventId>
gog calendar get <calendarId> <eventId>
gog calendar get <calendarId> <eventId> --json

# Search
gog calendar search "meeting" --today
gog calendar search "meeting" --from 2025-01-01T00:00:00Z --to 2025-01-31T00:00:00Z
```

### Team Calendars (Workspace)

```bash
# Team events
gog calendar team <group-email> --today
gog calendar team <group-email> --week
gog calendar team <group-email> --freebusy
gog calendar team <group-email> --query "standup"
```

### Create and Update

```bash
# Create basic event
gog calendar create <calendarId> \
  --summary "Meeting" \
  --from 2025-01-15T10:00:00Z \
  --to 2025-01-15T11:00:00Z

# Create with attendees
gog calendar create <calendarId> \
  --summary "Team Sync" \
  --from 2025-01-15T14:00:00Z \
  --to 2025-01-15T15:00:00Z \
  --attendees "alice@example.com,bob@example.com" \
  --location "Zoom"

# Send notifications
gog calendar create <calendarId> \
  --summary "Team Sync" \
  --from 2025-01-15T14:00:00Z \
  --to 2025-01-15T15:00:00Z \
  --send-updates all

# Recurrence with reminders
gog calendar create <calendarId> \
  --summary "Payment" \
  --from 2025-02-11T09:00:00-03:00 \
  --to 2025-02-11T09:15:00-03:00 \
  --rrule "RRULE:FREQ=MONTHLY;BYMONTHDAY=11" \
  --reminder "email:3d" \
  --reminder "popup:30m"

# Update event
gog calendar update <calendarId> <eventId> \
  --summary "Updated Meeting" \
  --from 2025-01-15T11:00:00Z \
  --to 2025-01-15T12:00:00Z

# Add attendees (without replacing)
gog calendar update <calendarId> <eventId> \
  --add-attendee "alice@example.com,bob@example.com"

# Delete event
gog calendar delete <calendarId> <eventId>
```

### Special Event Types

```bash
# Focus time
gog calendar create primary \
  --event-type focus-time \
  --from 2025-01-15T13:00:00Z \
  --to 2025-01-15T14:00:00Z

gog calendar focus-time --from 2025-01-15T13:00:00Z --to 2025-01-15T14:00:00Z

# Out of office
gog calendar create primary \
  --event-type out-of-office \
  --from 2025-01-20 \
  --to 2025-01-21 \
  --all-day

gog calendar out-of-office --from 2025-01-20 --to 2025-01-21 --all-day

# Working location
gog calendar create primary \
  --event-type working-location \
  --working-location-type office \
  --working-office-label "HQ" \
  --from 2025-01-22 \
  --to 2025-01-23

gog calendar working-location --type office --office-label "HQ" \
  --from 2025-01-22 --to 2025-01-23
```

### Invitations and Availability

```bash
# Respond to invitation
gog calendar respond <calendarId> <eventId> --status accepted
gog calendar respond <calendarId> <eventId> --status declined
gog calendar respond <calendarId> <eventId> --status tentative
gog calendar respond <calendarId> <eventId> --status declined --send-updates externalOnly

# Propose new time (browser-based)
gog calendar propose-time <calendarId> <eventId>
gog calendar propose-time <calendarId> <eventId> --open
gog calendar propose-time <calendarId> <eventId> --decline --comment "Can we do 5pm?"

# Free/busy
gog calendar freebusy --calendars "primary,work@example.com" \
  --from 2025-01-15T00:00:00Z \
  --to 2025-01-16T00:00:00Z

# Conflicts
gog calendar conflicts --calendars "primary,work@example.com" --today
```

## Drive

### List and Search

```bash
# List files
gog drive ls --max 20
gog drive ls --parent <folderId> --max 20

# Search
gog drive search "invoice" --max 20

# Get file metadata
gog drive get <fileId>

# Get web URL
gog drive url <fileId>

# Copy file
gog drive copy <fileId> "Copy Name"
```

### Upload and Download

```bash
# Upload
gog drive upload ./path/to/file --parent <folderId>

# Download
gog drive download <fileId> --out ./downloaded.bin
gog drive download <fileId> --format pdf --out ./exported.pdf
gog drive download <fileId> --format docx --out ./doc.docx
gog drive download <fileId> --format pptx --out ./slides.pptx
```

### Organize

```bash
# Create folder
gog drive mkdir "New Folder"
gog drive mkdir "New Folder" --parent <parentFolderId>

# Rename
gog drive rename <fileId> "New Name"

# Move
gog drive move <fileId> --parent <destinationFolderId>

# Delete (move to trash)
gog drive delete <fileId>
```

### Permissions

```bash
# List permissions
gog drive permissions <fileId>

# Share
gog drive share <fileId> --email user@example.com --role reader
gog drive share <fileId> --email user@example.com --role writer

# Unshare
gog drive unshare <fileId> --permission-id <permissionId>
```

### Shared Drives

```bash
# List shared drives
gog drive drives --max 100
```

## Contacts

### Personal Contacts

```bash
# List contacts
gog contacts list --max 50

# Search
gog contacts search "Ada" --max 50

# Get contact
gog contacts get people/<resourceName>
gog contacts get user@example.com

# Create contact
gog contacts create \
  --given-name "John" \
  --family-name "Doe" \
  --email "john@example.com" \
  --phone "+1234567890"

# Update contact
gog contacts update people/<resourceName> \
  --given-name "Jane" \
  --email "jane@example.com"

# Delete contact
gog contacts delete people/<resourceName>
```

### Other Contacts

```bash
# List other contacts
gog contacts other list --max 50

# Search other contacts
gog contacts other search "John" --max 50
```

### Directory (Workspace)

```bash
# List directory
gog contacts directory list --max 50

# Search directory
gog contacts directory search "Jane" --max 50
```

## Tasks

### Task Lists

```bash
# List task lists
gog tasks lists --max 50

# Create task list
gog tasks lists create <title>
```

### Tasks

```bash
# List tasks
gog tasks list <tasklistId> --max 50

# Get task
gog tasks get <tasklistId> <taskId>

# Add task
gog tasks add <tasklistId> --title "Task title"
gog tasks add <tasklistId> --title "Weekly sync" --due 2025-02-01 \
  --repeat weekly --repeat-count 4
gog tasks add <tasklistId> --title "Daily standup" --due 2025-02-01 \
  --repeat daily --repeat-until 2025-02-05

# Update task
gog tasks update <tasklistId> <taskId> --title "New title"

# Mark done
gog tasks done <tasklistId> <taskId>

# Undo
gog tasks undo <tasklistId> <taskId>

# Delete task
gog tasks delete <tasklistId> <taskId>

# Clear completed
gog tasks clear <tasklistId>
```

## Sheets

### Read

```bash
# Get metadata
gog sheets metadata <spreadsheetId>

# Read range
gog sheets get <spreadsheetId> 'Sheet1!A1:B10'
```

### Write

```bash
# Update cells
gog sheets update <spreadsheetId> 'A1' 'val1|val2,val3|val4'
gog sheets update <spreadsheetId> 'A1' --values-json '[[\"a\",\"b\"],[\"c\",\"d\"]]'
gog sheets update <spreadsheetId> 'Sheet1!A1:C1' 'new|row|data' \
  --copy-validation-from 'Sheet1!A2:C2'

# Append rows
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'new|row|data'
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'new|row|data' \
  --copy-validation-from 'Sheet1!A2:C2'

# Clear range
gog sheets clear <spreadsheetId> 'Sheet1!A1:B10'
```

### Format

```bash
# Format cells
gog sheets format <spreadsheetId> 'Sheet1!A1:B2' \
  --format-json '{"textFormat":{"bold":true}}' \
  --format-fields 'userEnteredFormat.textFormat.bold'
```

### Create and Export

```bash
# Create spreadsheet
gog sheets create "My New Spreadsheet" --sheets "Sheet1,Sheet2"

# Export (via Drive)
gog sheets export <spreadsheetId> --format pdf --out ./sheet.pdf
gog sheets export <spreadsheetId> --format xlsx --out ./sheet.xlsx
```

## Docs

```bash
# Get info
gog docs info <docId>

# Extract text
gog docs cat <docId> --max-bytes 10000

# Create
gog docs create "My Doc"

# Copy
gog docs copy <docId> "My Doc Copy"

# Export
gog docs export <docId> --format pdf --out ./doc.pdf
gog docs export <docId> --format docx --out ./doc.docx
gog docs export <docId> --format txt --out ./doc.txt
```

## Slides

```bash
# Get info
gog slides info <presentationId>

# Create
gog slides create "My Deck"

# Copy
gog slides copy <presentationId> "My Deck Copy"

# Export
gog slides export <presentationId> --format pptx --out ./deck.pptx
gog slides export <presentationId> --format pdf --out ./deck.pdf
```

## Chat

### Spaces

```bash
# List spaces
gog chat spaces list

# Find space
gog chat spaces find "Engineering"

# Create space
gog chat spaces create "Engineering" \
  --member alice@company.com \
  --member bob@company.com
```

### Messages

```bash
# List messages
gog chat messages list spaces/<spaceId> --max 5
gog chat messages list spaces/<spaceId> --thread <threadId>
gog chat messages list spaces/<spaceId> --unread

# Send message
gog chat messages send spaces/<spaceId> --text "Build complete!"
gog chat messages send spaces/<spaceId> --text "Reply" \
  --thread spaces/<spaceId>/threads/<threadId>
```

### Threads

```bash
# List threads
gog chat threads list spaces/<spaceId>
```

### Direct Messages

```bash
# Get DM space
gog chat dm space user@company.com

# Send DM
gog chat dm send user@company.com --text "ping"
```

## Classroom

### Courses

```bash
# List courses
gog classroom courses list
gog classroom courses list --role teacher

# Get course
gog classroom courses get <courseId>

# Create course
gog classroom courses create --name "Math 101"

# Update course
gog classroom courses update <courseId> --name "Math 102"

# Archive/unarchive
gog classroom courses archive <courseId>
gog classroom courses unarchive <courseId>

# Get URL
gog classroom courses url <courseId>
```

### Roster

```bash
# List roster
gog classroom roster <courseId>
gog classroom roster <courseId> --students

# Add students/teachers
gog classroom students add <courseId> <userId>
gog classroom teachers add <courseId> <userId>
```

### Coursework

```bash
# List coursework
gog classroom coursework list <courseId>

# Get coursework
gog classroom coursework get <courseId> <courseworkId>

# Create coursework
gog classroom coursework create <courseId> \
  --title "Homework 1" \
  --type ASSIGNMENT \
  --state PUBLISHED

# Update coursework
gog classroom coursework update <courseId> <courseworkId> --title "Updated"

# Set assignees
gog classroom coursework assignees <courseId> <courseworkId> \
  --mode INDIVIDUAL_STUDENTS \
  --add-student <studentId>
```

### Materials

```bash
# List materials
gog classroom materials list <courseId>

# Create material
gog classroom materials create <courseId> \
  --title "Syllabus" \
  --state PUBLISHED
```

### Submissions

```bash
# List submissions
gog classroom submissions list <courseId> <courseworkId>

# Get submission
gog classroom submissions get <courseId> <courseworkId> <submissionId>

# Grade submission
gog classroom submissions grade <courseId> <courseworkId> <submissionId> --grade 85

# Return/turn in/reclaim
gog classroom submissions return <courseId> <courseworkId> <submissionId>
gog classroom submissions turn-in <courseId> <courseworkId> <submissionId>
gog classroom submissions reclaim <courseId> <courseworkId> <submissionId>
```

### Announcements

```bash
# List announcements
gog classroom announcements list <courseId>

# Create announcement
gog classroom announcements create <courseId> --text "Welcome!"

# Update announcement
gog classroom announcements update <courseId> <announcementId> --text "Updated"

# Set assignees
gog classroom announcements assignees <courseId> <announcementId> \
  --mode INDIVIDUAL_STUDENTS \
  --add-student <studentId>
```

### Topics, Invitations, Guardians

```bash
# Topics
gog classroom topics list <courseId>
gog classroom topics create <courseId> --name "Unit 1"
gog classroom topics update <courseId> <topicId> --name "Unit 2"

# Invitations
gog classroom invitations list
gog classroom invitations create <courseId> <userId> --role student
gog classroom invitations accept <invitationId>

# Guardians
gog classroom guardians list <studentId>
gog classroom guardians get <studentId> <guardianId>
gog classroom guardians delete <studentId> <guardianId>

# Guardian invitations
gog classroom guardian-invitations list <studentId>
gog classroom guardian-invitations create <studentId> --email parent@example.com

# Profiles
gog classroom profile get
gog classroom profile get <userId>
```

## Groups

```bash
# List groups you belong to
gog groups list

# List group members
gog groups members engineering@company.com
```

## Keep

```bash
# List notes (Workspace only)
gog keep list --account you@yourdomain.com

# Get note
gog keep get <noteId> --account you@yourdomain.com

# Search notes
gog keep search <query> --account you@yourdomain.com

# Download attachment
gog keep attachment <attachmentName> --account you@yourdomain.com --out ./file.bin
```

## People

```bash
# Get profile
gog people me
gog people get people/<userId>

# Search directory
gog people search "Ada Lovelace" --max 5

# Get relations
gog people relations
gog people relations people/<userId> --type manager
```

## Time

```bash
# Current time
gog time now
gog time now --timezone UTC
```

## Global Flags

All commands support:

- `--account <email|alias|auto>` - Account to use
- `--enable-commands <csv>` - Allowlist commands
- `--json` - JSON output
- `--plain` - Plain text output (TSV)
- `--color <mode>` - Color mode (auto/always/never)
- `--force` - Skip confirmations
- `--no-input` - Never prompt
- `--verbose` - Verbose logging
- `--help` - Show help

## Environment Variables

- `GOG_ACCOUNT` - Default account
- `GOG_CLIENT` - OAuth client name
- `GOG_JSON` - Default JSON output
- `GOG_PLAIN` - Default plain output
- `GOG_COLOR` - Color mode
- `GOG_TIMEZONE` - Default timezone
- `GOG_ENABLE_COMMANDS` - Command allowlist
- `GOG_KEYRING_BACKEND` - Keyring backend
- `GOG_KEYRING_PASSWORD` - Keyring password (for file backend)
