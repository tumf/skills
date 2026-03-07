#!/usr/bin/env python3
"""Compute additive or multiplicative Fermi estimates from factor ranges."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


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


def validate_factor(factor: dict, index: int) -> dict:
    name = factor.get("name") or f"factor_{index}"
    base = factor.get("base")
    low = factor.get("low", base)
    high = factor.get("high", base)
    unit = factor.get("unit", "")
    source = factor.get("source", "")
    note = factor.get("note", "")

    if base is None:
        raise ValueError(f"Factor '{name}' is missing 'base'")

    values = {"low": low, "base": base, "high": high}
    for key, value in values.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"Factor '{name}' has non-numeric {key}: {value!r}")

    if low > base or base > high:
        raise ValueError(f"Factor '{name}' must satisfy low <= base <= high")

    low_value = to_float(low, name, "low")
    base_value = to_float(base, name, "base")
    high_value = to_float(high, name, "high")

    return {
        "name": name,
        "low": low_value,
        "base": base_value,
        "high": high_value,
        "unit": unit,
        "source": source,
        "note": note,
    }


def compute_total(factors: list[dict], mode: str) -> dict:
    if mode == "product":
        low = 1.0
        base = 1.0
        high = 1.0
        for factor in factors:
            low *= factor["low"]
            base *= factor["base"]
            high *= factor["high"]
    else:
        low = sum(factor["low"] for factor in factors)
        base = sum(factor["base"] for factor in factors)
        high = sum(factor["high"] for factor in factors)

    return {"mode": mode, "low": low, "base": base, "high": high}


def sensitivity_score(factor: dict, mode: str) -> float:
    if mode == "product":
        if factor["low"] <= 0 or factor["high"] <= 0:
            return float("inf")
        return abs(math.log(factor["high"] / factor["low"]))
    return abs(factor["high"] - factor["low"])


def add_sensitivity(factors: list[dict], mode: str) -> list[dict]:
    enriched = []
    for factor in factors:
        item = dict(factor)
        item["sensitivity"] = sensitivity_score(factor, mode)
        enriched.append(item)
    return sorted(enriched, key=lambda item: item["sensitivity"], reverse=True)


def format_number(value: float) -> str:
    if value == 0:
        return "0"
    magnitude = abs(value)
    if magnitude >= 1_000_000_000:
        return f"{value:,.3g}"
    if magnitude >= 1_000:
        return f"{value:,.4g}"
    if magnitude >= 1:
        return f"{value:,.4g}"
    return f"{value:.4g}"


def render_markdown(result: dict) -> str:
    lines = []
    lines.append(f"Mode: {result['total']['mode']}")
    lines.append("")
    lines.append("| Factor | Low | Base | High | Unit | Source |")
    lines.append("| --- | ---: | ---: | ---: | --- | --- |")
    for factor in result["factors"]:
        lines.append(
            "| {name} | {low} | {base} | {high} | {unit} | {source} |".format(
                name=factor["name"],
                low=format_number(factor["low"]),
                base=format_number(factor["base"]),
                high=format_number(factor["high"]),
                unit=factor["unit"] or "-",
                source=factor["source"] or "-",
            )
        )

    lines.append("")
    lines.append("| Total low | Total base | Total high |")
    lines.append("| ---: | ---: | ---: |")
    lines.append(
        "| {low} | {base} | {high} |".format(
            low=format_number(result["total"]["low"]),
            base=format_number(result["total"]["base"]),
            high=format_number(result["total"]["high"]),
        )
    )

    lines.append("")
    lines.append("Sensitivity ranking:")
    for factor in result["sensitivity"]:
        lines.append(f"- {factor['name']}: {format_number(factor['sensitivity'])}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", required=True, help="JSON file path or inline JSON payload"
    )
    parser.add_argument("--mode", choices=["product", "sum"], default=None)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    try:
        payload = load_payload(args.input)
        factors = [
            validate_factor(item, i + 1) for i, item in enumerate(payload["factors"])
        ]
        mode = args.mode or payload.get("mode", "product")
        if mode not in {"product", "sum"}:
            raise ValueError(f"Unsupported mode: {mode}")

        result = {
            "total": compute_total(factors, mode),
            "factors": factors,
            "sensitivity": add_sensitivity(factors, mode),
        }

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
