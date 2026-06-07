# Shicheng Guo — Personal Research Site & Pharma Intelligence Hub

[![Deploy](https://img.shields.io/badge/GitHub%20Pages-live-brightgreen?logo=github)](https://shicheng-guo.github.io)
[![Built with Jekyll](https://img.shields.io/badge/built%20with-Jekyll-cc0000?logo=jekyll&logoColor=white)](https://jekyllrb.com)
[![Daily data updates](https://img.shields.io/badge/data-auto--updated%20daily-blue?logo=githubactions&logoColor=white)](.github/workflows)

The source for **[shicheng-guo.github.io](https://shicheng-guo.github.io)** — the personal and professional site of **Shicheng Guo, Ph.D.**, Senior Director of Translational Genetics & Data Science at Arrowhead Pharmaceuticals.

It is two things at once:

1. **An academic site** — research themes, projects, publications, and a technical blog.
2. **A living pharma-intelligence hub** — a set of dashboards (AI in pharma, biobanks, BD deals, clinical-trial readouts, real-world evidence, and more) that **refresh themselves every day** via Python scrapers and GitHub Actions.

---

## ✨ Highlights

- 🧬 **Research & projects** — translational genetics, biobank & RWE, computational biology, and agentic AI.
- 📝 **Technical blog** — bioinformatics, statistics, and data-science write-ups (`_posts/`).
- 🤖 **Self-updating dashboards** — seven daily pipelines fetch fresh data into JSON, committed automatically and rendered client-side.
- ⚡ **Zero-build deployment** — pushed to `master`, built and served by GitHub Pages.
- 📊 **Lightweight, privacy-friendly analytics** via GoatCounter.

---

## 🗂️ Site Sections

| Page | URL | Source | Content |
|---|---|---|---|
| Home | `/` | `index.html` | Landing page |
| About | `/about/` | `about.md` | Bio & background |
| Research | `/research/` | `research.md` + `_portfolio/` | Research themes & project cards |
| Publications | `/publications/` | `publications.md` + `_publications/` | Selected papers |
| Blog | `/blog/` | `_posts/` | Paginated technical posts |
| AI in Pharma | `/ai/` | `ai.md` ← `assets/data/ai.json` | 🔄 Auto-updated |
| Biobank | `/biobank/` | `biobank.md` ← `biobank.json` | 🔄 Auto-updated |
| BD Deals | `/deals/` | `deals.md` ← `deals.json` | 🔄 Auto-updated |
| Pharma 5.0 | `/pharma/` | `pharma.md` ← `pharma.json` | 🔄 Auto-updated |
| Real-World Evidence | `/rwe/` | `rwe.md` ← `rwe.json` | 🔄 Auto-updated |
| Clinical Trials | `/trials/` | `trials.md` ← `trials.json` | 🔄 Auto-updated |
| Innovation | `/innovation/` | `innovation.md` ← `startups.json` | 🔄 Auto-updated |
| Trending | `/trending/` | `trending.md` | Live from the GitHub API |
| Conferences / KOL / Consortium | `/conference/`, `/kol/`, … | `*.md` ← `assets/data/*.json` | Curated lists |

---

## 🤖 Automated Data Pipelines

The intelligence dashboards stay current without manual edits. Each pipeline follows the same pattern:

```
GitHub Actions (daily cron)  →  scripts/fetch_*.py  →  assets/data/*.json  →  page renders the JSON
                                       ↓
                          git commit "[skip ci]" & push
```

| Workflow | Script | Output | Schedule |
|---|---|---|---|
| [`update-ai.yml`](.github/workflows/update-ai.yml) | `scripts/fetch_ai.py` | `ai.json` | Daily 07:07 UTC |
| [`update-biobank.yml`](.github/workflows/update-biobank.yml) | `scripts/fetch_biobank.py` | `biobank.json` | Daily |
| [`update-deals.yml`](.github/workflows/update-deals.yml) | `scripts/fetch_deals.py` | `deals.json` | Daily |
| [`update-pharma.yml`](.github/workflows/update-pharma.yml) | `scripts/fetch_pharma.py` | `pharma.json` | Daily |
| [`update-rwe.yml`](.github/workflows/update-rwe.yml) | `scripts/fetch_rwe.py` | `rwe.json` | Daily |
| [`update-startups.yml`](.github/workflows/update-startups.yml) | `scripts/fetch_startup_news.py` | `startup_news.json`, `startups.json` | Daily |
| [`update-trials.yml`](.github/workflows/update-trials.yml) | `scripts/fetch_trials.py` | `trials.json` | Daily |

Each workflow can also be triggered manually from the **Actions** tab (`workflow_dispatch`). Commits are tagged `[skip ci]` to avoid retriggering the page build loop.

**Run a scraper locally:**

```bash
python3 scripts/fetch_ai.py   # writes assets/data/ai.json
```

---

## 🏗️ Tech Stack

- **[Jekyll](https://jekyllrb.com/)** (`~> 3.1`) — static site generator
- **Plugins** — `jekyll-sitemap`, `jekyll-paginate`
- **Rouge** — syntax highlighting
- **Python 3.12** — daily data scrapers
- **GitHub Actions** — scheduled automation
- **GitHub Pages** — hosting & build
- **GoatCounter** — analytics

---

## 📁 Repository Structure

```
.
├── _config.yml          # Jekyll configuration
├── index.html           # Home page
├── about.md             # Bio
├── research.md          # Research themes (+ _portfolio cards)
├── publications.md      # Publications (+ _publications)
├── ai.md, biobank.md … # Dynamic dashboard pages (render assets/data/*.json)
├── _posts/              # Blog posts (YYYY-MM-DD-title.md)
├── _portfolio/          # Project cards shown on /research/
├── _publications/       # Publication entries
├── _layouts/            # default, page, post
├── _includes/           # Reusable partials & theme
├── assets/
│   ├── css/  js/  images/
│   └── data/            # JSON data, refreshed by scrapers
├── scripts/             # Python data-fetch scripts
└── .github/workflows/   # Daily update automations
```

---

## 🚀 Local Development

**Prerequisites:** Ruby + Bundler, and Python 3.12 (only if running scrapers).

```bash
# 1. Install dependencies
bundle install

# 2. Serve locally with live reload
bundle exec jekyll serve

# 3. Open the site
open http://localhost:4000
```

The generated site lands in `_site/` (do not edit by hand — it's build output).

---

## ✍️ Adding Content

### New blog post

Create `_posts/YYYY-MM-DD-title.md` with front matter:

```yaml
---
layout: post
title: "Your Post Title"
author: Shicheng Guo
date: 2026-06-06
categories: tutorials
tags: tag-one tag-two
---

Your content in Markdown…
```

The URL follows the permalink rule `/:categories/:year/:month/:day/:title` →
`https://shicheng-guo.github.io/tutorials/2026/06/06/title.html`.

### New project card (Research page)

Add `_portfolio/N-slug.md`:

```yaml
---
title: "Project Title"
excerpt: "One-line summary."
icon: "fa-solid fa-dna"
link: "https://github.com/Shicheng-Guo/…"
tags: "Tag one, Tag two, Tag three"
order: 5
---
```

---

## 🌐 Deployment

Deployment is fully automatic: **push to `master` → GitHub Pages rebuilds → live in ~1–2 minutes.** No manual build step is required.

---

## 📈 Analytics

Privacy-friendly analytics via **GoatCounter** (`goatcounter_code: sguo` in `_config.yml`).
Dashboard: [shichengguo.goatcounter.com](https://shichengguo.goatcounter.com).

---

## 📫 Contact

**Shicheng Guo, Ph.D.**
Senior Director, Translational Genetics & Data Science — Arrowhead Pharmaceuticals

- 🌐 [shicheng-guo.github.io](https://shicheng-guo.github.io)
- 🐙 [github.com/Shicheng-Guo](https://github.com/Shicheng-Guo)
- ✉️ Shihcheng.Guo@gmail.com

---

## 📄 License

Code and templates are released under the **MIT License** — see [LICENSE](LICENSE). Blog posts and written content © Shicheng Guo.
