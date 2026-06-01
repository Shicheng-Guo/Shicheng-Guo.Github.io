---
layout: default
title: "Talks & Presentations"
nav: talks
permalink: /talks/
content_class: archive
eyebrow: "Invited Talks · Seminars · Conferences"
tagline: "Selected presentations. Placeholder entries below — replace with your own."
description: "Talks and presentations by Shicheng Guo, Ph.D."
---

{% assign talks = site.talks | sort: "date" | reverse %}
<div class="archive">
  {% for talk in talks %}
  <div class="list-entry">
    {% if talk.url and talk.url != "" %}
      <a class="list-entry__title" href="{{ talk.url }}">{{ talk.title }}</a>
    {% else %}
      <span class="list-entry__title">{{ talk.title }}</span>
    {% endif %}
    <div class="list-entry__meta">{{ talk.type }} · <em>{{ talk.venue }}</em>{% if talk.location %} · {{ talk.location }}{% endif %} · {{ talk.date | date: "%B %Y" }}</div>
    {% if talk.excerpt %}<p class="list-entry__desc">{{ talk.excerpt }}</p>{% endif %}
  </div>
  {% endfor %}
</div>
