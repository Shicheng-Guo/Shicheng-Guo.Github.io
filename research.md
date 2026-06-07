---
layout: default
title: "Research"
nav: research
permalink: /research/
wide: true
content_class: archive
eyebrow: "Genomics · Biobank &amp; RWE · Data Science"
tagline: "Translating human genetics into validated drug targets and biomarkers."
description: "Research areas and projects of Shicheng Guo, Ph.D. — translational genetics, biobank & real-world evidence, statistical genetics, and data science."
---

<p class="lead">My research turns population-scale human biology into therapeutic decisions — identifying which targets are worth pursuing and which patients a medicine can help.</p>

<h2 class="archive__subtitle">Research Themes</h2>

<div class="highlights">
  <div class="hl-card">
    <i class="fa-solid fa-dna"></i>
    <h3>Translational Genetics</h3>
    <p>Human-genetics-driven target identification and validation across the druggable genome, de-risking discovery with population evidence.</p>
  </div>
  <div class="hl-card">
    <i class="fa-solid fa-database"></i>
    <h3>Biobank &amp; RWE</h3>
    <p>Population-scale biobanks (UK Biobank, eMERGE, PMRP) and real-world evidence from EHR and claims to drive target validation, safety, and patient stratification.</p>
  </div>
  <div class="hl-card">
    <i class="fa-solid fa-chart-line"></i>
    <h3>Computational Biology</h3>
    <p>Association, rare-variant and gene-based methods (SKAT, recessive diplotype) across biobanks — UK Biobank, eMERGE, PMRP, TCGA, GTEx.</p>
  </div>
  <div class="hl-card">
    <i class="fa-solid fa-microchip"></i>
    <h3>Data Science &amp; Agentic AI</h3>
    <p>Scalable bioinformatics pipelines and predictive models that turn multi-omic and clinical big data into program decisions.</p>
  </div>
</div>

<h2 class="archive__subtitle">Projects &amp; Methods</h2>

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

<p style="margin-top:2em">
  <a href="{{ site.url }}/publications/" style="border:0;font-weight:600"><i class="fa-solid fa-arrow-right"></i> See selected publications</a>
</p>
