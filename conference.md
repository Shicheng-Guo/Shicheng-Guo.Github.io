---
layout: default
title: "Conferences"
nav: conference
permalink: /conference/
wide: true
content_class: archive
eyebrow: "Upcoming Biopharma Conferences"
tagline: "Key biopharma conferences ahead — with dates and locations."
description: "A curated calendar of important upcoming biopharma conferences, with dates and locations."
---

<p class="lead">A curated calendar of important upcoming biopharma conferences — oncology, genetics, immuno-oncology, regulatory, and industry meetings — with dates and locations. Past events drop off automatically.</p>

<input type="search" id="confSearch" class="deal-search" placeholder="Search conferences (name, location, topic)…" aria-label="Search conferences">

<div class="trending-toolbar">
  <div class="toolbar-row"><span class="toolbar-label">Focus</span><div class="filters" id="confTags"></div></div>
</div>

<div class="trending-status" id="confStatus" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>Loading…</div>

<p class="trending-updated"><span id="confCount"></span></p>
<div class="conf-list" id="confList"></div>
<p class="trending-updated" id="confUpdated"></p>

<p class="trending-updated">
  Note: this is a <strong>curated calendar</strong> — dates are best-known/expected and shift year to year, so always confirm via the official site (each title links out). Edit <code>assets/data/conferences.json</code> to add events or set exact dates; past conferences hide automatically.
</p>

<script src="{{ site.url }}/assets/js/conference.js"></script>
