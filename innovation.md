---
layout: default
title: "Innovation"
nav: innovation
permalink: /innovation/
wide: true
content_class: archive
eyebrow: "Breakthrough Startups & Their Innovation"
tagline: "The startups redefining how medicines are discovered and developed."
description: "Breakthrough biotech and AI drug-discovery startups and their innovation — a curated showcase plus a daily-updated startup-news feed."
---

<p class="lead">A spotlight on the breakthrough startups reinventing drug discovery and development — what they're building, and the latest news on fundings, launches, and breakthroughs across the field.</p>

<h2 class="archive__subtitle">Breakthrough Startups</h2>
<p style="color:var(--muted);margin-top:-0.4em">A curated showcase of companies pushing the frontier — AI, generative biology, and new discovery platforms. <em>(Curated; edit <code>assets/data/startups.json</code> to update.)</em></p>
<div class="portfolio-grid" id="startupBoard"></div>

<h2 class="archive__subtitle" style="margin-top:2.4em">Latest Startup News</h2>

<input type="search" id="startupSearch" class="deal-search" placeholder="Search startup news (company, topic, keyword)…" aria-label="Search startup news">

<div class="trending-toolbar">
  <div class="toolbar-row"><span class="toolbar-label">Category</span><div class="filters" id="startupCat"></div></div>
</div>

<div class="trending-status" id="startupStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated"><span id="startupCount"></span></p>
<div id="startupTable"></div>
<p class="trending-updated" id="startupUpdated"></p>

<p class="trending-updated">
  Note: the news feed is auto-aggregated from public news (Google News) and grouped by keyword matching into categories (Funding, Launch, Breakthrough, Partnership, Regulatory, News), so categorization is best-effort. Always read the linked source. Updated daily by an automated job.
</p>

<script src="{{ site.url }}/assets/js/innovation.js"></script>
