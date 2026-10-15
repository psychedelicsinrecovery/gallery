# The photo assets

Photos live in **album folders**:

```
assets/albums/<album-id>/01-opening-ceremony.jpg
assets/albums/<album-id>/_meta.json   (optional: title, when, place, pixieset, emptyTitle, emptyBody)
```

- Name files with a number prefix to control the order: `01-...`, `02-...`
- The caption comes from the filename: `03-photo-by-maria-r.jpg` becomes "Photo by Maria R."
  (first name + last initial, per the fellowship's anonymity tradition).
- After adding photos, rebuild the manifest from the repo root:

  ```sh
  python3 tools/build_manifest.py
  ```

- Commit, push, and the gallery is live in about a minute (GitHub Actions).
