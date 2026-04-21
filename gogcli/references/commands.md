# gogcli Commands Reference

This is a condensed agent-oriented command reference aligned with the upstream `steipete/gogcli` README.

## Authentication

```bash
gog auth credentials <path>
gog auth credentials list
gog --client work auth credentials <path>

gog auth add <email>
gog auth add <email> --services drive,calendar
gog auth add <email> --services drive,calendar --readonly
gog auth add <email> --services gmail --gmail-scope readonly
gog auth add <email> --listen-addr 0.0.0.0:8080 --redirect-host gog.example.com

gog auth status        # current/selected account context
gog auth services
gog auth list          # all authenticated accounts
gog auth list --check  # validate stored auth entries
gog auth list --check
gog auth remove <email>

gog auth service-account set <email> --key <path>
gog auth service-account status <email>
gog auth service-account unset <email>

gog auth keyring
gog auth keyring auto
gog auth keyring keychain
gog auth keyring file

gog auth alias set work work@company.com
gog auth alias list
gog auth alias unset work
```

## Gmail

```bash
# Search and read
gog gmail search 'newer_than:7d' --max 10
gog gmail thread get <threadId>
gog gmail thread get <threadId> --download --out-dir ./attachments
gog gmail get <messageId>
gog gmail attachment <messageId> <attachmentId> --out ./attachment.bin
gog gmail url <threadId>

# Send / drafts
gog gmail send --to a@b.com --subject "Hi" --body "Plain fallback"
gog gmail send --to a@b.com --subject "Hi" --body "Plain fallback" --body-html "<p>Hello</p>"
gog gmail drafts list
gog gmail drafts create --subject "Draft" --body "Body"
gog gmail drafts update <draftId> --subject "Draft" --body "Body"
gog gmail drafts send <draftId>

# Labels / filters / settings
gog gmail labels list
gog gmail labels get INBOX --json
gog gmail labels create "My Label"
gog gmail labels rename "Old Label" "New Label"
gog gmail labels delete <labelIdOrName>
gog gmail filters list
gog gmail filters create --from 'noreply@example.com' --add-label 'Notifications'
gog gmail filters export --out ./filters.json
gog gmail delegates list
gog gmail vacation get

# Batch
gog gmail batch delete <messageId1> <messageId2>
gog gmail batch modify <messageId1> <messageId2> --add STARRED --remove INBOX

# Tracking
gog gmail track setup --worker-url https://gog-email-tracker.<acct>.workers.dev
gog gmail track opens <tracking_id>
gog gmail track status

# Watch
gog gmail watch start --topic projects/<p>/topics/<t> --label INBOX
gog gmail watch status
gog gmail watch renew
gog gmail watch stop
gog gmail watch serve --bind 127.0.0.1 --port 8788 --path /gmail-pubsub --token <shared> --hook-url http://127.0.0.1:18789/hooks/agent
gog gmail history --since <historyId>
```

## Calendar

```bash
gog calendar calendars
gog calendar acl <calendarId>
gog calendar colors
gog calendar users

gog calendar events <calendarId> --today
gog calendar events <calendarId> --week
gog calendar events --all
gog calendar search "meeting" --today
gog calendar get <calendarId> <eventId>

gog calendar create <calendarId> --summary "Meeting" --from 2025-01-15T10:00:00Z --to 2025-01-15T11:00:00Z
gog calendar update <calendarId> <eventId> --summary "Updated Meeting"
gog calendar delete <calendarId> <eventId>
gog calendar respond <calendarId> <eventId> --status accepted
gog calendar propose-time <calendarId> <eventId>

gog calendar team <group-email> --today
gog calendar team <group-email> --freebusy
gog calendar freebusy --calendars "primary,work@example.com" --from 2025-01-15T00:00:00Z --to 2025-01-16T00:00:00Z
gog calendar conflicts --all --today

gog calendar focus-time --from 2025-01-15T13:00:00Z --to 2025-01-15T14:00:00Z
gog calendar out-of-office --from 2025-01-20 --to 2025-01-21 --all-day
gog calendar working-location --type office --office-label "HQ" --from 2025-01-22 --to 2025-01-23
```

## Drive

```bash
gog drive ls --max 20
gog drive ls --parent <folderId>
gog drive search "invoice" --max 20
gog drive get <fileId>
gog drive url <fileId>
gog drive copy <fileId> "Copy Name"

gog drive upload ./path/to/file --parent <folderId>
gog drive upload ./path/to/file --replace <fileId>
gog drive upload ./report.docx --convert
gog drive download <fileId> --out ./downloaded.bin
gog drive download <fileId> --format pdf --out ./exported.pdf

gog drive mkdir "New Folder"
gog drive rename <fileId> "New Name"
gog drive move <fileId> --parent <destinationFolderId>
gog drive delete <fileId>
gog drive delete <fileId> --permanent

gog drive permissions <fileId>
gog drive share <fileId> --to user --email user@example.com --role reader
gog drive unshare <fileId> --permission-id <permissionId>
gog drive drives --max 100
```

## Docs / Slides / Sheets

```bash
# Docs
gog docs info <docId>
gog docs cat <docId> --max-bytes 10000
gog docs create "My Doc"
gog docs create "My Doc" --file ./doc.md
gog docs copy <docId> "My Doc Copy"
gog docs export <docId> --format pdf --out ./doc.pdf
gog docs update <docId> --text "Append this later"
gog docs write <docId> --text "Fresh content"
gog docs find-replace <docId> "old" "new"

# Slides
gog slides info <presentationId>
gog slides create "My Deck"
gog slides create-from-markdown "My Deck" --content-file ./slides.md
gog slides create-from-template <templateId> "My Deck" --replace "name=John"
gog slides copy <presentationId> "My Deck Copy"
gog slides export <presentationId> --format pdf --out ./deck.pdf
gog slides list-slides <presentationId>

# Sheets
gog sheets metadata <spreadsheetId>
gog sheets get <spreadsheetId> 'Sheet1!A1:B10'
gog sheets update <spreadsheetId> 'A1' 'val1|val2,val3|val4'
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'new|row|data'
gog sheets clear <spreadsheetId> 'Sheet1!A1:B10'
gog sheets format <spreadsheetId> 'Sheet1!A1:B2' --format-json '{"textFormat":{"bold":true}}' --format-fields 'userEnteredFormat.textFormat.bold'
gog sheets merge <spreadsheetId> 'Sheet1!A1:B2'
gog sheets unmerge <spreadsheetId> 'Sheet1!A1:B2'
gog sheets named-ranges <spreadsheetId>
gog sheets add-tab <spreadsheetId> <tabName>
gog sheets create "My New Spreadsheet" --sheets "Sheet1,Sheet2"
gog sheets export <spreadsheetId> --format pdf --out ./sheet.pdf
```

## Contacts / People / Tasks

```bash
# Contacts
gog contacts list --max 50
gog contacts search "Ada" --max 50
gog contacts get people/<resourceName>
gog contacts create --given "John" --family "Doe" --email "john@example.com"
gog contacts update people/<resourceName> --given "Jane"
gog contacts delete people/<resourceName>
gog contacts other list --max 50
gog contacts directory search "Jane" --max 50

# People
gog people me
gog people get people/<userId>
gog people search "Ada Lovelace" --max 5
gog people relations
gog people relations people/<userId> --type manager

# Tasks
gog tasks lists
gog tasks lists create <title>
gog tasks list <tasklistId> --max 50
gog tasks get <tasklistId> <taskId>
gog tasks add <tasklistId> --title "Task title"
gog tasks update <tasklistId> <taskId> --title "New title"
gog tasks done <tasklistId> <taskId>
gog tasks undo <tasklistId> <taskId>
gog tasks delete <tasklistId> <taskId>
gog tasks clear <tasklistId>
```

## Chat / Forms / Apps Script

```bash
# Chat
gog chat spaces list
gog chat spaces find "Engineering"
gog chat spaces create "Engineering" --member alice@company.com
gog chat messages list spaces/<spaceId> --max 5
gog chat messages send spaces/<spaceId> --text "Build complete!"
gog chat threads list spaces/<spaceId>
gog chat dm send user@company.com --text "ping"

# Forms
gog forms get <formId>
gog forms create --title "Weekly Check-in"
gog forms update <formId> --title "Weekly Sync" --quiz true
gog forms add-question <formId> --title "What shipped?" --type paragraph --required
gog forms responses list <formId> --max 20
gog forms watch create <formId> --topic projects/<project>/topics/<topic>

# Apps Script
gog appscript get <scriptId>
gog appscript content <scriptId>
gog appscript create --title "Automation Helpers"
gog appscript run <scriptId> myFunction --params '["arg1",123,true]'
```

## Workspace-only Commands

```bash
# Keep
gog keep list --account you@yourdomain.com
gog keep get <noteId> --account you@yourdomain.com
gog keep create --title "Todo" --item "Milk" --item "Eggs" --account you@yourdomain.com
gog keep delete <noteId> --account you@yourdomain.com --force

# Groups
gog groups list
gog groups members engineering@company.com

# Admin
gog admin users list --domain example.com
gog admin users get user@example.com
gog admin groups list --domain example.com
gog admin groups members list engineering@example.com

# Classroom
gog classroom courses list
gog classroom courses get <courseId>
```

## Notes

- Prefer `--json` for machine parsing.
- Confirm account selection with `gog auth status` before writes.
- Keep, Admin, and many Workspace flows require service account + domain-wide delegation.
- Chat and Groups are typically Workspace-only scenarios.
