#!/usr/bin/env python3
"""Fetch AI-in-pharma news and build assets/data/ai.json.

Dependency-free (stdlib only). Aggregates news, events, commentary, and
perspectives on artificial intelligence in pharma/biotech from Google News
RSS, classifies each item by category, dedupes by link, MERGES with existing
data so history accumulates, and writes JSON the AI page renders.

Run locally:  python3 scripts/fetch_ai.py
In CI:        invoked daily by .github/workflows/update-ai.yml
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
OUT = os.path.join(ROOT, "assets", "data", "ai.json")
MAX_ROWS = 300
UA = "Mozilla/5.0 (compatible; ShichengGuoAITracker/1.0; +https://shicheng-guo.github.io)"

GNEWS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
QUERIES = [
    "AI drug discovery",
    "artificial intelligence pharma",
    "machine learning drug development",
    "generative AI biotech",
    "AI clinical trials",
    "FDA artificial intelligence drug",
    "AI pharmaceutical industry",
    "foundation model biology drug discovery",
    "AI precision medicine",
    "AI biomarker genomics",
]

# Must mention AI to be relevant.
AI_RE = re.compile(
    r"\b(a\.?i\.?|artificial intelligence|machine learning|deep learning|"
    r"generative|gen-?ai|\bllm\b|large language model|foundation model|"
    r"neural network|deepmind|alphafold|transformer model|algorithm)\b",
    re.I,
)


def classify(text):
    t = text.lower()
    if re.search(r"\b(fda|ema|mhra|regulat\w*|guidance|approval|approv\w+|cleared|policy|oversight)\b", t):
        return "Regulatory"
    if re.search(r"\b(raises?|funding|fundraise|series [a-e]\b|\$\d|million|billion|invest\w*|"
                 r"acqui\w+|partnership|partners with|collaborat\w+|venture|ipo)\b", t):
        return "Funding/Deal"
    if re.search(r"\b(opinion|perspective|commentary|op-?ed|viewpoint|column|essay|"
                 r"the future of|why |how |what )\b", t):
        return "Opinion"
    if re.search(r"\b(study|research|paper|published|preprint|model|algorithm|breakthrough|"
                 r"discover\w*|nature|science|cell\b|journal|benchmark)\b", t):
        return "Research"
    if re.search(r"\b(conference|summit|webinar|symposium|event|keynote|panel)\b", t):
        return "Event"
    if re.search(r"\b(launch\w*|unveil\w*|introduc\w+|debut|releases?|rolls out|platform|tool|"
                 r"agent|copilot)\b", t):
        return "Product"
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
            if not AI_RE.search(headline):
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
    print(f"Wrote {len(items)} AI items to {OUT}")


if __name__ == "__main__":
    main()
