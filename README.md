# 🖼️ The PIR® Convention Gallery

The fellowship's own photo gallery for **Psychedelics In Recovery™ – PIR®** — the gatherings,
kept on GitHub. Live at: **https://psychedelicsinrecovery.github.io/gallery/**

A sibling of the [Convention site](https://github.com/psychedelicsinrecovery/convention-astro)
and the [AstroLog](https://github.com/psychedelicsinrecovery/changelog-astro). One night sky,
many desks.

## Why a gallery of our own

Pixieset is lovely for sharing right now — and this is the version the fellowship owns:

- **No platform.** The photos live in this repository; the gallery is a single HTML page.
- **No cost, no expiry.** GitHub Pages serves it free, fast, worldwide — until the day we outgrow GitHub (and what a day that will be).
- **Anonymity-aware.** Captions use first name + last initial, per the fellowship's tradition.
- **Consent first.** Any photo comes down on request to the gallery's trusted servants.

## The photo workflow (for trusted servants and volunteers)

1. Photos arrive in the shared [Drive folder](https://drive.google.com/drive/folders/1zUL1fHkDlWJLKrtHzfToceFoFl-PiTu?usp=sharing)
   (or any way they arrive — WhatsApp, email, a USB stick at a convention).
2. Drop them into `assets/albums/<album-id>/`. Name them with a number prefix so the order is
   right: `01-opening-ceremony.jpg`, `02-...`.
3. Rebuild the manifest (no dependencies, just Python):

   ```sh
   python3 tools/build_manifest.py
   ```

   The manifest (`photos.json`) is what the gallery page reads. Captions come from filenames;
   `03-photo-by-maria-r.jpg` gets the credit "Maria R." automatically.
4. Optional per-album details go in `assets/albums/<album-id>/_meta.json`:

   ```json
   { "title": "The Inaugural PIR® Convention", "when": "October 8-11, 2026", "place": "Denver, Colorado" }
   ```

5. Commit and push. GitHub Actions publishes the gallery in about a minute.

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## The structure

```
index.html      the whole gallery — masonry grid, album filters, lightbox, downloads
photos.json     the manifest the page reads (generated or hand-edited)
assets/         the photographs, in album folders
tools/          build_manifest.py — scans assets/ and writes photos.json
```

## Trademark

Psychedelics In Recovery™ – PIR®. The marks belong to the fellowship.

---

*Built with care for the fellowship by the PIR® Tech Committee's helpers.*
