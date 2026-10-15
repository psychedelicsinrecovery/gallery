#!/usr/bin/env python3
"""Build photos.json by scanning assets/albums/.

Zero dependencies. Run from the repo root:

    python3 tools/build_manifest.py

Conventions
-----------
assets/albums/<album-id>/<files...>   photos, in filename order (use 01-, 02- ... prefixes)
assets/albums/<album-id>/_meta.json   optional per-album overrides, e.g.:
    {
      "title": "The Inaugural PIR(R) Convention",
      "when": "October 8-11, 2026",
      "place": "Denver, Colorado",
      "pixieset": "https://...",
      "emptyTitle": "...", "emptyBody": "..."
    }

Captions: "01-opening-ceremony.jpg" -> caption "opening ceremony".
Credits : "03-photo-by-maria-r.jpg" -> credit "Maria R." (first name + last initial).
JPEG and PNG dimensions are read from the file headers so the grid can reserve space (no reflow).
"""
import json, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALBUMS_DIR = os.path.join(ROOT, "assets", "albums")
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def dimensions(path):
    try:
        with open(path, "rb") as f:
            head = f.read(33)
        if head[:2] == b"\xff\xd8":                      # JPEG: scan for SOF
            with open(path, "rb") as f:
                data = f.read(65536)
            i = 2
            while i < len(data) - 9:
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return w, h
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    i += 2
                else:
                    i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
        elif head[:8] == b"\x89PNG\r\n\x1a\n":            # PNG: IHDR
            w, h = struct.unpack(">II", head[16:24])
            return w, h
    except Exception:
        pass
    return None


def tidy(name):
    s = re.sub(r"^\d+[-_ ]*", "", name)
    s = re.sub(r"\.(jpe?g|png|webp|gif)$", "", s, flags=re.I)
    s = s.replace("_", " ").replace("-", " ").strip()
    return s[0].upper() + s[1:] if s else ""


def credit_of(caption):
    m = re.search(r"photo by ([A-Za-z]+ [A-Za-z])\b", caption, re.I)
    return (m.group(1).title()) if m else None


def main():
    manifest_path = os.path.join(ROOT, "photos.json")
    manifest = {"albums": []}
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest = json.load(f)
    prev = {a.get("id"): a for a in manifest.get("albums", [])}
    albums = []
    if os.path.isdir(ALBUMS_DIR):
        for album_id in sorted(os.listdir(ALBUMS_DIR)):
            d = os.path.join(ALBUMS_DIR, album_id)
            if not os.path.isdir(d):
                continue
            meta = {}
            meta_p = os.path.join(d, "_meta.json")
            if os.path.exists(meta_p):
                with open(meta_p) as f:
                    meta = json.load(f)
            photos = []
            for fn in sorted(os.listdir(d)):
                base, ext = os.path.splitext(fn)
                if ext.lower() not in IMG_EXT:
                    continue
                w, h = dimensions(os.path.join(d, fn)) or (None, None)
                caption = tidy(base)
                credit = credit_of(caption)
                photos.append({
                    "src": f"assets/albums/{album_id}/{fn}",
                    "thumb": f"assets/albums/{album_id}/{fn}",
                    "caption": caption,
                    **({"credit": credit} if credit else {}),
                    **({"w": w, "h": h} if w else {}),
                })
            old = prev.get(album_id, {})
            a = {
                "id": album_id,
                "title": meta.get("title") or old.get("title") or tidy(album_id) or album_id,
                "when": meta.get("when") or old.get("when", ""),
                "place": meta.get("place") or old.get("place", ""),
                "photos": photos,
            }
            for k in ("pixieset", "emptyTitle", "emptyBody"):
                if k in meta:
                    a[k] = meta[k]
            for k, v in old.items():          # keep any hand-written keys not covered above
                a.setdefault(k, v)
            albums.append(a)
    # preserve hand-maintained albums that have no folder yet (e.g. placeholders with pixieset links)
    for aid, a in prev.items():
        if aid not in {x["id"] for x in albums} and a.get("photos") is not None:
            albums.append(a)
    with open(manifest_path, "w") as f:
        json.dump({"albums": albums}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote photos.json with {len(albums)} album(s), "
          f"{sum(len(a['photos']) for a in albums)} photo(s).")


if __name__ == "__main__":
    sys.exit(main())
