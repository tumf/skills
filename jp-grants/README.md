# jp-grants

Collect and answer questions about Japanese subsidies/grants (補助金・助成金) using up-to-date sources.

This skill is optimized for:

- Finding relevant programs (national + local)
- Summarizing eligibility, deadlines, and required documents
- Producing answers with official URLs and short supporting quotes

## Optional tooling

This skill includes helper scripts that use the Firecrawl API.

Requirements:

- `python3`
- `pip install firecrawl-py`
- Set `FIRECRAWL_API_KEY`

Examples:

```bash
export FIRECRAWL_API_KEY=...

./jp-grants/scripts/find_candidates.py --query "東京都 中小企業 DX 補助金" --limit 15

# Include local government (site:lg.jp) and common executing secretariat sites
./jp-grants/scripts/find_candidates.py --query "東京都 中小企業 DX 補助金" --limit 15 --include-local --include-executing-sites

# Copy URLs from the JSON output, then:
./jp-grants/scripts/extract_programs.py \
  "https://jgrants-portal.go.jp/subsidy/xxxxx" \
  "https://www.metro.tokyo.lg.jp/..."
```

Notes:

- Always verify deadlines and eligibility on the official page.
- Many programs have PDFs (公募要領/交付要綱). Prefer extracting from the official PDF if available.
- Executing secretariat sites are helpful for discovery, but treat them as secondary authority.
