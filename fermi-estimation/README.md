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
      "correlation": {"group": "demand", "direction": "positive", "strength": 0.8, "apply_to": ["volume"]},
      "factors": [
        {"name": "firms", "low": 450000, "base": 500000, "high": 550000, "unit": "accounts", "geo": "US", "basis_type": "sourced", "source": "census", "tags": ["volume"]},
        {"name": "adoption", "low": 0.02, "base": 0.03, "high": 0.04, "unit": "share", "geo": "US", "basis_type": "derived", "source": "industry mix", "tags": ["volume"], "scenarios": {"conservative": 0.025, "aggressive": 0.035}},
        {"name": "annual_spend", "low": 900, "base": 1200, "high": 1500, "currency": "USD", "period": "year", "geo": "US", "basis_type": "sourced", "source": "pricing pages", "correlation": {"group": "pricing"}, "scenarios": {"conservative": 1000, "aggressive": 1400}}
      ]
    },
    {
      "name": "Enterprise",
      "mode": "product",
      "correlation": {"group": "demand", "direction": "positive", "strength": 0.8, "apply_to": ["volume"]},
      "factors": [
        {"name": "firms", "low": 10000, "base": 12000, "high": 14000, "unit": "accounts", "geo": "US", "basis_type": "sourced", "source": "census", "tags": ["volume"]},
        {"name": "adoption", "low": 0.12, "base": 0.15, "high": 0.18, "unit": "share", "geo": "US", "basis_type": "derived", "source": "industry mix", "tags": ["volume"], "scenarios": {"conservative": 0.14, "aggressive": 0.17}},
        {"name": "annual_spend", "low": 40000, "base": 50000, "high": 65000, "currency": "USD", "period": "year", "geo": "US", "basis_type": "sourced", "source": "pricing pages", "correlation": {"group": "pricing", "direction": "negative", "strength": 0.6}, "scenarios": {"conservative": 45000, "aggressive": 60000}}
      ]
    }
  ]
}' --format markdown
```

The script validates empty groups, period names, source tiers, and sum-model consistency for `unit`, `period`, `currency`, `geo`, and `dimension`.

Monte Carlo options:

- Add `"monte_carlo": {"enabled": true, "samples": 5000, "seed": 42}` to the payload, or pass `--samples 5000 --seed 42`
- Sampling uses a triangular distribution anchored on each factor's `low`, `base`, and `high`
- If correlation groups are present, Monte Carlo uses them by default via shared group quantiles; disable with `"correlated_groups": false`
- Output includes `p05`, `p50`, `p95`, `mean`, `min`, and `max`

Optional fields:

- `scenarios.conservative` / `scenarios.aggressive` for scenario totals that are less extreme than literal low/high
- `correlation_group` to stress-test linked drivers together
- `correlation_direction` as `positive` or `negative` to flip a driver's move within the group
- `correlation_strength` from `0` to `1` to dampen how far the correlated move goes
- `correlation: {group, direction, strength}` on a group or factor to set inherited defaults without repeating the same fields
- `tags` on factors plus `correlation.apply_to` on a group to target inherited correlation only to selected drivers

Example correlated output excerpt:

```markdown
## Bottom line
- Best estimate: about 108M
- Plausible range: about 56M to about 197M
- Scenario view: conservative about 74M, base about 108M, aggressive about 170M
- Monte Carlo: p05 about 77M, p50 about 106M, p95 about 145M, mean about 109M from 5000 draws, correlated across 2 groups

## Sensitivity and confidence
- Biggest uncertainty: US CRM TAM > Enterprise > annual_spend
- Correlated groups:
  - pricing: total moves from about 101M to about 121M when this group moves together [US CRM TAM > Enterprise > annual_spend (negative, 0.60), US CRM TAM > SMB > annual_spend (negative, 0.60)]
  - demand: total moves from about 101M to about 120M when this group moves together [US CRM TAM > Enterprise > adoption (positive, 0.80), US CRM TAM > SMB > adoption (positive, 0.80)]
```

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
