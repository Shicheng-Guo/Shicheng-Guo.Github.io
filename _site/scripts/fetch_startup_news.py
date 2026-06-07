#!/usr/bin/env python3
"""Fetch breakthrough biotech/AI drug-discovery startup news → assets/data/startup_news.json.

Dependency-free (stdlib only). Aggregates startup news (fundings, launches,
partnerships, breakthroughs) from Google News RSS, classifies by category,
dedupes by link, MERGES with existing data so history accumulates.

Run locally:  python3 scripts/fetch_startup_news.py
In CI:        invoked daily by .github/workflows/update-startups.yml
"""

import json
import os
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "startup_news.json")
MAX_ROWS = 250
UA = "Mozilla/5.0 (compatible; ShichengGuoStartupTracker/1.0; +https://shicheng-guo.github.io)"

GNEWS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
QUERIES = [
    "biotech startup funding",
    "AI drug discovery startup",
    "biotech startup launches",
    "techbio startup raises",
    "drug discovery startup breakthrough",
    "biotech company emerges from stealth",
    "AI biology startup Series",
    "biotech seed round drug",
]

# Must look like a startup/company-stage story.
STARTUP_RE = re.compile(
    r"\b(startup|start-up|techbio|stealth|seed round|series [a-e]\b|raises?|raised|"
    r"launch\w*|emerg\w+|founded|spin-?out|biotech|venture)\b",
    re.I,
)
# ...and be bio/drug/AI relevant.
DOMAIN_RE = re.compile(
    r"\b(biotech|drug|therap\w*|pharma\w*|\bai\b|artificial intelligence|machine learning|"
    r"genomic\w*|molecul\w*|protein|discovery|medicine|disease|antibod\w*|rna\b|oncolog\w*)\b",
    re.I,
)


def classify(text):
    t = text.lower()
    if re.search(r"\b(raises?|raised|funding|series [a-e]\b|seed round|\$\d|million|billion|invest\w*|round)\b", t):
        return "Funding"
    if re.search(r"\b(launch\w*|unveil\w*|debut|emerg\w+ from stealth|introduc\w+|releases?|platform|spin-?out)\b", t):
        return "Launch"
    if re.search(r"\b(partner\w*|collaborat\w+|alliance|deal|teams? up|acqui\w+)\b", t):
        return "Partnership"
    if re.search(r"\b(breakthrough|study|publish\w*|data|results|preclinical|phase|trial|discover\w*)\b", t):
        return "Breakthrough"
    if re.search(r"\b(fda|ema|regulat\w*|approval|cleared)\b", t):
        return "Regulatory"
    return "News"


def parse_pubdate(s):
    if not s:
        return None
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def parse_feed(raw):
    out = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return out
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        src_el = item.find("source")
        source = (src_el.text.strip() if src_el is not None and src_el.text else "")
        out.append((title, link, source, item.findtext("pubDate")))
    return out


def clean_headline(title, source):
    if not source and " - " in title:
        head, _, tail = title.rpartition(" - ")
        if head:
            return head.strip(), tail.strip()
    return title.strip(), source


def collect():
    items = []
    for q in QUERIES:
        url = GNEWS.format(q=urllib.parse.quote(q))
        try:
            raw = fetch(url)
        except Exception as e:
            print(f"  skip {url}: {e}", file=sys.stderr)
            continue
        for title, link, source, pub in parse_feed(raw):
            if not title or not link:
                continue
            headline, source = clean_headline(title, source)
            if not (STARTUP_RE.search(headline) and DOMAIN_RE.search(headline)):
                continue
            dt = parse_pubdate(pub)
            items.append({
                "date": dt.date().isoformat() if dt else "",
                "headline": headline,
                "source": source,
                "link": link,
                "category": classify(headline),
            })
    return items


def load_existing():
    if os.path.exists(OUT):
        try:
            with open(OUT) as f:
                return json.load(f).get("items", [])
        except Exception:
            return []
    return []


def main():
    fresh = collect()
    merged = {d["link"]: d for d in load_existing()}
    for d in fresh:
        merged[d["link"]] = {**merged.get(d["link"], {}), **d}
    items = list(merged.values())
    items.sort(key=lambda d: d.get("date", ""), reverse=True)
    items = items[:MAX_ROWS]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "items": items}, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(items)} startup-news items to {OUT}")


if __name__ == "__main__":
    main()
