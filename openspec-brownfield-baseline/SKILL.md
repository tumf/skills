---
name: openspec-brownfield-baseline
description: Introduce OpenSpec into an existing codebase by deriving baseline specs from current behavior, then switch future work to change-driven development.
---

# OpenSpec Brownfield Baseline

Use this when a user wants to adopt OpenSpec in the middle of an existing software project and needs to create trustworthy baseline specs from the current implementation.

## Goal

Create `openspec/specs/` as a current-state source of truth for the parts of the system that matter now, without blindly canonizing accidental behavior, bugs, or implementation details. After the baseline exists, all future work should flow through `openspec/changes/`.

## Core principles

- `openspec/specs/` is the current source of truth for system behavior.
- Focus on behavior contracts, not internal implementation details.
- Reverse-engineered specs are drafts until reviewed by a human.
- Start with high-change or high-risk domains first; do not try to spec the whole repository unless explicitly asked.
- Prefer domain boundaries based on user-visible capabilities, not folder layout.

## When to use this

- A project already has substantial implementation but no OpenSpec baseline.
- The team wants to move from code-first to spec-driven development.
- The user asks to generate or bootstrap specs from an existing repo.
- The repo has tests, APIs, or workflows whose current behavior should be captured before more changes are made.

## Expected outputs

1. A proposed domain map for `openspec/specs/`.
2. Draft `spec.md` files for selected domains.
3. A short review note listing:
   - intended behavior confirmed
   - inferred behavior needing review
   - likely bugs or accidental behavior not promoted to spec
4. A recommendation for how future changes should be done under `openspec/changes/`.

## Standard workflow

### 1. Initialize or normalize OpenSpec structure

If OpenSpec is not present:

- run `openspec init` if the CLI is available
- otherwise create the structure manually:
  - `openspec/specs/`
  - `openspec/changes/`

Do not start by writing change artifacts. First establish the current-state baseline in `openspec/specs/`.

### 2. Choose scope before drafting

Do not attempt full-repo coverage by default. Propose a first wave of domains such as:

- auth
- users
- billing
- public-api
- webhooks
- admin
- sync
- notifications

Choose domains by answering:

- what external contracts exist?
- what areas change often?
- what areas would be risky to modify without a baseline?
- what areas already have tests or stable workflows?

### 3. Gather evidence for each domain

For each domain, inspect the current implementation surface and collect evidence from:

- routes, controllers, handlers
- schemas, validation, serializers
- service-layer entry points
- tests, especially integration and end-to-end tests
- README/docs/API references
- DB constraints or state transitions when behaviorally relevant
- logs, telemetry, retry semantics, idempotency, and side effects if externally observable

Prefer existing tests as strong evidence of intended behavior.

### 4. Extract contracts, not code structure

Translate the evidence into behavior statements that answer:

- what inputs are accepted?
- what outputs or state changes occur?
- what are the success conditions?
- what failures are user-visible?
- what side effects occur?
- what authorization or timing constraints exist?
- what ordering, idempotency, or retry guarantees exist?

Do not copy implementation detail into the spec unless it is part of an external contract.

## What belongs in a baseline spec

Good candidates:

- API request/response behavior
- validation and authorization rules
- state transitions
- error behavior
- idempotency and retry rules
- notification or webhook behavior
- side effects visible to operators or users
- business constraints and invariants

Avoid unless explicitly required:

- helper methods and class decomposition
- ORM-specific details
- internal caching tricks
- exact module layout
- accidental or buggy behavior
- implementation plans or refactor strategy

### 5. Draft `spec.md` files in OpenSpec format

Each domain should usually live under:

- `openspec/specs/<domain>/spec.md`

Use a structure like:

```md
# <Domain Name>

## Purpose
<Short statement of what the domain is responsible for>

## Requirements

### Requirement: <Behavior name>
The system SHALL <observable behavior>.

#### Scenario: <Happy path>
- GIVEN <context>
- WHEN <action>
- THEN <expected outcome>

#### Scenario: <Failure or edge case>
- GIVEN <context>
- WHEN <action>
- THEN <expected outcome>
```

Use RFC 2119 language where appropriate: SHALL, MUST, SHOULD.

Prefer a few solid requirements with concrete scenarios over a giant dump of implementation trivia.

### 6. Keep draft confidence separate from final truth

While drafting, track whether each requirement is:

- confirmed by tests or docs
- inferred from code
- needs human review

This confidence labeling can live in review notes or draft comments, but should not pollute the final baseline spec unless the user explicitly wants that.

### 7. Review before promoting to source of truth

Before treating the generated specs as canonical, perform a review pass that distinguishes:

- intentional product behavior
- implementation leakage
- legacy quirks
- known bugs
- under-specified areas

If something looks like a bug or accidental behavior, call it out instead of silently turning it into a requirement.

### 8. Verify the baseline

Before finishing, verify that:

- selected high-value domains are covered
- each requirement is observable and testable
- scenarios include not only happy paths but also failure or edge conditions where relevant
- spec language matches current behavior closely enough to guide future changes
- the baseline is small enough to maintain

If asked, identify gaps between the specs and the code/tests.

### 9. Switch future work to changes

After the baseline is accepted, recommend that all new work go through:

- `openspec/changes/<change-id>/proposal.md`
- `openspec/changes/<change-id>/specs/...`
- `design.md`
- `tasks.md`

The baseline captures current truth; changes capture deltas.

## Recommended rollout strategy

Use phased adoption unless the user explicitly wants exhaustive coverage.

### Phase 1

Capture the most important domains first, usually:

- auth
- billing
- public-api
- webhooks

### Phase 2

Add internal but operationally important areas:

- admin
- sync
- batch jobs
- notifications

### Phase 3

Expand to lower-risk or edge-case-heavy areas as they are touched.

This keeps OpenSpec adoption practical and aligned with real development work.

## Agent operating guidance

When applying this skill:

1. Start by proposing a domain map and a narrow first-wave scope.
2. Inspect the repo and tests before drafting specs.
3. Draft specs domain by domain.
4. Call out ambiguities and likely accidental behavior explicitly.
5. Do not claim the whole repo is now spec-covered unless it actually is.
6. If the user wants execution, create files under `openspec/specs/` rather than only describing the approach.

## Good response shape

When responding to the user, prefer this structure:

- recommended first-wave domains
- proposed files to create under `openspec/specs/`
- sample requirement/scenario for one domain
- review risks or ambiguities
- next action: draft the baseline specs now, or start with one selected domain

## Pitfalls

- Trying to spec the entire system in one pass
- Treating current code as automatically correct
- Writing implementation details instead of contracts
- Omitting failure scenarios
- Mixing current-state baseline with future change design
- Generating specs without checking tests or externally visible behavior

## Completion criteria

This skill is successfully applied when:

- `openspec/specs/` exists with draft baseline specs for the chosen domains
- each baseline spec captures observable behavior in requirement/scenario form
- questionable behavior is called out for review instead of silently canonized
- the user can continue future work via `openspec/changes/`
