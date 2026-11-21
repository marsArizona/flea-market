#!/usr/bin/env python3
"""Genera site/data.js y site/img/ a partir de las carpetas de productos.

El estado se toma de data.txt (estado:) o, si está vacío, de la línea
"Estado: ..." en ficha.md.

Uso:  python3 build.py

Edita data.txt (precio, estado, vendido) en cada carpeta y vuelve a correrlo.
"""
import json, os, re, shutil, subprocess, unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

# URL pública del sitio, con / al final (ej. "https://bastians.netlify.app/").
# WhatsApp necesita la URL completa para mostrar la imagen al compartir.
SITE_URL = ""
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
    embed_provenance(img_root)
    set_share_urls()
    print(f"Listo: {len(products)} productos → site/data.js")


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


def embed_provenance(img_root):
    """Marca el origen de cada foto (opcional; solo si la herramienta está instalada)."""
    if not os.path.exists(IMPECCABLE):
        return
    for d, _, files in os.walk(img_root):
        for f in files:
            subprocess.run([IMPECCABLE, "embed-prompt", os.path.join(d, f), "--prompt", ORIGIN],
                           capture_output=True)


if __name__ == "__main__":
    main()
