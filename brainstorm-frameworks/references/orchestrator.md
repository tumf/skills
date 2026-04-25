# Brainstorm Pipeline Orchestrator

Use this file when a parent agent needs to run the brainstorming pipeline end to end.

The orchestrator is responsible for routing, not for doing all the thinking itself.
It should choose which stages to run, pass structured outputs forward, and stop the pipeline once the answer is useful enough.

## Core responsibility

The orchestrator should:
- receive the raw user request
- decide whether a full pipeline is needed
- call the right stage agents in order
- validate handoffs informally or with schemas
- avoid over-processing simple requests
- produce one coherent final answer

## Default rule

Do not run every stage by default.
Use the smallest pipeline that can produce a useful answer.

## Minimal orchestration flow

1. Theme Clarifier
2. Framework Selector
3. Divergence Agent
4. Optional Clustering Agent
5. Optional Business Framing Agent
6. Optional Ranking Agent
7. Optional Experiment Designer
8. Final Synthesis

## Fast routing table

### Case 1: User wants more ideas fast
Run:
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Final Synthesis

### Case 2: User wants ideas plus structure
Run:
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Clustering Agent
- Final Synthesis

### Case 3: User wants business-useful options
Run:
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Business Framing Agent
- Ranking Agent
- Final Synthesis

### Case 4: User wants experiments or validation
Run:
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Ranking Agent
- Experiment Designer
- Final Synthesis

### Case 5: User already has many raw ideas
Run:
- Theme Clarifier
- Framework Selector
- Clustering Agent
- Ranking Agent
- Final Synthesis

### Case 6: User wants a workshop design
Run:
- Theme Clarifier
- Framework Selector
- Divergence Agent or Facilitation-style agent
- Clustering Agent
- Final Synthesis

## Orchestrator decision logic

Use this sequence:

1. Clarify the task.
2. Ask: is the task mostly divergence, synthesis, business framing, or validation?
3. Choose a short route.
4. Run one stage at a time.
5. After each stage, ask whether another stage is necessary.
6. Stop early if the answer is already good enough.

## Stop conditions

Stop the pipeline when any of these is true:
- the user asked for simple ideation only and divergence output is already useful
- clustering made the idea space clear enough
- ranking produced an actionable shortlist
- experiment design produced concrete next steps
- additional stages would mostly rephrase the same output

## Handoff contract

At each step, pass forward:
- the original raw request
- the latest structured stage output
- only the minimum prior outputs needed

Do not dump all previous logs into every stage.
Compress context as the pipeline progresses.

## Preferred stage payloads

### To Framework Selector
Pass:
- clarified task only

### To Divergence Agent
Pass:
- clarified task
- framework selection

### To Clustering Agent
Pass:
- divergence output
- optionally clarified task if needed for naming clusters

### To Business Framing Agent
Pass:
- clarified task
- clusters or divergence output

### To Ranking Agent
Pass:
- clusters
- optional business framing

### To Experiment Designer
Pass:
- clarified task
- ranking output

### To Final Synthesis
Pass:
- clarified task
- framework selection
- only the key outputs from downstream stages

## Example orchestration pseudo-flow

```text
raw_request
  -> theme_clarifier
  -> framework_selector
  -> divergence_agent
  -> if ideas messy: clustering_agent
  -> if business lens needed: business_framing_agent
  -> if prioritization needed: ranking_agent
  -> if testing needed: experiment_designer
  -> final_synthesis
```

## Parent-agent prompt shape

Use a parent prompt like this:

```text
You are the orchestrator for a brainstorming pipeline.
Your job is to decide which stages to run and in what order.
Keep the pipeline as short as possible while still producing a useful result.
Use structured outputs between stages.
Stop early when the answer is already actionable.
```

## Orchestrator output to itself

Before calling child stages, write a short execution plan like this:

```yaml
route:
  - Theme Clarifier
  - Framework Selector
  - Divergence Agent
  - Ranking Agent
  - Final Synthesis
why:
  - user wants options plus prioritization
  - no clustering stage needed because idea volume is expected to stay manageable
stop_rule:
  - stop after ranking if top options are already clear
```

This helps the parent stay disciplined.

## Failure handling

### If the framework choice looks wrong
- rerun Framework Selector with tighter constraints
- do not rerun the whole pipeline first

### If divergence output is repetitive
- switch to Random stimulus or SCAMPER
- rerun only Divergence Agent onward

### If outputs are too messy
- insert Clustering Agent

### If ideas are interesting but weak in business value
- insert Business Framing Agent with JTBD or ERRC

### If shortlist feels arbitrary
- rerun Ranking Agent with clearer scoring guidance

### If next steps are vague
- run Experiment Designer

## Compression rule

After each stage, compress outputs to their durable essence.
Example:
- do not pass all 40 raw ideas if 5 clusters are enough
- do not pass full ranking explanation to Experiment Designer if top candidates and assumptions are enough

## Human-in-the-loop rule

If the user asks for brainstorming only, do not force validation.
If the user asks for strategy, do not stop at raw idea generation.
If the user asks for a workshop, optimize for facilitation quality, not just idea count.

## Single-agent fallback

If subagents are unavailable, the orchestrator can simulate the same flow inline:
- explicitly label each stage
- produce structured intermediate outputs
- then write the final synthesis

Do not skip the stage boundaries mentally. Keep them explicit.

## Suggested orchestration presets

### Preset: quick-ideas
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Final Synthesis

### Preset: structured-ideas
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Clustering Agent
- Final Synthesis

### Preset: business-shortlist
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Business Framing Agent
- Ranking Agent
- Final Synthesis

### Preset: testable-options
- Theme Clarifier
- Framework Selector
- Divergence Agent
- Ranking Agent
- Experiment Designer
- Final Synthesis

### Preset: workshop-plan
- Theme Clarifier
- Framework Selector
- Facilitation-style Divergence Agent
- Clustering Agent
- Final Synthesis

## Relationship to templates and schemas

Use together with:
- `templates/*.md` for per-stage prompts
- `schemas/*.json` for handoff validation
- `references/examples.md` for end-to-end examples

The orchestrator is the routing layer that ties them together.
