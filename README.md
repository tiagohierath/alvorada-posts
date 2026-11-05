# Alvorada carousel template

`alvorada-carousel.typ` is a square Typst template for Instagram carousels.

- Canvas: 1080 x 1080 pt, 1:1.
- Background: `#00035d`, sampled from the Alvorada reference.
- Type: EB Garamond. Change `serif` to `Baskerville` if that is the installed face.
- Text color: warm paper for strong contrast.
- Header: centered “movimento alvorada”; page numbers only in the footer.
- Artwork: Fra Angelico and Caravaggio, sourced from Wikimedia Commons public-domain reproductions.
- Final card: the supplied blackletter A SVG, aligned flush to the bottom and right at 500 pt. It is a vector trace from the supplied reference with a very light grain on the contour. `closing-seal-page` is an occasional alternate using the pixelated Alvorada crest.
- One text slide uses the original `brasaoalv.svg` as a subtle, low-opacity watermark. The pixel crest is derived from that SVG.
- Helpers: `title-page`, `text-page`, `image-page`, `closing-page`, and `closing-seal-page`.

The final A uses `alvorada-medieval-a.svg`, a white vector trace with transparent background made from the supplied blackletter A reference.

Replace the example pages at the bottom with any sequence of those helpers. Keep each page between `#pagebreak()` calls. Export each page as a square PNG for Instagram.
