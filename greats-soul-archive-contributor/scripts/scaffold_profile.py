#!/usr/bin/env python3
"""Scaffold a new profile folder for tumf/greats-soul-archive.

Usage examples:
  python3 scripts/scaffold_profile.py --repo /path/to/repo --kind people --slug grace-hopper --name "Grace Hopper" --category computing --tags assistant
  python3 scripts/scaffold_profile.py --repo /path/to/repo --kind fiction-public-domain --slug john-watson --name "Dr. John Watson" --genre mystery --work "Arthur Conan Doyle — Sherlock Holmes stories" --tags assistant

Notes:
- This is intentionally a tiny parser (no external deps).
- It writes only if the target folder does not exist.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Path to a local clone of greats-soul-archive")
    ap.add_argument("--kind", required=True, choices=["people", "fiction-public-domain", "fiction-inspired"])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--name", required=True)

    # meta
    ap.add_argument("--category", help="People category (business/politics/strategy/philosophy/science/computing/economics/art)")
    ap.add_argument("--tags", action="append", default=[], help="Repeatable tag (e.g., --tags assistant)")

    # fiction-only
    ap.add_argument("--genre", help="Fiction genre (mystery/horror/scifi/fantasy/drama/comedy/other)")
    ap.add_argument("--work", help="Short work/universe reference")

    args = ap.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists():
        raise SystemExit(f"repo not found: {repo}")

    if args.kind == "people":
        base = repo / "people"
    elif args.kind == "fiction-public-domain":
        base = repo / "fiction" / "public-domain"
    else:
        base = repo / "fiction" / "inspired"

    target = base / args.slug
    if target.exists():
        raise SystemExit(f"target already exists: {target}")

    target.mkdir(parents=True)

    # Files
    (target / "IDENTITY.md").write_text(
        f"""# {args.name} — IDENTITY.md

- **Name:** {args.name}
- **Creature:** A distilled agent persona inspired by the public record
- **Vibe:** Clear thinking, high standards, evidence-seeking
- **Emoji:** ✨

## One-liner

(Describe this person-as-agent in one sentence.)
""",
        encoding="utf-8",
    )

    (target / "SOUL.md").write_text(
        f"""# {args.name} — SOUL.md

## Core Truths
- Prefer clarity over cleverness.
- Separate observations from interpretations.
- Make uncertainty explicit.

## Operating Principles
- Define terms before debating conclusions.
- Decide with a written rationale and a checkable prediction.
- When stuck, change representation (diagram, table, equation, example).

## Communication Style
- Be concise.
- State assumptions.
- Offer concrete next steps.

## Boundaries
- Don’t present speculation as fact.
- No personal attacks.

## Blind Spots / Failure Modes
- Over-indexing on rational structure; underweighting human incentives.

## Sources & Confidence
- See `sources.md`.
""",
        encoding="utf-8",
    )

    (target / "sources.md").write_text(
        f"""# Sources — {args.name}

## Primary / canonical
- (add speeches, letters, filings, papers, lectures, interviews)

## Secondary
- (add biographies, reputable histories, scholarly works)

## Notes
- Keep a clear line between what the sources state and what the agent persona infers.
""",
        encoding="utf-8",
    )

    # meta.yml
    meta_lines: list[str] = []
    if args.kind == "people":
        if args.category:
            meta_lines.append(f"category: {args.category}")
    else:
        meta_lines.append("category: public-domain" if args.kind == "fiction-public-domain" else "category: inspired")
        if args.work:
            meta_lines.append(f"work: {args.work}")
        if args.genre:
            meta_lines.append(f"genre: {args.genre}")

    if args.tags:
        meta_lines.append("tags:")
        for t in args.tags:
            meta_lines.append(f"  - {t}")

    if meta_lines:
        (target / "meta.yml").write_text("\n".join(meta_lines) + "\n", encoding="utf-8")

    print(str(target))


if __name__ == "__main__":
    main()
