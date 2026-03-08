# fermi-estimation

Solve user questions with defensible Fermi estimates using explicit assumptions, source-backed inputs, uncertainty ranges, and sensitivity analysis.

This skill is optimized for:

- Market sizing and demand estimation
- Cost, revenue, capacity, and throughput estimation
- Transparent low/base/high modeling
- Source-backed answers with sanity checks and sensitivity analysis

## Install

Install this skill from the repo:

```bash
npx skills add tumf/skills --skill fermi-estimation
```

## Helper script

This skill includes a helper script for additive, multiplicative, and nested sum-of-products models.

Requirements:

- `python3`

Example:

```bash
python3 fermi-estimation/scripts/factor_model.py --input '{
  "name": "US CRM TAM",
  "mode": "sum",
  "groups": [
    {
      "name": "SMB",
      "mode": "product",
      "factors": [
        {"name": "firms", "low": 450000, "base": 500000, "high": 550000, "unit": "accounts", "geo": "US", "basis_type": "sourced", "source": "census"},
        {"name": "adoption", "low": 0.02, "base": 0.03, "high": 0.04, "unit": "share", "geo": "US", "basis_type": "derived", "source": "industry mix", "correlation_group": "demand", "scenarios": {"conservative": 0.025, "aggressive": 0.035}},
        {"name": "annual_spend", "low": 900, "base": 1200, "high": 1500, "currency": "USD", "period": "year", "geo": "US", "basis_type": "sourced", "source": "pricing pages", "correlation_group": "pricing", "scenarios": {"conservative": 1000, "aggressive": 1400}}
      ]
    },
    {
      "name": "Enterprise",
      "mode": "product",
      "factors": [
        {"name": "firms", "low": 10000, "base": 12000, "high": 14000, "unit": "accounts", "geo": "US", "basis_type": "sourced", "source": "census"},
        {"name": "adoption", "low": 0.12, "base": 0.15, "high": 0.18, "unit": "share", "geo": "US", "basis_type": "derived", "source": "industry mix", "correlation_group": "demand", "scenarios": {"conservative": 0.14, "aggressive": 0.17}},
        {"name": "annual_spend", "low": 40000, "base": 50000, "high": 65000, "currency": "USD", "period": "year", "geo": "US", "basis_type": "sourced", "source": "pricing pages", "correlation_group": "pricing", "scenarios": {"conservative": 45000, "aggressive": 60000}}
      ]
    }
  ]
}' --format markdown
```

The script validates empty groups, period names, source tiers, and sum-model consistency for `unit`, `period`, `currency`, `geo`, and `dimension`.

Optional fields:

- `scenarios.conservative` / `scenarios.aggressive` for scenario totals that are less extreme than literal low/high
- `correlation_group` to stress-test linked drivers together

`factor_product.py` remains available as a backward-compatible alias.

## End-to-end patterns

Use the skill for questions like:

- B2C market size: `population x target-share x purchase-frequency x spend`
- B2B TAM: `segment A product + segment B product + segment C product`
- Staffing: `tasks per period x minutes per task / productive minutes per worker`

## Included resources

- `SKILL.md` - agent workflow and quality bar
- `scripts/factor_model.py` - deterministic calculator for low/base/high factors and nested models
- `scripts/factor_product.py` - backward-compatible alias for the calculator
- `references/evidence-patterns.md` - source selection and decomposition patterns
- `references/report-template.md` - compact answer template
