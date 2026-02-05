# Agentic CLI Design Scorecard

Use this checklist to evaluate CLI tools for agent-friendliness. Each principle has specific checkboxes for evaluation.

## Scoring Guide

For each checkbox:
- ✅ Fully implemented (2 points)
- ⚠️ Partially implemented (1 point)
- ❌ Not implemented (0 points)

**Maximum Score**: 28 points (14 items × 2 points each)

**Scoring Tiers**:
- 24-28: Excellent (agent-ready)
- 18-23: Good (minor improvements needed)
- 12-17: Fair (significant gaps)
- 0-11: Poor (major redesign needed)

---

## P1. Machine-readable

**Goal**: Machine-readable output is the primary interface.

### Checklist

- [ ] **`--output json` flag exists**
  - Command supports `--output json` or `--json` flag
  - JSON output is well-formed and parseable
  - Works for all commands (not just some)

- [ ] **stdout=results / stderr=logs separation**
  - stdout contains ONLY the result data
  - All logs, progress, diagnostics go to stderr
  - No mixing of human-readable messages in JSON output

- [ ] **Errors are structured**
  - Errors output JSON format (when `--output json` is used)
  - Error JSON includes: code, message, details
  - Error structure is consistent across all commands

- [ ] **`schemaVersion` exists and compatibility is documented**
  - JSON output includes `schemaVersion` field
  - Breaking changes increment schema version
  - Migration guide exists for schema changes

**Score**: _____ / 8 points

---

## P2. Non-interactive

**Goal**: Commands complete without human intervention.

### Checklist

- [ ] **`--non-interactive` flag exists (or TTY auto-detection)**
  - Explicit `--non-interactive` flag available, OR
  - Automatically detects non-TTY environment
  - No prompts when non-interactive mode is active

- [ ] **Interactive prompts are opt-in (not default)**
  - Commands don't prompt by default
  - All required inputs are flags/arguments
  - Interactive mode requires explicit flag (e.g., `--interactive`)

- [ ] **`--yes`/`--force`/`--no-confirm` vocabulary is consistent**
  - Confirmation bypass flags exist
  - Flag names are consistent across commands
  - Documented in `--help`

**Score**: _____ / 6 points

---

## P3. Idempotent & Replayable

**Goal**: Commands are safe to run multiple times.

### Checklist

- [ ] **Write operations accept `--client-request-id` / `--dedupe-key`**
  - Create/send operations accept deduplication key
  - Same key returns same result (doesn't create duplicates)
  - Documented in `--help` and examples

- [ ] **`--if-exists` policy exists**
  - Create operations support `--if-exists skip|update|error`
  - Default behavior is safe (error on conflict)
  - Documented clearly

- [ ] **`--cursor`/`--limit`/`--all` pagination exists**
  - List operations support `--limit` and `--cursor`
  - `--all` flag exists and handles pagination internally
  - Default limit is reasonable (not unbounded)

**Score**: _____ / 6 points

---

## P4. Safe-by-default

**Goal**: Destructive operations require explicit confirmation.

### Checklist

- [ ] **Destructive operations support `--dry-run`**
  - Delete/update operations have `--dry-run` flag
  - Dry-run shows what would happen (structured output)
  - Dry-run doesn't execute the operation

- [ ] **Execution requires `--confirm <id>` / `--force`**
  - Destructive operations require explicit confirmation
  - Confirmation can be ID from dry-run or `--force` flag
  - Fails safely if confirmation is missing

**Score**: _____ / 4 points

---

## P5. Observable & Debuggable

**Goal**: Operations are traceable and debuggable.

### Checklist

- [ ] **`--debug` flag exists (logs to stderr)**
  - `--debug` or `--verbose` flag available
  - Debug output goes to stderr (not stdout)
  - Includes useful diagnostic information

- [ ] **`--log-format json` exists**
  - Structured logging format available
  - Logs are parseable JSON
  - Includes timestamps, levels, context

- [ ] **`--trace-id` is accepted**
  - Commands accept `--trace-id` for correlation
  - Trace ID is included in logs and API calls
  - Enables distributed tracing

- [ ] **Exit codes are categorized (0/2/3/4)**
  - Exit code 0: success
  - Exit code 2: invalid arguments/usage
  - Exit code 3: authentication/permission errors
  - Exit code 4: retryable errors (rate limit, transient)
  - Documented in `--help`

**Score**: _____ / 8 points

---

## P6. Context-efficient

**Goal**: Minimize token/context consumption.

### Checklist

- [ ] **`--fields`/`--select` projection exists**
  - Commands support field selection
  - Can request specific fields only
  - Reduces output size significantly

- [ ] **`--output ndjson` streaming exists**
  - NDJSON (newline-delimited JSON) format available
  - Enables line-by-line processing
  - Works with large datasets

- [ ] **Heavy fields are opt-in via `--include-*`**
  - Large fields (bodies, metadata) excluded by default
  - Explicit flags to include heavy fields
  - Default output is minimal/summary

**Score**: _____ / 6 points

---

## P7. Introspectable

**Goal**: CLI is self-describing.

### Checklist

- [ ] **`commands --json` exists**
  - Lists all commands in JSON format
  - Includes descriptions, arguments, flags
  - Machine-readable command discovery

- [ ] **`schema --command ... --output json-schema` exists**
  - Exports JSON Schema for commands
  - Includes input and output schemas
  - Enables validation and code generation

**Score**: _____ / 4 points

---

## Total Score

| Principle | Score | Max |
|-----------|-------|-----|
| P1. Machine-readable | _____ | 8 |
| P2. Non-interactive | _____ | 6 |
| P3. Idempotent & Replayable | _____ | 6 |
| P4. Safe-by-default | _____ | 4 |
| P5. Observable & Debuggable | _____ | 8 |
| P6. Context-efficient | _____ | 6 |
| P7. Introspectable | _____ | 4 |
| **TOTAL** | **_____** | **42** |

---

## Detailed Scoring Template

Use this template for detailed evaluation:

### CLI Tool: _______________
**Version**: _______________  
**Evaluated by**: _______________  
**Date**: _______________

---

#### P1. Machine-readable (8 points)

| Item | Status | Points | Notes |
|------|--------|--------|-------|
| `--output json` exists | ⬜ | ___/2 | |
| stdout/stderr separation | ⬜ | ___/2 | |
| Structured errors | ⬜ | ___/2 | |
| `schemaVersion` + docs | ⬜ | ___/2 | |
| **Subtotal** | | **___/8** | |

**Issues**:
- 
- 

**Recommendations**:
- 
- 

---

#### P2. Non-interactive (6 points)

| Item | Status | Points | Notes |
|------|--------|--------|-------|
| `--non-interactive` or TTY detection | ⬜ | ___/2 | |
| Prompts are opt-in | ⬜ | ___/2 | |
| Consistent `--yes`/`--force` | ⬜ | ___/2 | |
| **Subtotal** | | **___/6** | |

**Issues**:
- 
- 

**Recommendations**:
- 
- 

---

#### P3. Idempotent & Replayable (6 points)

| Item | Status | Points | Notes |
|------|--------|--------|-------|
| `--dedupe-key` support | ⬜ | ___/2 | |
| `--if-exists` policy | ⬜ | ___/2 | |
| Pagination support | ⬜ | ___/2 | |
| **Subtotal** | | **___/6** | |

**Issues**:
- 
- 

**Recommendations**:
- 
- 

---

#### P4. Safe-by-default (4 points)

| Item | Status | Points | Notes |
|------|--------|--------|-------|
| `--dry-run` support | ⬜ | ___/2 | |
| `--confirm`/`--force` required | ⬜ | ___/2 | |
| **Subtotal** | | **___/4** | |

**Issues**:
- 
- 

**Recommendations**:
- 
- 

---

#### P5. Observable & Debuggable (8 points)

| Item | Status | Points | Notes |
|------|--------|--------|-------|
| `--debug` flag | ⬜ | ___/2 | |
| `--log-format json` | ⬜ | ___/2 | |
| `--trace-id` support | ⬜ | ___/2 | |
| Categorized exit codes | ⬜ | ___/2 | |
| **Subtotal** | | **___/8** | |

**Issues**:
- 
- 

**Recommendations**:
- 
- 

---

#### P6. Context-efficient (6 points)

| Item | Status | Points | Notes |
|------|--------|--------|-------|
| `--fields`/`--select` | ⬜ | ___/2 | |
| `--output ndjson` | ⬜ | ___/2 | |
| Heavy fields opt-in | ⬜ | ___/2 | |
| **Subtotal** | | **___/6** | |

**Issues**:
- 
- 

**Recommendations**:
- 
- 

---

#### P7. Introspectable (4 points)

| Item | Status | Points | Notes |
|------|--------|--------|-------|
| `commands --json` | ⬜ | ___/2 | |
| `schema` export | ⬜ | ___/2 | |
| **Subtotal** | | **___/4** | |

**Issues**:
- 
- 

**Recommendations**:
- 
- 

---

## Overall Assessment

**Total Score**: _____ / 42 points

**Rating**: 
- [ ] Excellent (36-42 points) - Agent-ready
- [ ] Good (28-35 points) - Minor improvements needed
- [ ] Fair (20-27 points) - Significant gaps
- [ ] Poor (0-19 points) - Major redesign needed

**Top 3 Strengths**:
1. 
2. 
3. 

**Top 3 Weaknesses**:
1. 
2. 
3. 

**Priority Improvements** (ranked):
1. 
2. 
3. 

**Estimated Effort**:
- [ ] Low (< 1 week)
- [ ] Medium (1-4 weeks)
- [ ] High (> 1 month)

**Agent Readiness**:
- [ ] Ready for production agent use
- [ ] Ready with workarounds
- [ ] Not ready (needs improvements)

---

## Quick Reference: Common Issues

### High-Impact Issues (Fix First)

1. **No `--output json`** → Agents can't parse output
2. **Interactive by default** → Agents get stuck
3. **No exit code categorization** → Agents can't retry intelligently
4. **No pagination** → Context explosion
5. **Destructive without confirmation** → Dangerous for agents

### Medium-Impact Issues

6. **No `--dry-run`** → Can't preview changes
7. **No deduplication** → Duplicate operations on retry
8. **No `--fields` selection** → Wastes context
9. **Mixed stdout/stderr** → Parsing failures
10. **No structured errors** → Hard to handle errors

### Low-Impact Issues (Nice to Have)

11. **No `--trace-id`** → Harder to debug
12. **No `--log-format json`** → Manual log parsing
13. **No `commands --json`** → Manual discovery
14. **No `schemaVersion`** → Breaking changes harder to handle

---

## Example Evaluations

### Example 1: GitHub CLI (`gh`)

**Score**: 32/42 (Good)

**Strengths**:
- Excellent `--json` support across all commands
- Good pagination with `--limit`
- Structured errors

**Weaknesses**:
- No `--dedupe-key` for idempotency
- No `--dry-run` for destructive operations
- No `commands --json` introspection

**Recommendation**: Add idempotency and dry-run support for agent use.

---

### Example 2: kubectl

**Score**: 34/42 (Good)

**Strengths**:
- Strong idempotency (declarative apply)
- Excellent `--dry-run` support
- Good `--output json|yaml`

**Weaknesses**:
- No `--dedupe-key` (relies on declarative model)
- No `commands --json` introspection
- Exit codes not fully categorized

**Recommendation**: Already agent-friendly due to declarative model.

---

### Example 3: AWS CLI

**Score**: 28/42 (Good)

**Strengths**:
- Comprehensive `--output json`
- Good pagination with `--max-items` and `--starting-token`
- Rich filtering options

**Weaknesses**:
- No `--dry-run` for many operations
- No `--dedupe-key` (uses client-request-token inconsistently)
- No introspection commands

**Recommendation**: Add dry-run and consistent idempotency support.

---

## Using This Scorecard

### For New CLI Design

1. Use checklist as design requirements
2. Aim for 36+ points (Excellent tier)
3. Prioritize P1, P2, P5 for agent use

### For Existing CLI Review

1. Complete detailed scoring template
2. Identify top 3 weaknesses
3. Prioritize high-impact fixes
4. Create improvement roadmap

### For CLI Selection

1. Score multiple CLI options
2. Compare scores and specific features
3. Choose based on agent use case priorities
4. Document workarounds for gaps

---

## Next Steps

After completing this scorecard:

1. **Review** [principles.md](principles.md) for detailed guidance on gaps
2. **Check** [anti-patterns.md](anti-patterns.md) for specific issues found
3. **Use** [templates.md](templates.md) for implementation patterns
4. **Create** improvement plan with prioritized fixes
