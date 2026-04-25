# business-planning

Build rational, persuasive business plans with reader-specific framing and bottom-up numerical planning.

This skill is for turning a vague business idea into a decision-ready plan. It emphasizes explicit assumptions, clear strategic choices, evidence-backed reasoning, and bottom-up forecasting rather than reverse-engineering a desired outcome.

## What it does

- Clarifies the business question and planning context
- Identifies the target customer, buyer, value proposition, and wedge
- Uses frameworks only as supporting tools when they improve reasoning
- Adapts emphasis for the main reader such as investor, board, or enterprise buyer
- Builds a numerical plan from researched facts, benchmarks, and labeled estimates
- Produces low / base / high scenarios with driver-based logic
- Highlights risks, dominant assumptions, and next research to improve confidence

## Best fit

Use this skill when you want:

- a new business plan for a startup, SaaS, or AI agent business
- a strategy memo that is more rational and decision-oriented
- a plan that distinguishes facts, assumptions, and unknowns
- reader-specific persuasion without changing the underlying business logic
- bottom-up numerical planning instead of target-first storytelling
- a forecast that can survive scrutiny from investors, boards, or enterprise buyers

## Install

```bash
npx skills add tumf/skills --skill business-planning
```

## Example prompts

- "Create a business plan for this AI infrastructure idea. Keep frameworks in the background and focus on the actual business logic."
- "Turn this vague SaaS idea into a board-ready strategy memo with resource asks, risks, and milestones."
- "Write the same business plan three ways: investor, board, and enterprise buyer. Keep the business the same but change the emphasis."
- "Build a bottom-up numerical plan for this product. Separate researched facts, benchmarks, and estimates, then show low/base/high scenarios."
- "Review this existing business plan and tell me whether the numbers are causal and defensible or just target-driven."

## Included references

- `references/framework-selection.md`
- `references/frameworks.md`
- `references/business-plan-template.md`
- `references/readers.md`
- `references/ai-saas-notes.md`
- `references/numeric-planning.md`

## Eval cases

- `evals/evals.json` - audience-specific and numeric-planning eval cases
- `evals/README.md` - grading intent and benchmark notes

## Notes

- This skill is not framework-first. It is business-logic-first.
- It works best when the output keeps the business model stable while changing persuasion style for the reader.
- For missing quantitative inputs, it pairs well with `fermi-estimation` as a support method rather than a substitute for research.
