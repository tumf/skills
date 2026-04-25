# brainstorm-frameworks

A multi-framework brainstorming skill for expanding ideas with the right thinking pattern.

This skill is for ideation tasks where a single checklist is not enough. It selects and applies brainstorming frameworks based on the job: fast divergence, solo exploration, group discussion, synthesis, business framing, or validation planning.

## What it does

- Reframes a theme into a sharper problem statement
- Chooses a suitable brainstorming framework
- Expands ideas with one or more methods
- Synthesizes options when the idea set gets messy
- Connects ideation to business decisions or quick experiments

## Included frameworks

- SCAMPER
- Mind map
- Six Thinking Hats
- KJ method / affinity diagram
- Brainwriting (6-3-5)
- Random stimulus
- Why / How ladder
- JTBD
- ERRC / Blue Ocean
- Design Sprint

## Best fit

Use this skill when you want:

- fast idea expansion from multiple viewpoints
- a structured solo brainstorming method
- a facilitation pattern for group ideation
- a way to cluster and prioritize a messy idea set
- business-oriented reframing after creative exploration
- a bridge from ideation to validation

## Default output shape

The default output is:

- Theme restatement
- Recommended framework and why
- Expanded ideas grouped by framework
- Strong candidates
- Next actions / quick experiments

## Install

```bash
npx skills add tumf/skills --skill brainstorm-frameworks
```

## Example prompts

- "Brainstorm ways to improve this SaaS onboarding flow. Pick the right framework and give me concrete ideas."
- "I need a solo ideation method for a new B2B product concept. Expand the space, then narrow it."
- "Design a workshop flow for a team brainstorm on pricing strategy."
- "We already have too many rough ideas. Group and structure them, then show the strongest bets."
- "Give me business-facing feature ideas using JTBD or ERRC if that fits better than a plain brainstorm."

## References

- `references/frameworks.md`
- `references/playbooks.md`
- `references/automation.md`
- `references/examples.md`
- `references/orchestrator.md`

## Templates

- `templates/theme-clarifier.md`
- `templates/framework-selector.md`
- `templates/divergence-agent.md`
- `templates/clustering-agent.md`
- `templates/business-framing-agent.md`
- `templates/ranking-agent.md`
- `templates/experiment-designer.md`
- `templates/final-synthesis.md`

## Schemas

- `schemas/clarified-task.schema.json`
- `schemas/framework-selection.schema.json`
- `schemas/divergence-output.schema.json`
- `schemas/clusters.schema.json`
- `schemas/ranking-output.schema.json`
- `schemas/experiment-plan.schema.json`

## Notes

- This skill is framework-selection first, not framework-dumping.
- It works best when the answer chooses one primary method and optionally one secondary method.
- Use SCAMPER or random stimulus for raw divergence, then KJ / JTBD / ERRC when structure is needed.
