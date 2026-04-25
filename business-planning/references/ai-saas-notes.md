# AI Agent / SaaS Planning Notes

Use this reference when the user is planning an AI agent, model infrastructure, or SaaS business.

These businesses often fail because the plan stays at the feature level.
Force a distinction between operator, buyer, user, and technical dependency.

## Questions to check explicitly

### Customer and buying process
- Who feels the pain?
- Who approves budget?
- Who integrates or operates the system?
- Who will resist adoption?

### Technical and deployment constraints
- Shared SaaS, dedicated cluster, VPC, on-prem, or air-gapped?
- What data may leave the customer environment?
- What observability and audit requirements exist?
- Is model portability a customer priority or only a founder thesis?

### Economic structure
- Is pricing per seat, per workspace, per request, per token, per GPU hour, or annual contract?
- What cost drivers scale fastest?
- Are margins destroyed by inference cost, support burden, or long sales cycles?
- What deployment mix should be assumed across shared SaaS, dedicated, VPC, and on-prem?
- What implementation and customer-success load must be modeled per account?
- What evidence exists for ACV, sales cycle, retention, and expansion assumptions?

### Competitive dynamics
- Is the real competitor another startup, an incumbent suite, internal engineering, or the status quo?
- Is the market buying a tool, a workflow outcome, or governance?
- Is the wedge a product feature, deployment model, cost advantage, compliance, or control?

## Common planning mistakes
- assuming the end user is the buyer
- underestimating implementation friction
- calling vendor flexibility a benefit without showing why the buyer cares
- ignoring services load hidden inside an apparent software business
- skipping unit economics because pricing is not final yet

## Helpful planning pattern
For AI SaaS or infrastructure, a strong default is:
- 3C for market reality
- Lean Canvas for hypothesis structure
- STP for segment focus
- Unit economics for viability
- KPI design for operating control

Add PEST when regulation, sovereignty, procurement rules, or cross-border data handling are material.

## Specific note for control-plane businesses
A control-plane business must usually prove value in one or more of these categories:
- governance and policy control
- vendor independence or model portability
- cost visibility and allocation
- deployment flexibility
- operational reliability across multiple model providers or clusters

If none of these are urgent to the buyer, the business may be a feature rather than a company.
