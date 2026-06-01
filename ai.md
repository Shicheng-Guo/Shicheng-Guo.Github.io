---
layout: default
title: "AI in Pharma"
nav: ai
permalink: /ai/
wide: true
content_class: archive
eyebrow: "News · Events · Commentary · Perspectives"
tagline: "Tracking artificial intelligence across drug discovery and development."
description: "A live-updating tracker of AI in pharma and biotech — news, events, funding, research, regulation, and commentary."
---

<p class="lead">A live feed of artificial intelligence across pharma and biotech — news, deals and funding, research, regulation, product launches, events, and commentary — aggregated daily from public news and grouped by category.</p>

<input type="search" id="aiSearch" class="deal-search" placeholder="Search AI news (company, model, topic, keyword)…" aria-label="Search AI in pharma">

<div class="trending-toolbar">
  <div class="toolbar-row"><span class="toolbar-label">Category</span><div class="filters" id="aiCategory"></div></div>
</div>

<div class="trending-status" id="aiStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated"><span id="aiCount"></span></p>
<div id="aiTable"></div>
<p class="trending-updated" id="aiUpdated"></p>

<p class="trending-updated">
  Note: items are auto-aggregated from public news (Google News) and grouped by keyword matching into categories (News, Research, Funding/Deal, Regulatory, Opinion, Event, Product), so categorization is best-effort. Always read the linked source. Updated daily by an automated job.
</p>

<script src="{{ site.url }}/assets/js/ai.js"></script>
