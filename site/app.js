(() => {
  "use strict";

  const shop = window.SHOP || { shelves: [], products: [] };
  const cfg = window.SHOP_CONFIG || {};
  const cabinet = document.getElementById("shop");
  const tplDrawer = document.getElementById("tpl-drawer");
  const money = new Intl.NumberFormat("es-MX", { maximumFractionDigits: 0 });
  const tilts = [-2.2, 1.4, -0.8, 2, -1.6, 0.9, -2.6, 1.8];

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };

  const priceText = (p) => (p == null ? "Pregunta" : "$" + money.format(p));

  const waLink = (text) =>
    "https://wa.me/" + (cfg.whatsapp || "") + "?text=" + encodeURIComponent(text);

  const waMessage = (p) =>
    p
      ? `Hola, vi en ${cfg.name || "Bastians Flea Market"} el ${p.name}` +
        (p.price != null ? ` ($${money.format(p.price)} MXN)` : "") +
        ". ¿Sigue disponible?"
      : `Hola, vi ${cfg.name || "Bastians Flea Market"} y tengo una pregunta.`;

  const prettyPhone = (n) => {
    const d = String(n || "").replace(/^52/, "");
    return d.length === 10 ? `${d.slice(0, 2)} ${d.slice(2, 6)} ${d.slice(6)}` : d;
  };

  /* ───── Shelves ───── */

  const byShelf = new Map(shop.shelves.map((s) => [s.id, []]));
  shop.products.forEach((p) => byShelf.has(p.shelf) && byShelf.get(p.shelf).push(p));

  const compactQ = window.matchMedia("(max-width: 760px)");
  let buttons = new Map();

  const chunk = (arr, n) => arr.reduce((out, x, i) => (i % n ? out[out.length - 1].push(x) : out.push([x]), out), []);

  function itemNode(p, i, tilt, eager) {
    const main = p.photos[0];
    const li = el("li", "item" + (p.sold ? " item--sold" : ""));
    li.style.gridColumn = String(i * 2 + 2);
    li.style.setProperty("--tilt", tilt + "deg");

    const btn = el("button", "item-btn");
    btn.type = "button";
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", "drawer");
    btn.dataset.slug = p.slug;

    const photo = el("span", "item-photo");
    if (main) {
      const img = new Image(main.w, main.h);
      img.src = main.src;
      img.alt = "";
      img.decoding = "async";
      if (!eager) img.loading = "lazy";
      photo.append(img);
    }
    if (p.sold) photo.append(hanko());

    const tag = el("span", "item-tag");
    tag.append(el("span", "tag-model", `${p.brand} ${p.model}`));
    const price = el("span", "tag-price", priceText(p.price));
    if (p.price != null) price.append(el("small", null, "MXN"));
    tag.append(price);
    if (p.sold) tag.append(el("span", "tag-condition", "Vendido"));

    btn.setAttribute(
      "aria-label",
      `${p.brand} ${p.model}, ${p.price != null ? money.format(p.price) + " pesos" : "precio a preguntar"}` +
        (p.sold ? ", vendido" : "")
    );
    btn.append(photo, tag);
    li.append(btn);
    buttons.set(p.slug, btn);
    return li;
  }

  function hanko() {
    const h = el("span", "hanko");
    h.setAttribute("aria-hidden", "true");
    const jp = el("span", "hanko-jp", "売約済");
    jp.lang = "ja";
    h.append(jp, el("span", "hanko-es", "VENDIDO"));
    return h;
  }

  // Desktop: one shelf board per bay. Phones: two items per board, stacked, no sideways scroll.
  function renderShelves() {
    const compact = compactQ.matches;
    cabinet.querySelectorAll(".shelf").forEach((n) => n.remove());
    buttons = new Map();
    let n = 0;

    shop.shelves.forEach((s) => {
      const items = byShelf.get(s.id);
      if (!items.length) return;

      const shelf = el("section", "shelf" + (items.length > 2 ? " shelf--wide" : ""));
      shelf.dataset.shelf = s.id;
      shelf.setAttribute("aria-labelledby", `shelf-${s.id}`);

      const sign = el("h2", "shelf-sign");
      sign.id = `shelf-${s.id}`;
      const kanji = el("span", "shelf-sign-kanji", s.kanji);
      kanji.lang = "ja";
      kanji.setAttribute("aria-hidden", "true");
      sign.append(kanji, el("span", "shelf-sign-label", s.label));

      const bay = el("div", "bay");
      (compact ? chunk(items, 2) : [items]).forEach((group) => {
        const row = el("ul", "row");
        row.setAttribute("role", "list");
        const spacer = compact ? "12px" : "minmax(18px, 1fr)";
        const cols = [spacer];
        group.forEach((p, i) => {
          const main = p.photos[0];
          const landscape = main && main.w > main.h;
          cols.push(compact ? "minmax(0, 1fr)" : landscape ? "var(--l-w)" : "var(--p-w)", spacer);
          row.append(itemNode(p, i, tilts[n % tilts.length], n < 4));
          n++;
        });
        if (compact && group.length === 1) cols.push("minmax(0, 1fr)", spacer);
        row.style.gridTemplateColumns = cols.join(" ");

        const rail = el("li", "rail");
        rail.setAttribute("aria-hidden", "true");
        rail.setAttribute("role", "presentation");
        row.append(rail);

        if (compact) bay.append(row);
        else {
          const scroll = el("div", "bay-scroll");
          scroll.append(row);
          bay.append(scroll);
        }
      });

      shelf.append(sign, bay);
      cabinet.append(shelf);
    });
  }

  renderShelves();

  const total = shop.products.length;
  const sold = shop.products.filter((p) => p.sold).length;
  const count = document.getElementById("stock-count");
  if (count) count.textContent = `${total - sold} de ${total} disponibles.`;

  /* ───── Drawer ───── */

  const drawer = el("div", "drawer");
  drawer.id = "drawer";
  drawer.setAttribute("role", "region");
  drawer.hidden = true;
  drawer.append(tplDrawer.content.cloneNode(true));

  const $ = (sel) => drawer.querySelector(sel);
  const nameEl = $(".sheet-name");
  nameEl.id = "drawer-title";
  drawer.setAttribute("aria-labelledby", "drawer-title");
  const mainFig = $(".gallery-main");
  const mainImg = new Image();
  mainImg.decoding = "async";
  const mainHanko = hanko();
  mainHanko.classList.add("gallery-hanko");
  mainFig.append(mainImg, mainHanko);
  const thumbs = $(".gallery-thumbs");
  const form = $(".note");
  const status = $(".note-status");

  let current = null;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function showPhoto(p, i) {
    const ph = p.photos[i];
    if (!ph) return;
    mainImg.src = ph.src;
    mainImg.width = ph.w;
    mainImg.height = ph.h;
    mainImg.alt = `${p.name}, foto ${i + 1} de ${p.photos.length}`;
    thumbs.querySelectorAll(".thumb").forEach((t, j) => t.setAttribute("aria-pressed", String(i === j)));
  }

  function fill(p) {
    nameEl.textContent = p.name;
    const price = $(".sheet-price");
    price.textContent = priceText(p.price);
    if (p.price != null) price.append(el("small", null, "MXN"));
    const cond = $(".sheet-condition");
    cond.replaceChildren();
    if (!p.sold && p.condition) cond.append(el("b", null, "Estado"), p.condition);
    $(".sheet-blurb").textContent = p.blurb;

    const tbody = $(".specs tbody");
    tbody.replaceChildren(
      ...p.specs.map(([k, v]) => {
        const tr = el("tr");
        const th = el("th", null, k);
        th.scope = "row";
        tr.append(th, el("td", null, v));
        return tr;
      })
    );

    thumbs.replaceChildren(
      ...p.photos.map((ph, i) => {
        const b = el("button", "thumb");
        b.type = "button";
        b.setAttribute("aria-label", `Ver foto ${i + 1}`);
        const im = new Image(ph.w, ph.h);
        im.src = ph.src;
        im.alt = "";
        im.loading = "lazy";
        b.append(im);
        b.addEventListener("click", () => showPhoto(p, i));
        return b;
      })
    );
    thumbs.hidden = p.photos.length < 2;
    showPhoto(p, 0);

    $(".sheet-wa").href = waLink(waMessage(p));
    drawer.classList.toggle("is-sold", p.sold);

    form.reset();
    form.message.value = p.sold
      ? `Hola, vi que el ${p.name} ya se vendió. Busco algo parecido.`
      : `Hola, me interesa el ${p.name}.`;
    status.textContent = "";
    status.classList.remove("is-error");
    form.querySelectorAll("[aria-invalid]").forEach((n) => n.removeAttribute("aria-invalid"));
  }

  // The drawer slides out under the last shelf of the visual row the item sits in.
  function anchorFor(shelf) {
    const shelves = [...cabinet.querySelectorAll(".shelf")];
    const top = shelf.offsetTop;
    return shelves.filter((s) => s.offsetTop === top).pop() || shelf;
  }

  function open(slug, { scroll = true, focus = true } = {}) {
    const p = shop.products.find((x) => x.slug === slug);
    const btn = buttons.get(slug);
    if (!p || !btn) return;

    if (current) buttons.get(current).setAttribute("aria-expanded", "false");
    const anchor = anchorFor(btn.closest(".shelf"));
    const moving = drawer.previousElementSibling !== anchor;

    fill(p);
    current = slug;
    const sc = btn.closest(".bay-scroll");
    const br = btn.getBoundingClientRect(), sr = sc ? sc.getBoundingClientRect() : br;
    if (sc && (br.left < sr.left || br.right > sr.right)) {
      sc.scrollBy({ left: br.left - sr.left - 18, behavior: reduceMotion.matches ? "auto" : "smooth" });
    }
    btn.setAttribute("aria-expanded", "true");

    if (moving || drawer.hidden) {
      drawer.classList.remove("is-open");
      anchor.after(drawer);
      drawer.hidden = false;
      void drawer.offsetHeight; // start the slide from closed
    }
    requestAnimationFrame(() => drawer.classList.add("is-open"));

    if (history.replaceState) history.replaceState(null, "", "#" + slug);
    if (focus) nameEl.focus({ preventScroll: true });
    if (scroll) {
      const behavior = reduceMotion.matches ? "auto" : "smooth";
      setTimeout(() => {
        const y = drawer.getBoundingClientRect().top + window.scrollY - 12;
        window.scrollTo({ top: y, behavior });
      }, reduceMotion.matches ? 0 : 120);
    }
  }

  function close() {
    if (!current) return;
    const btn = buttons.get(current);
    btn.setAttribute("aria-expanded", "false");
    drawer.classList.remove("is-open");
    current = null;
    if (history.replaceState) history.replaceState(null, "", location.pathname + location.search);
    const done = () => { if (!current) drawer.hidden = true; };
    if (reduceMotion.matches) done();
    else setTimeout(done, 700);
    btn.focus({ preventScroll: true });
    const r = btn.getBoundingClientRect();
    if (r.top < 0 || r.bottom > innerHeight) btn.scrollIntoView({ block: "center", behavior: reduceMotion.matches ? "auto" : "smooth" });
  }

  cabinet.addEventListener("click", (e) => {
    const btn = e.target.closest(".item-btn");
    if (!btn) return;
    if (btn.dataset.slug === current) close();
    else open(btn.dataset.slug);
  });

  $(".drawer-close").addEventListener("click", close);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && current && drawer.contains(document.activeElement)) close();
  });

  /* ───── Message form ───── */

  const looksValid = (v) => /\S+@\S+\.\S+/.test(v) || v.replace(/\D/g, "").length >= 8;

  function bindForm(form, status, getProduct) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const p = getProduct();
    const name = form.name.value.trim();
    const contact = form.contact.value.trim();
    const message = form.message.value.trim();

    const bad = [];
    if (!name) bad.push([form.name, "Falta tu nombre."]);
    if (!looksValid(contact)) bad.push([form.contact, "Escribe un WhatsApp de 10 dígitos o un correo válido."]);
    if (!message) bad.push([form.message, "Escribe tu mensaje."]);
    form.querySelectorAll("[aria-invalid]").forEach((n) => n.removeAttribute("aria-invalid"));
    if (bad.length) {
      bad.forEach(([f]) => f.setAttribute("aria-invalid", "true"));
      bad[0][0].focus();
      status.textContent = bad[0][1];
      status.classList.add("is-error");
      return;
    }

    const full = `${message}\n\n— ${name} (${contact})`;

    // Sin access key de Web3Forms: el mensaje se manda por WhatsApp.
    if (!cfg.web3formsKey) {
      window.open(waLink(full), "_blank", "noopener");
      status.classList.remove("is-error");
      status.textContent = "Abrí WhatsApp con tu mensaje listo para enviar.";
      return;
    }

    const submit = form.querySelector('[type="submit"]');
    submit.disabled = true;
    status.classList.remove("is-error");
    status.textContent = "Enviando…";
    try {
      const res = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          access_key: cfg.web3formsKey,
          subject: `${cfg.name || "Bazar"}: ${p ? p.name : "mensaje"}`,
          from_name: cfg.name || "Bazar",
          producto: p ? `${p.name} — ${priceText(p.price)}` : "",
          nombre: name,
          contacto: contact,
          message,
          botcheck: form.botcheck.checked,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || data.success === false) throw new Error(data.message || res.status);
      form.reset();
      status.textContent = "¡Listo! Te contesto pronto.";
    } catch (err) {
      status.classList.add("is-error");
      status.textContent = "No se pudo enviar. Intenta de nuevo o escríbeme por WhatsApp.";
    } finally {
      submit.disabled = false;
    }
  });
  }

  bindForm(form, status, () => shop.products.find((x) => x.slug === current));
  const counterForm = document.getElementById("counter-form");
  if (counterForm) bindForm(counterForm, counterForm.querySelector(".note-status"), () => null);

  /* ───── Footer ───── */

  const fwa = document.getElementById("footer-wa");
  fwa.href = waLink(waMessage(null));
  document.getElementById("footer-wa-number").textContent = prettyPhone(cfg.whatsapp);
  const upd = document.getElementById("updated");
  if (shop.updated) {
    upd.dateTime = shop.updated;
    upd.textContent = new Date(shop.updated + "T12:00:00").toLocaleDateString("es-MX", {
      day: "numeric", month: "long", year: "numeric",
    });
  }

  /* ───── Deep link ───── */

  compactQ.addEventListener("change", () => {
    const keep = current;
    if (current) buttons.get(current)?.setAttribute("aria-expanded", "false");
    current = null;
    drawer.classList.remove("is-open");
    drawer.hidden = true;
    drawer.remove();
    renderShelves();
    if (keep) open(keep, { scroll: false, focus: false });
  });

  const fromHash = decodeURIComponent(location.hash.slice(1));
  if (fromHash && buttons.has(fromHash)) open(fromHash, { focus: false });
})();
