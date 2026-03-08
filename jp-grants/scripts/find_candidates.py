#!/usr/bin/env python3
"""
Find candidate Japanese subsidy/grant program pages using Firecrawl web search.

Usage:
    find_candidates.py --query "東京都 中小企業 DX 補助金" [--limit N] [--include-local]
    find_candidates.py --query "ものづくり補助金" --include-award-results

Examples:
    find_candidates.py --query "中小企業 省エネ 設備更新 補助金" --limit 20
    find_candidates.py --query "横浜市 小規模事業者 補助金" --include-local
    find_candidates.py --query "事業再構築補助金" --include-award-results
"""

import argparse
import json
import os
import sys
from urllib.parse import urlparse


DEFAULT_SITE_QUERIES = [
    "site:chusho.meti.go.jp",
    "site:meti.go.jp",
    "site:mhlw.go.jp",
    "site:smrj.go.jp",
    "site:j-net21.smrj.go.jp",
    "site:jetro.go.jp",
    "site:jgrants-portal.go.jp",
]


LOCAL_SITE_QUERIES = [
    "site:lg.jp",
]


# Executing secretariat sites are common for major subsidy programs, but they are not always
# a primary authority. Use for discovery and then confirm against primary sources/PDFs.
EXECUTING_SITE_QUERIES = [
    "site:it-hojo.jp",
    "site:jizokukahojokin.info",
    "site:monodukuri-hojo.jp",
]


DEFAULT_KEYWORDS = [
    "補助金",
    "助成金",
    "公募",
    "公募要領",
    "募集要項",
]


AWARD_RESULT_KEYWORDS = [
    "採択結果",
    "採択者一覧",
    "採択事例",
    "交付決定",
    "採択",
]


AWARD_RESULT_PDF_SUFFIXES = [
    "pdf",
    "PDF",
]


def _dedupe_results(results):
    seen = set()
    out = []
    for r in results:
        url = (r.get("url") or "").strip()
        if not url:
            continue
        # Normalize by scheme+netloc+path (drop query/fragment)
        try:
            p = urlparse(url)
            norm = f"{p.scheme}://{p.netloc}{p.path}"
        except Exception:
            norm = url
        if norm in seen:
            continue
        seen.add(norm)
        out.append({**r, "url": url, "url_normalized": norm})
    return out


def _to_jsonable(obj):
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, list):
        return [_to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}
    for meth in ("model_dump", "dict"):
        if hasattr(obj, meth):
            try:
                return _to_jsonable(getattr(obj, meth)())
            except Exception:
                pass
    if hasattr(obj, "__dict__"):
        try:
            return _to_jsonable(obj.__dict__)
        except Exception:
            pass
    return str(obj)


def _extract_items(search_result):
    # firecrawl-py v2 returns a SearchData object with .data
    if hasattr(search_result, "data"):
        try:
            items = getattr(search_result, "data")
            if isinstance(items, list):
                return [_to_jsonable(x) for x in items]
        except Exception:
            pass

    # Older variants: dict-like with "data".
    if isinstance(search_result, dict):
        data = search_result.get("data")
        if isinstance(data, list):
            return [_to_jsonable(x) for x in data]

    # Fallback: attempt to coerce to list.
    if isinstance(search_result, list):
        return [_to_jsonable(x) for x in search_result]

    return []


def main():
    parser = argparse.ArgumentParser(
        description="Find candidate Japanese subsidy/grant pages via Firecrawl search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "東京都 中小企業 DX 補助金" --limit 15 --include-local
  %(prog)s --query "キャリアアップ助成金 申請" --limit 10
        """,
    )
    parser.add_argument(
        "--query", required=True, help="Free-text query (Japanese recommended)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max results per search query (default: 10)",
    )
    parser.add_argument(
        "--include-local",
        action="store_true",
        help="Include local government sites (site:lg.jp) in discovery",
    )
    parser.add_argument(
        "--include-executing-sites",
        action="store_true",
        help="Include common executing secretariat sites (discovery only; ignored for award-result searches)",
    )
    parser.add_argument(
        "--include-award-results",
        action="store_true",
        help="Also search for past award/adoption result pages and PDFs from official public sources",
    )
    parser.add_argument(
        "--max-queries",
        type=int,
        default=60,
        help="Maximum number of expanded search queries (default: 60)",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Return raw Firecrawl search results without normalization",
    )
    args = parser.parse_args()

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "FIRECRAWL_API_KEY environment variable not set",
                }
            )
        )
        sys.exit(1)

    try:
        from firecrawl import FirecrawlApp
    except ImportError:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "firecrawl-py not installed. Run: pip install firecrawl-py",
                }
            )
        )
        sys.exit(1)

    site_queries = list(DEFAULT_SITE_QUERIES)
    if args.include_local:
        site_queries.extend(LOCAL_SITE_QUERIES)
    if args.include_executing_sites and not args.include_award_results:
        site_queries.extend(EXECUTING_SITE_QUERIES)

    if args.include_award_results:
        prioritized = [
            "site:chusho.meti.go.jp",
            "site:meti.go.jp",
            "site:lg.jp",
        ]
        remaining = [site for site in site_queries if site not in prioritized]
        site_queries = [
            site for site in prioritized if site in site_queries
        ] + remaining

    # Construct multiple queries to improve recall.
    expanded_queries = []
    for site_q in site_queries:
        expanded_queries.append(f"{site_q} {args.query}")
        if args.include_award_results:
            for kw in AWARD_RESULT_KEYWORDS:
                expanded_queries.append(f"{site_q} {args.query} {kw}")
                for suffix in AWARD_RESULT_PDF_SUFFIXES:
                    expanded_queries.append(f"{site_q} {args.query} {kw} {suffix}")
        for kw in DEFAULT_KEYWORDS:
            expanded_queries.append(f"{site_q} {args.query} {kw}")

    # Preserve order while removing duplicates so higher-priority award-result queries survive.
    expanded_queries = list(dict.fromkeys(expanded_queries))

    # Cap to avoid excessive API usage.
    expanded_queries = expanded_queries[: max(1, args.max_queries)]

    app = FirecrawlApp(api_key=api_key)

    all_results = []
    per_query = []
    try:
        for q in expanded_queries:
            r = app.search(q, limit=args.limit)
            items = _extract_items(r)
            per_query.append({"query": q, "count": len(items)})
            all_results.extend(items)

        if args.raw:
            payload = {
                "success": True,
                "queries": per_query,
                "results": all_results,
            }
        else:
            payload = {
                "success": True,
                "queries": per_query,
                "results": _dedupe_results(all_results),
            }

        print(json.dumps(payload, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
