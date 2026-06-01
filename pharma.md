---
layout: default
title: "Pharma 5.0"
nav: pharma
permalink: /pharma/
wide: true
content_class: archive
eyebrow: "Pharma 4.0 · 5.0 · 6.0"
tagline: "The digital transformation of pharma — news, perspectives, and commentary."
description: "A live-updating tracker of Pharma 4.0, 5.0, and 6.0 — digital transformation, smart manufacturing, AI-enabled operations, news, perspectives, and commentary."
---

<p class="lead">A live feed on the evolution of pharma — <strong>Pharma 4.0, 5.0, and 6.0</strong>: digital transformation, smart and continuous manufacturing, AI-enabled operations, and the human-centric, sustainable future of the industry — aggregated daily, with news, perspectives, and commentary.</p>

<input type="search" id="phSearch" class="deal-search" placeholder="Search Pharma 4.0/5.0/6.0 (topic, company, keyword)…" aria-label="Search Pharma 5.0">

<div class="trending-toolbar">
  <div class="toolbar-row"><span class="toolbar-label">Category</span><div class="filters" id="phCategory"></div></div>
</div>

<div class="trending-status" id="phStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated"><span id="phCount"></span></p>
<div id="phTable"></div>
<p class="trending-updated" id="phUpdated"></p>

<p class="trending-updated">
  Note: items are auto-aggregated from public news (Google News) and grouped by keyword matching into categories (News, Perspective, Technology, Research, Regulatory, Event), so categorization is best-effort. Always read the linked source. Updated daily by an automated job.
</p>

<script src="{{ site.url }}/assets/js/pharma.js"></script>
