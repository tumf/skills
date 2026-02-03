# Google APIs and Scopes Reference

## Required APIs by Service

| Service | API | Console Link |
|---------|-----|--------------|
| Gmail | Gmail API | https://console.cloud.google.com/apis/api/gmail.googleapis.com |
| Calendar | Google Calendar API | https://console.cloud.google.com/apis/api/calendar-json.googleapis.com |
| Chat | Google Chat API | https://console.cloud.google.com/apis/api/chat.googleapis.com |
| Drive | Google Drive API | https://console.cloud.google.com/apis/api/drive.googleapis.com |
| Classroom | Google Classroom API | https://console.cloud.google.com/apis/api/classroom.googleapis.com |
| Contacts | People API | https://console.cloud.google.com/apis/api/people.googleapis.com |
| Tasks | Google Tasks API | https://console.cloud.google.com/apis/api/tasks.googleapis.com |
| Sheets | Google Sheets API | https://console.cloud.google.com/apis/api/sheets.googleapis.com |
| Groups | Cloud Identity API | https://console.cloud.google.com/apis/api/cloudidentity.googleapis.com |

## OAuth Scopes by Service

### Gmail
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/gmail.settings.sharing`

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

### Docs
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`

### Contacts
- `https://www.googleapis.com/auth/contacts`
- `https://www.googleapis.com/auth/contacts.other.readonly`
- `https://www.googleapis.com/auth/directory.readonly`

### Tasks
- `https://www.googleapis.com/auth/tasks`

### Sheets
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/spreadsheets`

### People
- `profile` (OIDC profile scope)

### Groups (Workspace only)
- `https://www.googleapis.com/auth/cloud-identity.groups.readonly`

## Minimal Setup (Core Services)

For basic gogcli usage, enable these APIs:
- Gmail API
- Google Calendar API
- Google Drive API
- People API

## Service Account Setup (Workspace Only)

For Google Workspace with domain-wide delegation:
1. Create service account in Google Cloud Console
2. Enable domain-wide delegation
3. Download JSON key
4. Configure in Workspace Admin Console
5. Register with gog: `gog auth service-account set user@domain.com --key key.json`
