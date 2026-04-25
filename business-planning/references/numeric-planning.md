# Numerical Planning for Business Plans

Use this reference when the user needs a business plan with defensible numbers.

The purpose is not to produce impressive numbers.
The purpose is to produce numbers that can be explained, stress-tested, and improved over time.

## Core rule

Do not begin with the desired result.
Do not hide reverse-engineering.
Start from what can be observed, then estimate only the missing parts.

## Planning ladder

Build the number plan in this order:

1. Observable facts
2. Derived quantities
3. Estimated missing variables
4. Driver model
5. Scenario outputs
6. Sensitivity
7. Research backlog

## 1. Observable facts

Collect what can be directly grounded first.
Examples:
- public pricing
- public company filings
- regulator statistics
- user-provided pipeline counts
- current deal sizes from comparable offerings
- cloud, GPU, support, or headcount cost anchors
- known deployment mixes from case studies or customer requests

Mark these as:
- sourced
- internal evidence
- benchmark

## 2. Derived quantities

Compute obvious derived values before estimating harder ones.
Examples:
- annual contract value from monthly price × seats
- gross margin from price minus service cost
- service capacity from headcount × hours × utilization
- reachable market from total segment × fit ratio

Derived quantities are not assumptions if they come from already stated inputs.

## 3. Estimated missing variables

For each missing variable, choose one estimation method and label it:
- benchmark transfer
- bottom-up operational estimate
- top-down allocation
- Fermi estimate
- strategic assumption

For every estimate, record:
- base value
- low value
- high value
- unit
- reason it is plausible
- what evidence would improve it

## 4. Driver model

Keep the model sparse.
Use 3 to 7 drivers where possible.

Typical business-plan driver patterns:

### Revenue
- addressable accounts
- reachable accounts
- win rate
- average contract value
- ramp timing

### Cost
- hosting or delivery cost per account
- implementation cost per account
- support cost per account
- sales and success headcount needed
- fixed platform cost

### Capacity
- deals per sales rep
- implementations per solutions engineer
- accounts supported per CSM
- infrastructure throughput per cluster or environment

### Expansion
- retention
- expansion revenue
- deployment mix shift
- attach rate of premium controls or dedicated environments

## 5. Scenario outputs

Always produce at least:
- low
- base
- high

If useful, also provide:
- conservative
- aggressive

Do not pretend base is truth.
Base is just the best current synthesis.

## 6. Sensitivity

Show which assumptions matter most.
Usually this means one or more of:
- win rate
- ACV
- deployment mix
- gross margin
- support burden
- sales cycle length
- retention

If a single weak assumption changes the conclusion materially, say so clearly.

## 7. Research backlog

End with the next research tasks that would most improve confidence.
Examples:
- validate average enterprise deal size
- verify deployment mix demand by customer segment
- benchmark implementation cost per dedicated environment
- estimate realistic sales cycle for security-sensitive buyers
- test expansion willingness for governance and billing modules

## Good output structure

### Numerical planning summary
- what is measured
- what is benchmarked
- what is estimated

### Driver model
- driver name
- low / base / high
- source or method

### Forecast output
- revenue
- gross margin
- implementation load
- sales capacity need
- base-case and range

### Sensitivity
- top 3 drivers
- what changes the conclusion

### Research next
- highest-value questions to reduce uncertainty

## Common traps

- starting from target ARR and backing into assumptions invisibly
- treating TAM as a revenue forecast
- using only a top-down market number without a go-to-market filter
- assuming enterprise deployment mix without evidence
- forgetting services burden in infrastructure-heavy products
- mixing monthly, annual, and one-time numbers
- giving a single point estimate where uncertainty is obviously large

## Relation to Fermi estimation

When direct measurement is weak or incomplete, use Fermi-style estimation as a support tool.
That means:
- explicit factors
- low / base / high values
- visible assumptions
- sanity checks against market and operational reality

Use Fermi estimation to fill gaps, not to replace all research.
