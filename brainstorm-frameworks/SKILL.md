---
name: brainstorm-frameworks
description: Use this skill whenever the user asks for brainstorming, ideation, concept expansion, service improvement ideas, strategy options, workshop structure, or says thinking is stuck and needs more perspectives. Select and apply one or more brainstorming frameworks based on the user's goal, solo vs group setting, divergence vs convergence need, and business vs creative context. Use it even if the user does not name a framework.
---

# Brainstorm Frameworks

Use this skill to widen the idea space with the right framework, not just more words.

The main failure mode in brainstorming is viewpoint fixation. Solve it by choosing a framework that matches the user's situation, then drive divergence and convergence deliberately.

## When to use

Use this skill when the user:
- wants more ideas
- says thinking is stuck
- asks for feature, product, service, workflow, campaign, or content ideas
- wants to run or design a brainstorming session
- wants to structure messy ideas after a brainstorm
- wants to connect ideation to business decisions

## First choose the mode

Before generating ideas, classify the task on these axes:
- Solo or group
- Fast divergence or structured evaluation
- Creative exploration or business framing
- Need many raw ideas or need synthesis
- Need strategy, execution, or customer insight

Then select one or more frameworks.

## Framework selection guide

Use these defaults unless the user asks otherwise:

- Fast divergence
  - SCAMPER
  - Random stimulus

- Solo ideation
  - Mind map
  - Why / How ladder

- Group discussion
  - Six Thinking Hats
  - Brainwriting

- Synthesis and clustering
  - KJ method

- Business framing
  - JTBD
  - ERRC

- From ideas to validation
  - Design Sprint

## Operating principle

Do not force a single framework on every problem.
Choose the smallest useful set.
Usually 1 primary framework plus 1 secondary framework is enough.

Example combinations:
- SCAMPER -> KJ method
- Random stimulus -> JTBD
- Mind map -> Why / How ladder
- Six Thinking Hats -> ERRC

## Default workflow

1. Restate the theme as a sharper problem statement.
2. Select the best-fit framework or framework pair.
3. Run a divergence pass.
4. If needed, run a synthesis pass.
5. Highlight strong options.
6. Suggest next experiments or decisions.

## Default output format

Use this structure unless the user asks for something else:

### Theme
- One-line restatement of the problem

### Recommended framework
- Primary framework
- Optional secondary framework
- Why this choice fits

### Expanded ideas
- Ideas grouped by the chosen framework

### Strong candidates
- Top 3 to 5 options
- Why they stand out
- Main assumption or risk for each

### Next actions
- 3 quick experiments, validation steps, or meeting prompts

## Practical rules

- Prefer short bullets over long essays.
- Make ideas concrete enough to act on.
- If the theme is vague, sharpen it before brainstorming.
- If the user wants business utility, include impact, cost, speed, and risk hints.
- If the user wants pure exploration, stay divergent longer.
- If a session produces too many ideas, switch to KJ method or ERRC to structure them.

## Use references

Read the relevant references file before applying a framework:
- `references/frameworks.md` for the framework catalog
- `references/playbooks.md` for framework selection and combination patterns
- `references/automation.md` for AI-agent automation design, routing, and stage contracts

## Anti-patterns

Avoid these mistakes:
- using the same pattern of ideas in every framework
- choosing a meeting framework for a solo task without reason
- evaluating too early and killing divergence
- staying abstract when the user needs actionable options
- dumping frameworks without selecting one

## If the user is very stuck

Use a two-pass recovery pattern:
1. Random stimulus or SCAMPER for forced divergence.
2. KJ method or Why / How ladder for structure.

## If the user asks for an AI-agent workflow

Provide a staged automation design:
- theme clarification
- framework selection
- idea generation
- clustering
- ranking
- experiment design

Keep the answer practical and lightweight unless the user asks for a full system design.
