---
layout: default
title: "Key Opinion Leaders"
nav: kol
permalink: /kol/
wide: true
content_class: archive
eyebrow: "Leaders & Influential Experts"
tagline: "Key Opinion Leaders shaping drug discovery and development."
description: "A curated board of Key Opinion Leaders (KOLs) and influential experts across drug discovery and development."
---

<p class="lead">A curated board of Key Opinion Leaders and influential experts shaping the science and direction of drug discovery and development.</p>

<input type="search" id="kolSearch" class="deal-search" placeholder="Search KOLs (name, focus area, keyword)…" aria-label="Search Key Opinion Leaders">

<div class="trending-status" id="kolStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated" id="kolUpdated"></p>
<div class="kol-grid" id="kolBoard"></div>

<p class="trending-updated">
  <strong>Methodology &amp; honesty note.</strong> A true automated "hotness" ranking that fuses publications, conference talks, media coverage, and social engagement is <em>not reliably buildable from free, public data</em> — there is no free social-media API, conference/media influence isn't openly structured, and author-name disambiguation in literature databases is unreliable (we tested a PubMed publication-volume ranking and it surfaced merged, ambiguous names rather than recognized leaders). So this is a <strong>curated</strong> board: edit <code>assets/data/kol.json</code> to add, reorder, or annotate the experts you want to feature. The seed entries are well-known public figures shown as examples.
</p>

<script src="{{ site.url }}/assets/js/kol.js"></script>
