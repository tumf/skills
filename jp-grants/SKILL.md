---
name: jp-grants
description: |
  Collect and answer questions about Japanese subsidies/grants (補助金・助成金) with up-to-date sources.
  Use when a user asks: which programs they qualify for, eligibility, deadlines, required documents,
  application steps, or where to find official calls for proposals (e.g. J-Grants, METI/SME Agency,
  MHLW, prefectures/municipalities). Includes workflows and scripts for web search + structured
  extraction with citations.
---

# jp-grants - Japan Subsidies / Grants (補助金・助成金)

Operate with a "freshness first" mindset: deadlines and rules change frequently. Prefer official sources (e.g. *.go.jp, *.lg.jp, jgrants-portal.go.jp). Always provide URLs and, when possible, short supporting quotes.

## Operating rules

- Avoid hallucinating program details. If a field is unknown, say so and provide the official URL to verify.
- Distinguish clearly between:
  - Subsidies/grants (補助金)
  - Employment-related support / allowances (助成金, often MHLW)
  - Loans/financing (融資) and tax incentives (税制) (not grants)
- Do not provide legal/tax advice; provide procedural guidance and point to official documents.

## Minimal intake (ask only if needed)

If the user question is underspecified, ask for only the 3-6 items that most affect eligibility:

1. Applicant type: individual / sole proprietor / SME corporation / NPO / school / other
2. Location: prefecture + city/ward (local programs are common)
3. Purpose: equipment (capex) / IT & DX / hiring & wages / R&D / export / energy saving / disaster recovery / other
4. Company size: employees, capital, sales (rough ranges are fine)
5. Timeline: when they want to apply / start the project
6. Industry constraints: manufacturing / retail / services / construction / healthcare / etc.

If the user refuses details, proceed with generic national programs and give a checklist to narrow down.

## Workflow: answer a user question

1. Restate constraints + assumptions (explicitly).
2. Collect candidate programs from official sources.
3. Extract structured details (eligibility, amounts, deadlines, how to apply).
4. Shortlist 3-7 best fits; explain fit and disqualifiers.
5. Provide next steps: what to read, what documents to prepare, and where to apply.

## Source strategy

- Primary: official government and local government sites
  - `jgrants-portal.go.jp` (J-Grants)
  - `*.go.jp` (METI, MHLW, SME Agency, etc.)
  - `*.lg.jp` (prefecture/municipality)
- Secondary: public support organizations (confirm against primary)
  - J-Net21, chambers of commerce, SME support centers
- Avoid: consultant blogs as an authority (may be outdated).

For a curated list of sources and query templates, read `jp-grants/references/sources.md`.

## Scripts (optional but recommended)

These scripts use Firecrawl for web search + structured extraction.

- Find candidate pages: `jp-grants/scripts/find_candidates.py`
- Extract program fields: `jp-grants/scripts/extract_programs.py`

`find_candidates.py` flags:

- `--include-local`: include local government sites (`site:lg.jp`)
- `--include-executing-sites`: include common executing secretariat sites (discovery only)

If using the scripts:

1. Run `find_candidates.py` to produce URLs.
2. Feed URLs into `extract_programs.py`.
3. Manually verify deadlines and any hard eligibility constraints against the official page/PDF.

## Output pattern (what to return to the user)

Provide a short list of candidates with consistent fields:

- Program name + administering body
- What it funds (eligible costs)
- Amount/rate (if specified)
- Key eligibility constraints
- Application window / deadline (with "as-of" date)
- Official URL (required)
- Why it fits / why it might not

Keep the list short. If there are many, offer a second pass after the user answers 1-2 narrowing questions.
