#!/usr/bin/env python3
"""Fetch biobank news and build assets/data/biobank.json.

Dependency-free (stdlib only). Aggregates news on major biobank initiatives
and datasets worldwide — data releases, cohort expansions, partnerships,
technology, publications, funding, and opportunities for drug discovery and
human genetics — from Google News RSS, classifies by category, dedupes by
link, MERGES with existing data so history accumulates.

Run locally:  python3 scripts/fetch_biobank.py
In CI:        invoked daily by .github/workflows/update-biobank.yml
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
OUT = os.path.join(ROOT, "assets", "data", "biobank.json")
MAX_ROWS = 300
UA = "Mozilla/5.0 (compatible; ShichengGuoBiobankTracker/1.0; +https://shicheng-guo.github.io)"

GNEWS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
QUERIES = [
    "biobank",
    "UK Biobank",
    "All of Us research program genomics",
    "biobank data release",
    "biobank genomics drug discovery",
    "population cohort genomics",
    "biobank partnership pharma",
    "FinnGen biobank",
    "Genomics England biobank",
    "biobank funding announcement",
]

# Must be biobank / large-cohort related.
BIOBANK_RE = re.compile(
    r"\b(biobank|uk biobank|all of us|finngen|genomics england|million veteran|"
    r"estonian biobank|china kadoorie|population cohort|reference panel|"
    r"\d{2,3},?\d{3}\s+(?:participants|genomes|samples)|cohort stud\w*)\b",
    re.I,
)


def classify(text):
    t = text.lower()
    if re.search(r"\b(funding|fund\b|grant\w*|raises?|\$\d|million|billion|invest\w*|awarded|backs?)\b", t):
        return "Funding/Deal"
    if re.search(r"\b(partner\w*|collaborat\w+|alliance|consortium|joins?|teams? up|agreement)\b", t):
        return "Partnership"
    if re.search(r"\b(regulat\w*|governance|consent|ethics|data protection|gdpr|privacy|policy)\b", t):
        return "Regulatory"
    if re.search(r"\b(study|paper|published|findings|preprint|journal|gwas|association stud\w*|analysis|discover\w*)\b", t):
        return "Research"
    if re.search(r"\b(technolog\w*|platform|\bai\b|artificial intelligence|machine learning|multi-?omic|"
                 r"proteomic|single-?cell|spatial|imaging|sequencing technolog\w*)\b", t):
        return "Technology"
    if re.search(r"\b(data release|releases? .*data|new dataset|whole[- ]genome|exome|sequenc\w+|"
                 r"data available|participants|recruit\w*|enroll\w*|cohort|samples|expands?|reaches|grows to)\b", t):
        return "Data/Cohort"
    if re.search(r"\b(opinion|perspective|commentary|the future of|why |how )\b", t):
        return "Opinion"
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
            if not BIOBANK_RE.search(headline):
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
    print(f"Wrote {len(items)} biobank items to {OUT}")


if __name__ == "__main__":
    main()
