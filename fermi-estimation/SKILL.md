---
name: fermi-estimation
description: Solve user questions with defensible Fermi estimates using explicit assumptions, source-backed inputs, uncertainty ranges, and sensitivity analysis. Use when exact data is unavailable or too slow to collect but the user still needs a quantitative answer for counts, market size, demand, costs, revenue, capacity, timing, or operational scale. Prefer quick primary-source lookup when it exists; use Fermi estimation as fallback or cross-check when direct measurement is unavailable, stale, fragmented, or too slow. Autonomously gather accessible evidence, prefer current primary sources, and drive to a conclusion without asking for approval.
---

# Fermi Estimation

Produce an answer that is numerically useful, transparent about uncertainty, and persuasive to a skeptical reader. Favor externally checkable facts over intuition, and turn intuition into labeled assumptions only after exhausting accessible evidence.

## Core Workflow

1. Define the target precisely.
2. Gather accessible evidence before inventing assumptions.
3. Decompose the target into a small number of drivers.
4. Assign low/base/high values to each driver.
5. Calculate the estimate and stress-test it.
6. Present the conclusion, uncertainty, and biggest drivers.

If the user says to solve by Fermi estimation, do not stop for approval. Work through to a final answer with the best evidence you can access.

## When Not To Use It

Do not use Fermi estimation when a current primary-source answer is directly available with a quick lookup.

Prefer exact lookup first when the answer can be retrieved quickly from:

- Official statistics or regulator datasets
- Public filings or company disclosures
- Current pricing, usage, or policy pages
- A user-provided source that directly answers the question

Use Fermi estimation as a fallback or cross-check when direct measurement is unavailable, stale, fragmented, or too slow.

## Step 1: Define The Quantity

Lock down these items explicitly in the answer, even if you infer them:

- Geography
- Time window
- Unit of measure
- Inclusion and exclusion rules

If the request is ambiguous, choose the most decision-useful interpretation, state it, and continue.

If unresolved scope ambiguity is likely to change the estimate materially, either:

1. present two scoped estimates, or
2. ask one critical clarification.

Otherwise, infer the most decision-useful scope and continue.

## Step 2: Evidence First

Use the strongest accessible evidence in this order:

1. User-provided files, URLs, and constraints
2. Official statistics, regulator data, public filings, company disclosures, product pricing pages
3. Industry reports or reputable research summaries
4. Stable background facts already known with high confidence
5. Heuristic assumptions labeled as assumptions

Do not ask the user for permission to search or proceed. Use available tools and public sources proactively.

For source strategy and common decomposition patterns, read `fermi-estimation/references/evidence-patterns.md`.

## Step 3: Build A Sparse Model

Prefer a model with 3-7 drivers. More factors usually create fake precision.

Good patterns:

- Population x penetration x frequency x price
- Locations x utilization x throughput
- Employees x time per task x tasks per period
- Revenue pool x reachable share x conversion
- Total demand = segment A + segment B + segment C

For each driver, record:

- Name
- Base value
- Low/high range
- Unit
- Why the value is plausible
- Best supporting source or assumption label

## Step 4: Quantify Uncertainty

Always provide a range unless the user explicitly wants a point estimate only.

- `base`: best estimate
- `low`: conservative but plausible
- `high`: optimistic but plausible

Use narrow ranges for sourced facts and wider ranges for inferred behavior. Never hide uncertainty behind a single precise number.

If the model is multiplicative, additive, or nested (for example sum-of-products), and you want consistent arithmetic, use `fermi-estimation/scripts/factor_model.py`.

Example:

```bash
python3 fermi-estimation/scripts/factor_model.py --input factors.json --format markdown
```

The script accepts either a JSON file or inline JSON and returns low/base/high totals plus validation warnings, rollups, scenario totals, one-at-a-time sensitivity, and correlated-group stress tests.

Optional scenario support:

- Add `scenarios.conservative` and `scenarios.aggressive` on a factor when you want scenario values that differ from literal `low` and `high`
- Add `correlation_group` on related factors when they should be stress-tested together

## Step 5: Stress-Test The Result

Before presenting the final answer, run at least two checks:

1. Bottom-up vs top-down comparison, if both are possible
2. Capacity or budget realism check
3. Compare against a known benchmark, adjacent market, or public company metric
4. Check unit consistency and time consistency

If checks disagree materially, explain the mismatch and either revise the model or present both bounds with the reason for divergence.

## Step 6: Write The Answer

Use this structure unless the user asks for another format:

1. Bottom line
2. Model summary
3. Key assumptions and evidence
4. Calculation table
5. Sanity checks
6. Sensitivity and confidence

For a concise template, read `fermi-estimation/references/report-template.md`.

## Quality Bar

- Show assumptions explicitly; never bury them
- Distinguish sourced inputs from inferred inputs
- Prefer orders of magnitude that are memorable and decision-useful
- Round final answers to a believable precision level
- State the as-of date when current data matters
- If an input is weak, say it is weak and show its effect on the result

## Failure Modes To Avoid

- Using too many factors with weak justification
- Multiplying percentages and counts with mismatched populations
- Mixing monthly, annual, and daily units
- Adding segments with mismatched currency, geography, or time basis
- Treating one anecdote as a market-wide fact
- Presenting a point estimate without a plausible range
- Asking the user for unnecessary confirmation before concluding
