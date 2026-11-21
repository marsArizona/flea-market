#!/usr/bin/env python3
"""Genera site/data.js y site/img/ a partir de las carpetas de productos.

El estado se toma de data.txt (estado:) o, si está vacío, de la línea
"Estado: ..." en ficha.md.

Uso:  python3 build.py

Edita data.txt (precio, estado, vendido) en cada carpeta y vuelve a correrlo.
"""
import html, json, os, re, shutil, subprocess, tempfile, unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

# URL pública del sitio, con / al final (ej. "https://bastians.netlify.app/").
# WhatsApp necesita la URL completa para mostrar la imagen al compartir.
SITE_URL = "https://bastianfleamarket.netlify.app/"
SITE = os.path.join(ROOT, "site")

# Repisas en orden de aparición.
SHELVES = [
    {"id": "tocar",    "kanji": "弾", "label": "Para tocar"},
    {"id": "crear",    "kanji": "作", "label": "Para crear"},
    {"id": "grabar",   "kanji": "録", "label": "Para grabar"},
    {"id": "escuchar", "kanji": "聴", "label": "Para escuchar"},
]

# carpeta -> repisa, marca, modelo corto, foto principal (prefijo), fotos a excluir (prefijos)
CATALOG = {
    "gretsch bass":       ("tocar",    "Gretsch",   "Junior Jet Bass II", "B3AE5A6C", ["AC5260D9"]),
    "orange bass":        ("tocar",    "Orange",    "Crush Bass 100",     "F2266BED", []),
    "boss pedalera":      ("tocar",    "Boss",      "ME-80",              "7ED557FA", []),
    "akai mpc":           ("crear",    "Akai",      "MPC One",            "8DEB2628", []),
    "beringer td 3":      ("crear",    "Behringer", "TD-3",               "DE6F70BE", []),
    "tascam model 12":    ("grabar",   "Tascam",    "Model 12",           "E1903C04", []),
    "tascam interfaz":    ("grabar",   "Tascam",    "US-2x2HR",           "FF48D32F", []),
    "dyson headphones":   ("escuchar", "Dyson",     "Zone",               "747FD38A", []),
    "meters headphone":   ("escuchar", "Meters",    "OV-1-B Connect",     "DBBE6705", []),
    "creative gigablast": ("escuchar", "Creative",  "GigaWorks T40 II",   "065E28D5", []),
}

YES = {"si", "sí", "yes", "true", "1", "vendido", "x"}


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def read_data(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip().lower()] = v.strip()
    return out


def read_ficha(path):
    specs, blurb, estado = [], "", ""
    if not os.path.exists(path):
        return specs, blurb, estado
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) == 2 and not set(cells[0]) <= set("-: ") and cells[0] != "Característica":
                    specs.append(cells)
            elif line.lower().startswith("estado:"):
                estado = line.split(":", 1)[1].strip()
            elif line and not line.startswith(("#", "**")):
                blurb = line
    return specs, blurb, estado


def dims(path):
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                       capture_output=True, text=True).stdout
    w = int(re.search(r"pixelWidth: (\d+)", r).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", r).group(1))
    return w, h


def price(v):
    digits = re.sub(r"[^\d]", "", v or "")
    return int(digits) if digits else None


def main():
    img_root = os.path.join(SITE, "img")
    shutil.rmtree(img_root, ignore_errors=True)
    products = []
    for folder, (shelf, brand, model, main_prefix, exclude) in CATALOG.items():
        src = os.path.join(ROOT, folder)
        if not os.path.isdir(src):
            print(f"  ! falta la carpeta: {folder}")
            continue
        data = read_data(os.path.join(src, "data.txt"))
        specs, blurb, ficha_estado = read_ficha(os.path.join(src, "ficha.md"))
        slug = slugify(f"{brand} {model}")
        photos = sorted(p for p in os.listdir(src)
                        if p.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
                        and not any(p.startswith(x) for x in exclude))
        photos.sort(key=lambda p: not p.startswith(main_prefix))
        dest = os.path.join(img_root, slug)
        os.makedirs(dest, exist_ok=True)
        pics = []
        for i, p in enumerate(photos, 1):
            ext = os.path.splitext(p)[1].lower().replace("jpeg", "jpg")
            name = f"{i}{ext}"
            shutil.copy2(os.path.join(src, p), os.path.join(dest, name))
            w, h = dims(os.path.join(dest, name))
            pics.append({"src": f"img/{slug}/{name}", "w": w, "h": h})
        products.append({
            "slug": slug,
            "shelf": shelf,
            "brand": brand,
            "model": model,
            "name": data.get("nombre") or f"{brand} {model}",
            "price": price(data.get("precio")),
            "condition": data.get("estado") or ficha_estado,
            "sold": data.get("vendido", "").strip().lower() in YES,
            "specs": specs,
            "blurb": blurb,
            "photos": pics,
        })
        print(f"  ✓ {slug:24s} ${products[-1]['price'] or '—'}  {len(pics)} fotos"
              + ("  VENDIDO" if products[-1]["sold"] else ""))
    payload = {"updated": date.today().isoformat(), "shelves": SHELVES, "products": products}
    with open(os.path.join(SITE, "data.js"), "w", encoding="utf-8") as f:
        f.write("// Generado por build.py — no editar a mano.\nwindow.SHOP = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")
    write_share_cards(products)
    write_product_pages(products)
    embed_provenance(img_root, ORIGIN)
    embed_provenance(os.path.join(SITE, "share"), CARD_ORIGIN)
    set_share_urls()
    print(f"Listo: {len(products)} productos → site/data.js")


def write_share_cards(products):
    """Imagen 1200x630 por producto (site/share/<slug>.jpg) a partir de tools/share-card.html.
    Requiere la herramienta de capturas; si no está, se usa la foto principal."""
    out = os.path.join(SITE, "share")
    shutil.rmtree(out, ignore_errors=True)
    if not os.path.exists(IMPECCABLE):
        print("  ! sin herramienta de capturas: las páginas usarán la foto principal")
        return
    os.makedirs(out)
    tpl = "file://" + os.path.join(ROOT, "tools", "share-card.html")
    with tempfile.TemporaryDirectory() as tmp:
        for p in products:
            d = os.path.join(tmp, p["slug"])
            subprocess.run([IMPECCABLE, "shot", f"{tpl}?slug={p['slug']}", "--viewport", "1200x630", "--out", d],
                           capture_output=True)
            png = os.path.join(d, "1200x630.png")
            if os.path.exists(png):
                subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", png,
                                "--out", os.path.join(out, p["slug"] + ".jpg")], capture_output=True)
    print(f"  ✓ {len(os.listdir(out))} imágenes para compartir")


def money(n):
    return "Pregunta" if n is None else "${:,}".format(n)


def write_product_pages(products):
    """site/p/<slug>/index.html: página ligera con la vista previa del producto que redirige al cajón."""
    root = os.path.join(SITE, "p")
    shutil.rmtree(root, ignore_errors=True)
    base = SITE_URL.rstrip("/") + "/" if SITE_URL else "../../"
    for p in products:
        slug = p["slug"]
        title = f"{p['brand']} {p['model']} · {money(p['price'])} MXN" + (" · VENDIDO" if p["sold"] else "")
        desc = p["blurb"]
        if p["sold"]:
            desc = "Ya se vendió. " + desc
        elif p["condition"]:
            desc = f"Estado: {p['condition'].rstrip('.')}. {desc}"
        if len(desc) > 200:
            desc = desc[:197].rsplit(" ", 1)[0] + "…"
        card = os.path.join(SITE, "share", slug + ".jpg")
        if os.path.exists(card):
            image, w, h = f"share/{slug}.jpg", 1200, 630
        else:
            ph = p["photos"][0]
            image, w, h = ph["src"], ph["w"], ph["h"]
        page_url = f"{base}p/{slug}/" if SITE_URL else ""
        target = f"../../#{slug}"
        e = lambda v: html.escape(str(v), quote=True)
        doc = f"""<!doctype html>
<html lang="es-MX">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} — Bastians Flea Market</title>
  <meta name="description" content="{e(desc)}">
  <meta property="og:type" content="product">
  <meta property="og:locale" content="es_MX">
  <meta property="og:site_name" content="Bastians Flea Market">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{e(page_url)}">
  <meta property="og:image" content="{e(base + image)}">
  <meta property="og:image:width" content="{w}">
  <meta property="og:image:height" content="{h}">
  <meta property="og:image:alt" content="{e(p['name'])}">
  <meta property="product:price:amount" content="{p['price'] or ''}">
  <meta property="product:price:currency" content="MXN">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="robots" content="noindex, follow">
  <meta http-equiv="refresh" content="0; url={e(target)}">
  <link rel="canonical" href="{e((base if SITE_URL else '../../') + '#' + slug)}">
  <script>location.replace({json.dumps(target)});</script>
</head>
<body style="background:#cdcac2;color:#151514;font:16px system-ui,sans-serif;padding:24px">
  <p><a href="{e(target)}" style="color:inherit">Ver {e(p['name'])} en Bastians Flea Market</a></p>
</body>
</html>
"""
        os.makedirs(os.path.join(root, slug), exist_ok=True)
        with open(os.path.join(root, slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(doc)
    print(f"  ✓ {len(products)} páginas para compartir en site/p/")


def set_share_urls():
    """Escribe og:url y og:image con la URL completa en index.html."""
    path = os.path.join(SITE, "index.html")
    with open(path, encoding="utf-8") as f:
        html = f.read()
    base = SITE_URL.rstrip("/") + "/" if SITE_URL else ""
    html = re.sub(r'(<meta property="og:url" content=")[^"]*(")', r"\g<1>" + base + r"\g<2>", html)
    html = re.sub(r'(<meta property="og:image" content=")[^"]*(")', r"\g<1>" + base + r"og.jpg\g<2>", html)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    if not SITE_URL:
        print("  ! SITE_URL vacío: la imagen al compartir no saldrá en WhatsApp hasta que lo llenes.")


IMPECCABLE = os.path.expanduser("~/.claude/skills/impeccable/scripts/impeccable")
ORIGIN = ("Origin: owner's own photo of the actual unit for sale, taken in the owner's studio; "
          "copied unmodified from the product folder by build.py. Not generated.")


CARD_ORIGIN = ("Origin: share card rendered by build.py from tools/share-card.html (site CSS + the owner's own "
               "product photo), screenshotted at 1200x630 and converted to JPEG. Not AI-generated.")


def embed_provenance(img_root, origin):
    """Marca el origen de cada foto (opcional; solo si la herramienta está instalada)."""
    if not os.path.exists(IMPECCABLE):
        return
    for d, _, files in os.walk(img_root):
        for f in files:
            subprocess.run([IMPECCABLE, "embed-prompt", os.path.join(d, f), "--prompt", origin],
                           capture_output=True)


if __name__ == "__main__":
    main()
