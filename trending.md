---
layout: default
title: "Trending"
nav: trending
permalink: /trending/
content_class: archive
eyebrow: "Live from the GitHub API"
tagline: "Today's hot open-source projects in pharma & biology."
description: "A live feed of fast-rising open-source GitHub repositories across bioinformatics, drug discovery, genomics, and computational biology."
---

<p class="lead">A live feed of fast-rising open-source repositories across bioinformatics, drug discovery, genomics, and computational biology — pulled straight from the <a href="https://docs.github.com/en/rest/search" target="_blank" rel="noopener">GitHub Search API</a>. Pick a topic and a time window to see the most-starred projects created in that period.</p>

<div class="trending-toolbar">
  <div class="toolbar-row">
    <span class="toolbar-label">Topic</span>
    <div class="filters" id="trendingTopics" role="group" aria-label="Filter trending repositories by topic"></div>
  </div>
  <div class="toolbar-row">
    <span class="toolbar-label">Created</span>
    <div class="filters" id="trendingWindow" role="group" aria-label="Filter trending repositories by time window"></div>
  </div>
</div>

<div class="trending-status" id="trendingStatus" role="status" aria-live="polite">
  <span class="spin" aria-hidden="true"></span>Loading…
</div>

<div class="repo-grid" id="trendingCards"></div>
<p class="trending-updated" id="trendingUpdated"></p>

<p class="trending-updated">
  Note: GitHub has no official "trending" API, so this ranks repositories by stars among
  those created within the selected window — a close proxy for what's hot. Results are
  cached for 30 minutes to respect GitHub's public rate limit.
</p>

<script src="{{ site.url }}/assets/js/trending.js"></script>
