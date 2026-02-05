# Agentic CLI Design Templates

This document provides concrete templates and examples for implementing the 7 principles.

## Table of Contents

1. [JSON Response Formats](#json-response-formats)
2. [Exit Code Conventions](#exit-code-conventions)
3. [Introspection Commands](#introspection-commands)
4. [Authentication Patterns](#authentication-patterns)
5. [Error Handling](#error-handling)
6. [Pagination Patterns](#pagination-patterns)
7. [Command Line Flags](#command-line-flags)

---

## JSON Response Formats

### Success Response Template

```json
{
  "schemaVersion": 1,
  "type": "resource.action",
  "ok": true,
  "data": {
    // Actual response data
  },
  "metadata": {
    "requestId": "req-abc-123",
    "timestamp": "2026-02-05T10:00:00Z",
    "duration": 1.23
  }
}
```

### Error Response Template

```json
{
  "schemaVersion": 1,
  "type": "resource.action",
  "ok": false,
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": {
      // Additional context
    },
    "retryable": true,
    "retryAfterMs": 1200
  },
  "metadata": {
    "requestId": "req-abc-123",
    "timestamp": "2026-02-05T10:00:00Z"
  }
}
```

### Paginated Response Template

```json
{
  "schemaVersion": 1,
  "type": "resources.list",
  "ok": true,
  "data": {
    "items": [
      // Array of items
    ],
    "pagination": {
      "nextCursor": "eyJpZCI6IjEyMyJ9",
      "hasMore": true,
      "total": 1543
    }
  }
}
```

### Dry-run Response Template

```json
{
  "schemaVersion": 1,
  "type": "resource.delete",
  "ok": true,
  "dryRun": true,
  "plan": {
    "action": "delete",
    "resource": "channel",
    "id": "C123456",
    "name": "old-channel",
    "impact": {
      "messagesDeleted": 1543,
      "membersAffected": 23,
      "subresourcesDeleted": ["webhooks", "pins"]
    },
    "warnings": [
      "This operation is irreversible",
      "23 members will lose access"
    ]
  },
  "confirmationId": "delete-C123456-20260205-abc123"
}
```

---

## Exit Code Conventions

### Standard Exit Codes

```bash
# Exit code definitions
EXIT_SUCCESS=0           # Operation completed successfully
EXIT_GENERAL_ERROR=1     # General error (unspecified)
EXIT_USAGE_ERROR=2       # Invalid arguments or usage
EXIT_AUTH_ERROR=3        # Authentication or permission error
EXIT_RETRYABLE_ERROR=4   # Transient error (rate limit, network, etc.)
```

### Implementation Example (Bash)

```bash
#!/bin/bash

# Exit code constants
readonly EXIT_SUCCESS=0
readonly EXIT_GENERAL_ERROR=1
readonly EXIT_USAGE_ERROR=2
readonly EXIT_AUTH_ERROR=3
readonly EXIT_RETRYABLE_ERROR=4

# Usage error
if [ -z "$REQUIRED_ARG" ]; then
  echo '{"ok":false,"error":{"code":"missing_argument","message":"Required argument missing"}}' >&1
  exit $EXIT_USAGE_ERROR
fi

# Auth error
if ! check_auth; then
  echo '{"ok":false,"error":{"code":"auth_required","message":"Authentication required"}}' >&1
  exit $EXIT_AUTH_ERROR
fi

# Retryable error
if is_rate_limited; then
  echo '{"ok":false,"error":{"code":"rate_limited","message":"Rate limit exceeded","retryAfterMs":1200}}' >&1
  exit $EXIT_RETRYABLE_ERROR
fi

# Success
echo '{"ok":true,"data":{...}}' >&1
exit $EXIT_SUCCESS
```

### Implementation Example (Python)

```python
import sys
import json

# Exit code constants
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_AUTH_ERROR = 3
EXIT_RETRYABLE_ERROR = 4

def error_response(code, message, **kwargs):
    """Print error response and exit with appropriate code."""
    response = {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
            **kwargs
        }
    }
    print(json.dumps(response))
    
    # Determine exit code based on error code
    if code in ["missing_argument", "invalid_argument", "invalid_format"]:
        sys.exit(EXIT_USAGE_ERROR)
    elif code in ["auth_required", "permission_denied", "token_expired"]:
        sys.exit(EXIT_AUTH_ERROR)
    elif code in ["rate_limited", "service_unavailable", "timeout"]:
        sys.exit(EXIT_RETRYABLE_ERROR)
    else:
        sys.exit(EXIT_GENERAL_ERROR)

def success_response(data):
    """Print success response and exit."""
    response = {
        "ok": True,
        "data": data
    }
    print(json.dumps(response))
    sys.exit(EXIT_SUCCESS)

# Usage
if not args.required_field:
    error_response("missing_argument", "Required field missing: required_field")

if not is_authenticated():
    error_response("auth_required", "Authentication required", 
                   nextSteps=["Run: mycli auth login"])

if is_rate_limited():
    error_response("rate_limited", "Rate limit exceeded", 
                   retryable=True, retryAfterMs=1200)

success_response({"id": "123", "status": "created"})
```

---

## Introspection Commands

### `commands --json` Template

```json
{
  "schemaVersion": 1,
  "type": "introspection.commands",
  "ok": true,
  "data": {
    "commands": [
      {
        "name": "messages",
        "description": "Manage messages",
        "subcommands": [
          {
            "name": "list",
            "description": "List messages in a channel",
            "usage": "mycli messages list [flags]",
            "flags": [
              {
                "name": "channel",
                "type": "string",
                "required": false,
                "description": "Channel to list messages from",
                "default": "general"
              },
              {
                "name": "limit",
                "type": "integer",
                "required": false,
                "description": "Maximum number of messages to return",
                "default": 20
              },
              {
                "name": "cursor",
                "type": "string",
                "required": false,
                "description": "Pagination cursor"
              },
              {
                "name": "output",
                "type": "string",
                "required": false,
                "description": "Output format",
                "enum": ["json", "yaml", "text", "ndjson"],
                "default": "text"
              }
            ],
            "examples": [
              "mycli messages list --channel general --limit 10",
              "mycli messages list --output json",
              "mycli messages list --cursor eyJpZCI6IjEyMyJ9"
            ]
          },
          {
            "name": "send",
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
              "mycli messages send --channel general --text 'Hello world'",
              "mycli messages send --channel general --text 'Deploy complete' --dedupe-key deploy-123"
            ]
          }
        ]
      },
      {
        "name": "auth",
        "description": "Manage authentication",
        "subcommands": [
          {
            "name": "login",
            "description": "Authenticate with the service"
          },
          {
            "name": "status",
            "description": "Check authentication status"
          },
          {
            "name": "logout",
            "description": "Remove authentication credentials"
          }
        ]
      }
    ]
  }
}
```

### `schema --command <cmd> --output json-schema` Template

```json
{
  "schemaVersion": 1,
  "type": "introspection.schema",
  "ok": true,
  "data": {
    "command": "messages.list",
    "inputSchema": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "properties": {
        "channel": {
          "type": "string",
          "description": "Channel to list messages from"
        },
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 1000,
          "default": 20
        },
        "cursor": {
          "type": "string",
          "description": "Pagination cursor"
        }
      }
    },
    "outputSchema": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "required": ["schemaVersion", "type", "ok"],
      "properties": {
        "schemaVersion": {
          "type": "integer",
          "const": 1
        },
        "type": {
          "type": "string",
          "const": "messages.list"
        },
        "ok": {
          "type": "boolean"
        },
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
                  "user": {"type": "string"},
                  "timestamp": {"type": "string", "format": "date-time"}
                },
                "required": ["id", "text", "user", "timestamp"]
              }
            },
            "pagination": {
              "type": "object",
              "properties": {
                "nextCursor": {"type": "string"},
                "hasMore": {"type": "boolean"}
              }
            }
          }
        },
        "error": {
          "type": "object",
          "properties": {
            "code": {"type": "string"},
            "message": {"type": "string"},
            "details": {"type": "object"}
          }
        }
      }
    }
  }
}
```

### `--help --json` Template

```json
{
  "schemaVersion": 1,
  "type": "introspection.help",
  "ok": true,
  "data": {
    "command": "messages send",
    "description": "Send a message to a channel",
    "usage": "mycli messages send --channel <channel> --text <text> [flags]",
    "flags": [
      {
        "name": "channel",
        "shorthand": "c",
        "type": "string",
        "required": true,
        "description": "Channel to send message to"
      },
      {
        "name": "text",
        "shorthand": "t",
        "type": "string",
        "required": true,
        "description": "Message text"
      },
      {
        "name": "dedupe-key",
        "type": "string",
        "required": false,
        "description": "Deduplication key for idempotent sends"
      },
      {
        "name": "output",
        "shorthand": "o",
        "type": "string",
        "required": false,
        "description": "Output format (json|yaml|text)",
        "default": "text"
      }
    ],
    "examples": [
      {
        "description": "Send a simple message",
        "command": "mycli messages send --channel general --text 'Hello world'"
      },
      {
        "description": "Send with deduplication",
        "command": "mycli messages send -c general -t 'Deploy complete' --dedupe-key deploy-123"
      },
      {
        "description": "Send with JSON output",
        "command": "mycli messages send -c general -t 'Hello' -o json"
      }
    ],
    "exitCodes": [
      {"code": 0, "description": "Success"},
      {"code": 2, "description": "Invalid arguments (missing required flag)"},
      {"code": 3, "description": "Authentication required or permission denied"},
      {"code": 4, "description": "Rate limited (retry after delay)"}
    ],
    "errorCodes": [
      {
        "code": "channel_not_found",
        "description": "Specified channel does not exist",
        "retryable": false,
        "suggestion": "Use 'mycli channels list' to see available channels"
      },
      {
        "code": "rate_limited",
        "description": "Rate limit exceeded",
        "retryable": true,
        "suggestion": "Wait for retryAfterMs and retry"
      },
      {
        "code": "auth_required",
        "description": "Authentication token expired or invalid",
        "retryable": false,
        "suggestion": "Run 'mycli auth login' to re-authenticate"
      }
    ]
  }
}
```

---

## Authentication Patterns

### `auth status --json` Template

```json
{
  "schemaVersion": 1,
  "type": "auth.status",
  "ok": true,
  "data": {
    "authenticated": true,
    "user": {
      "id": "U123456",
      "name": "Alice",
      "email": "alice@example.com"
    },
    "workspace": {
      "id": "W789012",
      "name": "My Workspace"
    },
    "scopes": [
      "channels:read",
      "channels:write",
      "messages:read",
      "messages:write"
    ],
    "tokenExpiry": "2026-03-05T10:00:00Z",
    "tokenValid": true
  }
}
```

### `auth status --json` (Not Authenticated)

```json
{
  "schemaVersion": 1,
  "type": "auth.status",
  "ok": false,
  "data": {
    "authenticated": false,
    "reason": "No credentials found"
  },
  "error": {
    "code": "not_authenticated",
    "message": "Not authenticated",
    "nextSteps": [
      "Run: mycli auth login"
    ]
  }
}
```

### Device Authorization Flow Template

```bash
# Step 1: Initiate device flow
$ mycli auth login --output json
{
  "ok": true,
  "type": "auth.device_flow_initiated",
  "data": {
    "deviceCode": "ABCD-1234",
    "userCode": "WXYZ-5678",
    "verificationUri": "https://example.com/device",
    "verificationUriComplete": "https://example.com/device?code=WXYZ-5678",
    "expiresIn": 900,
    "interval": 5
  },
  "instructions": [
    "1. Visit: https://example.com/device",
    "2. Enter code: WXYZ-5678",
    "3. Waiting for authorization..."
  ]
}

# Step 2: Poll for completion (automatic)
# ...

# Step 3: Success
{
  "ok": true,
  "type": "auth.login_success",
  "data": {
    "authenticated": true,
    "user": {
      "id": "U123456",
      "name": "Alice"
    },
    "scopes": ["channels:read", "messages:write"]
  }
}
```

### `auth export` / `auth import` Template

```bash
# Export credentials (encrypted)
$ mycli auth export --output json
{
  "ok": true,
  "type": "auth.export",
  "data": {
    "encrypted": true,
    "format": "age",
    "credentials": "-----BEGIN AGE ENCRYPTED FILE-----\n...\n-----END AGE ENCRYPTED FILE-----"
  },
  "instructions": [
    "Save this output to a secure location",
    "Import on another machine with: mycli auth import"
  ]
}

# Import credentials
$ mycli auth import --file credentials.json
{
  "ok": true,
  "type": "auth.import",
  "data": {
    "authenticated": true,
    "user": {
      "id": "U123456",
      "name": "Alice"
    }
  }
}
```

---

## Error Handling

### Common Error Codes

```json
{
  "errorCodes": [
    {
      "code": "missing_argument",
      "exitCode": 2,
      "retryable": false,
      "category": "usage"
    },
    {
      "code": "invalid_argument",
      "exitCode": 2,
      "retryable": false,
      "category": "usage"
    },
    {
      "code": "auth_required",
      "exitCode": 3,
      "retryable": false,
      "category": "auth"
    },
    {
      "code": "permission_denied",
      "exitCode": 3,
      "retryable": false,
      "category": "auth"
    },
    {
      "code": "token_expired",
      "exitCode": 3,
      "retryable": false,
      "category": "auth"
    },
    {
      "code": "rate_limited",
      "exitCode": 4,
      "retryable": true,
      "category": "transient"
    },
    {
      "code": "service_unavailable",
      "exitCode": 4,
      "retryable": true,
      "category": "transient"
    },
    {
      "code": "timeout",
      "exitCode": 4,
      "retryable": true,
      "category": "transient"
    },
    {
      "code": "not_found",
      "exitCode": 1,
      "retryable": false,
      "category": "client"
    },
    {
      "code": "already_exists",
      "exitCode": 1,
      "retryable": false,
      "category": "client"
    }
  ]
}
```

### Error Response Examples

**Rate Limited**:
```json
{
  "ok": false,
  "error": {
    "code": "rate_limited",
    "message": "Rate limit exceeded: 100 requests per minute",
    "retryable": true,
    "retryAfterMs": 1200,
    "details": {
      "limit": 100,
      "remaining": 0,
      "resetAt": "2026-02-05T10:01:00Z"
    }
  }
}
```

**Authentication Required**:
```json
{
  "ok": false,
  "error": {
    "code": "auth_required",
    "message": "Authentication required",
    "retryable": false,
    "nextSteps": [
      "Run: mycli auth login",
      "Or set environment variable: MYCLI_TOKEN"
    ]
  }
}
```

**Permission Denied**:
```json
{
  "ok": false,
  "error": {
    "code": "permission_denied",
    "message": "Insufficient permissions",
    "retryable": false,
    "details": {
      "requiredScopes": ["channels:write"],
      "currentScopes": ["channels:read", "messages:read"]
    },
    "nextSteps": [
      "Run: mycli auth reauthorize --add-scope channels:write"
    ]
  }
}
```

**Not Found**:
```json
{
  "ok": false,
  "error": {
    "code": "not_found",
    "message": "Channel not found: non-existent-channel",
    "retryable": false,
    "details": {
      "resource": "channel",
      "id": "non-existent-channel"
    },
    "nextSteps": [
      "Use: mycli channels list --output json"
    ]
  }
}
```

---

## Pagination Patterns

### Cursor-based Pagination

```bash
# First page
$ mycli messages list --limit 100 --output json
{
  "ok": true,
  "data": {
    "items": [...],
    "pagination": {
      "nextCursor": "eyJpZCI6Im1zZy0xMDAiLCJ0cyI6MTczODc1MjAwMH0=",
      "hasMore": true,
      "total": 1543
    }
  }
}

# Next page
$ mycli messages list --limit 100 --cursor "eyJpZCI6Im1zZy0xMDAiLCJ0cyI6MTczODc1MjAwMH0=" --output json
{
  "ok": true,
  "data": {
    "items": [...],
    "pagination": {
      "nextCursor": "eyJpZCI6Im1zZy0yMDAiLCJ0cyI6MTczODc1MTAwMH0=",
      "hasMore": true,
      "total": 1543
    }
  }
}

# Last page
$ mycli messages list --limit 100 --cursor "..." --output json
{
  "ok": true,
  "data": {
    "items": [...],
    "pagination": {
      "nextCursor": null,
      "hasMore": false,
      "total": 1543
    }
  }
}
```

### `--all` Flag (Internal Pagination)

```bash
# NDJSON output for streaming
$ mycli messages list --all --output ndjson
{"id":"msg-1","text":"Hello","timestamp":"2026-02-05T10:00:00Z"}
{"id":"msg-2","text":"Hi","timestamp":"2026-02-05T10:01:00Z"}
{"id":"msg-3","text":"How are you?","timestamp":"2026-02-05T10:02:00Z"}
...

# JSON output (all items in array)
$ mycli messages list --all --output json
{
  "ok": true,
  "data": {
    "items": [
      {"id":"msg-1",...},
      {"id":"msg-2",...},
      ...
    ],
    "total": 1543
  }
}
```

---

## Command Line Flags

### Standard Flags (All Commands)

```bash
--output, -o        Output format (json|yaml|text|ndjson) [default: text]
--verbose, -v       Verbose output (to stderr)
--debug             Debug output (to stderr)
--log-format        Log format (text|json) [default: text]
--trace-id          Trace ID for correlation
--non-interactive   Disable interactive prompts
--help, -h          Show help
--version           Show version
```

### Write Operation Flags

```bash
--dedupe-key        Deduplication key for idempotent operations
--if-exists         Behavior if resource exists (skip|update|error) [default: error]
--dry-run           Show what would happen without executing
--confirm           Confirmation ID from dry-run
--force             Force execution (skip confirmation)
```

### Read Operation Flags

```bash
--limit             Maximum number of items to return [default: 20]
--cursor            Pagination cursor
--all               Fetch all items (internal pagination)
--fields            Comma-separated list of fields to include
--output            Output format (json|yaml|text|ndjson)
```

### Filtering Flags

```bash
--since             Start date/time (ISO 8601)
--until             End date/time (ISO 8601)
--query             Search query
--type              Resource type filter
--status            Status filter
--user              User filter
```

### Flag Naming Conventions

| Pattern | Example | Purpose |
|---------|---------|---------|
| `--<noun>` | `--channel` | Resource identifier |
| `--<verb>-<noun>` | `--include-metadata` | Action on resource |
| `--if-<condition>` | `--if-exists` | Conditional behavior |
| `--no-<feature>` | `--no-confirm` | Disable feature |
| `--<feature>-<property>` | `--log-format` | Feature configuration |

---

## Complete Example: Messages CLI

### Command Structure

```
mycli messages list [flags]
mycli messages get --id <id> [flags]
mycli messages send --channel <channel> --text <text> [flags]
mycli messages delete --id <id> [flags]
```

### Example Session

```bash
# List messages with JSON output
$ mycli messages list --channel general --limit 5 --output json
{
  "schemaVersion": 1,
  "type": "messages.list",
  "ok": true,
  "data": {
    "items": [
      {"id": "msg-1", "text": "Hello", "user": "alice", "timestamp": "2026-02-05T10:00:00Z"},
      {"id": "msg-2", "text": "Hi", "user": "bob", "timestamp": "2026-02-05T10:01:00Z"}
    ],
    "pagination": {
      "nextCursor": "eyJpZCI6Im1zZy0yIn0=",
      "hasMore": true
    }
  }
}

# Send message with deduplication
$ mycli messages send --channel general --text "Deploy complete" --dedupe-key deploy-123 --output json
{
  "schemaVersion": 1,
  "type": "messages.send",
  "ok": true,
  "data": {
    "id": "msg-789",
    "channel": "general",
    "text": "Deploy complete",
    "timestamp": "2026-02-05T10:05:00Z",
    "created": true
  }
}

# Retry (idempotent)
$ mycli messages send --channel general --text "Deploy complete" --dedupe-key deploy-123 --output json
{
  "schemaVersion": 1,
  "type": "messages.send",
  "ok": true,
  "data": {
    "id": "msg-789",
    "channel": "general",
    "text": "Deploy complete",
    "timestamp": "2026-02-05T10:05:00Z",
    "created": false,
    "note": "Message already sent with this dedupe key"
  }
}

# Delete with dry-run
$ mycli messages delete --id msg-789 --dry-run --output json
{
  "schemaVersion": 1,
  "type": "messages.delete",
  "ok": true,
  "dryRun": true,
  "plan": {
    "action": "delete",
    "resource": "message",
    "id": "msg-789",
    "text": "Deploy complete",
    "warnings": ["This operation is irreversible"]
  },
  "confirmationId": "delete-msg-789-20260205-abc"
}

# Delete with confirmation
$ mycli messages delete --id msg-789 --confirm delete-msg-789-20260205-abc --output json
{
  "schemaVersion": 1,
  "type": "messages.delete",
  "ok": true,
  "data": {
    "id": "msg-789",
    "deleted": true
  }
}
```

---

## Implementation Checklist

Use this checklist when implementing these templates:

### JSON Output
- [ ] Include `schemaVersion`, `type`, `ok` in all responses
- [ ] Consistent error structure across all commands
- [ ] Metadata includes `requestId`, `timestamp`
- [ ] Schema documented and versioned

### Exit Codes
- [ ] 0 for success
- [ ] 2 for usage errors
- [ ] 3 for auth errors
- [ ] 4 for retryable errors
- [ ] Documented in `--help`

### Introspection
- [ ] `commands --json` implemented
- [ ] `schema --command <cmd>` implemented
- [ ] `--help --json` implemented
- [ ] Error codes documented

### Authentication
- [ ] `auth status --json` implemented
- [ ] Device flow or headless-compatible auth
- [ ] `auth export` / `auth import` for headless environments
- [ ] Clear error messages with next steps

### Pagination
- [ ] `--limit` and `--cursor` supported
- [ ] `--all` flag with internal pagination
- [ ] NDJSON output for streaming
- [ ] Pagination metadata in responses

### Flags
- [ ] Standard flags on all commands
- [ ] Consistent naming conventions
- [ ] `--dry-run` for destructive operations
- [ ] `--dedupe-key` for write operations
- [ ] `--fields` for projection
