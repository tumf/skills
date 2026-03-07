# Evidence Patterns

Use this file when choosing sources, decompositions, and cross-checks.

## Source Ladder

Prefer higher-quality sources first.

1. Official statistics and regulators
2. Audited filings and investor materials
3. Product pages, pricing pages, API docs, company help centers
4. Reputable industry reports and trade associations
5. News coverage summarizing primary facts
6. Heuristics derived from comparable systems

If you rely on levels 4-6, say so explicitly.

## Common Decomposition Patterns

### Population / household questions

- Start from total population or households
- Apply age, income, geography, or device ownership filters
- Apply adoption or participation rate
- Apply activity frequency if needed

Useful checks:

- Compare against census or city statistics
- Convert to per-household or per-capita figures and check plausibility

### B2C demand / market size

- Population x target segment share x awareness x conversion x purchase frequency x spend
- Or merchants x average customers x basket size x commission rate

Useful checks:

- Compare to known category revenue or public competitor revenue
- Compare spend per person to adjacent categories

### B2B market size

- Number of firms x eligible share x buyers per firm x annual spend per buyer
- Or seats x price per seat x renewal rate

Useful checks:

- Compare to public SaaS revenue benchmarks
- Check whether implied spend is a realistic share of payroll or IT budget

### Operations / staffing / capacity

- Demand per period x handling time / utilization
- Sites x hours open x throughput per hour
- Employees x productive hours x output per hour

Useful checks:

- Compare to queueing intuition and physical constraints
- Verify staffing against opening hours and labor law basics

### Financial / revenue questions

- Customers x ARPU
- Transactions x take rate
- Units sold x gross margin

Useful checks:

- Reconcile to plausible headcount, ad spend, or market share

## Range Setting Heuristics

- Use narrow ranges for directly sourced quantities
- Use moderate ranges for extrapolated quantities from comparable segments
- Use wide ranges for behavioral assumptions such as conversion, utilization, or frequency
- If a driver dominates uncertainty, spend more time strengthening that driver instead of adding more detail elsewhere

## Cross-Check Playbook

Try at least two of these:

1. Top-down market pool vs bottom-up operational build
2. Revenue vs headcount productivity benchmark
3. Spend per user vs budget share benchmark
4. Time-use check: does the implied time fit in a day, week, or year?
5. Capacity check: does the implied output fit available machines, stores, staff, or inventory?

## Weak-Evidence Language

When evidence is limited, use wording like:

- "No direct source was available, so I anchor this on X and apply Y adjustment."
- "This assumption is the least certain input and explains most of the range."
- "The estimate is directionally useful, not a substitute for primary measurement."
