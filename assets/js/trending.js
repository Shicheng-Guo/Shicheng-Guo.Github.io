// trending.js — live feed of fast-rising GitHub repos in pharma & biology.
// Adapted for shicheng-guo.github.io from the DS4CABS trending page.
// Uses the public GitHub Search API (no auth, no backend). GitHub has no
// official "trending" endpoint, so we rank repos CREATED within the selected
// window by stars descending. Results are cached in sessionStorage for 30 min
// to stay under the unauthenticated rate limit (60 req/hour/IP).

(function () {
  const mount = document.getElementById("trendingCards");
  if (!mount) return;
  const statusEl  = document.getElementById("trendingStatus");
  const topicsEl  = document.getElementById("trendingTopics");
  const windowEl  = document.getElementById("trendingWindow");
  const updatedEl = document.getElementById("trendingUpdated");

  function el(tag, attrs, ...kids) {
    const node = document.createElement(tag);
    if (attrs) {
      for (const [k, v] of Object.entries(attrs)) {
        if (v == null || v === false) continue;
        if (k === "class") node.className = v;
        else if (k === "html") node.innerHTML = v;
        else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2), v);
        else node.setAttribute(k, v === true ? "" : String(v));
      }
    }
    for (const c of kids.flat(Infinity)) {
      if (c == null || c === false || c === true) continue;
      node.appendChild(c instanceof Node ? c : document.createTextNode(String(c)));
    }
    return node;
  }
  const pill = (text, title) => el("span", { class: "repo-pill", title: title || null }, text);
  const fmt  = (n) => (n >= 1000 ? (n / 1000).toFixed(n >= 10000 ? 0 : 1) + "k" : String(n));

  const TOPICS = [
    { id: "all",          label: "🔥 All bio + pharma",
      q: "bioinformatics OR genomics OR drug-discovery OR pharma OR proteomics OR cheminformatics" },
    { id: "bioinformatics",        label: "🧬 Bioinformatics",         q: "topic:bioinformatics" },
    { id: "drug-discovery",        label: "💊 Drug discovery",         q: "topic:drug-discovery" },
    { id: "genomics",              label: "🧪 Genomics",               q: "topic:genomics" },
    { id: "computational-biology", label: "🔬 Computational biology",  q: "topic:computational-biology" },
    { id: "cheminformatics",       label: "⚗️ Cheminformatics",        q: "topic:cheminformatics" },
    { id: "single-cell",           label: "🦠 Single cell",            q: "topic:single-cell" },
  ];

  const WINDOWS = [
    { id: "7",   label: "This week" },
    { id: "30",  label: "This month" },
    { id: "90",  label: "Last 90 days" },
    { id: "365", label: "This year" },
  ];

  let activeTopic  = TOPICS[0];
  let activeWindow = WINDOWS[1];

  function sinceDate(days) {
    const d = new Date();
    d.setDate(d.getDate() - Number(days));
    return d.toISOString().slice(0, 10);
  }

  function buildUrl() {
    const q = `${activeTopic.q} created:>=${sinceDate(activeWindow.id)}`;
    const params = new URLSearchParams({ q, sort: "stars", order: "desc", per_page: "30" });
    return "https://api.github.com/search/repositories?" + params.toString();
  }

  function renderControls() {
    [[topicsEl, TOPICS, "activeTopic"], [windowEl, WINDOWS, "activeWindow"]].forEach(([box, list, key]) => {
      if (!box) return;
      box.replaceChildren();
      const active = key === "activeTopic" ? activeTopic : activeWindow;
      list.forEach(item => {
        const isActive = item.id === active.id;
        box.appendChild(el("button", {
          class: "filter-pill" + (isActive ? " is-active" : ""),
          type: "button",
          "aria-pressed": isActive ? "true" : "false",
          onclick: () => {
            if (key === "activeTopic" && activeTopic.id !== item.id) { activeTopic = item; renderControls(); load(); }
            if (key === "activeWindow" && activeWindow.id !== item.id) { activeWindow = item; renderControls(); load(); }
          }
        }, item.label));
      });
    });
  }

  function repoCard(r) {
    const topics = (r.topics || []).slice(0, 4);
    return el("article", { class: "repo-card" },
      el("div", { class: "repo-card__head" },
        el("h3", null, el("a", { href: r.html_url, target: "_blank", rel: "noopener" }, r.full_name)),
        r.language && el("span", { class: "repo-lang" }, r.language)
      ),
      el("p", { class: "repo-desc" }, r.description || "No description provided."),
      topics.length > 0 && el("div", { class: "tags" }, topics.map(t => el("span", { class: "tag" }, t))),
      el("div", { class: "repo-meta" },
        pill("★ " + fmt(r.stargazers_count), r.stargazers_count + " stars"),
        r.forks_count > 0 && pill("⑂ " + fmt(r.forks_count), r.forks_count + " forks"),
        el("a", { class: "repo-view", href: r.html_url, target: "_blank", rel: "noopener" }, "View →")
      )
    );
  }

  function setStatus(msg, isError) {
    if (!statusEl) return;
    statusEl.hidden = !msg;
    statusEl.textContent = msg || "";
    statusEl.classList.toggle("is-error", !!isError);
  }

  async function load() {
    const url = buildUrl();
    const cacheKey = "sg-trending:" + url;
    mount.replaceChildren();
    setStatus("Loading hot repositories from GitHub…", false);
    if (updatedEl) updatedEl.textContent = "";

    try {
      const cached = JSON.parse(sessionStorage.getItem(cacheKey) || "null");
      if (cached && (Date.now() - cached.t) < 30 * 60 * 1000) {
        return render(cached.items, new Date(cached.t), true);
      }
    } catch (_) {}

    try {
      const res = await fetch(url, { headers: { Accept: "application/vnd.github+json" } });
      if (res.status === 403 || res.status === 429) {
        setStatus("GitHub's hourly request limit was reached (the public API allows 60/hour). Please try again in a little while.", true);
        return;
      }
      if (!res.ok) {
        setStatus("Could not load repositories from GitHub (HTTP " + res.status + "). Please try again later.", true);
        return;
      }
      const data = await res.json();
      const items = data.items || [];
      try { sessionStorage.setItem(cacheKey, JSON.stringify({ t: Date.now(), items })); } catch (_) {}
      render(items, new Date(), false);
    } catch (err) {
      setStatus("Network error while contacting GitHub. Check your connection and try again.", true);
    }
  }

  function render(items, when, fromCache) {
    mount.replaceChildren();
    if (!items.length) {
      setStatus("No repositories found for this filter in the selected time window.", false);
      return;
    }
    setStatus("", false);
    items.forEach(r => mount.appendChild(repoCard(r)));
    if (updatedEl) {
      const t = when.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
      updatedEl.textContent = "Showing " + items.length + " repositories · updated " + t + (fromCache ? " (cached)" : " (live)");
    }
  }

  renderControls();
  load();
})();
