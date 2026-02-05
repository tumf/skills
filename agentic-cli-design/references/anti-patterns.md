# Agentic CLI Design Anti-Patterns

This document catalogs common failure patterns that break agent compatibility. Each anti-pattern includes the problem, why it fails, and how to fix it.

## Table of Contents

1. [Output Anti-Patterns](#output-anti-patterns)
2. [Interaction Anti-Patterns](#interaction-anti-patterns)
3. [Idempotency Anti-Patterns](#idempotency-anti-patterns)
4. [Safety Anti-Patterns](#safety-anti-patterns)
5. [Context Anti-Patterns](#context-anti-patterns)
6. [Authentication Anti-Patterns](#authentication-anti-patterns)
7. [Error Handling Anti-Patterns](#error-handling-anti-patterns)

---

## Output Anti-Patterns

### AP-O1: Mixed stdout/stderr

**Problem**: Logs, progress messages, or diagnostics mixed with result data on stdout.

**Why it fails**: Agents cannot parse the output. JSON parsers fail when encountering non-JSON text.

**Example (Bad)**:
```bash
$ badcli users list --json
Loading users...
{"users": [{"id": "u123", "name": "Alice"}]}
Done! Found 1 user.
```

**Agent impact**: 
```python
import json
output = subprocess.check_output(["badcli", "users", "list", "--json"])
data = json.loads(output)  # ❌ JSONDecodeError: Expecting value
```

**Fix**:
```bash
# Correct: stdout = data only, stderr = logs
$ goodcli users list --json 2>debug.log
{"ok":true,"data":{"users":[{"id":"u123","name":"Alice"}]}}

$ cat debug.log
2026-02-05 10:00:00 INFO Loading users...
2026-02-05 10:00:01 INFO Found 1 user
```

**Implementation**:
```python
# Bad
print("Loading users...")  # Goes to stdout
print(json.dumps(result))
print("Done!")

# Good
import sys
sys.stderr.write("Loading users...\n")
print(json.dumps(result))  # Only result to stdout
sys.stderr.write("Done!\n")
```

---

### AP-O2: Inconsistent JSON Schema

**Problem**: JSON structure changes based on conditions, making parsing unreliable.

**Why it fails**: Agents cannot rely on consistent field names or types.

**Example (Bad)**:
```bash
# Success: returns array
$ badcli users list --json
[{"id": "u123", "name": "Alice"}]

# No results: returns object
$ badcli users list --json
{"message": "No users found"}

# Error: returns string
$ badcli users list --json
"Error: connection failed"
```

**Agent impact**: Agent must handle 3+ different response shapes, leading to brittle code.

**Fix**:
```bash
# Consistent structure for all cases
$ goodcli users list --json
{"ok":true,"data":{"items":[{"id":"u123","name":"Alice"}]}}

$ goodcli users list --json
{"ok":true,"data":{"items":[]}}

$ goodcli users list --json
{"ok":false,"error":{"code":"connection_failed","message":"Connection failed"}}
```

**Implementation**:
```python
# Bad
if users:
    return json.dumps(users)
elif not users:
    return json.dumps({"message": "No users found"})
else:
    return json.dumps("Error: " + str(error))

# Good
def success_response(data):
    return json.dumps({"ok": True, "data": data})

def error_response(code, message):
    return json.dumps({"ok": False, "error": {"code": code, "message": message}})

if error:
    print(error_response("connection_failed", str(error)))
else:
    print(success_response({"items": users}))
```

---

### AP-O3: No Schema Versioning

**Problem**: Breaking changes to JSON output without version indicator.

**Why it fails**: Agents cannot detect when output format has changed, leading to parsing errors.

**Example (Bad)**:
```bash
# Version 1.0
$ badcli users list --json
{"users": [{"id": "u123"}]}

# Version 2.0 (breaking change)
$ badcli users list --json
{"data": {"items": [{"userId": "u123"}]}}
# Field renamed: users → data.items, id → userId
```

**Agent impact**: Agent written for v1.0 breaks when CLI updates to v2.0.

**Fix**:
```bash
# Version 1
$ goodcli users list --json
{"schemaVersion":1,"users":[{"id":"u123"}]}

# Version 2 (with migration path)
$ goodcli users list --json
{"schemaVersion":2,"data":{"items":[{"userId":"u123"}]}}

# Support both versions or provide clear migration
$ goodcli users list --json --schema-version 1
{"schemaVersion":1,"users":[{"id":"u123"}]}
```

**Implementation**:
```python
SCHEMA_VERSION = 2

def format_response(data, schema_version=SCHEMA_VERSION):
    if schema_version == 1:
        # Legacy format
        return {"schemaVersion": 1, "users": data}
    else:
        # Current format
        return {"schemaVersion": 2, "data": {"items": data}}
```

---

### AP-O4: Human-readable Only

**Problem**: No machine-readable output format available.

**Why it fails**: Agents cannot parse human-readable text reliably.

**Example (Bad)**:
```bash
$ badcli users list
Users:
  - Alice (u123) <alice@example.com>
  - Bob (u456) <bob@example.com>
Total: 2 users
```

**Agent impact**: Must use fragile regex parsing, breaks with formatting changes.

**Fix**:
```bash
$ goodcli users list --output json
{"ok":true,"data":{"items":[
  {"id":"u123","name":"Alice","email":"alice@example.com"},
  {"id":"u456","name":"Bob","email":"bob@example.com"}
]}}
```

---

## Interaction Anti-Patterns

### AP-I1: Interactive by Default

**Problem**: Commands prompt for input by default, blocking non-interactive execution.

**Why it fails**: Agents cannot respond to prompts, causing indefinite hangs.

**Example (Bad)**:
```bash
$ badcli deploy
Environment (dev/staging/prod): _
# Agent hangs here forever
```

**Agent impact**: Command never completes, agent times out or gets stuck.

**Fix**:
```bash
# Option 1: Require flags
$ goodcli deploy --environment prod
Deployed to prod

# Option 2: Fail with clear error
$ goodcli deploy
Error: Missing required flag: --environment
Usage: goodcli deploy --environment <env>

# Option 3: Non-interactive flag
$ goodcli deploy --non-interactive
Error: Missing required flag: --environment (non-interactive mode)
```

**Implementation**:
```python
# Bad
env = input("Environment (dev/staging/prod): ")

# Good
import sys
if not args.environment:
    if sys.stdin.isatty():
        # Interactive mode: can prompt
        env = input("Environment (dev/staging/prod): ")
    else:
        # Non-interactive mode: fail fast
        print(json.dumps({
            "ok": False,
            "error": {
                "code": "missing_argument",
                "message": "Missing required flag: --environment"
            }
        }))
        sys.exit(2)
```

---

### AP-I2: Confirmation Without Bypass

**Problem**: Destructive operations always prompt for confirmation, no way to bypass.

**Why it fails**: Agents cannot confirm prompts, blocking automation.

**Example (Bad)**:
```bash
$ badcli delete --id prod-db
Are you sure? (yes/no): _
# No --yes or --force flag available
```

**Fix**:
```bash
$ goodcli delete --id prod-db --force
Deleted: prod-db

# Or with confirmation ID from dry-run
$ goodcli delete --id prod-db --dry-run
{"confirmationId": "delete-prod-db-abc123", ...}

$ goodcli delete --id prod-db --confirm delete-prod-db-abc123
Deleted: prod-db
```

---

### AP-I3: Browser-only Authentication

**Problem**: Authentication requires opening a browser, impossible in headless environments.

**Why it fails**: Agents running in containers, CI, or remote servers cannot open browsers.

**Example (Bad)**:
```bash
$ badcli auth login
Opening browser for authentication...
# Opens browser on local machine only
```

**Agent impact**: Cannot authenticate in Docker, CI/CD, remote servers.

**Fix**:
```bash
# Device Authorization Grant (RFC 8628)
$ goodcli auth login
Visit: https://example.com/device
Enter code: WXYZ-5678
Waiting for authorization...

# Or token-based auth
$ goodcli auth login --token $TOKEN

# Or export/import for headless
$ goodcli auth export > creds.json
$ scp creds.json remote:
$ ssh remote "goodcli auth import < creds.json"
```

---

## Idempotency Anti-Patterns

### AP-ID1: No Deduplication

**Problem**: Retrying operations creates duplicates.

**Why it fails**: Agents retry on timeouts/errors, creating duplicate resources.

**Example (Bad)**:
```bash
$ badcli messages send --text "Deploy complete"
Sent: msg-123

# Retry due to timeout
$ badcli messages send --text "Deploy complete"
Sent: msg-124  # Duplicate!
```

**Agent impact**: Multiple identical messages, resources, or actions.

**Fix**:
```bash
$ goodcli messages send --text "Deploy complete" --dedupe-key deploy-v1.2.3
{"ok":true,"data":{"id":"msg-123","created":true}}

# Retry with same key
$ goodcli messages send --text "Deploy complete" --dedupe-key deploy-v1.2.3
{"ok":true,"data":{"id":"msg-123","created":false,"note":"Already sent"}}
```

**Implementation**:
```python
# Store dedupe keys in database
def send_message(text, dedupe_key=None):
    if dedupe_key:
        existing = db.get_by_dedupe_key(dedupe_key)
        if existing:
            return {"id": existing.id, "created": False}
    
    msg = create_message(text)
    if dedupe_key:
        db.store_dedupe_key(dedupe_key, msg.id)
    
    return {"id": msg.id, "created": True}
```

---

### AP-ID2: Unclear Conflict Behavior

**Problem**: Behavior when resource exists is unpredictable or undocumented.

**Why it fails**: Agents don't know if retry will fail, overwrite, or skip.

**Example (Bad)**:
```bash
$ badcli files upload config.json
Uploaded: config.json

$ badcli files upload config.json
Error: File already exists
# No way to control behavior
```

**Fix**:
```bash
$ goodcli files upload config.json --if-exists error
Error: File already exists

$ goodcli files upload config.json --if-exists skip
Skipped: config.json (already exists)

$ goodcli files upload config.json --if-exists update
Updated: config.json (version 2)
```

---

### AP-ID3: Unbounded Pagination

**Problem**: List operations return all results without pagination.

**Why it fails**: Large result sets consume memory and context, may timeout.

**Example (Bad)**:
```bash
$ badcli messages list --all
# Returns 100,000 messages in one JSON array
# Consumes gigabytes of memory, takes minutes
```

**Agent impact**: Out of memory, timeout, context window exceeded.

**Fix**:
```bash
# Default: limited results
$ goodcli messages list
{"items":[...100 items...],"nextCursor":"abc123"}

# Explicit limit
$ goodcli messages list --limit 1000

# Stream with NDJSON
$ goodcli messages list --all --output ndjson
{"id":"msg-1",...}
{"id":"msg-2",...}
...
```

---

## Safety Anti-Patterns

### AP-S1: Destructive Without Confirmation

**Problem**: Destructive operations execute immediately without confirmation.

**Why it fails**: Agents may accidentally destroy data due to bugs or misunderstandings.

**Example (Bad)**:
```bash
$ badcli database drop production
Dropped database: production
# No confirmation, no dry-run, no recovery
```

**Agent impact**: Catastrophic data loss from agent errors.

**Fix**:
```bash
$ goodcli database drop production
Error: Destructive operation requires --force flag

$ goodcli database drop production --dry-run
{"plan":{"action":"drop","database":"production","tables":42,"rows":1000000}}

$ goodcli database drop production --force
Dropped database: production
```

---

### AP-S2: No Dry-run

**Problem**: No way to preview destructive operations before executing.

**Why it fails**: Agents cannot verify operations before committing.

**Example (Bad)**:
```bash
$ badcli delete --channel old-channel
Deleted: old-channel (1543 messages, 23 members)
# No way to preview impact
```

**Fix**:
```bash
$ goodcli delete --channel old-channel --dry-run
{
  "plan": {
    "action": "delete",
    "channel": "old-channel",
    "messagesDeleted": 1543,
    "membersAffected": 23
  },
  "confirmationId": "delete-abc123"
}

$ goodcli delete --channel old-channel --confirm delete-abc123
Deleted: old-channel
```

---

### AP-S3: Overly Permissive Defaults

**Problem**: Default behavior is dangerous or permissive.

**Why it fails**: Agents may unintentionally perform dangerous operations.

**Example (Bad)**:
```bash
# Defaults to production
$ badcli deploy
Deploying to production...

# Defaults to --force
$ badcli delete --id important-data
Deleted: important-data
```

**Fix**:
```bash
# Require explicit environment
$ goodcli deploy
Error: Missing required flag: --environment

# Require explicit confirmation
$ goodcli delete --id important-data
Error: Destructive operation requires --force or --confirm
```

---

## Context Anti-Patterns

### AP-C1: Always Return Everything

**Problem**: Commands always return full objects with all fields.

**Why it fails**: Wastes context window, slows processing, exceeds token limits.

**Example (Bad)**:
```bash
$ badcli messages list --limit 10
{
  "items": [
    {
      "id": "msg-1",
      "text": "Hello",
      "user": {
        "id": "u123",
        "name": "Alice",
        "email": "alice@example.com",
        "profile": {...},  # Full profile object
        "settings": {...}  # Full settings object
      },
      "channel": {...},  # Full channel object
      "reactions": [...],  # All reactions
      "thread": {...},  # Full thread
      "attachments": [...],  # All attachments
      "metadata": {...}  # All metadata
    },
    ...
  ]
}
```

**Agent impact**: 10 messages consume 50KB+ of context, most data unused.

**Fix**:
```bash
# Default: minimal fields
$ goodcli messages list --limit 10
{"items":[
  {"id":"msg-1","text":"Hello","user":"alice","timestamp":"..."},
  ...
]}

# Explicit fields
$ goodcli messages list --limit 10 --fields id,text,user
{"items":[
  {"id":"msg-1","text":"Hello","user":"alice"},
  ...
]}

# Opt-in heavy fields
$ goodcli messages list --limit 10 --include-reactions --include-thread
{"items":[
  {"id":"msg-1","text":"Hello","reactions":[...],"thread":{...}},
  ...
]}
```

---

### AP-C2: No Field Selection

**Problem**: Cannot select specific fields, must receive all data.

**Why it fails**: Agents waste context on unneeded data.

**Example (Bad)**:
```bash
$ badcli users list
# Always returns: id, name, email, profile, settings, preferences, ...
# Agent only needs: id, name
```

**Fix**:
```bash
$ goodcli users list --fields id,name
{"items":[
  {"id":"u123","name":"Alice"},
  {"id":"u456","name":"Bob"}
]}
```

---

### AP-C3: No Streaming Output

**Problem**: Large datasets returned as single JSON array.

**Why it fails**: Must load entire dataset into memory, cannot process incrementally.

**Example (Bad)**:
```bash
$ badcli messages list --all
{
  "items": [
    // 100,000 messages in one array
  ]
}
# Must wait for all data, parse entire JSON
```

**Fix**:
```bash
$ goodcli messages list --all --output ndjson
{"id":"msg-1","text":"Hello"}
{"id":"msg-2","text":"Hi"}
...
# Agent can process line-by-line, stop early
```

---

### AP-C4: No Server-side Filtering

**Problem**: Must fetch all data and filter client-side.

**Why it fails**: Wastes bandwidth, context, and processing time.

**Example (Bad)**:
```bash
# Must fetch all messages, filter locally
$ badcli messages list --all | jq '.items[] | select(.user=="alice")'
```

**Fix**:
```bash
# Server-side filtering
$ goodcli messages list --user alice --since 2026-02-01 --query "error"
{"items":[...]}  # Only matching messages
```

---

## Authentication Anti-Patterns

### AP-A1: Hardcoded Credentials

**Problem**: Credentials stored in code or config files.

**Why it fails**: Security risk, credentials leak in version control.

**Example (Bad)**:
```python
# config.py
API_TOKEN = "sk_live_abc123xyz"  # Hardcoded secret
```

**Fix**:
```python
# Use environment variables
import os
API_TOKEN = os.environ.get("MYCLI_TOKEN")
if not API_TOKEN:
    print(json.dumps({
        "ok": False,
        "error": {
            "code": "auth_required",
            "message": "Missing MYCLI_TOKEN environment variable"
        }
    }))
    sys.exit(3)
```

---

### AP-A2: No Auth Status Check

**Problem**: No way to check if authenticated before running commands.

**Why it fails**: Agents cannot verify prerequisites, leading to failures mid-workflow.

**Example (Bad)**:
```bash
$ badcli messages send --text "Hello"
Error: Not authenticated
# No way to check auth status first
```

**Fix**:
```bash
# Check auth status first
$ goodcli auth status --output json
{"ok":true,"authenticated":true,"user":{"id":"u123"}}

# Or
$ goodcli auth status --output json
{"ok":false,"authenticated":false,"error":{"code":"not_authenticated"}}

# Then proceed with operations
$ goodcli messages send --text "Hello"
```

---

### AP-A3: Unclear Permission Errors

**Problem**: Permission errors don't explain what's needed or how to fix.

**Why it fails**: Agents cannot self-recover from permission issues.

**Example (Bad)**:
```bash
$ badcli channels create --name new-channel
Error: Permission denied
```

**Fix**:
```bash
$ goodcli channels create --name new-channel
{
  "ok": false,
  "error": {
    "code": "permission_denied",
    "message": "Insufficient permissions",
    "details": {
      "requiredScopes": ["channels:write"],
      "currentScopes": ["channels:read", "messages:read"]
    },
    "nextSteps": [
      "Run: goodcli auth reauthorize --add-scope channels:write"
    ]
  }
}
```

---

## Error Handling Anti-Patterns

### AP-E1: Generic Exit Codes

**Problem**: All errors return exit code 1, no differentiation.

**Why it fails**: Agents cannot determine if error is retryable or requires different action.

**Example (Bad)**:
```bash
$ badcli messages send --text "Hello"
Error: Rate limited
$ echo $?
1

$ badcli messages send
Error: Missing argument
$ echo $?
1

$ badcli messages send --text "Hello"
Error: Not authenticated
$ echo $?
1
# All errors return 1, agent can't distinguish
```

**Fix**:
```bash
$ goodcli messages send --text "Hello"
{"ok":false,"error":{"code":"rate_limited",...}}
$ echo $?
4  # Retryable error

$ goodcli messages send
{"ok":false,"error":{"code":"missing_argument",...}}
$ echo $?
2  # Usage error

$ goodcli messages send --text "Hello"
{"ok":false,"error":{"code":"auth_required",...}}
$ echo $?
3  # Auth error
```

---

### AP-E2: No Error Codes

**Problem**: Errors only have human-readable messages, no machine-readable codes.

**Why it fails**: Agents must parse error messages with regex, brittle and unreliable.

**Example (Bad)**:
```bash
$ badcli messages send --text "Hello"
{"error": "Rate limit exceeded: 100 requests per minute"}
# Agent must parse message to detect rate limit
```

**Fix**:
```bash
$ goodcli messages send --text "Hello"
{
  "ok": false,
  "error": {
    "code": "rate_limited",
    "message": "Rate limit exceeded: 100 requests per minute",
    "retryable": true,
    "retryAfterMs": 1200
  }
}
# Agent checks error.code === "rate_limited"
```

---

### AP-E3: No Retry Guidance

**Problem**: Errors don't indicate if retry is appropriate or when to retry.

**Why it fails**: Agents don't know if they should retry or give up.

**Example (Bad)**:
```bash
$ badcli messages send --text "Hello"
{"error": "Service unavailable"}
# Should I retry? When? How many times?
```

**Fix**:
```bash
$ goodcli messages send --text "Hello"
{
  "ok": false,
  "error": {
    "code": "service_unavailable",
    "message": "Service temporarily unavailable",
    "retryable": true,
    "retryAfterMs": 5000,
    "maxRetries": 3
  }
}
```

---

### AP-E4: No Next Steps

**Problem**: Errors don't explain how to fix the problem.

**Why it fails**: Agents cannot self-recover or provide useful feedback.

**Example (Bad)**:
```bash
$ badcli channels create --name new-channel
{"error": "Forbidden"}
```

**Fix**:
```bash
$ goodcli channels create --name new-channel
{
  "ok": false,
  "error": {
    "code": "permission_denied",
    "message": "Insufficient permissions to create channels",
    "nextSteps": [
      "Run: goodcli auth reauthorize --add-scope channels:write",
      "Or contact your workspace admin to grant permissions"
    ]
  }
}
```

---

## Summary: Most Critical Anti-Patterns

### Top 5 High-Impact Anti-Patterns (Fix These First)

1. **AP-O1: Mixed stdout/stderr** → Breaks all JSON parsing
2. **AP-I1: Interactive by default** → Agents hang indefinitely
3. **AP-S1: Destructive without confirmation** → Data loss risk
4. **AP-ID1: No deduplication** → Duplicate operations on retry
5. **AP-E1: Generic exit codes** → Cannot retry intelligently

### Top 5 Medium-Impact Anti-Patterns

6. **AP-O2: Inconsistent JSON schema** → Brittle parsing code
7. **AP-C1: Always return everything** → Context explosion
8. **AP-A2: No auth status check** → Cannot verify prerequisites
9. **AP-ID3: Unbounded pagination** → Memory/timeout issues
10. **AP-E2: No error codes** → Must parse error messages

### Quick Fixes

| Anti-Pattern | Quick Fix | Effort |
|--------------|-----------|--------|
| AP-O1 | Move logs to stderr | Low |
| AP-I1 | Add `--non-interactive` flag | Low |
| AP-E1 | Use exit codes 0/2/3/4 | Low |
| AP-E2 | Add `error.code` field | Low |
| AP-O2 | Standardize response structure | Medium |
| AP-ID1 | Add `--dedupe-key` flag | Medium |
| AP-S1 | Add `--force` requirement | Low |
| AP-C1 | Add `--fields` flag | Medium |
| AP-A2 | Add `auth status` command | Low |
| AP-ID3 | Add pagination | High |

---

## Using This Guide

### For Code Review

1. Check each command against anti-patterns
2. Prioritize high-impact fixes
3. Create issues for each anti-pattern found
4. Track fixes with scorecard

### For New Development

1. Review anti-patterns before designing CLI
2. Use templates from [templates.md](templates.md) to avoid anti-patterns
3. Test with agent scenarios
4. Validate with scorecard

### For Debugging Agent Failures

1. Check error logs for symptoms
2. Match symptoms to anti-patterns
3. Apply recommended fixes
4. Re-test with agent

---

## Next Steps

After reviewing anti-patterns:

1. **Assess** your CLI using [scorecard.md](scorecard.md)
2. **Prioritize** fixes based on impact and effort
3. **Implement** using patterns from [templates.md](templates.md)
4. **Validate** against [principles.md](principles.md)
