#!/usr/bin/env python3
"""Compute additive, multiplicative, and nested Fermi estimates."""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from copy import deepcopy
from pathlib import Path

ALLOWED_MODES = {"product", "sum"}
SCENARIO_NAMES = ("conservative", "base", "aggressive")
ALLOWED_PERIODS = {
    "hour",
    "day",
    "week",
    "month",
    "quarter",
    "year",
    "one_time",
}
METADATA_KEYS = (
    "unit",
    "period",
    "currency",
    "geo",
    "dimension",
    "basis_type",
    "source",
    "source_url",
    "source_tier",
    "as_of",
    "note",
    "tags",
    "correlation_group",
    "correlation_direction",
)
SUM_CONSISTENCY_KEYS = ("unit", "period", "currency", "geo", "dimension")
ALLOWED_CORRELATION_DIRECTIONS = {"positive", "negative"}
DEFAULT_MONTE_CARLO_SAMPLES = 5000


def load_payload(raw_input: str) -> dict:
    try:
        path = Path(raw_input)
        if path.exists():
            return json.loads(path.read_text())
    except OSError:
        pass
    return json.loads(raw_input)


def to_float(value: object, factor_name: str, key: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"Factor '{factor_name}' has non-numeric {key}: {value!r}")
    return float(value)


def validate_period(name: str, period: object) -> str:
    if period in (None, ""):
        return ""
    if not isinstance(period, str):
        raise ValueError(f"Factor '{name}' has non-string period: {period!r}")
    if period not in ALLOWED_PERIODS:
        allowed = ", ".join(sorted(ALLOWED_PERIODS))
        raise ValueError(
            f"Factor '{name}' has unsupported period '{period}'. Expected one of: {allowed}"
        )
    return period


def validate_source_tier(name: str, source_tier: object) -> int | None:
    if source_tier in (None, ""):
        return None
    if not isinstance(source_tier, int):
        raise ValueError(
            f"Factor '{name}' has non-integer source_tier: {source_tier!r}"
        )
    if not 1 <= source_tier <= 6:
        raise ValueError(f"Factor '{name}' has source_tier outside 1-6")
    return source_tier


def validate_correlation_direction(name: str, direction: object) -> str:
    if direction in (None, ""):
        return ""
    if not isinstance(direction, str):
        raise ValueError(
            f"Factor '{name}' has non-string correlation_direction: {direction!r}"
        )
    if direction not in ALLOWED_CORRELATION_DIRECTIONS:
        allowed = ", ".join(sorted(ALLOWED_CORRELATION_DIRECTIONS))
        raise ValueError(
            f"Factor '{name}' has unsupported correlation_direction '{direction}'. Expected one of: {allowed}"
        )
    return direction


def validate_correlation_strength(name: str, strength: object) -> float:
    if strength in (None, ""):
        return 1.0
    if not isinstance(strength, (int, float)):
        raise ValueError(
            f"Factor '{name}' has non-numeric correlation_strength: {strength!r}"
        )
    value = float(strength)
    if value < 0 or value > 1:
        raise ValueError(
            f"Factor '{name}' has correlation_strength outside 0-1: {strength!r}"
        )
    return value


def validate_string_list(name: str, key: str, value: object) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise ValueError(f"Factor or group '{name}' has non-list {key}: {value!r}")
    normalized = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError(
                f"Factor or group '{name}' has non-string {key} entry: {item!r}"
            )
        normalized.append(item)
    return normalized


def correlation_applies_to_factor(
    factor: dict, inherited: dict[str, object] | None
) -> bool:
    if not inherited:
        return True
    apply_to = inherited.get("correlation_apply_to", [])
    if not apply_to:
        return True
    if not isinstance(apply_to, list):
        return True
    factor_tags = set(
        validate_string_list(
            factor.get("name", "factor"), "tags", factor.get("tags", [])
        )
    )
    return bool(factor_tags.intersection(apply_to))


def merge_correlation_config(
    owner_name: str, raw_node: dict, inherited: dict[str, object] | None = None
) -> dict[str, object]:
    inherited = inherited or {}
    raw_config = raw_node.get("correlation", {})
    if raw_config in (None, ""):
        raw_config = {}
    if not isinstance(raw_config, dict):
        raise ValueError(
            f"Group or factor '{owner_name}' has non-object correlation: {raw_config!r}"
        )

    group = raw_node.get("correlation_group")
    if group is None:
        group = raw_config.get("group", inherited.get("correlation_group", ""))
    direction = raw_node.get("correlation_direction")
    if direction is None:
        direction = raw_config.get(
            "direction", inherited.get("correlation_direction", "")
        )
    strength = raw_node.get("correlation_strength")
    if strength is None:
        strength = raw_config.get(
            "strength", inherited.get("correlation_strength", 1.0)
        )
    apply_to = raw_config.get("apply_to", inherited.get("correlation_apply_to", []))
    apply_to = validate_string_list(owner_name, "correlation.apply_to", apply_to)

    if group in (None, ""):
        return {
            "correlation_group": "",
            "correlation_direction": "",
            "correlation_strength": 1.0,
            "correlation_apply_to": apply_to,
        }
    if not isinstance(group, str):
        raise ValueError(
            f"Group or factor '{owner_name}' has non-string correlation_group: {group!r}"
        )

    return {
        "correlation_group": group,
        "correlation_direction": validate_correlation_direction(owner_name, direction),
        "correlation_strength": validate_correlation_strength(owner_name, strength),
        "correlation_apply_to": apply_to,
    }


def validate_factor(
    factor: dict,
    index: int,
    prefix: str = "",
    inherited_correlation: dict[str, object] | None = None,
) -> dict:
    name = factor.get("name") or f"factor_{index}"
    qualified_name = f"{prefix}{name}" if prefix else name
    base = factor.get("base")
    low = factor.get("low", base)
    high = factor.get("high", base)

    if base is None:
        raise ValueError(f"Factor '{qualified_name}' is missing 'base'")

    values = {"low": low, "base": base, "high": high}
    for key, value in values.items():
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Factor '{qualified_name}' has non-numeric {key}: {value!r}"
            )

    low_value = to_float(low, qualified_name, "low")
    base_value = to_float(base, qualified_name, "base")
    high_value = to_float(high, qualified_name, "high")

    if low_value > base_value or base_value > high_value:
        raise ValueError(f"Factor '{qualified_name}' must satisfy low <= base <= high")

    item = {
        "kind": "factor",
        "name": name,
        "path": qualified_name,
        "low": low_value,
        "base": base_value,
        "high": high_value,
    }

    scenario_values = factor.get("scenarios", {})
    if scenario_values in (None, ""):
        scenario_values = {}
    if not isinstance(scenario_values, dict):
        raise ValueError(
            f"Factor '{qualified_name}' has non-object scenarios: {scenario_values!r}"
        )

    normalized_scenarios = {"base": base_value}
    for scenario_name in ("conservative", "aggressive"):
        raw_value = scenario_values.get(scenario_name)
        if raw_value is None:
            continue
        normalized_scenarios[scenario_name] = to_float(
            raw_value, qualified_name, f"scenarios.{scenario_name}"
        )

    conservative_value = normalized_scenarios.get("conservative", low_value)
    aggressive_value = normalized_scenarios.get("aggressive", high_value)
    if conservative_value > base_value:
        raise ValueError(f"Factor '{qualified_name}' must satisfy conservative <= base")
    if aggressive_value < base_value:
        raise ValueError(f"Factor '{qualified_name}' must satisfy base <= aggressive")

    item["scenarios"] = {
        "conservative": conservative_value,
        "base": base_value,
        "aggressive": aggressive_value,
    }
    inherited_for_factor = inherited_correlation
    if inherited_for_factor and not correlation_applies_to_factor(
        factor, inherited_for_factor
    ):
        inherited_for_factor = {
            "correlation_group": "",
            "correlation_direction": "",
            "correlation_strength": 1.0,
            "correlation_apply_to": [],
        }
    item.update(merge_correlation_config(qualified_name, factor, inherited_for_factor))
    item["tags"] = validate_string_list(qualified_name, "tags", factor.get("tags", []))

    for key in METADATA_KEYS:
        if key == "period":
            item[key] = validate_period(qualified_name, factor.get(key, ""))
        elif key == "tags":
            continue
        elif key == "correlation_direction":
            continue
        elif key == "source_tier":
            item[key] = validate_source_tier(qualified_name, factor.get(key))
        elif key == "correlation_group":
            continue
        else:
            value = factor.get(key, "")
            if value is None:
                value = ""
            if key != "source_tier" and value != "" and not isinstance(value, str):
                raise ValueError(
                    f"Factor '{qualified_name}' has non-string {key}: {value!r}"
                )
            item[key] = value

    return item


def ensure_children(name: str, children: list[dict]) -> None:
    if not children:
        raise ValueError(f"Group '{name}' must contain at least one factor or subgroup")


def coalesce_field(children: list[dict], key: str) -> str:
    values = {
        child.get(key, "") for child in children if child.get(key, "") not in (None, "")
    }
    if len(values) > 1:
        ordered = ", ".join(sorted(values))
        raise ValueError(f"Sum model mixes {key} values: {ordered}")
    return next(iter(values), "")


def unique_values(children: list[dict], key: str) -> set[str]:
    return {
        child.get(key, "") for child in children if child.get(key, "") not in (None, "")
    }


def infer_group_metadata(node: dict, mode: str, children: list[dict]) -> dict:
    metadata = {}
    for key in METADATA_KEYS:
        if key == "tags":
            metadata[key] = []
            continue
        explicit_value = node.get(key, "")
        if explicit_value not in (None, ""):
            metadata[key] = explicit_value
            continue
        if mode == "sum" and key in SUM_CONSISTENCY_KEYS:
            metadata[key] = coalesce_field(children, key)
            continue
        values = unique_values(children, key)
        if key == "geo":
            metadata[key] = next(iter(values), "") if len(values) <= 1 else ""
        elif key in {"period", "currency"}:
            metadata[key] = next(iter(values), "") if len(values) == 1 else ""
        else:
            metadata[key] = ""
    return metadata


def parse_node(node: dict, prefix: str = "") -> dict:
    if not isinstance(node, dict):
        raise ValueError(f"Each model node must be an object, got: {node!r}")

    mode = node.get("mode", "product")
    if mode not in ALLOWED_MODES:
        raise ValueError(f"Unsupported mode: {mode}")

    name = node.get("name") or "model"
    qualified_name = f"{prefix}{name}" if prefix else name
    inherited_correlation = merge_correlation_config(qualified_name, node)
    factors = node.get("factors", [])
    groups = node.get("groups", [])

    if not isinstance(factors, list):
        raise ValueError(f"Group '{qualified_name}' has non-list 'factors'")
    if not isinstance(groups, list):
        raise ValueError(f"Group '{qualified_name}' has non-list 'groups'")

    children = []
    for index, factor in enumerate(factors, start=1):
        children.append(
            validate_factor(
                factor,
                index,
                prefix=f"{qualified_name} > ",
                inherited_correlation=inherited_correlation,
            )
        )
    for index, group in enumerate(groups, start=1):
        child_name = group.get("name") or f"group_{index}"
        group_prefix = f"{qualified_name} > "
        child_group = {**group, "name": child_name}
        child_group.setdefault("correlation", inherited_correlation)
        parsed_group = parse_node(child_group, prefix=group_prefix)
        children.append(parsed_group)

    ensure_children(qualified_name, children)

    totals = compute_total(children, mode)
    metadata = infer_group_metadata(node, mode, children)
    return {
        "kind": "group",
        "name": name,
        "path": qualified_name,
        "mode": mode,
        "children": children,
        "low": totals["low"],
        "base": totals["base"],
        "high": totals["high"],
        **metadata,
    }


def compute_total(children: list[dict], mode: str) -> dict:
    if mode == "product":
        low = 1.0
        base = 1.0
        high = 1.0
        for child in children:
            low *= child["low"]
            base *= child["base"]
            high *= child["high"]
    else:
        low = sum(child["low"] for child in children)
        base = sum(child["base"] for child in children)
        high = sum(child["high"] for child in children)
    return {"mode": mode, "low": low, "base": base, "high": high}


def compute_node_value(children: list[float], mode: str) -> float:
    if mode == "product":
        total = 1.0
        for child in children:
            total *= child
        return total
    return sum(children)


def flatten_factors(node: dict) -> list[dict]:
    if node["kind"] == "factor":
        return [node]
    factors = []
    for child in node["children"]:
        factors.extend(flatten_factors(child))
    return factors


def sample_factor_value(factor: dict, rng: random.Random) -> float:
    return rng.triangular(factor["low"], factor["high"], factor["base"])


def triangular_quantile(low: float, high: float, mode: float, q: float) -> float:
    if q <= 0:
        return low
    if q >= 1:
        return high
    if high == low:
        return low
    midpoint = (mode - low) / (high - low)
    if q < midpoint:
        return low + math.sqrt(q * (high - low) * (mode - low))
    return high - math.sqrt((1 - q) * (high - low) * (high - mode))


def monte_carlo_factor_value(
    factor: dict, rng: random.Random, group_quantiles: dict[str, float]
) -> float:
    group = factor.get("correlation_group", "")
    independent_q = rng.random()
    if not group:
        return triangular_quantile(
            factor["low"], factor["high"], factor["base"], independent_q
        )

    group_q = group_quantiles[group]
    direction = factor.get("correlation_direction", "") or "positive"
    if direction == "negative":
        group_q = 1.0 - group_q
    strength = factor.get("correlation_strength", 1.0)
    effective_q = ((1.0 - strength) * independent_q) + (strength * group_q)
    return triangular_quantile(
        factor["low"], factor["high"], factor["base"], effective_q
    )


def sample_node_value(node: dict, rng: random.Random) -> float:
    if node["kind"] == "factor":
        return sample_factor_value(node, rng)
    child_values = [sample_node_value(child, rng) for child in node["children"]]
    return compute_node_value(child_values, node["mode"])


def sample_node_value_correlated(
    node: dict, rng: random.Random, group_quantiles: dict[str, float]
) -> float:
    if node["kind"] == "factor":
        return monte_carlo_factor_value(node, rng, group_quantiles)
    child_values = [
        sample_node_value_correlated(child, rng, group_quantiles)
        for child in node["children"]
    ]
    return compute_node_value(child_values, node["mode"])


def percentile(sorted_values: list[float], value: float) -> float:
    if not sorted_values:
        raise ValueError("Cannot compute percentile on empty sample set")
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * value
    lower_index = math.floor(position)
    upper_index = math.ceil(position)
    if lower_index == upper_index:
        return sorted_values[lower_index]
    weight = position - lower_index
    lower = sorted_values[lower_index]
    upper = sorted_values[upper_index]
    return lower + ((upper - lower) * weight)


def resolve_monte_carlo_config(
    payload: dict, samples_override: int | None, seed_override: int | None
) -> dict | None:
    raw_config = payload.get("monte_carlo", {})
    if raw_config in (None, ""):
        raw_config = {}
    if not isinstance(raw_config, dict):
        raise ValueError(f"Model has non-object monte_carlo config: {raw_config!r}")

    enabled = raw_config.get("enabled")
    if enabled is None:
        enabled = samples_override is not None
    if not isinstance(enabled, bool):
        raise ValueError(f"Model has non-boolean monte_carlo.enabled: {enabled!r}")
    if not enabled:
        return None

    samples = samples_override
    if samples is None:
        samples = raw_config.get("samples", DEFAULT_MONTE_CARLO_SAMPLES)
    if not isinstance(samples, int) or samples <= 0:
        raise ValueError(f"Model has invalid monte_carlo sample count: {samples!r}")

    seed = seed_override if seed_override is not None else raw_config.get("seed")
    if seed is not None and not isinstance(seed, int):
        raise ValueError(f"Model has non-integer monte_carlo seed: {seed!r}")

    correlated_groups = raw_config.get("correlated_groups", True)
    if not isinstance(correlated_groups, bool):
        raise ValueError(
            "Model has non-boolean monte_carlo.correlated_groups: "
            f"{correlated_groups!r}"
        )

    return {
        "enabled": True,
        "samples": samples,
        "seed": seed,
        "correlated_groups": correlated_groups,
    }


def monte_carlo_summary(model: dict, config: dict | None) -> dict | None:
    if not config:
        return None
    rng = random.Random(config.get("seed"))
    groups = sorted(factor_paths_by_correlation_group(model))
    use_correlated_groups = bool(groups) and config.get("correlated_groups", True)
    draws = []
    for _ in range(config["samples"]):
        if use_correlated_groups:
            group_quantiles = {group: rng.random() for group in groups}
            draws.append(sample_node_value_correlated(model, rng, group_quantiles))
        else:
            draws.append(sample_node_value(model, rng))
    draws.sort()
    mean = sum(draws) / len(draws)
    return {
        "samples": config["samples"],
        "seed": config.get("seed"),
        "correlated_groups": use_correlated_groups,
        "group_count": len(groups) if use_correlated_groups else 0,
        "mean": mean,
        "p05": percentile(draws, 0.05),
        "p50": percentile(draws, 0.50),
        "p95": percentile(draws, 0.95),
        "min": draws[0],
        "max": draws[-1],
    }


def factor_scenario_value(factor: dict, scenario_name: str) -> float:
    if scenario_name == "conservative":
        return factor["scenarios"]["conservative"]
    if scenario_name == "aggressive":
        return factor["scenarios"]["aggressive"]
    return factor["base"]


def interpolated_value(base: float, target: float, strength: float) -> float:
    return base + ((target - base) * strength)


def set_factor_value(node: dict, target_path: str, scenario_key: str) -> None:
    if node["kind"] == "factor":
        if node["path"] == target_path:
            value = node[scenario_key]
            node["low"] = value
            node["base"] = value
            node["high"] = value
        else:
            value = node["base"]
            node["low"] = value
            node["base"] = value
            node["high"] = value
        return

    for child in node["children"]:
        set_factor_value(child, target_path, scenario_key)

    totals = compute_total(node["children"], node["mode"])
    node["low"] = totals["low"]
    node["base"] = totals["base"]
    node["high"] = totals["high"]


def set_model_to_scenario(node: dict, scenario_name: str) -> None:
    if node["kind"] == "factor":
        value = factor_scenario_value(node, scenario_name)
        node["low"] = value
        node["base"] = value
        node["high"] = value
        return

    for child in node["children"]:
        set_model_to_scenario(child, scenario_name)

    totals = compute_total(node["children"], node["mode"])
    node["low"] = totals["low"]
    node["base"] = totals["base"]
    node["high"] = totals["high"]


def sensitivity_entries(model: dict) -> list[dict]:
    base_total = model["base"]
    factors = flatten_factors(model)
    entries = []

    for factor in factors:
        low_model = deepcopy(model)
        high_model = deepcopy(model)
        set_factor_value(low_model, factor["path"], "low")
        set_factor_value(high_model, factor["path"], "high")

        low_total = low_model["base"]
        high_total = high_model["base"]
        swing = max(abs(base_total - low_total), abs(high_total - base_total))

        entries.append(
            {
                "name": factor["name"],
                "path": factor["path"],
                "base": factor["base"],
                "factor_low": factor["low"],
                "factor_high": factor["high"],
                "total_if_low": low_total,
                "total_if_high": high_total,
                "swing": swing,
            }
        )

    return sorted(entries, key=lambda item: item["swing"], reverse=True)


def factor_paths_by_correlation_group(model: dict) -> dict[str, list[dict]]:
    grouped = {}
    for factor in flatten_factors(model):
        group = factor.get("correlation_group", "")
        if not group:
            continue
        grouped.setdefault(group, []).append(factor)
    return grouped


def correlation_target_value(factor: dict, scenario_name: str) -> float:
    direction = factor.get("correlation_direction", "") or "positive"
    if direction == "negative":
        mapped_scenario = (
            "aggressive" if scenario_name == "conservative" else "conservative"
        )
    else:
        mapped_scenario = scenario_name
    raw_target = factor_scenario_value(factor, mapped_scenario)
    return interpolated_value(
        factor["base"], raw_target, factor.get("correlation_strength", 1.0)
    )


def set_paths_to_scenario(
    node: dict, target_factors: dict[str, dict], scenario_name: str
) -> None:
    if node["kind"] == "factor":
        if node["path"] in target_factors:
            value = correlation_target_value(
                target_factors[node["path"]], scenario_name
            )
        else:
            value = node["base"]
        node["low"] = value
        node["base"] = value
        node["high"] = value
        return

    for child in node["children"]:
        set_paths_to_scenario(child, target_factors, scenario_name)

    totals = compute_total(node["children"], node["mode"])
    node["low"] = totals["low"]
    node["base"] = totals["base"]
    node["high"] = totals["high"]


def correlation_entries(model: dict) -> list[dict]:
    base_total = model["base"]
    entries = []
    for group, factors in factor_paths_by_correlation_group(model).items():
        conservative_model = deepcopy(model)
        aggressive_model = deepcopy(model)
        target_factors = {factor["path"]: factor for factor in factors}
        set_paths_to_scenario(conservative_model, target_factors, "conservative")
        set_paths_to_scenario(aggressive_model, target_factors, "aggressive")
        low_total = conservative_model["base"]
        high_total = aggressive_model["base"]
        swing = max(abs(base_total - low_total), abs(high_total - base_total))
        lower_total = min(low_total, high_total)
        upper_total = max(low_total, high_total)
        entries.append(
            {
                "correlation_group": group,
                "paths": sorted(target_factors),
                "drivers": [
                    {
                        "path": factor["path"],
                        "direction": factor.get("correlation_direction", "")
                        or "positive",
                        "strength": factor.get("correlation_strength", 1.0),
                    }
                    for factor in sorted(factors, key=lambda item: item["path"])
                ],
                "total_if_conservative": low_total,
                "total_if_aggressive": high_total,
                "total_lower": lower_total,
                "total_upper": upper_total,
                "swing": swing,
            }
        )
    return sorted(entries, key=lambda item: item["swing"], reverse=True)


def scenario_totals(model: dict) -> dict[str, float]:
    totals = {}
    for scenario_name in SCENARIO_NAMES:
        scenario_model = deepcopy(model)
        set_model_to_scenario(scenario_model, scenario_name)
        totals[scenario_name] = scenario_model["base"]
    return totals


def short_number(value: float) -> str:
    magnitude = abs(value)
    suffixes = (
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "k"),
    )
    for threshold, suffix in suffixes:
        if magnitude >= threshold:
            scaled = value / threshold
            precision = 1 if abs(scaled) < 10 else 0
            return f"{scaled:.{precision}f}{suffix}"
    if magnitude >= 1:
        return f"{value:,.2f}".rstrip("0").rstrip(".")
    if value == 0:
        return "0"
    return f"{value:.3g}"


def headline_number(value: float) -> str:
    if value == 0:
        return "about 0"
    return f"about {short_number(value)}"


def metadata_summary(node: dict) -> str:
    parts = []
    for key in ("geo", "period", "unit", "currency", "dimension"):
        value = node.get(key, "")
        if value:
            parts.append(f"{key}={value}")
    return ", ".join(parts) if parts else "-"


def formula(node: dict) -> str:
    if node["kind"] == "factor":
        return node["name"]
    joiner = " x " if node["mode"] == "product" else " + "
    pieces = [formula(child) for child in node["children"]]
    if len(pieces) == 1:
        return pieces[0]
    return f"({joiner.join(pieces)})"


def render_inputs_rows(model: dict) -> list[str]:
    rows = []
    for factor in flatten_factors(model):
        basis = factor.get("basis_type", "") or "-"
        source = factor.get("source", "") or factor.get("source_url", "") or "-"
        rows.append(
            "| {path} | {low} | {base} | {high} | {basis} | {source} | {meta} | {scenario} |".format(
                path=factor["path"],
                low=short_number(factor["low"]),
                base=short_number(factor["base"]),
                high=short_number(factor["high"]),
                basis=basis,
                source=source,
                meta=metadata_summary(factor),
                scenario=render_factor_scenarios(factor),
            )
        )
    return rows


def render_factor_scenarios(factor: dict) -> str:
    parts = []
    scenario_map = factor["scenarios"]
    if scenario_map["conservative"] != factor["low"]:
        parts.append(f"cons={short_number(scenario_map['conservative'])}")
    if scenario_map["aggressive"] != factor["high"]:
        parts.append(f"aggr={short_number(scenario_map['aggressive'])}")
    if factor.get("correlation_group", ""):
        parts.append(f"corr={factor['correlation_group']}")
    direction = factor.get("correlation_direction", "")
    if direction:
        parts.append(f"dir={direction}")
    strength = factor.get("correlation_strength", 1.0)
    if strength != 1.0:
        parts.append(f"strength={strength:.2f}")
    return ", ".join(parts) if parts else "-"


def render_calculation_rows(node: dict, depth: int = 0) -> list[str]:
    indent = "  " * depth
    label = f"{indent}{node['path']}"
    rows = [
        "| {label} | {mode} | {low} | {base} | {high} |".format(
            label=label,
            mode=node.get("mode", "factor"),
            low=short_number(node["low"]),
            base=short_number(node["base"]),
            high=short_number(node["high"]),
        )
    ]
    if node["kind"] == "group":
        for child in node["children"]:
            rows.extend(render_calculation_rows(child, depth + 1))
    return rows


def confidence_label(model: dict, sensitivity: list[dict]) -> str:
    factor_count = len(flatten_factors(model))
    ratio = model["high"] / model["low"] if model["low"] > 0 else math.inf
    top_swing = sensitivity[0]["swing"] if sensitivity else 0.0
    swing_ratio = top_swing / abs(model["base"]) if model["base"] else math.inf

    if factor_count <= 4 and ratio <= 2 and swing_ratio <= 0.25:
        return "high"
    if ratio <= 5 and swing_ratio <= 0.6:
        return "medium"
    return "low"


def render_markdown(result: dict) -> str:
    model = result["model"]
    sensitivity = result["sensitivity"]
    scenarios = result["scenarios"]
    correlations = result["correlations"]
    monte_carlo = result.get("monte_carlo")
    lines = ["## Bottom line"]
    lines.append(f"- Best estimate: {headline_number(model['base'])}")
    lines.append(
        f"- Plausible range: {headline_number(model['low'])} to {headline_number(model['high'])}"
    )
    lines.append(f"- Scope metadata: {metadata_summary(model)}")
    lines.append(
        "- Scenario view: conservative {cons}, base {base}, aggressive {aggr}".format(
            cons=headline_number(scenarios["conservative"]),
            base=headline_number(scenarios["base"]),
            aggr=headline_number(scenarios["aggressive"]),
        )
    )
    lines.append("")
    lines.append("## Model")
    lines.append(f"- Formula: {formula(model)}")
    lines.append(f"- Top mode: {model['mode']}")
    lines.append("")
    lines.append("## Inputs and evidence")
    lines.append(
        "| Driver | Low | Base | High | Basis | Source | Metadata | Scenario |"
    )
    lines.append("| --- | ---: | ---: | ---: | --- | --- | --- | --- |")
    lines.extend(render_inputs_rows(model))
    lines.append("")
    lines.append("## Calculation")
    lines.append("| Node | Mode | Low | Base | High |")
    lines.append("| --- | --- | ---: | ---: | ---: |")
    lines.extend(render_calculation_rows(model))
    lines.append("")
    lines.append("## Sanity checks")
    lines.append("- Fill in top-down vs bottom-up comparison")
    lines.append("- Fill in capacity, budget, or benchmark check")
    lines.append("")
    lines.append("## Sensitivity and confidence")
    if sensitivity:
        lines.append(f"- Biggest uncertainty: {sensitivity[0]['path']}")
    lines.append(f"- Confidence: {confidence_label(model, sensitivity)}")
    if monte_carlo:
        lines.append(
            "- Monte Carlo: p05 {p05}, p50 {p50}, p95 {p95}, mean {mean} from {samples} draws{suffix}".format(
                p05=headline_number(monte_carlo["p05"]),
                p50=headline_number(monte_carlo["p50"]),
                p95=headline_number(monte_carlo["p95"]),
                mean=headline_number(monte_carlo["mean"]),
                samples=monte_carlo["samples"],
                suffix=(
                    f", correlated across {monte_carlo['group_count']} groups"
                    if monte_carlo.get("correlated_groups")
                    else ""
                ),
            )
        )
    for item in sensitivity[:5]:
        lines.append(
            "- {path}: total moves from {low} to {high} when only this factor moves".format(
                path=item["path"],
                low=headline_number(item["total_if_low"]),
                high=headline_number(item["total_if_high"]),
            )
        )
    if correlations:
        lines.append("- Correlated groups:")
        for item in correlations[:3]:
            driver_summary = ", ".join(
                "{path} ({direction}, {strength:.2f})".format(
                    path=driver["path"],
                    direction=driver["direction"],
                    strength=driver["strength"],
                )
                for driver in item["drivers"]
            )
            lines.append(
                "  - {group}: total moves from {low} to {high} when this group moves together [{drivers}]".format(
                    group=item["correlation_group"],
                    low=headline_number(item["total_lower"]),
                    high=headline_number(item["total_upper"]),
                    drivers=driver_summary,
                )
            )
    return "\n".join(lines)


def build_result(
    payload: dict,
    forced_mode: str | None,
    monte_carlo_samples: int | None = None,
    monte_carlo_seed: int | None = None,
) -> dict:
    if forced_mode is not None:
        payload = dict(payload)
        payload["mode"] = forced_mode

    model = parse_node(payload)
    monte_carlo_config = resolve_monte_carlo_config(
        payload, monte_carlo_samples, monte_carlo_seed
    )
    return {
        "model": model,
        "factors": flatten_factors(model),
        "sensitivity": sensitivity_entries(model),
        "correlations": correlation_entries(model),
        "scenarios": scenario_totals(model),
        "monte_carlo": monte_carlo_summary(model, monte_carlo_config),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", required=True, help="JSON file path or inline JSON payload"
    )
    parser.add_argument("--mode", choices=sorted(ALLOWED_MODES), default=None)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument(
        "--samples",
        type=int,
        default=None,
        help="Enable Monte Carlo with this many samples",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for Monte Carlo sampling",
    )
    args = parser.parse_args()

    try:
        payload = load_payload(args.input)
        result = build_result(payload, args.mode, args.samples, args.seed)
        if args.format == "json":
            json.dump(result, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            sys.stdout.write(render_markdown(result) + "\n")
        return 0
    except Exception as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
