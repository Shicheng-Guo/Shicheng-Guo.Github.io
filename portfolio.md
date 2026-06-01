---
layout: default
title: "Portfolio & Projects"
nav: portfolio
permalink: /portfolio/
content_class: archive
eyebrow: "Methods · Pipelines · Open Source"
tagline: "Selected research software and methodological projects."
description: "Research projects and open-source software by Shicheng Guo, Ph.D."
---

<div class="portfolio-grid">
  {% assign items = site.portfolio | sort: "order" %}
  {% for item in items %}
  <a class="portfolio-card" href="{{ item.link }}">
    <i class="{{ item.icon | default: 'fa-solid fa-cube' }}"></i>
    <h3>{{ item.title }}</h3>
    <p>{{ item.excerpt }}</p>
    {% if item.tags %}
    <div class="tags">
      {% assign tags = item.tags | split: "," %}
      {% for t in tags %}<span class="tag">{{ t | strip }}</span>{% endfor %}
    </div>
    {% endif %}
  </a>
  {% endfor %}
</div>
