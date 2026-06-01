// visitor.js — friendly "you're visitor #N" badge + visitor location.
// Static-site friendly: uses free, no-key public APIs, called client-side.
//   - Hit counter: Abacus (abacus.jasoncameron.dev), incremented once per
//     browser via localStorage so the number is stable across page views.
//   - Geolocation: GeoJS (get.geojs.io) — city/country from the visitor IP.
// Everything fails silently: if a service is down, the badge just stays hidden.

(function () {
  var bar   = document.getElementById("visitorBar");
  var countEl = document.getElementById("visitorCount");
  var locEl   = document.getElementById("visitorLoc");
  var sepEl   = document.getElementById("visitorSep");
  if (!bar) return;

  var COUNTER = "https://abacus.jasoncameron.dev/hit/shicheng-guo.github.io/site-visits";
  var GEO = "https://get.geojs.io/v1/ip/geo.json";
  var NO_KEY = "sg-visitor-no";
  var GEO_KEY = "sg-visitor-geo";

  function reveal() { bar.hidden = false; }
  function maybeSep() {
    if (sepEl && countEl.textContent && locEl.textContent) sepEl.hidden = false;
  }
  function fmt(n) { return Number(n).toLocaleString(); }

  function flagFromCC(cc) {
    if (!cc || cc.length !== 2) return "";
    return cc.toUpperCase().replace(/./g, function (c) {
      return String.fromCodePoint(127397 + c.charCodeAt(0));
    });
  }

  // ---- visitor number (increment once per browser) ----
  var stored = null;
  try { stored = localStorage.getItem(NO_KEY); } catch (e) {}

  function showNumber(n, returning) {
    countEl.textContent = (returning ? "👋 Welcome back — you were visitor #" : "👋 You're visitor #") + fmt(n);
    reveal(); maybeSep();
  }

  if (stored) {
    showNumber(stored, true);
  } else {
    fetch(COUNTER)
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var n = d && (d.value != null ? d.value : d.count);
        if (n != null) {
          try { localStorage.setItem(NO_KEY, n); } catch (e) {}
          showNumber(n, false);
        }
      })
      .catch(function () {});
  }

  // ---- location (cache per session) ----
  function showLoc(city, country, cc) {
    var place = [city, country].filter(Boolean).join(", ");
    if (!place) return;
    var flag = flagFromCC(cc);
    locEl.textContent = "Visiting from " + place + (flag ? " " + flag : "");
    reveal(); maybeSep();
  }

  var cached = null;
  try { cached = JSON.parse(sessionStorage.getItem(GEO_KEY) || "null"); } catch (e) {}
  if (cached) {
    showLoc(cached.city, cached.country, cached.cc);
  } else {
    fetch(GEO)
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var info = { city: d.city || "", country: d.country || "", cc: d.country_code || "" };
        try { sessionStorage.setItem(GEO_KEY, JSON.stringify(info)); } catch (e) {}
        showLoc(info.city, info.country, info.cc);
      })
      .catch(function () {});
  }
})();
