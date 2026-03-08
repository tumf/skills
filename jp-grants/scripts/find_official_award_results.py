#!/usr/bin/env python3
"""
Find official public subsidy/grant award-result pages without Firecrawl.

This script fetches known official index pages directly and filters result links by query.

Usage:
    find_official_award_results.py --query "ものづくり補助金"

Examples:
    find_official_award_results.py --query "ものづくり補助金"
    find_official_award_results.py --query "IT導入補助金" --limit 5
"""

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


INDEX_SOURCES = [
    {
        "name": "SMEA award results",
        "url": "https://www.chusho.meti.go.jp/koukai/hojyokin/saitaku.html",
        "base_url": "https://www.chusho.meti.go.jp",
    },
]


GENERIC_TOKENS = {"補助金", "助成金", "交付金"}


def _fetch_text(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; jp-grants/1.0)"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def _strip_tags(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _extract_links(page_text, base_url):
    pattern = re.compile(
        r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL
    )
    links = []
    for href, label_html in pattern.findall(page_text):
        label = _strip_tags(label_html)
        if not label:
            continue
        links.append(
            {
                "url": urllib.parse.urljoin(base_url, html.unescape(href)),
                "title": label,
            }
        )
    return links


def _score_link(query, link):
    score = 0
    title = link["title"]
    url = link["url"]
    if query in title:
        score += 5
    for token in _meaningful_tokens(query):
        if token and token in title:
            score += 2
        if token and token in url:
            score += 1
    if "採択" in title or "交付決定" in title:
        score += 2
    if "/saitaku/" in url or "saitaku" in url:
        score += 1
    return score


def _query_tokens(query):
    expanded = query
    for suffix in ("補助金", "助成金", "交付金"):
        expanded = expanded.replace(suffix, f" {suffix}")
    tokens = [part.strip() for part in expanded.split() if part.strip()]
    return list(dict.fromkeys(tokens or [query]))


def _meaningful_tokens(query):
    tokens = [token for token in _query_tokens(query) if token not in GENERIC_TOKENS]
    return tokens or [query]


def _dedupe_links(links):
    seen = set()
    result = []
    for link in links:
        url = link["url"]
        if url in seen:
            continue
        seen.add(url)
        result.append(link)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Find official public award-result pages without Firecrawl",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "ものづくり補助金"
  %(prog)s --query "IT導入補助金" --limit 5
        """,
    )
    parser.add_argument(
        "--query", required=True, help="Filter official result pages by query"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of matches to return (default: 10)",
    )
    args = parser.parse_args()

    try:
        candidates = []
        fetched = []
        for source in INDEX_SOURCES:
            page_text = _fetch_text(source["url"])
            fetched.append({"name": source["name"], "url": source["url"]})
            for link in _extract_links(page_text, source["base_url"]):
                score = _score_link(args.query, link)
                title = link["title"]
                tokens = _meaningful_tokens(args.query)
                if score <= 0 or not any(token in title for token in tokens):
                    continue
                candidates.append(
                    {
                        "source_name": source["name"],
                        "source_url": source["url"],
                        "title": link["title"],
                        "url": link["url"],
                        "score": score,
                    }
                )

        candidates = _dedupe_links(
            sorted(
                candidates,
                key=lambda item: (-item["score"], item["title"], item["url"]),
            )
        )
        print(
            json.dumps(
                {
                    "success": True,
                    "query": args.query,
                    "sources_checked": fetched,
                    "results": candidates[: max(1, args.limit)],
                },
                indent=2,
                default=str,
            )
        )
    except urllib.error.URLError as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
        sys.exit(1)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
