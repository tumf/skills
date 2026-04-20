# Google APIs and Scopes Reference

## Common Google Cloud APIs

| Service | API | Console Link |
|---------|-----|--------------|
| Gmail | Gmail API | https://console.cloud.google.com/apis/api/gmail.googleapis.com |
| Calendar | Google Calendar API | https://console.cloud.google.com/apis/api/calendar-json.googleapis.com |
| Chat | Google Chat API | https://console.cloud.google.com/apis/api/chat.googleapis.com |
| Drive | Google Drive API | https://console.cloud.google.com/apis/api/drive.googleapis.com |
| Docs | Google Docs API | https://console.cloud.google.com/apis/api/docs.googleapis.com |
| Slides | Google Slides API | https://console.cloud.google.com/apis/api/slides.googleapis.com |
| Sheets | Google Sheets API | https://console.cloud.google.com/apis/api/sheets.googleapis.com |
| Forms | Google Forms API | https://console.cloud.google.com/apis/api/forms.googleapis.com |
| Apps Script | Apps Script API | https://console.cloud.google.com/apis/api/script.googleapis.com |
| Classroom | Google Classroom API | https://console.cloud.google.com/apis/api/classroom.googleapis.com |
| Contacts / People | People API | https://console.cloud.google.com/apis/api/people.googleapis.com |
| Tasks | Google Tasks API | https://console.cloud.google.com/apis/api/tasks.googleapis.com |
| Groups | Cloud Identity API | https://console.cloud.google.com/apis/api/cloudidentity.googleapis.com |
| Admin | Admin SDK API | https://console.cloud.google.com/apis/api/admin.googleapis.com |
| Keep | Google Keep API | https://console.cloud.google.com/apis/api/keep.googleapis.com |

## Typical OAuth scopes by service

### Gmail
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/gmail.settings.sharing`
- Read-only option: `--gmail-scope readonly`

### Calendar
- `https://www.googleapis.com/auth/calendar`

### Chat (Workspace only)
- `https://www.googleapis.com/auth/chat.spaces`
- `https://www.googleapis.com/auth/chat.messages`
- `https://www.googleapis.com/auth/chat.memberships`
- `https://www.googleapis.com/auth/chat.users.readstate.readonly`

### Classroom
- `https://www.googleapis.com/auth/classroom.courses`
- `https://www.googleapis.com/auth/classroom.rosters`
- `https://www.googleapis.com/auth/classroom.coursework.students`
- `https://www.googleapis.com/auth/classroom.coursework.me`
- `https://www.googleapis.com/auth/classroom.courseworkmaterials`
- `https://www.googleapis.com/auth/classroom.announcements`
- `https://www.googleapis.com/auth/classroom.topics`
- `https://www.googleapis.com/auth/classroom.guardianlinks.students`
- `https://www.googleapis.com/auth/classroom.profile.emails`
- `https://www.googleapis.com/auth/classroom.profile.photos`

### Drive
- `https://www.googleapis.com/auth/drive`
- Narrower options: `--drive-scope readonly`, `--drive-scope file`

### Docs
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`

### Slides
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/presentations`

### Sheets
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/spreadsheets`

### Contacts
- `https://www.googleapis.com/auth/contacts`
- `https://www.googleapis.com/auth/contacts.other.readonly`
- `https://www.googleapis.com/auth/directory.readonly`

### Tasks
- `https://www.googleapis.com/auth/tasks`

### People
- `profile`

### Forms
- `https://www.googleapis.com/auth/forms.body`
- `https://www.googleapis.com/auth/forms.responses.readonly`

### Apps Script
- `https://www.googleapis.com/auth/script.projects`
- `https://www.googleapis.com/auth/script.deployments`
- `https://www.googleapis.com/auth/script.processes`

### Groups (Workspace only)
- `https://www.googleapis.com/auth/cloud-identity.groups.readonly`

### Keep (Workspace only)
- `https://www.googleapis.com/auth/keep`
- Typically used via service account + domain-wide delegation

### Admin (Workspace only)
- `https://www.googleapis.com/auth/admin.directory.user`
- `https://www.googleapis.com/auth/admin.directory.group`
- `https://www.googleapis.com/auth/admin.directory.group.member`
- Requires service account with domain-wide delegation

## Minimal setup for common agent usage

For the most common read-only automation flows, start with:

- Gmail API
- Google Calendar API
- Google Drive API
- People API

## Workspace-only setup reminder

For Keep, Admin, and many Workspace automation flows:

1. Create a service account in Google Cloud.
2. Enable domain-wide delegation.
3. Allowlist the exact OAuth scopes in Google Workspace Admin Console.
4. Register the key with:

```bash
gog auth service-account set user@domain.com --key key.json
```
