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

This skill includes a helper script for additive or multiplicative models.

Requirements:

- `python3`

Example:

```bash
python3 fermi-estimation/scripts/factor_product.py --input '{
  "mode": "product",
  "factors": [
    {"name": "population", "low": 900000, "base": 1000000, "high": 1100000, "unit": "people", "source": "census"},
    {"name": "buyers", "low": 0.08, "base": 0.10, "high": 0.12, "unit": "share", "source": "assumption"},
    {"name": "annual_spend", "low": 80, "base": 100, "high": 120, "unit": "USD", "source": "pricing"}
  ]
}' --format markdown
```

## Included resources

- `SKILL.md` - agent workflow and quality bar
- `scripts/factor_product.py` - deterministic calculator for low/base/high factors
- `references/evidence-patterns.md` - source selection and decomposition patterns
- `references/report-template.md` - compact answer template
