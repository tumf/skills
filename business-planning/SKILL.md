---
name: business-planning
description: Use this skill whenever the user asks to create, structure, review, or refine a business plan, new business proposal, growth strategy, GTM outline, or venture hypothesis. Build a rational, persuasive business plan with reader-specific framing and bottom-up numerical planning. Distinguish researched facts from benchmarks and estimates, use frameworks only as supporting tools, and forecast outcomes from causal drivers instead of reverse-engineering a desired result. Use it even when the user only says "事業計画", "戦略を考えたい", "新規事業を整理したい", or asks for AI agent / SaaS business planning without naming any framework.
---

# Business Planning

Use this skill to produce business plans that are both rational and persuasive.

The primary goal is not framework selection.
The primary goal is to help the user make and explain good business decisions.

Frameworks are only means.
Use them quietly in the background when they sharpen judgment, expose gaps, or improve communication.

## When to use

Use this skill when the user wants to:
- build a new business plan
- test whether a business idea is worth pursuing
- structure a strategy memo for a startup, SaaS, or AI agent business
- refine an existing plan so it becomes more convincing
- compare strategic directions and choose one
- define target customer, value proposition, differentiation, economics, or growth path
- turn a vague concept into an actionable plan

## Desired outcome

Produce a plan that does all of the following:
- explains what business should be built or pursued
- shows why the opportunity exists now
- identifies who pays and why they buy
- clarifies why this approach can win against alternatives
- makes key assumptions visible
- translates strategy into execution, metrics, and next steps
- turns the business logic into a bottom-up numerical plan
- forecasts plausible end states from accumulated evidence rather than reverse-engineering a desired outcome

A good plan is not just structured.
It is believable.
It can survive quantitative scrutiny.

## Operating principle

1. Start from the decision the user actually needs to make.
2. Separate facts, assumptions, and unknowns.
3. Identify the business logic before polishing the narrative.
4. Use frameworks only where they improve reasoning.
5. Convert analysis into choices, trade-offs, and action.
6. End with execution implications: KPI, experiments, milestones, and risks.

## Core thinking sequence

Follow this reasoning order unless the task clearly calls for another order:

### 1. Planning context
Clarify:
- what decision is being made
- what stage the business is in
- what time horizon matters
- what constraints matter most
- what output form the user needs
- who the primary reader is
- what that reader must believe, approve, or do after reading
- what level of detail, evidence, and risk discussion that reader expects

### 2. Business reality
Establish the minimum reality needed to avoid fantasy planning:
- customer and pain
- buyer and budget owner
- alternatives and competitors
- delivery constraints
- economic shape of the business

### 3. Strategic choice
Make explicit choices about:
- who to serve first
- what problem to solve first
- what offer to lead with
- what not to do yet
- what edge or wedge makes entry plausible

### 4. Business model
Define:
- revenue logic
- pricing logic if possible
- channel / distribution logic
- delivery model
- cost drivers
- what must scale efficiently

### 5. Execution logic
Turn the strategy into:
- MVP or first offer
- near-term milestones
- KGI and leading KPI
- experiments that reduce risk
- open questions that still need evidence

### 6. Persuasive narrative
Make sure the plan can answer:
- Why this market?
- Why this customer?
- Why this offer?
- Why now?
- Why us?
- Why will this make money?

### 7. Reader optimization
Optimize the plan for the main target reader.
Do not rewrite the business logic for each audience.
Keep the core logic stable, but change emphasis, ordering, evidence, and tone.

For every plan, identify:
- primary reader
- secondary readers if any
- decision expected after reading
- likely objections
- proof required to overcome those objections

Common reader patterns:
- Founder / internal team
  - emphasize clarity of choice, focus, trade-offs, and execution sequence
  - be explicit about what not to do yet
- Executive approver / board
  - emphasize strategic fit, risk, resource needs, and milestones
  - show downside control and why this deserves prioritization
- Investor
  - emphasize market size, timing, wedge, defensibility, capital efficiency, and scale path
  - show why this can become a meaningful business, not just a useful feature
- Business partner / enterprise buyer
  - emphasize pain solved, ROI, deployment fit, implementation risk, and credibility
  - reduce theory and increase practical adoption logic
- Technical evaluator
  - emphasize feasibility, architecture implications, integration constraints, and operational risks
  - connect technical choices to business consequences

If the user does not specify the audience, infer the most likely primary reader from the task.
If audience optimization is central, read `references/readers.md`.

## Numerical planning principle

Do not start from a target valuation, target ARR, or desired headline outcome and work backward invisibly.
Start from observable facts, explicit assumptions, and causal drivers.
Then project the business forward.

Use this sequence for numerical planning:
1. collect what can be directly researched
2. identify missing variables that still matter materially
3. estimate the missing variables with labeled methods
4. build a sparse driver model
5. generate low / base / high outcomes
6. stress-test the result against operational and market reality
7. show which assumptions matter most

If exact data is missing, estimate transparently.
If uncertainty is large, widen ranges instead of pretending precision.
If the user needs a hard number, still show the range and the base case.

## Research before estimation

Before inventing assumptions, gather accessible evidence such as:
- public pricing pages
- public filings and annual reports
- regulator or official statistics
- market-share or category benchmarks
- public job posts, case studies, implementation stories, and procurement signals
- customer interviews, pipeline notes, or user-provided internal evidence
- adjacent-company metrics that can anchor conversion, sales cycle, or margin assumptions

For AI / SaaS businesses, explicitly research or estimate:
- addressable customer count by segment
- expected deal size or contract structure
- deployment mix: shared SaaS, dedicated, VPC, on-prem
- gross-margin shape by serving model
- sales cycle length and implementation burden
- retention or expansion drivers
- support and services load

## Estimation when data is incomplete

When a critical variable cannot be directly measured, use one of these methods and label it:
- benchmark transfer from a close analog
- bottom-up operational estimate
- top-down market allocation
- Fermi estimate with explicit low / base / high inputs
- scenario assumption stated as assumption, not fact

Prefer the smallest useful model with 3 to 7 drivers.
Do not create fake rigor by multiplying too many weak assumptions.

If the quantitative problem is substantial, read `references/numeric-planning.md`.
If exact data is unavailable or fragmented, use the approach in `fermi-estimation` as a supporting method.

## How to use frameworks

Do not present frameworks as the product.
Use them as hidden scaffolding unless the user explicitly wants to see them.

Typical uses:
- 3C when customer / company / competitor must be clarified
- PEST when regulation, macro shifts, or technology change matters
- SWOT when integrating internal and external findings into strategic direction
- Lean Canvas or Business Model Canvas when the business model is still fuzzy
- 5 Forces when structural margin pressure matters
- STP when target segment and positioning are unclear
- Ansoff when the key question is growth path
- KGI / KPI when execution tracking matters
- Unit economics when acquisition cost, retention, or gross margin is central
- Lean Startup or Design Thinking when uncertainty must be reduced through learning

Use the smallest useful set.
Usually 2 to 4 frameworks are enough.

If the user asks which frameworks were used or wants the reasoning exposed, read `references/framework-selection.md` and summarize only the relevant ones.
If you need a compact reminder of the supported frameworks, read `references/frameworks.md`.

## Plan quality standards

A strong plan should include:

### 1. Opportunity claim
- what opportunity exists
- why it is economically meaningful
- why now is a good entry point

### 2. Customer logic
- specific target customer
- concrete pain or desired outcome
- why they will switch or pay

### 3. Offer logic
- product or service scope
- what is in scope first
- what is deliberately deferred

### 4. Competitive logic
- current alternatives
- why this plan can win anyway
- what edge is durable versus temporary

### 5. Economic logic
- how revenue happens
- what costs dominate
- what assumptions drive profitability
- what must be true for the model to work

### 6. Numerical logic
- what variables are directly evidenced versus estimated
- what the driver tree looks like
- low / base / high scenario outputs
- what the near-term metrics imply for later outcomes
- which assumptions dominate the forecast
- where the model is still weak and needs further research

### 7. Execution logic
- next 30 to 90 days
- milestones
- metrics
- experiments
- major dependencies

### 7. Risk logic
- strategic risks
- market risks
- operational risks
- assumption-sensitive areas

## Default output structure

Use this structure unless the user asks otherwise:

### Theme
- One-line restatement of the business planning task

### Executive view
- recommended direction
- why this is the rational choice
- what must be true for success
- why the primary reader should accept or support it now

### Planning context
- stage
- scope
- assumptions
- constraints

### Business plan
- Customer
- Problem
- Value proposition
- Offer
- Revenue model
- Delivery / channel
- Competitive edge
- Growth path

### Economics and validation
- key economic assumptions
- what is directly evidenced vs estimated
- driver model summary
- low / base / high scenario outputs
- unit economics assumptions if relevant
- KGI
- leading KPI
- MVP / pilot / experiment plan
- what to research next to improve forecast confidence

### Risks and open questions
- top risks
- unresolved assumptions
- what to verify next

### Immediate next actions
- next 30 days
- next 90 days

## Reader-tailored emphasis

Before finalizing, tune the draft for the main reader.
Change the emphasis, proof style, and section ordering as needed.

### Founder / internal team
Prioritize:
- strategic focus
- trade-offs
- execution sequence
- KPI and learning plan

### Executive approver / board
Prioritize:
- strategic rationale
- resource ask
- risk management
- milestone visibility

### Investor
Prioritize:
- market size and timing
- growth logic
- defensibility
- capital efficiency
- scale narrative

### Business partner / enterprise buyer
Prioritize:
- customer problem
- ROI or business impact
- implementation path
- deployment and compliance fit
- proof of reliability

### Technical evaluator
Prioritize:
- feasibility
- integration constraints
- architecture implications
- operational burden
- security and governance concerns

## Output variants

### If the user wants a one-page internal memo
Compress into:
- Situation
- Recommended strategy
- Why it works
- Economics
- 90-day execution plan
- Risks

### If the user wants investor-facing planning
Add:
- market size assumption
- why this team can win
- capital efficiency or use of funds
- milestone narrative
- why this can become a venture-scale or strategically meaningful business

### If the user wants executive or board approval
Add:
- strategic fit with current business or portfolio
- resource requirement and opportunity cost
- downside risks and control points
- decision gates and review cadence

### If the user wants enterprise buyer or partner persuasion
Add:
- ROI logic
- implementation scope and time-to-value
- deployment, compliance, and procurement fit
- proof points needed for trust

### If the user wants technical stakeholder buy-in
Add:
- architecture implications
- integration burden
- operational ownership
- security, governance, and observability implications

### If the user wants a workshop-ready draft
Add:
- decision points needing discussion
- assumptions needing validation
- options rejected and why

## Practical rules

- Do not hide uncertainty. Label assumptions clearly.
- Do not turn framework output into a fake conclusion.
- Do not confuse a feature list with a business model.
- Do not discuss expansion before basic viability is visible.
- Do not fabricate precise numbers when inputs are missing.
- If data is missing, define formulas, thresholds, evidence needed, and the estimation method used.
- Prefer low / base / high ranges over false precision.
- Show what part of the forecast is measured, benchmarked, or estimated.
- Prefer crisp trade-offs over generic completeness.

## Special guidance for AI agent / SaaS businesses

When the business involves AI, agent systems, or model infrastructure, check explicitly:
- buyer vs end user distinction
- deployment model requirements: SaaS, dedicated, VPC, on-prem, air-gapped
- compliance and data-governance constraints
- model / vendor dependency risk
- switching cost and lock-in dynamics
- observability, billing, and control-plane needs
- whether the business is truly a company or only a feature

If the user is exploring an AI infrastructure business, read `references/ai-saas-notes.md`.
If the user wants a reusable plan skeleton, read `references/business-plan-template.md`.

## Anti-patterns

Avoid these mistakes:
- dumping named frameworks instead of building a case
- writing a neat story with no business logic underneath
- failing to name the actual buyer
- claiming differentiation without a specific target segment
- recommending growth before validating economics
- presenting assumptions as facts
- listing KPIs that do not connect to the business model

## Quick operating flow

1. Restate the business question.
2. Clarify stage, uncertainty, and constraints.
3. Build the business logic.
4. Use only the supporting frameworks needed.
5. Synthesize into a clear, persuasive plan.
6. Add metrics, experiments, risks, and next actions.
7. Translate the business into a bottom-up numerical forecast and show uncertainty.

Keep the answer practical, structured, and decision-oriented.
