#!/usr/bin/env python3
"""Fetch Pharma 4.0 / 5.0 / 6.0 news and build assets/data/pharma.json.

Dependency-free (stdlib only). Aggregates news, perspectives, and commentary
on Pharma 4.0/5.0/6.0 and the digital transformation of pharma (Industry 4.0/
5.0, smart/continuous manufacturing, AI-enabled operations) from Google News
RSS, classifies by category, dedupes by link, MERGES history.

Run locally:  python3 scripts/fetch_pharma.py
In CI:        invoked daily by .github/workflows/update-pharma.yml
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
OUT = os.path.join(ROOT, "assets", "data", "pharma.json")
MAX_ROWS = 250
UA = "Mozilla/5.0 (compatible; ShichengGuoPharmaTracker/1.0; +https://shicheng-guo.github.io)"

GNEWS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
QUERIES = [
    "Pharma 4.0",
    "Pharma 5.0",
    "Pharma 6.0",
    "Industry 5.0 pharmaceutical",
    "pharma digital transformation manufacturing",
    "smart manufacturing pharmaceutical",
    "future of pharma manufacturing AI",
    "Pharma 4.0 perspective",
]

# Must be about Pharma X.0 / digital transformation of pharma.
VER_RE = re.compile(r"\b([456]\.0|industry\s*[456]\.0|digital transformation|smart manufacturing|continuous manufacturing|industry\s*4\.0)\b", re.I)
CTX_RE = re.compile(r"\b(pharma\w*|biopharma\w*|life science\w*|drug manufactur\w*|medicine\w*|biotech\w*|manufactur\w*)\b", re.I)


def classify(text):
    t = text.lower()
    if re.search(r"\b(opinion|perspective|commentary|viewpoint|op-?ed|column|the future of|why |how |what )\b", t):
        return "Perspective"
    if re.search(r"\b(fda|ema|regulat\w*|gmp|guidance|compliance|data integrity)\b", t):
        return "Regulatory"
    if re.search(r"\b(\bai\b|artificial intelligence|machine learning|automation|digital|iot|robot\w*|"
                 r"continuous manufacturing|smart manufacturing|cloud|platform|digital twin|data)\b", t):
        return "Technology"
    if re.search(r"\b(study|report|whitepaper|survey|published|research|findings|analysis)\b", t):
        return "Research"
    if re.search(r"\b(conference|summit|webinar|symposium|event|keynote|expo)\b", t):
        return "Event"
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
            if not (VER_RE.search(headline) and CTX_RE.search(headline)):
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
    print(f"Wrote {len(items)} Pharma X.0 items to {OUT}")


if __name__ == "__main__":
    main()
