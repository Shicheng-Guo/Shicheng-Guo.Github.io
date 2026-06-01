---
layout: default
title: "Publications"
nav: publications
permalink: /publications/
content_class: archive
eyebrow: "Peer-Reviewed Research"
tagline: "Selected publications in genomics, epigenetics, and statistical genetics. A complete, up-to-date list is on Google Scholar."
description: "Selected peer-reviewed publications by Shicheng Guo, Ph.D."
---

<p style="margin:-0.6em 0 2em">
  <a class="pub-links" style="display:inline-flex" href="https://scholar.google.com/citations?user=BixB4TsAAAAJ&hl=en"><span><i class="fa-solid fa-graduation-cap"></i> Full list on Google Scholar</span></a>
</p>

{% assign journal = site.publications | where: "category", "manuscripts" | sort: "date" | reverse %}
{% assign conf = site.publications | where: "category", "conferences" | sort: "date" | reverse %}

{% if journal.size > 0 %}
<h3 class="archive__subtitle">Journal Articles</h3>
<ul class="pub-list">
  {% for pub in journal %}
  <li class="pub-item">
    <a class="pub-item__title" href="{{ pub.paperurl }}">{{ pub.title }}</a>
    <div class="pub-item__venue">Published in <em>{{ pub.venue }}</em>, {{ pub.date | date: "%Y" }}</div>
    {% if pub.excerpt %}<p class="pub-item__excerpt">{{ pub.excerpt }}</p>{% endif %}
    {% if pub.citation %}<p class="pub-item__cite">{{ pub.citation }}</p>{% endif %}
    <div class="pub-links">
      {% if pub.paperurl %}<a href="{{ pub.paperurl }}"><i class="fa-solid fa-file-lines"></i> Paper</a>{% endif %}
      {% if pub.code %}<a href="{{ pub.code }}"><i class="fa-solid fa-code"></i> Code</a>{% endif %}
    </div>
  </li>
  {% endfor %}
</ul>
{% endif %}

{% if conf.size > 0 %}
<h3 class="archive__subtitle">Conference Papers</h3>
<ul class="pub-list">
  {% for pub in conf %}
  <li class="pub-item">
    <a class="pub-item__title" href="{{ pub.paperurl }}">{{ pub.title }}</a>
    <div class="pub-item__venue">Published in <em>{{ pub.venue }}</em>, {{ pub.date | date: "%Y" }}</div>
    {% if pub.excerpt %}<p class="pub-item__excerpt">{{ pub.excerpt }}</p>{% endif %}
    {% if pub.citation %}<p class="pub-item__cite">{{ pub.citation }}</p>{% endif %}
    <div class="pub-links">
      {% if pub.paperurl %}<a href="{{ pub.paperurl }}"><i class="fa-solid fa-file-lines"></i> Paper</a>{% endif %}
      {% if pub.code %}<a href="{{ pub.code }}"><i class="fa-solid fa-code"></i> Code</a>{% endif %}
    </div>
  </li>
  {% endfor %}
</ul>
{% endif %}
