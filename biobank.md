---
layout: default
title: "Biobank"
nav: biobank
permalink: /biobank/
wide: true
content_class: archive
eyebrow: "Initiatives · Datasets · Opportunities"
tagline: "Monitoring major biobank initiatives and datasets worldwide."
description: "A live-updating tracker of major biobank initiatives and datasets worldwide — data releases, cohort expansions, partnerships, technology, publications, and funding."
---

<p class="lead">A live feed of major biobank initiatives and datasets worldwide — new data releases, cohort expansions, strategic partnerships, technology advancements, publications, and funding — surfacing emerging opportunities for drug discovery and human genetics, aggregated daily and grouped by category.</p>

<input type="search" id="bbSearch" class="deal-search" placeholder="Search biobank news (UK Biobank, FinnGen, topic, keyword)…" aria-label="Search biobank updates">

<div class="trending-toolbar">
  <div class="toolbar-row"><span class="toolbar-label">Category</span><div class="filters" id="bbCategory"></div></div>
</div>

<div class="trending-status" id="bbStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated"><span id="bbCount"></span></p>
<div id="bbTable"></div>
<p class="trending-updated" id="bbUpdated"></p>

<p class="trending-updated">
  Note: items are auto-aggregated from public news (Google News) and grouped by keyword matching into categories (News, Data/Cohort, Research, Funding/Deal, Partnership, Technology, Regulatory, Opinion), so categorization is best-effort. Always read the linked source. Updated daily by an automated job.
</p>

<script src="{{ site.url }}/assets/js/biobank.js"></script>
