# jp-grants

Collect and answer questions about Japanese subsidies/grants (補助金・助成金) using up-to-date sources.

This skill is methodology-focused. It is meant to provide reusable ways to discover, verify, and extract official information across many subsidy programs, not to maintain a custom script for each individual program.

This skill is optimized for:

- Finding relevant programs (national + local)
- Summarizing eligibility, deadlines, and required documents
- Checking official public past award/adoption examples when they are published
- Producing answers with official URLs and short supporting quotes

## Scope

- Reusable workflow for official-source discovery and extraction
- National and local programs with similar public information patterns
- Current calls, official result announcements, and officially published individual case lists

## Non-goals

- Program-specific one-off automation for every subsidy
- Treating consultant summaries as authoritative
- Inventing individual accepted cases from summary-only announcements

## Optional tooling

This skill includes helper scripts that use the Firecrawl API.

For official public award-result discovery, it also includes a direct-fetch helper that does not use Firecrawl.

Requirements:

- `python3`
- `pip install firecrawl-py`
- Set `FIRECRAWL_API_KEY`

## Install

Install this skill from the repo:

```bash
npx skills add tumf/skills --skill jp-grants
```

```bash
export FIRECRAWL_API_KEY=...

# Core: current requirements
./jp-grants/scripts/find_candidates.py --query "東京都 中小企業 DX 補助金" --limit 15

# Copy URLs from the JSON output, then extract program details
./jp-grants/scripts/extract_programs.py \
  "https://jgrants-portal.go.jp/subsidy/xxxxx" \
  "https://www.metro.tokyo.lg.jp/..."

# Core: official result statistics
./jp-grants/scripts/extract_official_award_results.py --query "ものづくり補助金"

# Core: individual accepted cases
./jp-grants/scripts/extract_case_examples.py \
  "https://example.go.jp/saitakusha.pdf"
```

## Advanced helpers

```bash
# Discovery with award-result-oriented search terms
./jp-grants/scripts/find_candidates.py --query "ものづくり補助金" --limit 15 --include-award-results

# Direct official result-page discovery without Firecrawl
./jp-grants/scripts/find_official_award_results.py --query "ものづくり補助金"

# Direct extraction from a known official result page
./jp-grants/scripts/extract_award_results.py \
  "https://www.chusho.meti.go.jp/keiei/sapoin/2025/250728saitaku.html"
```

## Practical flow

- Need current requirements -> `find_candidates.py` -> `extract_programs.py`
- Need official result statistics -> `extract_official_award_results.py`
- Need individual accepted cases -> official `採択者一覧` / `交付決定一覧` / case-study page -> `extract_case_examples.py`
- If Firecrawl misses award-result discovery -> use the direct official fallback scripts

Notes:

- Always verify deadlines and eligibility on the official page.
- Many programs have PDFs (公募要領/交付要綱). Prefer extracting from the official PDF if available.
- For fit assessment, also look for official public `採択結果`, `採択者一覧`, `採択事例`, or `交付決定` pages/PDFs.
- When `--include-award-results` is enabled, the search script prioritizes result-related queries before generic public call queries.
- When `--include-award-results` is enabled, the search script prioritizes `chusho.meti.go.jp`, `meti.go.jp`, and `lg.jp` ahead of J-Grants.
- When `--include-award-results` is enabled, the search script also tries `... 採択結果 pdf`-style queries to improve discovery of official PDFs.
- When `--include-award-results` is enabled, executing secretariat sites are automatically excluded unless they are manually searched outside this helper.
- Executing secretariat sites are helpful for current-program discovery, but do not use them for past award-result assessment unless they are the official public source of the result document itself.
- `jgrants-portal.go.jp` has a restrictive `robots.txt` (`Disallow: /`, `Allow: /index.html`), so automated discovery there may miss public information.
- If Firecrawl returns no award-result hits, use `find_official_award_results.py` as the fallback for direct discovery from official public index pages.
- If you want discovery + extraction together, use `extract_official_award_results.py`.
- For official result pages, prefer `extract_award_results.py` over the general extractor so applicant counts and selected counts are extracted more reliably.
- If you need individual accepted organizations/projects, use `extract_case_examples.py` on official `採択者一覧`, `交付決定一覧`, or case-study pages/PDFs.
