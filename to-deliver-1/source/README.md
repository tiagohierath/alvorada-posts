# Alvorada carousel template

`alvorada-carousel.typ` is a square Typst template for Instagram carousels.

- Canvas: 1080 x 1080 pt, 1:1.
- Background: `#00035d`, sampled from the Alvorada reference.
- Display titles and headings: Mekzantine by MEK.txt. Body text, captions, and the hymn: EB Garamond. The final card credits Mekzantine.
- The EB Garamond variable font and SIL Open Font License are included in `fonts/`.
- Text color: warm paper for strong contrast.
- Header: centered “movimento alvorada”; page numbers only in the footer.
- Artwork: Fra Angelico and Caravaggio, sourced from Wikimedia Commons public-domain reproductions.
- Final card: the supplied blackletter A SVG, aligned flush to the bottom and right at 500 pt. It is a vector trace from the supplied reference with a very light grain on the contour. `closing-chrome-page` is an occasional Three.js rendering of only the chrome A on navy; `closing-hymn-page` pairs it with the centered hymn; `closing-seal-page` is an alternate using the pixelated Alvorada crest.
- One text slide uses the original `brasaoalv.svg` as a subtle, low-opacity watermark. The pixel crest is derived from that SVG.
- Helpers: `title-page`, `text-page`, `image-page`, `closing-page`, `closing-seal-page`, `closing-chrome-page`, and `closing-hymn-page`.
- `alvorada-specials-preview.typ` rebuilds text and artwork cards from reusable helpers and assembles them with the standout effects and alternate endings in a separate 3×3 preview.
- `BRAND-GUIDE.md` documents the palette, type system, spacing, and special treatments.
- `generate_posts.py` is the Python renderer. It reads a JSON post list and writes numbered PNGs, a PDF, and a 3×3 grid.

The final A uses `alvorada-medieval-a.svg`, a white vector trace with transparent background made from the supplied blackletter A reference.

Replace the example pages at the bottom with any sequence of those helpers. Keep each page between `#pagebreak()` calls. Export each page as a square PNG for Instagram.

## Python renderer

```sh
python -m pip install -r requirements.txt
python generate_posts.py examples/regular.json --output-dir build/regular
python generate_posts.py examples/specials.json --output-dir build/specials
```

The Python renderer uses bundled Mekzantine for titles and headings, with EB Garamond for text and captions. Each run creates `slide-01.png` and later slides, `carousel.pdf`, and `grid.png`.

Text is measured with the selected font before it is drawn. Long lines wrap, including unbroken long words, and text blocks reduce their type size to fit a protected area. If copy still cannot fit at the minimum readable size, the generator stops with the slide number and a request to shorten or split the copy. It never silently clips the text. The input file and referenced image assets are checked before rendering starts.
