// conference.js — renders the curated biopharma conference calendar from
// assets/data/conferences.json. Shows UPCOMING events (auto-hides past),
// sorted by date; filter by focus tag and search.

(function () {
  const mount = document.getElementById("confList");
  if (!mount) return;
  const statusEl  = document.getElementById("confStatus");
  const searchEl  = document.getElementById("confSearch");
  const updatedEl = document.getElementById("confUpdated");
  const countEl   = document.getElementById("confCount");
  const tagBox    = document.getElementById("confTags");
  const DATA_URL  = "/assets/data/conferences.json";

  let all = [];
  let activeTag = "";
  let query = "";

  function el(tag, attrs, ...kids) {
    const node = document.createElement(tag);
    if (attrs) for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === "class") node.className = v;
      else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2), v);
      else node.setAttribute(k, v === true ? "" : String(v));
    }
    for (const c of kids.flat(Infinity)) {
      if (c == null || c === false || c === true) continue;
      node.appendChild(c instanceof Node ? c : document.createTextNode(String(c)));
    }
    return node;
  }

  function renderFilters() {
    if (!tagBox) return;
    const tags = [...new Set(all.flatMap(c => c.tags || []))].sort();
    tagBox.replaceChildren();
    ["", ...tags].forEach(val => {
      const isActive = activeTag === val;
      tagBox.appendChild(el("button", {
        class: "filter-pill" + (isActive ? " is-active" : ""),
        type: "button",
        "aria-pressed": isActive ? "true" : "false",
        onclick: () => { activeTag = val; renderFilters(); render(); }
      }, val || "All"));
    });
  }

  function matches(c) {
    if (activeTag && !(c.tags || []).includes(activeTag)) return false;
    if (query) {
      var hay = [c.name, c.location, (c.tags || []).join(" ")].join(" ").toLowerCase();
      if (hay.indexOf(query) === -1) return false;
    }
    return true;
  }

  function item(c) {
    return el("div", { class: "conf-item" },
      el("div", { class: "conf-date" }, c.date || (c.start || "")),
      el("div", { class: "conf-body" },
        el("h3", { class: "conf-name" },
          c.link ? el("a", { href: c.link, target: "_blank", rel: "noopener" }, c.name) : c.name
        ),
        c.location && el("div", { class: "conf-loc" },
          el("i", { class: "fa-solid fa-location-dot" }), " " + c.location),
        (c.tags && c.tags.length) && el("div", { class: "tags" }, c.tags.map(t => el("span", { class: "tag" }, t)))
      )
    );
  }

  function render() {
    const rows = all.filter(matches).sort((a, b) => (a.start || "").localeCompare(b.start || ""));
    if (countEl) countEl.textContent = rows.length + (rows.length === 1 ? " upcoming conference" : " upcoming conferences");
    mount.replaceChildren();
    if (!rows.length) { mount.appendChild(el("p", { class: "deal-empty" }, "No upcoming conferences match.")); return; }
    rows.forEach(c => mount.appendChild(item(c)));
  }

  function setStatus(msg, isError) {
    if (!statusEl) return;
    statusEl.hidden = !msg;
    statusEl.textContent = msg || "";
    statusEl.classList.toggle("is-error", !!isError);
  }

  if (searchEl) searchEl.addEventListener("input", e => { query = e.target.value.trim().toLowerCase(); render(); });

  setStatus("Loading conferences…", false);
  fetch(DATA_URL, { cache: "no-cache" })
    .then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(data => {
      const today = new Date().toISOString().slice(0, 10);
      all = (data.conferences || []).filter(c => c.name && (!c.start || c.start >= today));
      setStatus("", false);
      if (updatedEl) updatedEl.textContent = (data.updated ? "Curated · updated " + data.updated + " · " : "") + all.length + " upcoming";
      renderFilters();
      render();
    })
    .catch(() => setStatus("Couldn't load the conference calendar (assets/data/conferences.json).", true));
})();
