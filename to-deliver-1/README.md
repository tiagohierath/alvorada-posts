# Alvorada carousel handoff

This folder contains the current source package, ready-to-share exports, and preview sheets for the Alvorada Instagram carousel system.

## Render posts with Python

From this folder, install Pillow and render either example:

```sh
python -m pip install -r source/requirements.txt
python source/generate_posts.py source/examples/regular.json --output-dir python/regular --size 2160
python source/generate_posts.py source/examples/specials.json --output-dir python/specials --size 2160
```

Each run writes square PNG slides, a PDF, and a 3×3 contact sheet. Mekzantine is used for display titles and headings. EB Garamond is used for body copy, captions, and the hymn. The final rendered slide receives the Mekzantine credit. The renderer measures text, wraps long lines and long words, and fits copy within its frame. It stops with a slide-specific error if the copy cannot fit at the minimum size, before replacing any output files.

## Folder map

- `source/` contains the Python generator, Typst templates, JSON examples, bundled fonts and notices, all referenced image assets, and the local Three.js scene and runtime.
- `previews/` contains the regular 3×3 preview and the separate special-treatments 3×3 preview.
- `python/` contains the prepared Python-generated slides, PDFs, and contact sheets.
- `BRAND-GUIDE.md` documents the type system, palette, spacing, and special treatments.

The example JSON files set `asset_root` to `..`. Because they live in `source/examples/`, that resolves to `source/`, where all example assets are included.

## Typst

From `source/`, compile with the bundled fonts available to Typst:

```sh
mkdir -p build
typst compile --font-path fonts --ppi 144 --format png alvorada-carousel.typ build/alvorada-slide-{p}.png
typst compile --font-path fonts --format pdf alvorada-specials-preview.typ build/alvorada-specials.pdf
```

The specials template rebuilds text and artwork cards from the current helpers, then adds the closing A, crest, chrome letter, and hymn assets.

## Font credit and licenses

EB Garamond is bundled with its SIL Open Font License in `source/fonts/OFL.txt`. Mekzantine is credited on the final post as `Mekzantine by MEK.txt`; its source and conversion note are in `source/fonts/MEKZANTINE-CREDIT.md`. The Mekzantine font files are included for local use by both the Python and Typst templates.
