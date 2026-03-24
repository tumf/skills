# Subcommand Reference

Complete reference for `scripts/autoresearch` subcommands and their flags.

## Table of Contents

- [Base loop](#base-loop)
- [ship](#ship)
- [plan](#plan)
- [security](#security)
- [debug](#debug)
- [fix](#fix)
- [scenario](#scenario)
- [predict](#predict)
- [learn](#learn)

## Base loop

Run the autonomous iteration loop.

```bash
scripts/autoresearch "Goal: <text>" --iterations N
scripts/autoresearch "Goal: coverage to 90% Scope: src/**/*.ts Verify: npm test -- --coverage"
```

Inline config fields (passed as prompt text):
- `Goal:` — what to improve
- `Scope:` — file globs to modify
- `Metric:` — measurable number
- `Verify:` — command that produces the metric
- `Guard:` — command that must always pass (optional)
- `Iterations:` — bounded iteration count (optional, default: unlimited)

**Headless note:** Without `Iterations:`, the loop runs forever.
Always set `--iterations N` or use `agent-exec --timeout` for safety.

## ship

Universal shipping workflow (code, content, marketing, etc.).

```bash
scripts/autoresearch ship --auto
scripts/autoresearch ship --dry-run
scripts/autoresearch ship --checklist-only
scripts/autoresearch ship --type deployment --monitor 10
scripts/autoresearch ship --rollback
```

| Flag | Purpose |
|------|---------|
| `--dry-run` | Validate without shipping (stop at Phase 5) |
| `--auto` | Auto-approve if checklist passes |
| `--force` | Skip non-critical items (blockers enforced) |
| `--rollback` | Undo last ship action |
| `--monitor N` | Post-ship monitoring for N minutes |
| `--type <type>` | Override auto-detection (code-pr, code-release, deployment, content, etc.) |
| `--checklist-only` | Only generate and evaluate checklist |
| `--iterations N` | Bounded preparation iterations |

## plan

Interactive wizard: Goal → Scope, Metric, Verify config.

```bash
scripts/autoresearch plan "Increase test coverage to 95%"
scripts/autoresearch plan "Reduce bundle size below 200KB"
```

No flags. Pass the goal as the argument.

**Headless note:** Plan requires interactive Q&A; results are printed to stdout.
Best run in foreground.

## security

Autonomous STRIDE + OWASP security audit.

```bash
scripts/autoresearch security --iterations 10
scripts/autoresearch security --diff --fix --fail-on critical
```

| Flag | Purpose |
|------|---------|
| `--diff` | Only audit files changed since last audit |
| `--fix` | Auto-fix confirmed Critical/High findings |
| `--fail-on <sev>` | Exit non-zero if findings meet threshold (critical, high, medium, low) |
| `--iterations N` | Bounded sweep iterations |

**CI/CD pattern:**
```bash
scripts/autoresearch security --fail-on critical --iterations 10
# exit code reflects findings severity
```

## debug

Autonomous bug-hunting loop.

```bash
scripts/autoresearch debug --scope "src/**/*.ts" --symptom "API 500 errors"
scripts/autoresearch debug --iterations 20
scripts/autoresearch debug --fix
```

| Flag | Purpose |
|------|---------|
| `--scope <glob>` | Limit investigation scope |
| `--symptom "<text>"` | Pre-fill symptom description |
| `--severity <level>` | Minimum severity to report |
| `--fix` | After hunting, auto-switch to fix mode |
| `--iterations N` | Bounded investigation iterations |

## fix

Autonomous error-fixing loop.

```bash
scripts/autoresearch fix
scripts/autoresearch fix --guard "npm test" --iterations 30
scripts/autoresearch fix --from-debug --target "npm run typecheck"
```

| Flag | Purpose |
|------|---------|
| `--target <cmd>` | Explicit verify command |
| `--guard <cmd>` | Safety command that must always pass |
| `--category <type>` | Only fix specific type (test, type, lint, build) |
| `--from-debug` | Read findings from latest debug session |
| `--iterations N` | Bounded fix iterations |

## scenario

Scenario-driven use case generator.

```bash
scripts/autoresearch scenario --domain software --depth standard
scripts/autoresearch scenario --focus edge-cases --iterations 25
```

| Flag | Purpose |
|------|---------|
| `--domain <type>` | Domain: software, product, business, security, marketing |
| `--depth <level>` | Depth: shallow (10), standard (25), deep (50+) |
| `--scope <glob>` | Limit to specific files/features |
| `--format <type>` | Output: use-cases, user-stories, test-scenarios, threat-scenarios, mixed |
| `--focus <area>` | Prioritize: edge-cases, failures, security, scale |
| `--iterations N` | Bounded scenario iterations |

## predict

Multi-persona swarm prediction.

```bash
scripts/autoresearch predict --depth standard --chain debug
scripts/autoresearch predict --adversarial --fail-on critical
```

| Flag | Purpose |
|------|---------|
| `--chain <targets>` | Chain to tools (e.g. `debug`, `scenario,debug,fix`) |
| `--personas N` | Number of personas (3-8, default 5) |
| `--rounds N` | Debate rounds (1-3, default 2) |
| `--depth <level>` | Preset: shallow, standard, deep |
| `--adversarial` | Use adversarial persona set |
| `--budget N` | Max total findings (default 40) |
| `--fail-on <sev>` | Exit non-zero if findings at or above severity |
| `--scope <glob>` | Limit analysis scope |

## learn

Autonomous codebase documentation engine.

```bash
scripts/autoresearch learn --mode init --depth deep
scripts/autoresearch learn --mode update --iterations 3
scripts/autoresearch learn --mode check
scripts/autoresearch learn --mode summarize --scan
```

| Flag | Purpose |
|------|---------|
| `--mode <mode>` | Operation: init, update, check, summarize (default: auto-detect) |
| `--scope <glob>` | Limit codebase learning scope |
| `--depth <level>` | Comprehensiveness: quick, standard, deep |
| `--scan` | Force fresh scout in summarize mode |
| `--topics <list>` | Focus summarize on specific topics |
| `--file <name>` | Selective update — target single doc |
| `--no-fix` | Skip validation-fix loop |
| `--iterations N` | Bounded learning iterations |
