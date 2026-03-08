#!/usr/bin/env python3
"""Compute additive, multiplicative, and nested Fermi estimates."""

from __future__ import annotations

import argparse
import json
import math
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
    "correlation_group",
)
SUM_CONSISTENCY_KEYS = ("unit", "period", "currency", "geo", "dimension")


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


def validate_factor(factor: dict, index: int, prefix: str = "") -> dict:
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

    for key in METADATA_KEYS:
        if key == "period":
            item[key] = validate_period(qualified_name, factor.get(key, ""))
        elif key == "source_tier":
            item[key] = validate_source_tier(qualified_name, factor.get(key))
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
    factors = node.get("factors", [])
    groups = node.get("groups", [])

    if not isinstance(factors, list):
        raise ValueError(f"Group '{qualified_name}' has non-list 'factors'")
    if not isinstance(groups, list):
        raise ValueError(f"Group '{qualified_name}' has non-list 'groups'")

    children = []
    for index, factor in enumerate(factors, start=1):
        children.append(validate_factor(factor, index, prefix=f"{qualified_name} > "))
    for index, group in enumerate(groups, start=1):
        child_name = group.get("name") or f"group_{index}"
        group_prefix = f"{qualified_name} > "
        parsed_group = parse_node({**group, "name": child_name}, prefix=group_prefix)
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


def flatten_factors(node: dict) -> list[dict]:
    if node["kind"] == "factor":
        return [node]
    factors = []
    for child in node["children"]:
        factors.extend(flatten_factors(child))
    return factors


def factor_scenario_value(factor: dict, scenario_name: str) -> float:
    if scenario_name == "conservative":
        return factor["scenarios"]["conservative"]
    if scenario_name == "aggressive":
        return factor["scenarios"]["aggressive"]
    return factor["base"]


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


def factor_paths_by_correlation_group(model: dict) -> dict[str, list[str]]:
    grouped = {}
    for factor in flatten_factors(model):
        group = factor.get("correlation_group", "")
        if not group:
            continue
        grouped.setdefault(group, []).append(factor["path"])
    return grouped


def set_paths_to_scenario(
    node: dict, target_paths: set[str], scenario_name: str
) -> None:
    if node["kind"] == "factor":
        if node["path"] in target_paths:
            value = factor_scenario_value(node, scenario_name)
        else:
            value = node["base"]
        node["low"] = value
        node["base"] = value
        node["high"] = value
        return

    for child in node["children"]:
        set_paths_to_scenario(child, target_paths, scenario_name)

    totals = compute_total(node["children"], node["mode"])
    node["low"] = totals["low"]
    node["base"] = totals["base"]
    node["high"] = totals["high"]


def correlation_entries(model: dict) -> list[dict]:
    base_total = model["base"]
    entries = []
    for group, paths in factor_paths_by_correlation_group(model).items():
        conservative_model = deepcopy(model)
        aggressive_model = deepcopy(model)
        target_paths = set(paths)
        set_paths_to_scenario(conservative_model, target_paths, "conservative")
        set_paths_to_scenario(aggressive_model, target_paths, "aggressive")
        low_total = conservative_model["base"]
        high_total = aggressive_model["base"]
        swing = max(abs(base_total - low_total), abs(high_total - base_total))
        entries.append(
            {
                "correlation_group": group,
                "paths": sorted(paths),
                "total_if_conservative": low_total,
                "total_if_aggressive": high_total,
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
            lines.append(
                "  - {group}: total moves from {low} to {high} when this group moves together".format(
                    group=item["correlation_group"],
                    low=headline_number(item["total_if_conservative"]),
                    high=headline_number(item["total_if_aggressive"]),
                )
            )
    return "\n".join(lines)


def build_result(payload: dict, forced_mode: str | None) -> dict:
    if forced_mode is not None:
        payload = dict(payload)
        payload["mode"] = forced_mode

    model = parse_node(payload)
    return {
        "model": model,
        "factors": flatten_factors(model),
        "sensitivity": sensitivity_entries(model),
        "correlations": correlation_entries(model),
        "scenarios": scenario_totals(model),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", required=True, help="JSON file path or inline JSON payload"
    )
    parser.add_argument("--mode", choices=sorted(ALLOWED_MODES), default=None)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    try:
        payload = load_payload(args.input)
        result = build_result(payload, args.mode)
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
