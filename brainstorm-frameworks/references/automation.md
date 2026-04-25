# AI-Agent Brainstorm Automation Design

Use this file when the user wants to automate brainstorming with AI agents.

The goal is not to run every framework every time. The goal is to build a modular pipeline that can choose the right framework, expand ideas, structure them, and produce next actions.

## Design principles

- Keep framework selection separate from idea generation.
- Separate divergence from convergence.
- Keep business framing optional but easy to insert.
- Make every stage produce structured output that the next stage can consume.
- Prefer swapping modules over rebuilding the whole pipeline.

## Minimum pipeline

Use this when you want a lightweight automated brainstorm:

1. Theme clarification
2. Framework selection
3. Idea generation
4. Clustering and synthesis
5. Ranking
6. Experiment design

## Agent roles

### 1. Theme Clarifier

Job:
- rewrite the user's topic into a sharper problem statement
- identify constraints, audience, objective, and time horizon
- detect whether the task is solo, group, creative, strategic, or execution-oriented

Input:
- raw user request

Output:
- clarified theme
- constraints
- success criteria
- task mode classification

Output example:
```yaml
clarified_theme: Improve activation in the first 7 days for a B2B SaaS onboarding flow
constraints:
  - no headcount increase
  - must ship within 1 month
success_criteria:
  - increase activation rate
  - reduce setup abandonment
mode:
  setting: solo
  need: divergence_then_synthesis
  orientation: business
```

### 2. Framework Selector

Job:
- choose the best primary framework
- choose an optional secondary framework
- explain why

Selection rules:
- use SCAMPER or Random stimulus for forced expansion
- use Mind map for solo exploration
- use Six Thinking Hats or Brainwriting for workshop-like collaboration
- use KJ method for clustering
- use JTBD or ERRC for business reframing
- use Design Sprint when validation matters immediately

Input:
- clarifier output

Output:
- primary framework
- optional secondary framework
- rationale
- run order

Output example:
```yaml
primary_framework: SCAMPER
secondary_framework: JTBD
why:
  - existing onboarding flow already exists and needs variants
  - ideas should be grounded in customer value after divergence
run_order:
  - SCAMPER
  - JTBD
```

### 3. Divergence Agent

Job:
- generate many options using the selected framework
- keep categories distinct
- avoid premature evaluation

Input:
- clarified theme
- selected framework

Output:
- categorized raw ideas
- short explanation per idea

Notes:
- If the framework is SCAMPER, output by each SCAMPER bucket.
- If the framework is Mind map, output by branch.
- If the framework is Random stimulus, show the stimulus and the forced connection.

### 4. Clustering Agent

Job:
- group overlapping ideas
- name clusters
- remove obvious duplicates
- preserve novelty where possible

Default method:
- use KJ-style affinity grouping even if the upstream framework was different

Input:
- raw idea set

Output:
- clusters
- cluster labels
- representative ideas
- discarded duplicates

Output example:
```yaml
clusters:
  - name: Reduce setup friction
    ideas:
      - template-based onboarding
      - one-click sample project
      - guided setup wizard
  - name: Increase early motivation
    ideas:
      - progress score
      - first-value milestone email
      - team invite reward
discarded_duplicates:
  - duplicate of guided setup wizard
```

### 5. Business Framing Agent

Optional.

Job:
- translate idea clusters into user value or strategy language
- use JTBD, ERRC, or both

Use JTBD when:
- the question is user-centered
- the output needs customer-job framing

Use ERRC when:
- the question is market or offer redesign
- the output needs category-level differentiation

Input:
- clustered ideas

Output:
- jobs served
- eliminated or reduced complexity
- raised or created value
- business implications

### 6. Ranking Agent

Job:
- score ideas without pretending to know the future
- rank by a simple rubric

Suggested rubric:
- impact
- speed
- implementation cost
- strategic fit
- novelty
- confidence

Input:
- structured ideas
- optional business framing

Output:
- ranked shortlist
- reasons
- open assumptions

Output example:
```yaml
top_candidates:
  - idea: guided setup wizard with prefilled templates
    score:
      impact: 5
      speed: 4
      cost: 3
      strategic_fit: 5
      novelty: 2
      confidence: 4
    key_assumption: setup friction is the main activation blocker
```

### 7. Experiment Designer

Job:
- turn top ideas into lightweight tests
- avoid full-project planning unless asked

Input:
- top candidates

Output:
- test design
- metric
- sample size heuristic if relevant
- failure signal
- next decision

Output example:
```yaml
experiments:
  - idea: guided setup wizard with prefilled templates
    test: show the wizard to 50% of new signups for 1 week
    success_metric: activation rate within 7 days
    failure_signal: no improvement and increased support tickets
    next_decision: ship, revise, or drop
```

## Orchestration patterns

### Pattern A: Fast solo brainstorm

Use:
1. Theme Clarifier
2. Framework Selector
3. Divergence Agent
4. Clustering Agent
5. Ranking Agent

Good defaults:
- Mind map -> Why / How ladder
- SCAMPER -> KJ method

### Pattern B: Workshop support

Use:
1. Theme Clarifier
2. Framework Selector
3. Facilitation Agent
4. Divergence Collector
5. Clustering Agent
6. Ranking Agent

Facilitation Agent can output:
- session agenda
- timeboxes
- prompt sequence
- speaking or writing rules

### Pattern C: Business concept generation

Use:
1. Theme Clarifier
2. Framework Selector
3. Divergence Agent
4. Business Framing Agent
5. Ranking Agent
6. Experiment Designer

Good defaults:
- Random stimulus -> JTBD
- SCAMPER -> ERRC

### Pattern D: End-to-end validation path

Use:
1. Theme Clarifier
2. Framework Selector
3. Divergence Agent
4. Clustering Agent
5. Business Framing Agent
6. Ranking Agent
7. Experiment Designer
8. Design Sprint Planner

Use when:
- the user wants not just ideas but a route to prototype and test

## Data contracts

Keep intermediate outputs structured.
Use YAML or JSON-like sections so downstream agents can consume them reliably.

Minimum fields across stages:
- theme
- constraints
- framework
- ideas
- clusters
- scores
- assumptions
- experiments

## Quality controls

Add simple checks between stages.

### After Theme Clarifier
- Is the problem statement actionable?
- Are constraints explicit?
- Is success defined?

### After Framework Selector
- Did it choose instead of dumping all frameworks?
- Is the choice aligned with solo/group and divergence/synthesis mode?

### After Divergence
- Are ideas actually distinct?
- Are framework buckets being used correctly?
- Has evaluation been deferred?

### After Clustering
- Are duplicates merged?
- Are labels meaningful?
- Was novelty preserved?

### After Ranking
- Are scores explained?
- Are assumptions visible?
- Is uncertainty acknowledged?

### After Experiment Design
- Is each experiment small enough?
- Is there a clear metric?
- Is there a clear next decision?

## Failure recovery

If the pipeline underperforms:
- If ideas are too narrow -> switch the divergence agent to Random stimulus or SCAMPER.
- If ideas are too messy -> insert or strengthen the Clustering Agent.
- If ideas are clever but not useful -> add JTBD or ERRC.
- If output is too theoretical -> strengthen the Experiment Designer.
- If the system keeps choosing badly -> improve the Framework Selector rules.

## Prompting guidance by agent

### Theme Clarifier prompt shape
- What is the real problem?
- Who is the target?
- What constraints matter?
- What outcome defines success?

### Framework Selector prompt shape
- Choose one primary framework and optionally one secondary framework.
- Explain why these fit better than the alternatives.
- Do not list all frameworks.

### Divergence Agent prompt shape
- Generate options grouped by the chosen framework.
- Maximize variety first.
- Do not rank yet.

### Clustering Agent prompt shape
- Group similar ideas.
- Name each cluster.
- Keep unusual but promising ideas visible.

### Ranking Agent prompt shape
- Score ideas with a small rubric.
- Show assumptions.
- Avoid fake precision.

### Experiment Designer prompt shape
- Turn each top idea into the smallest useful test.
- Define metric, failure signal, and next decision.

## Recommended default outputs to user

For lightweight use:
- chosen framework
- grouped ideas
- top candidates
- next experiments

For system-design use:
- agent graph
- stage inputs and outputs
- routing rules
- failure recovery rules

## Example agent graph

```text
User Theme
  -> Theme Clarifier
  -> Framework Selector
  -> Divergence Agent
  -> Clustering Agent
  -> Business Framing Agent
  -> Ranking Agent
  -> Experiment Designer
  -> Final Synthesis
```

## Final synthesis agent

Use a final synthesis step to produce a clean user-facing answer.

Job:
- compress intermediate outputs
- preserve why the framework was chosen
- present top ideas and next actions clearly

Without this step, multi-agent systems often feel fragmented.

## Prompt templates

Use these reusable templates under `templates/` when building the pipeline:

- `templates/theme-clarifier.md`
- `templates/framework-selector.md`
- `templates/divergence-agent.md`
- `templates/clustering-agent.md`
- `templates/business-framing-agent.md`
- `templates/ranking-agent.md`
- `templates/experiment-designer.md`
- `templates/final-synthesis.md`

These templates are intentionally lightweight. Fill them with stage outputs from the previous agent rather than rewriting the whole prompt each time.

## Schemas

Use these schemas under `schemas/` to keep agent handoffs stable:

- `schemas/clarified-task.schema.json`
- `schemas/framework-selection.schema.json`
- `schemas/divergence-output.schema.json`
- `schemas/clusters.schema.json`
- `schemas/ranking-output.schema.json`
- `schemas/experiment-plan.schema.json`

Use them when you want stronger contracts between agents, easier validation, or future script-based orchestration.

## Examples

See `references/examples.md` for end-to-end sample flows such as:
- SaaS onboarding improvement
- new business concept generation
- pricing workshop design
- clustering messy content ideas

## Orchestrator

See `references/orchestrator.md` for the parent-agent routing layer:
- when to run a short route vs full pipeline
- how to decide stage order
- how to stop early
- how to compress handoffs between stages
