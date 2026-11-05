# Alvorada brand guide

## Color

| Name | Hex | Use |
| --- | --- | --- |
| Alvorada navy | `#00035D` | Main post background and brand field |
| Warm paper | `#F3EAD7` | Main text on navy |
| White | `#FFFFFF` | Bright accents and the blackletter A |
| Chrome silver | `#C8CBD0` | Reflective metal on the isolated A |
| Cool reflection | `#C6D3ED` | Blue-tinted light within the chrome finish |

Keep navy and warm paper as the main palette. The letter alone uses reflective silver against the navy background.

## Typography

- Display titles: Mekzantine by MEK.txt. The credit appears on the last slide. Its source is [mek.gallery/mektype](https://www.mek.gallery/mektype).
- Book text: EB Garamond. The variable font and its SIL Open Font License are included in `fonts/`. Baskerville is the approved substitute.
- The Typst source uses `MEKZANTINE` for covers and headings, and `EB Garamond` for body copy. Compile with `--font-path fonts` so Typst finds both bundled faces. Python loads the corresponding font files directly.
- Use the display face for titles and headings only. Keep paragraphs, captions, attributions, and the hymn in EB Garamond. Use weight and size for hierarchy, with tracking reserved for short headers and labels.
- Use left alignment for paragraphs and centered alignment for covers, captions, and the hymn ending.

### Current post sizes

The canvas is 1080 × 1080 pt. At a 72 ppi export, the point values below map directly to pixels. The supplied 144 ppi previews are 2160 × 2160 px.

| Element | Size | Notes |
| --- | ---: | --- |
| Cover title | 96 pt maximum | Mekzantine; the Python renderer can reduce size to fit |
| Text-card heading | 84 pt maximum | Mekzantine with tight leading; Python can reduce size to fit |
| Body copy | 36 pt maximum | Left aligned; keep paragraphs brief; the Python renderer can reduce size to fit |
| Cover subtitle | 33 pt | Secondary line |
| Artwork caption | 27 pt | Centered |
| Header and page number | 21 pt | Header uses bold weight and light tracking |
| Kicker | 21 pt | Bold, short attribution or category |
| Chrome hymn | 42 pt | Centered, eight lines, no header or footer |

For new text-led posts, use 36–46 pt body text when the copy allows it. Keep essential information above 28 pt, body lines short, and leading generous.

## Layout

- Keep each post square at 1:1.
- Main text frame inset: 104 pt horizontally and 96 pt vertically.
- Header baseline placement: 72 pt from the top.
- Footer page number: 50 pt from the bottom.
- Main centered header: `movimento alvorada`.
- Leave clear space around the words. Avoid decorative micro-labels and extra footer copy.

## Marks and special treatments

- `brasaoalv.svg` is the source crest. Use the low-opacity `brasaoalv-watermark.png` on occasional text cards.
- `brasaoalv-pixel.png` is an occasional alternate closing mark.
- `alvorada-medieval-a.svg` is the supplied blackletter A traced as a vector, with a restrained grain on its edge. The standard ending places it flush to the bottom and right.
- `alvorada-chrome-a.png` is the Three.js render of the isolated blackletter A in reflective silver on navy. Use it occasionally as an alternate final card.
- The chrome hymn ending uses only the supplied German verse, centered over the isolated letter.
- Use `bg-noise.png` and the dark-blue blur backgrounds sparingly. Keep gradients subtle and preserve text contrast.

## Files and previews

- `alvorada-carousel.typ` is the reusable carousel template.
- `generate_posts.py` renders post sets from JSON examples. Install its Pillow dependency with `python -m pip install -r requirements.txt`.
- `alvorada-specials-preview.typ` assembles occasional effects and ending variations.
- `alvorada-9-grid.png` is the regular preview. `alvorada-specials-9-grid.png` is the separate special-treatment preview.
- `alvorada-chrome-scene.html` and `alvorada-chrome-vendor/` are the editable Three.js scene and local runtime assets.
- Individual post renders are 2160 × 2160 px. The 3 × 3 contact sheets use 640 px cards, 12 px gutters, and a white canvas.

The Python renderer measures every text block, wraps long lines and unbroken words, and reduces type size only within its reserved text area. It refuses to export a card if the copy still cannot fit at the minimum size, and it renders the complete carousel before replacing output files. Shorten or split copy when it reports a fit error.

The last card credits the display typeface with `Mekzantine by MEK.txt`.
