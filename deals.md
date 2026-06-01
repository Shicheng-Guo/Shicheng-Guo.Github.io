---
layout: default
title: "BD Deals"
nav: deals
permalink: /deals/
content_class: archive
eyebrow: "Pharma & Biotech Business Development"
tagline: "A tracker of recent M&A, licensing, and partnership deals across pharma & biotech."
description: "A live-updating tracker of pharma and biotech business-development deals — M&A, licensing, and partnerships."
---

<p class="lead">Recent business-development activity across pharma and biotech — mergers &amp; acquisitions, licensing, and partnerships — aggregated daily from public news and classified by type, value, therapeutic area, modality, and stage.</p>

<input type="search" id="dealSearch" class="deal-search" placeholder="Search deals (company, asset, keyword)…" aria-label="Search deals">

<div class="trending-toolbar">
  <div class="toolbar-row"><span class="toolbar-label">Type</span><div class="filters" id="dealType"></div></div>
  <div class="toolbar-row"><span class="toolbar-label">Area</span><div class="filters" id="dealArea"></div></div>
  <div class="toolbar-row"><span class="toolbar-label">Modality</span><div class="filters" id="dealModality"></div></div>
  <div class="toolbar-row"><span class="toolbar-label">Stage</span><div class="filters" id="dealStage"></div></div>
</div>

<div class="trending-status" id="dealStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated"><span id="dealCount"></span></p>
<div id="dealTable"></div>
<p class="trending-updated" id="dealUpdated"></p>

<p class="trending-updated">
  Note: deals are auto-aggregated from public news (Google News &amp; biotech trade feeds) and classified by keyword matching, so <strong>value, area, modality, and stage are best-effort and may be incomplete</strong> ("—" where not detected). Always confirm details via the linked source. Updated daily by an automated job.
</p>

<script src="{{ site.url }}/assets/js/deals.js"></script>
