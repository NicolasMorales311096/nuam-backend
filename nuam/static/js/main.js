/* =========================================
   NUAM - JS base (fetch + helpers + UI)
   Ruta esperada: /static/js/main.js
   ========================================= */

// ---------- Config ----------
const API_BASE = "/api/";                 // DRF router
const TOKEN_KEY = "nuam_token";           // guardamos JWT aquí (si lo usas)

// ---------- Helpers ----------
function $(sel, root = document) { return root.querySelector(sel); }
function $all(sel, root = document) { return [...root.querySelectorAll(sel)]; }

function getToken() { return localStorage.getItem(TOKEN_KEY) || ""; }
function setToken(t) { localStorage.setItem(TOKEN_KEY, t || ""); }

function authHeaders(extra = {}) {
  const token = getToken();
  const h = { "Accept": "application/json", ...extra };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

async function fetchJSON(url, opts = {}) {
  const res = await fetch(url, opts);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
  }
  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

function toast(msg, type = "ok") {
  let el = $("#toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "toast";
    el.style.cssText = `
      position: fixed; right: 16px; bottom: 16px; z-index: 9999;
      background: ${type === "ok" ? "#16a34a" : "#dc2626"};
      color: #fff; padding: 10px 14px; border-radius: 10px; font-weight:600;
      box-shadow: 0 6px 18px rgba(0,0,0,.15);
    `;
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.style.display = "block";
  setTimeout(() => (el.style.display = "none"), 2200);
}

// ---------- Login (opcional) ----------
/* 
   Si usas JWT:
   - Obtén el token con POST a /api/auth/login/ y guarda "access" en localStorage.
   - Llama setToken(token).
   Puedes montar un pequeño form con id="login-form" y campos username/password.
*/
async function tryLoginFromForm() {
  const form = $("#login-form");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    try {
      const res = await fetchJSON("/api/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: data.username, password: data.password }),
      });
      setToken(res.access);
      toast("Sesión iniciada", "ok");
    } catch (err) {
      toast("Login inválido", "err");
      console.error(err);
    }
  });
}

// ---------- Emisores (lista + alta) ----------
async function loadEmisores() {
  const table = $("#tabla-emisores");
  if (!table) return; // esta página no usa emisores

  const tbody = table.tBodies[0] || table.createTBody();
  tbody.innerHTML = `<tr><td colspan="3">Cargando…</td></tr>`;

  try {
    const emisores = await fetchJSON(`${API_BASE}emisores/`, {
      headers: authHeaders(),
    });
    tbody.innerHTML = "";
    if (!emisores.length) {
      tbody.innerHTML = `<tr><td colspan="3">Sin registros</td></tr>`;
      return;
    }
    for (const e of emisores) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${e.id}</td>
        <td>${e.nombre || "-"}</td>
        <td>${e.rut || "-"}</td>
      `;
      tbody.appendChild(tr);
    }
  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="3">Error al cargar</td></tr>`;
    toast("Error al cargar emisores", "err");
  }
}

function bindEmisorCreate() {
  const form = $("#form-emisor");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    try {
      await fetchJSON(`${API_BASE}emisores/`, {
        method: "POST",
        headers: authHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(data),
      });
      toast("Emisor creado", "ok");
      form.reset();
      loadEmisores();
    } catch (err) {
      console.error(err);
      toast("No se pudo crear", "err");
    }
  });
}

// ---------- Calificaciones (filtro simple por año) ----------
async function loadCalificaciones() {
  const table = $("#tabla-calificaciones");
  if (!table) return;

  const yearSel = $("#filtro-anio");
  const query = yearSel && yearSel.value ? `?anio=${encodeURIComponent(yearSel.value)}` : "";
  const tbody = table.tBodies[0] || table.createTBody();
  tbody.innerHTML = `<tr><td colspan="6">Cargando…</td></tr>`;

  try {
    const items = await fetchJSON(`${API_BASE}calificaciones/${query}`, {
      headers: authHeaders(),
    });
    tbody.innerHTML = "";
    if (!items.length) {
      tbody.innerHTML = `<tr><td colspan="6">Sin registros</td></tr>`;
      return;
    }
    for (const c of items) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${c.id}</td>
        <td>${c.anio ?? "-"}</td>
        <td>${c.instrumento ?? "-"}</td>
        <td>${c.tipo_calculo ?? "-"}</td>
        <td>${c.monto ?? "-"}</td>
        <td>${c.factor ?? "-"}</td>
      `;
      tbody.appendChild(tr);
    }
  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="6">Error al cargar</td></tr>`;
    toast("Error al cargar calificaciones", "err");
  }
}

function bindCalifFiltro() {
  const yearSel = $("#filtro-anio");
  if (yearSel) yearSel.addEventListener("change", loadCalificaciones);
}

// ---------- UI pequeños ----------
function initVideoAutoplay() {
  const v = document.querySelector(".hero-video");
  if (!v) return;
  // algunos navegadores bloquean autoplay si no está muted/playsinline.
  v.muted = true;
  v.playsInline = true;
  v.play().catch(() => {/* ignorar */});
}

// ---------- Init ----------
document.addEventListener("DOMContentLoaded", () => {
  tryLoginFromForm();

  loadEmisores();
  bindEmisorCreate();

  loadCalificaciones();
  bindCalifFiltro();

  initVideoAutoplay();
});
