// kol.js — renders the curated Key Opinion Leaders board from
// assets/data/kol.json. Ranked cards, with a search filter.
// This is a CURATED list (edit the JSON to maintain it) — see the page note.

(function () {
  const mount = document.getElementById("kolBoard");
  if (!mount) return;
  const statusEl  = document.getElementById("kolStatus");
  const searchEl  = document.getElementById("kolSearch");
  const updatedEl = document.getElementById("kolUpdated");
  const DATA_URL  = "/assets/data/kol.json";

  let all = [];
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

  function matches(k) {
    if (!query) return true;
    var hay = [k.name, k.title, k.note, (k.focus || []).join(" ")].join(" ").toLowerCase();
    return hay.indexOf(query) !== -1;
  }

  function card(k) {
    return el("article", { class: "kol-card" },
      el("div", { class: "kol-rank" }, "#" + (k.rank || "")),
      el("div", { class: "kol-body" },
        el("h3", { class: "kol-name" },
          k.link ? el("a", { href: k.link, target: "_blank", rel: "noopener" }, k.name) : k.name
        ),
        k.title && el("div", { class: "kol-title" }, k.title),
        (k.focus && k.focus.length) && el("div", { class: "tags" }, k.focus.map(f => el("span", { class: "tag" }, f))),
        k.note && el("p", { class: "kol-note" }, k.note)
      )
    );
  }

  function render() {
    const rows = all.filter(matches).sort((a, b) => (a.rank || 999) - (b.rank || 999));
    mount.replaceChildren();
    if (!rows.length) {
      mount.appendChild(el("p", { class: "deal-empty" }, "No KOLs match your search."));
      return;
    }
    rows.forEach(k => mount.appendChild(card(k)));
  }

  function setStatus(msg, isError) {
    if (!statusEl) return;
    statusEl.hidden = !msg;
    statusEl.textContent = msg || "";
    statusEl.classList.toggle("is-error", !!isError);
  }

  if (searchEl) searchEl.addEventListener("input", e => { query = e.target.value.trim().toLowerCase(); render(); });

  setStatus("Loading KOL board…", false);
  fetch(DATA_URL, { cache: "no-cache" })
    .then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(data => {
      all = (data.kols || []).filter(k => k.name);
      setStatus("", false);
      if (updatedEl) {
        var bits = [];
        if (data.updated) bits.push("Curated list · updated " + data.updated);
        bits.push(all.length + " featured");
        updatedEl.textContent = bits.join(" · ");
      }
      render();
    })
    .catch(() => setStatus("Couldn't load the KOL board (assets/data/kol.json).", true));
})();
