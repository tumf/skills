# Reader-specific eval cases for business-planning

These evals test whether the skill can do two things at the same time:

1. keep the same underlying business logic stable
2. change the persuasion style for the main target reader

The three current evals use the same business idea:
- a control plane for open-weight LLM operations
- sold to B2B SaaS companies facing enterprise demand for dedicated, VPC, or on-prem deployment
- with policy control, usage visibility, billing, deployment, and operational governance

## What should vary

The output should vary by audience emphasis:
- investor
- board / executive approval
- enterprise buyer

## What should stay the same

Across all evals, the grader should still find the same core business:
- same buyer category
- same product category
- same deployment logic
- same business direction
- same causal numerical story, even if emphasis changes by audience

If the output changes the business itself to fit the audience, that should count as a failure.
If the output changes the numbers without changing the stated assumptions or drivers, that should also count as a failure.

## Grading intent by eval

### Eval 1: investor
Pass when the output emphasizes:
- why now
- market size or scale path
- defensibility
- growth logic
- capital efficiency or return logic

Watch for failures like:
- reading like an internal approval memo
- focusing mainly on rollout detail or procurement detail
- failing to show why this could be a large business

### Eval 2: board / executive approval
Pass when the output emphasizes:
- strategic fit
- resource allocation
- risk control
- governance or decision gates
- milestone-based execution

Watch for failures like:
- sounding like a VC pitch instead of an approval memo
- omitting opportunity cost or resource implications
- lacking a clear approval ask

### Eval 3: enterprise buyer
Pass when the output emphasizes:
- customer pain
- ROI or business impact
- deployment / compliance fit
- implementation practicality
- trust and risk reduction

Watch for failures like:
- sounding mostly like an investor memo
- overemphasizing market size instead of adoption value
- failing to reduce implementation anxiety

## Benchmark use

These expectations are still partly qualitative.
That is OK.
The goal is not perfect mechanical grading.
The goal is discriminative grading: outputs with the skill should show clearer audience adaptation than outputs without the skill.

When benchmarking, compare:
- whether the audience is identified correctly
- whether the emphasis shifts appropriately
- whether the same business stays intact across all three outputs
- whether the wrong audience framing leaks into the answer
- whether the output distinguishes sourced, benchmarked, and estimated inputs
- whether the output uses a bottom-up driver model or scenario logic instead of hand-wavy numeric claims

For numeric grading, a strong output should make it possible to answer:
- what is measured
- what is inferred
- what assumptions drive the result most
- what research would tighten the forecast next

## Eval 4: numeric planning quality

This case is different from the first three.
It is not mainly about audience adaptation.
It is about whether the skill can produce a defensible number story.

Pass when the output:
- separates researched facts from benchmarks and estimates
- builds a sparse bottom-up driver model
- gives low / base / high outputs
- shows the causal chain from drivers to outcomes
- identifies the assumptions that dominate the forecast
- names the next research needed to improve confidence

Watch for failures like:
- starting from target ARR and backfilling assumptions invisibly
- presenting TAM as if it were a revenue forecast
- giving a single precise forecast with no uncertainty treatment
- changing the business model just to make the numbers work

## Suggested next eval

A strong fifth case would be:
- technical evaluator / security reviewer

That would test whether the skill can shift toward feasibility, integration burden, operational ownership, and governance without losing the business logic.
