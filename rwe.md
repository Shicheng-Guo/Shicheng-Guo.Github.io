---
layout: default
title: "Real-World Evidence"
nav: rwe
permalink: /rwe/
wide: true
content_class: archive
eyebrow: "News · Regulatory · Trends · Perspectives"
tagline: "Monitoring key developments in Real-World Evidence across drug development."
description: "A live-updating tracker of Real-World Evidence (RWE) in pharma — news, regulatory updates, events, trends, and expert perspectives."
---

<p class="lead">A curated, live feed of Real-World Evidence and real-world data across pharma and biotech — major news, regulatory updates, industry events, emerging trends, and expert perspectives — aggregated daily and grouped by category.</p>

<input type="search" id="rweSearch" class="deal-search" placeholder="Search RWE news (topic, company, keyword)…" aria-label="Search Real-World Evidence">

<div class="trending-toolbar">
  <div class="toolbar-row"><span class="toolbar-label">Category</span><div class="filters" id="rweCategory"></div></div>
</div>

<div class="trending-status" id="rweStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated"><span id="rweCount"></span></p>
<div id="rweTable"></div>
<p class="trending-updated" id="rweUpdated"></p>

<p class="trending-updated">
  Note: items are auto-aggregated from public news (Google News) and grouped by keyword matching into categories (News, Research, Regulatory, Funding/Deal, Opinion, Event, Product), so categorization is best-effort. Always read the linked source. Updated daily by an automated job.
</p>

<script src="{{ site.url }}/assets/js/rwe.js"></script>
