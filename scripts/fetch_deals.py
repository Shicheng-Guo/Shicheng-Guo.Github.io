#!/usr/bin/env python3
"""Fetch pharma/biotech BD deal news and build assets/data/deals.json.

Dependency-free (stdlib only): pulls Google News RSS search feeds (reliable,
no API key) plus a few biotech trade feeds, classifies each headline into
structured fields by keyword matching, dedupes by link, MERGES with any
existing data so history accumulates, and writes a JSON the Deals page renders.

Run locally:  python3 scripts/fetch_deals.py
In CI:        invoked daily by .github/workflows/update-deals.yml
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
OUT = os.path.join(ROOT, "assets", "data", "deals.json")
MAX_DEALS = 250
UA = "Mozilla/5.0 (compatible; ShichengGuoDealTracker/1.0; +https://shicheng-guo.github.io)"

GNEWS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
QUERIES = [
    "pharma acquisition",
    "biotech acquisition billion",
    "biotech licensing deal",
    "pharma partnership upfront milestone",
    "biotech merger",
    "pharma licensing agreement",
    "biotech collaboration deal",
]
# Best-effort trade feeds (skipped silently if unreachable / changed).
TRADE_FEEDS = [
    "https://www.biopharmadive.com/feeds/news/",
    "https://endpts.com/feed/",
    "https://www.fiercebiotech.com/rss/xml",
    "https://www.fiercepharma.com/rss/xml",
]

# Only keep items that look like a deal.
DEAL_RE = re.compile(
    r"\b(acquir|acquisition|merg|buyout|takeover|to buy|licens|partner|"
    r"collaborat|alliance|joint venture|upfront|milestone|royalt|option deal|"
    r"deal worth|inks|signs|stake)\b",
    re.I,
)

VALUE_RE = re.compile(r"\$\s?\d[\d,.]*\s?(?:billion|bn|million|mn|[bm])\b", re.I)


def classify(text):
    t = text.lower()

    if re.search(r"\b(acquir|acquisition|buyout|takeover|to buy|merg)\b", t):
        dtype = "M&A"
    elif re.search(r"\blicens", t):
        dtype = "Licensing"
    elif re.search(r"\b(partner|collaborat|alliance|joint venture)\b", t):
        dtype = "Partnership"
    elif re.search(r"\b(raises|series [a-e]\b|ipo|financing|funding round)\b", t):
        dtype = "Financing"
    else:
        dtype = "Deal"

    areas = [
        ("Oncology", r"oncolog|cancer|tumou?r|carcinoma|lymphoma|leukemia|melanoma"),
        ("Immunology", r"immunolog|immune|autoimmun|inflammat|lupus|rheumat|psoriasis|ibd|colitis|crohn"),
        ("Neurology", r"neuro|cns|alzheimer|parkinson|epilep|als\b|multiple sclerosis|migraine|schizophren|depression"),
        ("Cardiovascular", r"cardiovascular|cardio|heart|cardiac|hypertension|thrombo"),
        ("Metabolic", r"metabolic|obesity|diabet|glp-?1|nash|mash|weight loss"),
        ("Rare disease", r"rare disease|orphan|genetic disease"),
        ("Infectious", r"infectious|antivir|antibiotic|vaccine|covid|influenza|hiv|hepatitis"),
        ("Respiratory", r"respiratory|asthma|copd|pulmonary"),
        ("Ophthalmology", r"ophthalmolog|retina|eye disease|macular"),
        ("Hematology", r"hematolog|blood disorder|anemia|hemophilia|sickle cell"),
        ("Renal", r"renal|kidney|nephro"),
        ("Hepatology", r"liver|hepat"),
        ("Dermatology", r"dermatolog|skin disease|eczema|atopic"),
    ]
    area = next((name for name, pat in areas if re.search(pat, t)), "")

    mods = [
        ("RNAi / siRNA", r"sirna|rnai|rna interference"),
        ("mRNA", r"\bmrna\b"),
        ("ASO / oligo", r"antisense|oligonucleotide|\baso\b"),
        ("ADC", r"\badc\b|antibody-?drug conjugate"),
        ("Bispecific", r"bispecific|bi-?specific"),
        ("Antibody", r"antibod|monoclonal|\bmab\b"),
        ("Cell therapy", r"cell therapy|car-?t|car t|tcr|nk cell"),
        ("Gene therapy", r"gene therapy|\baav\b|gene editing|crispr"),
        ("Protein degrader", r"degrader|protac|molecular glue"),
        ("Radiopharma", r"radiopharm|radioconjugate|radioligand|radionuclide"),
        ("Peptide", r"peptide"),
        ("Small molecule", r"small molecule|oral drug"),
        ("Vaccine", r"vaccine"),
    ]
    modality = next((name for name, pat in mods if re.search(pat, t)), "")

    stages = [
        ("Approved", r"\bapproved\b|fda approval|approval"),
        ("Phase 3", r"phase 3|phase iii"),
        ("Phase 2", r"phase 2|phase ii\b"),
        ("Phase 1", r"phase 1|phase i\b"),
        ("Preclinical", r"preclinical|pre-?clinical|discovery-?stage"),
    ]
    stage = next((name for name, pat in stages if re.search(pat, t)), "")

    m = VALUE_RE.search(text)
    value = ""
    if m:
        value = re.sub(r"\s+", " ", m.group(0).strip())
        value = value.replace("$ ", "$")

    return dtype, value, area, modality, stage


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


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def parse_feed(raw):
    """Return list of (title, link, source, pubdate) from RSS or Atom."""
    out = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return out
    # RSS 2.0
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        src_el = item.find("source")
        source = (src_el.text.strip() if src_el is not None and src_el.text else "")
        pub = item.findtext("pubDate")
        out.append((title, link, source, pub))
    if out:
        return out
    # Atom
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title = (entry.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.get("href") if link_el is not None else ""
        pub = (entry.findtext("{http://www.w3.org/2005/Atom}updated")
               or entry.findtext("{http://www.w3.org/2005/Atom}published"))
        out.append((title, link, "", pub))
    return out


def clean_headline(title, source):
    """Google News titles end with ' - Source'; split that off."""
    if not source and " - " in title:
        head, _, tail = title.rpartition(" - ")
        if head:
            return head.strip(), tail.strip()
    return title.strip(), source


def collect():
    urls = [GNEWS.format(q=urllib.parse.quote(q)) for q in QUERIES] + TRADE_FEEDS
    items = []
    for url in urls:
        try:
            raw = fetch(url)
        except Exception as e:
            print(f"  skip {url}: {e}", file=sys.stderr)
            continue
        for title, link, source, pub in parse_feed(raw):
            if not title or not link:
                continue
            headline, source = clean_headline(title, source)
            if not DEAL_RE.search(headline):
                continue
            dt = parse_pubdate(pub)
            dtype, value, area, modality, stage = classify(headline)
            items.append({
                "date": dt.date().isoformat() if dt else "",
                "headline": headline,
                "source": source,
                "link": link,
                "type": dtype,
                "value": value,
                "area": area,
                "modality": modality,
                "stage": stage,
            })
    return items


def load_existing():
    if os.path.exists(OUT):
        try:
            with open(OUT) as f:
                return json.load(f).get("deals", [])
        except Exception:
            return []
    return []


def main():
    fresh = collect()
    merged = {d["link"]: d for d in load_existing()}
    for d in fresh:
        merged[d["link"]] = {**merged.get(d["link"], {}), **d}
    deals = list(merged.values())
    deals.sort(key=lambda d: d.get("date", ""), reverse=True)
    deals = deals[:MAX_DEALS]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "deals": deals}, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(deals)} deals to {OUT}")


if __name__ == "__main__":
    main()
