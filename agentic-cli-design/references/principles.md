# The 7 Principles of Agentic CLI Design

This document provides detailed explanations, examples, and implementation guidance for each of the 7 core principles.

## P1. Machine-readable (Primary Output Format)

### Principle

Machine-readable output is the primary interface, not human-readable text. Agents need structured, parseable data to make decisions and chain operations.

### Requirements

1. **Structured Output Formats**
   - Provide `--json` / `--output json|yaml|text` as first-class options
   - JSON should be the default or easily accessible format
   - Schema should be stable and versioned

2. **Stream Separation**
   - **stdout**: Results only (parseable data)
   - **stderr**: Logs, progress, diagnostics
   - **Never mix** human-readable messages into stdout when outputting JSON

3. **Structured Errors**
   - Errors should also be structured (JSON preferred)
   - Include error codes, messages, and actionable context
   - Exit codes should complement (not replace) structured errors

4. **Schema Versioning**
   - Include `schemaVersion` field in JSON output
   - Document breaking changes
   - Provide migration guides for schema updates

### Examples

**Good: Clean JSON output**
```bash
$ mycli users list --output json
{
  "schemaVersion": 1,
  "type": "users.list",
  "ok": true,
  "data": {
    "items": [
      {"id": "u123", "name": "Alice", "email": "alice@example.com"},
      {"id": "u456", "name": "Bob", "email": "bob@example.com"}
    ],
    "nextCursor": "eyJpZCI6InU0NTYifQ=="
  }
}
```

**Good: Structured error**
```bash
$ mycli users get --id invalid --output json
{
  "schemaVersion": 1,
  "type": "users.get",
  "ok": false,
  "error": {
    "code": "not_found",
    "message": "User not found: invalid",
    "details": {
      "userId": "invalid",
      "suggestion": "Use 'users list' to see available users"
    }
  }
}
```
Exit code: 1

**Bad: Mixed output**
```bash
$ badcli users list --json
Loading users...
{"users": [{"id": "u123"}]}
Done! Found 1 user.
```
Problem: Progress messages mixed with JSON, making parsing impossible.

### Implementation Checklist

- [ ] Add `--output json` flag to all commands
- [ ] Ensure stdout contains ONLY the result (no logs/progress)
- [ ] Move all diagnostic output to stderr
- [ ] Add `schemaVersion` to all JSON responses
- [ ] Document JSON schema for each command
- [ ] Implement structured error responses
- [ ] Test with `jq` or similar JSON parsers

---

## P2. Non-interactive by Default

### Principle

Interactive prompts should not be the default behavior. Agents cannot respond to prompts, and commands should complete without human intervention.

### Requirements

1. **No Interactive Prompts by Default**
   - Commands should not prompt for input unless explicitly requested
   - All required parameters should be flags or arguments

2. **Explicit Confirmation Flags**
   - Provide `--yes` / `--force` / `--no-confirm` / `--non-interactive`
   - Make dangerous operations require explicit flags

3. **TTY Detection**
   - Detect when running in non-TTY environment (CI, scripts)
   - Automatically disable interactive features when no TTY

4. **Clear Error Messages**
   - When required input is missing, fail with clear error message
   - Suggest the correct flag to provide the missing input

### Examples

**Good: Non-interactive by default**
```bash
# Fails with clear error, doesn't prompt
$ mycli deploy
Error: Missing required flag: --environment
Usage: mycli deploy --environment <env> [--confirm]

# Explicit confirmation required for destructive operation
$ mycli delete --id prod-db
Error: Destructive operation requires --confirm flag
Use: mycli delete --id prod-db --confirm

# Works non-interactively
$ mycli delete --id prod-db --confirm
Deleted: prod-db
```

**Good: TTY detection**
```bash
# In TTY: offers interactive mode
$ mycli deploy
Environment (dev/staging/prod): _

# In non-TTY: fails immediately
$ echo "" | mycli deploy
Error: Missing required flag: --environment (non-interactive mode)
```

**Bad: Interactive by default**
```bash
$ badcli deploy
Environment (dev/staging/prod): _
# Agent gets stuck here forever
```

**Bad: Assumes yes without flag**
```bash
$ badcli delete --id prod-db
Deleting prod-db... done
# Dangerous: no confirmation required
```

### Implementation Checklist

- [ ] Remove all interactive prompts from default behavior
- [ ] Add `--non-interactive` flag (or auto-detect TTY)
- [ ] Add `--yes`/`--force` flags for confirmations
- [ ] Fail fast with clear errors when required input is missing
- [ ] Document all required flags in `--help`
- [ ] Test in CI environment (no TTY)

---

## P3. Idempotent & Replayable

### Principle

Commands should be safe to run multiple times with the same result. Agents may retry operations due to timeouts, errors, or uncertainty about previous execution.

### Requirements

1. **Deduplication Keys**
   - Accept `--client-request-id` / `--dedupe-key` for write operations
   - Use these keys to detect and handle duplicate requests
   - Return success if operation already completed with same key

2. **Conflict Handling**
   - Provide `--if-exists skip|update|error` for create operations
   - Make behavior explicit and configurable
   - Default should be safe (error on conflict, not silent overwrite)

3. **Pagination**
   - Provide `--limit` and `--cursor` for list operations
   - Support `--all` that internally handles pagination
   - Never return unbounded results by default

4. **Deterministic Output**
   - Same input should produce same output (when data unchanged)
   - Avoid random ordering unless explicitly requested
   - Include timestamps/versions for change detection

### Examples

**Good: Idempotent create with dedupe key**
```bash
# First call: creates message
$ mycli messages send \
  --channel general \
  --text "Deploy complete" \
  --dedupe-key deploy-123
{
  "ok": true,
  "messageId": "msg-789",
  "created": true
}

# Retry: detects duplicate, returns same result
$ mycli messages send \
  --channel general \
  --text "Deploy complete" \
  --dedupe-key deploy-123
{
  "ok": true,
  "messageId": "msg-789",
  "created": false,
  "note": "Message already sent with this dedupe key"
}
```

**Good: Explicit conflict handling**
```bash
# Default: error on conflict
$ mycli files upload --path config.json
Error: File already exists: config.json
Use --if-exists skip|update|error

# Explicit update
$ mycli files upload --path config.json --if-exists update
Updated: config.json (version 2)

# Explicit skip
$ mycli files upload --path config.json --if-exists skip
Skipped: config.json (already exists)
```

**Good: Pagination**
```bash
# Limited results with cursor
$ mycli messages list --limit 100 --output json
{
  "items": [...],
  "nextCursor": "eyJpZCI6Im1zZy0xMDAifQ=="
}

# Continue pagination
$ mycli messages list --limit 100 --cursor "eyJpZCI6Im1zZy0xMDAifQ=="

# Get all (internally paginated)
$ mycli messages list --all --output ndjson
{"id": "msg-1", ...}
{"id": "msg-2", ...}
...
```

**Bad: Non-idempotent**
```bash
# Creates duplicate messages on retry
$ badcli send "Deploy complete"
Sent: msg-789

$ badcli send "Deploy complete"
Sent: msg-790  # Duplicate!
```

### Implementation Checklist

- [ ] Add `--client-request-id` to write operations
- [ ] Implement deduplication logic (store request IDs)
- [ ] Add `--if-exists` flag for create operations
- [ ] Implement pagination with `--limit` and `--cursor`
- [ ] Add `--all` flag that handles pagination internally
- [ ] Ensure deterministic output ordering
- [ ] Document idempotency guarantees

---

## P4. Safe-by-default

### Principle

Destructive operations require explicit confirmation. Default behavior should prevent accidents, not enable them.

### Requirements

1. **Dry-run Support**
   - Provide `--dry-run` for destructive operations
   - Show what would happen without executing
   - Return structured output showing planned changes

2. **Explicit Confirmation**
   - Require `--confirm <id>` or `--force` for destructive operations
   - Make users/agents explicitly acknowledge the risk
   - Fail safely if confirmation is missing

3. **Minimal Permissions**
   - Request minimum necessary permissions/scopes
   - Fail with clear error if permissions insufficient
   - Provide "next steps" to acquire needed permissions

4. **Reversibility**
   - Provide undo/rollback where possible
   - Support soft-delete with recovery period
   - Log operations for audit trail

### Examples

**Good: Dry-run before execution**
```bash
# Dry-run shows plan
$ mycli delete --channel old-channel --dry-run --output json
{
  "ok": true,
  "dryRun": true,
  "plan": {
    "action": "delete",
    "resource": "channel",
    "id": "C123456",
    "name": "old-channel",
    "messageCount": 1543,
    "memberCount": 23,
    "warnings": [
      "This channel has 1543 messages that will be permanently deleted",
      "23 members will lose access"
    ]
  },
  "confirmationId": "delete-C123456-20260205"
}

# Execute with confirmation
$ mycli delete --channel old-channel --confirm delete-C123456-20260205
{
  "ok": true,
  "deleted": true,
  "channelId": "C123456"
}
```

**Good: Safe defaults**
```bash
# Fails without explicit force
$ mycli database drop --name production
Error: Destructive operation requires --force flag
This will permanently delete database 'production' and all data.
Use: mycli database drop --name production --force

# Requires explicit confirmation
$ mycli database drop --name production --force
Dropped: production
```

**Good: Permission errors with next steps**
```bash
$ mycli channels create --name new-channel
Error: Insufficient permissions
Required scope: channels:write
Current scopes: channels:read, users:read

Next steps:
1. Run: mycli auth reauthorize --add-scope channels:write
2. Retry this command
```

**Bad: Destructive by default**
```bash
$ badcli delete old-channel
Deleted: old-channel (1543 messages, 23 members)
# No confirmation, no dry-run, no recovery
```

### Implementation Checklist

- [ ] Add `--dry-run` to all destructive operations
- [ ] Require `--force` or `--confirm <id>` for execution
- [ ] Show impact summary in dry-run output
- [ ] Implement permission checking with clear errors
- [ ] Provide "next steps" for permission errors
- [ ] Consider soft-delete with recovery period
- [ ] Log all destructive operations

---

## P5. Observable & Debuggable

### Principle

Operations must be traceable and debuggable. Agents need to understand what happened, why it failed, and how to recover.

### Requirements

1. **Verbose Logging**
   - Provide `--verbose` / `--debug` flags
   - Output detailed logs to stderr (never stdout)
   - Include timing, API calls, retry attempts

2. **Structured Logs**
   - Support `--log-format json` for machine-readable logs
   - Include correlation IDs, timestamps, context
   - Make logs parseable and searchable

3. **Trace IDs**
   - Accept `--trace-id` for correlation across systems
   - Include trace ID in all logs and API calls
   - Enable distributed tracing

4. **Categorized Exit Codes**
   - Use specific exit codes for different failure types
   - Enable automatic retry/recovery logic
   - Document exit code meanings

### Exit Code Convention

| Code | Meaning | Agent Action |
|------|---------|--------------|
| 0 | Success | Continue |
| 2 | Invalid arguments/usage | Fix arguments, don't retry |
| 3 | Authentication/permission | Re-authenticate, then retry |
| 4 | Retryable error (rate limit, transient) | Wait and retry |
| 1 | Other errors | Log and report |

### Examples

**Good: Structured logging**
```bash
$ mycli messages send --text "Hello" --debug --log-format json 2>debug.log
{
  "ok": true,
  "messageId": "msg-123"
}

$ cat debug.log
{"level":"debug","time":"2026-02-05T10:00:00Z","msg":"Starting message send","channel":"general","text":"Hello"}
{"level":"debug","time":"2026-02-05T10:00:01Z","msg":"API request","method":"POST","url":"https://api.example.com/messages","traceId":"trace-abc"}
{"level":"info","time":"2026-02-05T10:00:02Z","msg":"Message sent","messageId":"msg-123","duration":"2.1s"}
```

**Good: Trace ID support**
```bash
$ mycli messages send --text "Hello" --trace-id req-xyz-123
{
  "ok": true,
  "messageId": "msg-123",
  "traceId": "req-xyz-123"
}
```

**Good: Categorized exit codes**
```bash
# Rate limited
$ mycli messages send --text "Hello"
{
  "ok": false,
  "error": {
    "code": "rate_limited",
    "message": "Rate limit exceeded",
    "retryAfterMs": 1200
  }
}
$ echo $?
4  # Retryable error

# Authentication failed
$ mycli messages send --text "Hello"
{
  "ok": false,
  "error": {
    "code": "auth_required",
    "message": "Authentication token expired"
  }
}
$ echo $?
3  # Auth error

# Invalid argument
$ mycli messages send
{
  "ok": false,
  "error": {
    "code": "invalid_arguments",
    "message": "Missing required flag: --text"
  }
}
$ echo $?
2  # Usage error
```

**Bad: No observability**
```bash
$ badcli send "Hello"
Error
$ echo $?
1  # What kind of error? Should I retry?
```

### Implementation Checklist

- [ ] Add `--verbose` and `--debug` flags
- [ ] Implement `--log-format json`
- [ ] Add `--trace-id` support
- [ ] Use categorized exit codes (0, 2, 3, 4)
- [ ] Include timing information in logs
- [ ] Log all API calls and retries
- [ ] Document exit codes in `--help`

---

## P6. Context-efficient

### Principle

Minimize token/context consumption for LLM agents. Large outputs consume tokens and slow down processing.

### Requirements

1. **Field Projection**
   - Provide `--fields` / `--select` to choose specific fields
   - Default output should be minimal/summary
   - Full details available via explicit flags

2. **Streaming Output**
   - Support `--output ndjson` for line-by-line JSON
   - Enable processing large datasets without loading all into memory
   - Allow agents to stop reading when they have enough data

3. **Opt-in Heavy Fields**
   - Large fields (bodies, content, metadata) should be opt-in
   - Use `--include-body` / `--include-metadata` flags
   - Default response excludes heavy fields

4. **Server-side Filtering**
   - Provide rich filtering options (since/until/query/type)
   - Filter on server before returning data
   - Avoid returning data that will be filtered client-side

### Examples

**Good: Field projection**
```bash
# Default: minimal fields
$ mycli messages list --limit 5 --output json
{
  "items": [
    {"id": "msg-1", "timestamp": "2026-02-05T10:00:00Z", "user": "alice"},
    {"id": "msg-2", "timestamp": "2026-02-05T10:01:00Z", "user": "bob"}
  ]
}

# Select specific fields
$ mycli messages list --limit 5 --fields id,text --output json
{
  "items": [
    {"id": "msg-1", "text": "Hello"},
    {"id": "msg-2", "text": "Hi there"}
  ]
}

# Include heavy fields explicitly
$ mycli messages list --limit 5 --include-reactions --include-thread --output json
{
  "items": [
    {
      "id": "msg-1",
      "text": "Hello",
      "reactions": [...],
      "thread": {...}
    }
  ]
}
```

**Good: NDJSON streaming**
```bash
# Stream results line-by-line
$ mycli messages list --all --output ndjson
{"id":"msg-1","text":"Hello"}
{"id":"msg-2","text":"Hi"}
{"id":"msg-3","text":"How are you?"}
...

# Agent can stop reading early
$ mycli messages list --all --output ndjson | head -n 10
```

**Good: Server-side filtering**
```bash
# Filter by date range
$ mycli messages list --since 2026-02-01 --until 2026-02-05

# Filter by user
$ mycli messages list --user alice

# Filter by query
$ mycli messages list --query "deploy complete"

# Combine filters
$ mycli messages list --since 2026-02-01 --user alice --query "error"
```

**Bad: Always returns everything**
```bash
$ badcli messages list
{
  "items": [
    {
      "id": "msg-1",
      "text": "Hello",
      "user": {...},  # Full user object
      "channel": {...},  # Full channel object
      "reactions": [...],  # All reactions
      "thread": {...},  # Full thread
      "metadata": {...}  # All metadata
    },
    # ... 1000 more messages
  ]
}
# Consumes massive context, most data unused
```

### Implementation Checklist

- [ ] Add `--fields` / `--select` for field projection
- [ ] Implement `--output ndjson` for streaming
- [ ] Make heavy fields opt-in with `--include-*` flags
- [ ] Add server-side filtering (--since, --until, --query, --type)
- [ ] Default to summary/minimal output
- [ ] Document available fields and filters
- [ ] Test with large datasets

---

## P7. Introspectable (Self-describing CLI)

### Principle

The CLI itself can emit its specification in machine-readable format. Agents should be able to discover capabilities without reading documentation.

### Requirements

1. **Command Discovery**
   - Provide `commands --json` to list all commands
   - Include command descriptions, arguments, flags
   - Make it easy to discover what the CLI can do

2. **Schema Export**
   - Provide `schema --command <cmd> --output json-schema`
   - Export JSON Schema for command input/output
   - Enable validation and code generation

3. **Structured Help**
   - Support `--help --json` for machine-readable help
   - Include examples, exit codes, error codes
   - Make help parseable and searchable

4. **Response Metadata**
   - Include `schemaVersion` in all JSON responses
   - Include `type` field indicating response type
   - Include `ok` boolean for success/failure

### Examples

**Good: Command discovery**
```bash
$ mycli commands --json
{
  "commands": [
    {
      "name": "messages",
      "description": "Manage messages",
      "subcommands": [
        {
          "name": "list",
          "description": "List messages",
          "flags": [
            {"name": "channel", "type": "string", "required": false},
            {"name": "limit", "type": "integer", "default": 20},
            {"name": "cursor", "type": "string", "required": false}
          ]
        },
        {
          "name": "send",
          "description": "Send a message",
          "flags": [
            {"name": "channel", "type": "string", "required": true},
            {"name": "text", "type": "string", "required": true},
            {"name": "dedupe-key", "type": "string", "required": false}
          ]
        }
      ]
    }
  ]
}
```

**Good: Schema export**
```bash
$ mycli schema --command messages.list --output json-schema
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "schemaVersion": {"type": "integer", "const": 1},
    "type": {"type": "string", "const": "messages.list"},
    "ok": {"type": "boolean"},
    "data": {
      "type": "object",
      "properties": {
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {"type": "string"},
              "text": {"type": "string"},
              "timestamp": {"type": "string", "format": "date-time"}
            }
          }
        },
        "nextCursor": {"type": "string"}
      }
    }
  }
}
```

**Good: Structured help**
```bash
$ mycli messages send --help --json
{
  "command": "messages send",
  "description": "Send a message to a channel",
  "usage": "mycli messages send --channel <channel> --text <text> [flags]",
  "flags": [
    {
      "name": "channel",
      "type": "string",
      "required": true,
      "description": "Channel to send message to"
    },
    {
      "name": "text",
      "type": "string",
      "required": true,
      "description": "Message text"
    },
    {
      "name": "dedupe-key",
      "type": "string",
      "required": false,
      "description": "Deduplication key for idempotent sends"
    }
  ],
  "examples": [
    {
      "description": "Send a simple message",
      "command": "mycli messages send --channel general --text 'Hello world'"
    },
    {
      "description": "Send with deduplication",
      "command": "mycli messages send --channel general --text 'Deploy complete' --dedupe-key deploy-123"
    }
  ],
  "exitCodes": [
    {"code": 0, "description": "Success"},
    {"code": 2, "description": "Invalid arguments"},
    {"code": 3, "description": "Authentication required"},
    {"code": 4, "description": "Rate limited (retry after delay)"}
  ],
  "errorCodes": [
    {"code": "channel_not_found", "description": "Specified channel does not exist"},
    {"code": "rate_limited", "description": "Rate limit exceeded"},
    {"code": "auth_required", "description": "Authentication token expired"}
  ]
}
```

**Good: Response metadata**
```bash
$ mycli messages list --output json
{
  "schemaVersion": 1,
  "type": "messages.list",
  "ok": true,
  "data": {
    "items": [...]
  }
}
```

### Implementation Checklist

- [ ] Implement `commands --json` for command discovery
- [ ] Implement `schema --command <cmd> --output json-schema`
- [ ] Add `--help --json` to all commands
- [ ] Include `schemaVersion`, `type`, `ok` in all JSON responses
- [ ] Document all error codes
- [ ] Provide examples in structured help
- [ ] Document exit codes

---

## Summary

These 7 principles work together to create CLIs that agents can:

1. **Parse reliably** (P1: Machine-readable)
2. **Run without getting stuck** (P2: Non-interactive)
3. **Retry safely** (P3: Idempotent)
4. **Avoid breaking things** (P4: Safe-by-default)
5. **Debug and recover** (P5: Observable)
6. **Use efficiently** (P6: Context-efficient)
7. **Discover and understand** (P7: Introspectable)

When designing a CLI, prioritize these principles in order of your use case:
- **For automation/CI**: P2, P3, P5 are critical
- **For agent use**: All 7 are important, especially P1, P6, P7
- **For production systems**: P4, P5 are non-negotiable

Use the [scorecard](scorecard.md) to evaluate your CLI against these principles.
