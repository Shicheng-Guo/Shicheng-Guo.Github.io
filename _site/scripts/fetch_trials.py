#!/usr/bin/env python3
"""Fetch clinical-trial readout news and build assets/data/trials.json.

Dependency-free (stdlib only). Pulls trial-readout news from Google News RSS,
classifies each headline by outcome (success / failed / readout), phase,
statistical significance, drug target, and mechanism of action (MOA), dedupes
by link, MERGES with existing data so history accumulates, and writes JSON
the Clinical Trials page renders.

Run locally:  python3 scripts/fetch_trials.py
In CI:        invoked daily by .github/workflows/update-trials.yml
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
OUT = os.path.join(ROOT, "assets", "data", "trials.json")
MAX_ROWS = 250
UA = "Mozilla/5.0 (compatible; ShichengGuoTrialTracker/1.0; +https://shicheng-guo.github.io)"

GNEWS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
QUERIES = [
    "clinical trial met primary endpoint",
    "phase 3 trial topline results",
    "phase 2 trial results drug",
    "trial failed primary endpoint",
    "drug trial positive results",
    "clinical trial missed primary endpoint",
    "phase 3 readout drug",
    "biotech trial statistically significant",
]

# Keep only items that read like a trial readout.
TRIAL_RE = re.compile(
    r"\b(phase\s*[123i]|primary endpoint|topline|read[- ]?out|trial|study (?:met|missed|showed)|"
    r"clinical (?:trial|study)|pivotal)\b",
    re.I,
)

FAIL_RE = re.compile(
    r"\bfail(?:s|ed|ure|ing)?\b"
    r"|\bmiss(?:es|ed|ing)?\b\s+(?:the\s|its\s|all\s)?(?:co-?)?(?:primary|endpoint)"
    r"|\bmiss(?:es|ed)\b\s+endpoint"
    r"|did not (?:meet|hit|achieve)|does not meet|didn't (?:meet|hit)"
    r"|\bnot (?:statistically )?significant\b|\bno significant\b"
    r"|negative (?:topline|results|data|readout)"
    r"|discontinu\w*|\bhalt(?:s|ed)?\b|futility|terminat\w*|setback|disappoint\w*",
    re.I,
)
SUCCESS_RE = re.compile(
    r"\b(?:meet|meets|met|hit|hits|achiev\w+)\b\s+(?:the\s|its\s|all\s|co-?)?(?:primary|endpoint|goal)"
    r"|positive (?:topline|results|data|readout)"
    r"|\bstatistically significant\b"
    r"|\bsucceed(?:s|ed)?\b|\bsuccess(?:ful)?\b"
    r"|demonstrat\w+ significant|significant improvement|\bmet endpoint\b",
    re.I,
)

PVAL_RE = re.compile(r"p[\s-]*[<=]\s*0?\.\d+", re.I)


def classify(text):
    t = text.lower()

    if FAIL_RE.search(t):
        outcome = "Failed"
    elif SUCCESS_RE.search(t):
        outcome = "Success"
    else:
        outcome = "Readout"

    if re.search(r"phase\s*3|phase\s*iii", t): phase = "Phase 3"
    elif re.search(r"phase\s*2/3|phase\s*ii/iii", t): phase = "Phase 2/3"
    elif re.search(r"phase\s*2|phase\s*ii\b", t): phase = "Phase 2"
    elif re.search(r"phase\s*1/2|phase\s*i/ii", t): phase = "Phase 1/2"
    elif re.search(r"phase\s*1|phase\s*i\b", t): phase = "Phase 1"
    else: phase = ""

    # significance — prefer an explicit p-value, then qualitative, then outcome
    m = PVAL_RE.search(text)
    if m:
        significance = re.sub(r"\s+", "", m.group(0))
    elif re.search(r"not (?:statistically )?significant|no significant", t):
        significance = "Not significant"
    elif re.search(r"statistically significant", t):
        significance = "Statistically significant"
    elif outcome == "Success":
        significance = "Met primary"
    elif outcome == "Failed":
        significance = "Missed primary"
    else:
        significance = ""

    targets = [
        "PD-1", "PD-L1", "CTLA-4", "KRAS", "EGFR", "HER2", "HER3", "BCMA", "CD19", "CD20",
        "CD3", "TROP2", "GLP-1", "GIP", "amyloid", "tau", "BTK", "JAK", "TNF", "IL-23",
        "IL-17", "IL-4", "IL-13", "IL-6", "TSLP", "factor XI", "Lp(a)", "PCSK9", "ALK",
        "BRAF", "FGFR", "CGRP", "C5", "complement", "VEGF", "TIGIT", "LAG-3", "CLDN18.2",
        "DLL3", "GPRC5D", "Nav1.8", "APOC3", "ANGPTL3", "5-HT", "NMDA", "GABA",
    ]
    target = ""
    for tg in targets:
        if re.search(r"\b" + re.escape(tg.lower()) + r"\b", t) or ("anti-" + tg.lower()) in t:
            target = tg
            break

    moas = [
        ("siRNA / RNAi", r"sirna|rnai|rna interference"),
        ("ASO / antisense", r"antisense|\baso\b|oligonucleotide"),
        ("mRNA", r"\bmrna\b"),
        ("ADC", r"\badc\b|antibody-?drug conjugate"),
        ("Bispecific antibody", r"bispecific|bi-?specific"),
        ("Checkpoint inhibitor", r"checkpoint|pd-?1|pd-?l1|ctla"),
        ("CAR-T / cell therapy", r"car-?t|car t|cell therapy|tcr therapy"),
        ("Gene therapy", r"gene therapy|\baav\b|gene editing|crispr"),
        ("Monoclonal antibody", r"antibod|monoclonal|\bmab\b"),
        ("Kinase inhibitor", r"kinase inhibitor|\btki\b|inhibitor of .*kinase"),
        ("GLP-1 agonist", r"glp-?1|incretin|gip"),
        ("Protein degrader", r"degrader|protac|molecular glue"),
        ("Radiopharmaceutical", r"radiopharm|radioligand|radioconjugate"),
        ("Vaccine", r"vaccine"),
        ("Small molecule", r"small molecule|oral (?:drug|therapy)"),
    ]
    moa = next((name for name, pat in moas if re.search(pat, t)), "")

    return outcome, phase, significance, target, moa


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
            if not TRIAL_RE.search(headline):
                continue
            dt = parse_pubdate(pub)
            outcome, phase, significance, target, moa = classify(headline)
            items.append({
                "date": dt.date().isoformat() if dt else "",
                "headline": headline,
                "source": source,
                "link": link,
                "outcome": outcome,
                "phase": phase,
                "significance": significance,
                "target": target,
                "moa": moa,
            })
    return items


def load_existing():
    if os.path.exists(OUT):
        try:
            with open(OUT) as f:
                return json.load(f).get("trials", [])
        except Exception:
            return []
    return []


def main():
    fresh = collect()
    merged = {d["link"]: d for d in load_existing()}
    for d in fresh:
        merged[d["link"]] = {**merged.get(d["link"], {}), **d}
    trials = list(merged.values())
    trials.sort(key=lambda d: d.get("date", ""), reverse=True)
    trials = trials[:MAX_ROWS]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "trials": trials}, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(trials)} trial updates to {OUT}")


if __name__ == "__main__":
    main()
