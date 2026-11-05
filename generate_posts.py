#!/usr/bin/env python3
"""Render Alvorada carousel posts with checked, auto-fitted text layout."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
NAVY = "#00035D"
PAPER = "#F3EAD7"
FONT_BOOK = ROOT / "fonts" / "EBGaramond[wght].ttf"
FONT_DISPLAY = ROOT / "fonts" / "MEKZANTINE.ttf"
POST_TYPES = {"cover", "image", "text", "closing-a", "closing-seal", "closing-chrome", "hymn"}


def font(size: int, bold: bool = False, display: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_DISPLAY if display else FONT_BOOK
    face = ImageFont.truetype(str(path), max(1, int(size)))
    if display:
        return face
    try:
        face.set_variation_by_name("Bold" if bold else "Regular")
    except (AttributeError, OSError):
        pass
    return face


def fitted(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGBA"), size, method=Image.Resampling.LANCZOS)


def load_asset(base: Path, name: str) -> Image.Image:
    path = (base / name).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Asset not found: {path}")
    try:
        with Image.open(path) as source:
            source.load()
            return source.convert("RGBA")
    except (OSError, ValueError) as exc:
        raise ValueError(f"Could not read image asset {path}: {exc}") from exc


def _split_long_word(word: str, draw: ImageDraw.ImageDraw,
                     face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Break an unspaced token at character boundaries instead of clipping it."""
    # Measure each glyph once and pack conservatively. Measuring every growing prefix
    # makes long URLs/identifiers quadratic and can stall on pasted text.
    chunks: list[str] = []
    chunk: list[str] = []
    advance = 0.0
    safe_width = max(1, width * 0.88)
    char_widths: dict[str, float] = {}
    for char in word:
        if char not in char_widths:
            char_widths[char] = draw.textlength(char, font=face)
        char_width = char_widths[char]
        if chunk and advance + char_width > safe_width:
            chunks.append("".join(chunk))
            chunk = [char]
            advance = char_width
        else:
            chunk.append(char)
            advance += char_width
    if chunk:
        chunks.append("".join(chunk))

    # Verify actual shaped widths and split any chunk whose kerning exceeds the margin.
    safe_chunks: list[str] = []
    for piece in chunks:
        while piece and draw.textlength(piece, font=face) > width:
            low, high = 1, len(piece)
            while low < high:
                middle = (low + high) // 2
                if draw.textlength(piece[:middle], font=face) <= width:
                    low = middle + 1
                else:
                    high = middle
            split_at = max(1, low - 1)
            safe_chunks.append(piece[:split_at])
            piece = piece[split_at:]
        if piece:
            safe_chunks.append(piece)
    return safe_chunks


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont,
         width: int) -> list[str]:
    """Wrap paragraphs to a measured width, including unusually long words."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = ""
        for word in words:
            pieces = [word] if draw.textlength(word, font=face) <= width else \
                _split_long_word(word, draw, face, width)
            for piece in pieces:
                candidate = f"{line} {piece}".strip()
                if line and draw.textlength(candidate, font=face) > width:
                    lines.append(line)
                    line = piece
                else:
                    line = candidate
        lines.append(line)
    return lines


def block_height(face: ImageFont.FreeTypeFont, lines: list[str], leading: int) -> int:
    if not lines:
        return 0
    line_heights = []
    for line in lines:
        box = face.getbbox(line or "Ag", anchor="lt")
        line_heights.append(max(1, box[3] - box[1]))
    line_advance = max(max(1, leading), *line_heights)
    return max(line_heights) + max(0, len(lines) - 1) * line_advance


def fit_block(draw: ImageDraw.ImageDraw, text: str, width: int, height: int,
              max_size: int, min_size: int, leading_ratio: float = 1.2,
              bold: bool = False) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    """Choose the largest font size whose wrapped block fits its frame."""
    largest = max(1, int(max_size))
    smallest = max(1, min(int(min_size), largest))
    for size in range(largest, smallest - 1, -1):
        face = font(size, bold)
        lines = wrap(draw, text, face, width)
        leading = max(1, round(size * leading_ratio))
        if all(draw.textlength(line, font=face) <= width + 0.5 for line in lines) \
                and block_height(face, lines, leading) <= height:
            return face, lines, leading
    raise ValueError(
        f"Text cannot fit its frame ({width} × {height}px) at the minimum font size "
        f"({min_size}px). Shorten the copy or give it a dedicated slide."
    )


def draw_lines(draw: ImageDraw.ImageDraw, lines: list[str], face: ImageFont.FreeTypeFont,
               x: int, y: int, width: int, leading: int, fill: str,
               align: str = "left") -> int:
    line_heights = []
    for line in lines:
        box = face.getbbox(line or "Ag", anchor="lt")
        line_heights.append(max(1, box[3] - box[1]))
    line_advance = max([max(1, leading), *line_heights])
    for index, line in enumerate(lines):
        line_width = draw.textlength(line, font=face)
        line_x = x if align == "left" else round(x + (width - line_width) / 2)
        draw.text((line_x, y), line, font=face, fill=fill, anchor="lt")
        if index < len(lines) - 1:
            y += line_advance
    return y + max(line_heights, default=0)


def background(slide: dict[str, Any], base: Path, size: int) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), NAVY)
    bg = slide.get("background")
    if bg:
        layer = fitted(load_asset(base, str(bg)), (size, size))
        strength = float(slide.get("background_strength", 0.58))
        canvas = Image.blend(canvas, layer, strength)
    return canvas


def tracked(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont,
            y: int, center: int, fill: str, spacing: int) -> None:
    width = sum(draw.textlength(char, font=face) for char in text)
    width += max(0, len(text) - 1) * spacing
    x = center - width / 2
    for char in text:
        draw.text((round(x), y), char, font=face, fill=fill, anchor="lt")
        x += draw.textlength(char, font=face) + spacing


def header_footer(canvas: Image.Image, draw: ImageDraw.ImageDraw, number: Any,
                  scale: float, on_left: bool = False) -> None:
    header_face, header_lines, header_leading = fit_block(
        draw, "movimento alvorada", round(800 * scale), round(45 * scale),
        round(21 * scale), max(12, round(16 * scale)), 1.1, True)
    header_width = draw.textlength(header_lines[0], font=header_face)
    # Keep the centered masthead clear of both page edges even at small exports.
    draw.text(((canvas.width - header_width) // 2, round(64 * scale)),
              header_lines[0], font=header_face, fill=PAPER, anchor="lt")
    if number is not None:
        x = round((104 if on_left else 976) * scale)
        anchor = "ls" if on_left else "rs"
        footer_face = font(max(12, round(21 * scale)))
        draw.text((x, round(1030 * scale)), str(number), font=footer_face,
                  fill=PAPER, anchor=anchor)


def add_font_credit(image: Image.Image) -> None:
    """Credit the display face on the final card, clear of the page number."""
    scale = image.width / 1080
    draw = ImageDraw.Draw(image)
    minimum = max(8, round(14 * scale))
    face, lines, leading = fit_block(
        draw, "Mekzantine by MEK.txt", round(330 * scale), round(30 * scale),
        max(minimum, round(18 * scale)), minimum, 1.05)
    draw_lines(draw, lines, face, round(200 * scale), round(1008 * scale),
               round(330 * scale), leading, PAPER)


def _render_cover(canvas: Image.Image, draw: ImageDraw.ImageDraw,
                  slide: dict[str, Any], scale: float) -> None:
    title = str(slide["title"])
    subtitle = str(slide.get("subtitle", ""))
    width = round(880 * scale)
    max_size, min_size = round(96 * scale), max(24, round(34 * scale))

    def measure(size: int) -> tuple[bool, tuple[Any, ...]]:
        title_face = font(size, display=True)
        title_lines = wrap(draw, title, title_face, width)
        title_leading = round(size * 1.04)
        title_height = block_height(title_face, title_lines, title_leading)
        if subtitle:
            sub_size = max(round(20 * scale), round(33 * scale * size / max_size))
            sub_face = font(sub_size)
            sub_lines = wrap(draw, subtitle, sub_face, width)
            sub_leading = round(sub_size * 1.2)
            sub_height = block_height(sub_face, sub_lines, sub_leading)
        else:
            sub_face, sub_lines, sub_leading, sub_height = None, [], 0, 0
        gap = round(24 * scale) if subtitle else 0
        fits = (max((draw.textlength(line, font=title_face) for line in title_lines), default=0) <= width
                and (not subtitle or max((draw.textlength(line, font=sub_face) for line in sub_lines), default=0) <= width)
                and title_height + gap + sub_height <= round(480 * scale))
        return fits, (title_face, title_lines, title_leading, title_height,
                      sub_face, sub_lines, sub_leading, sub_height, gap)

    best: tuple[Any, ...] | None = None
    low, high = min_size, max_size
    while low <= high:
        size = (low + high) // 2
        fits, layout = measure(size)
        if fits:
            best = layout
            low = size + 1
        else:
            high = size - 1
    if best is None:
        raise ValueError("Cover title and subtitle cannot fit safely on one post.")

    (title_face, title_lines, title_leading, title_height,
     sub_face, sub_lines, sub_leading, sub_height, gap) = best
    y = round(520 * scale - (title_height + gap + sub_height) / 2)
    draw_lines(draw, title_lines, title_face, round(100 * scale), y, width,
               title_leading, PAPER, "center")
    if subtitle and sub_face:
        draw_lines(draw, sub_lines, sub_face, round(100 * scale),
                   y + title_height + gap, width, sub_leading, PAPER, "center")


def _render_text_card(canvas: Image.Image, draw: ImageDraw.ImageDraw,
                      slide: dict[str, Any], scale: float) -> None:
    x = round(104 * scale)
    has_seal = bool(slide.get("seal"))
    width = round((650 if has_seal else 872) * scale)
    top = round(160 * scale)
    bottom = round((930 if not has_seal else 900) * scale)
    available_height = bottom - top
    kicker = str(slide.get("kicker", ""))
    heading = str(slide["heading"])
    body = str(slide.get("body", ""))

    def measure(factor_step: int) -> tuple[bool, tuple[Any, ...]]:
        factor = factor_step / 100
        kicker_face = font(max(12, round(21 * scale * factor)), True) if kicker else None
        kicker_lines = wrap(draw, kicker, kicker_face, width) if kicker_face else []
        kicker_leading = max(1, round(25 * scale * factor))
        kicker_height = block_height(kicker_face, kicker_lines, kicker_leading) if kicker_face else 0

        heading_face = font(max(18, round(84 * scale * factor)), display=True)
        heading_lines = wrap(draw, heading, heading_face, width)
        heading_leading = max(1, round(88 * scale * factor))
        heading_height = block_height(heading_face, heading_lines, heading_leading)

        body_face = font(max(round(26 * scale), round(36 * scale * factor))) if body else None
        body_lines = wrap(draw, body, body_face, width) if body_face else []
        body_leading = max(1, round(47 * scale * factor))
        body_height = block_height(body_face, body_lines, body_leading) if body_face else 0

        gap_kicker = round(26 * scale * factor) if kicker and heading_lines else 0
        gap_body = round(30 * scale * factor) if body else 0
        total = kicker_height + gap_kicker + heading_height + gap_body + body_height
        widths_fit = all(draw.textlength(line, font=kicker_face) <= width + 0.5
                         for line in kicker_lines) if kicker_face else True
        widths_fit = widths_fit and all(draw.textlength(line, font=heading_face) <= width + 0.5
                                        for line in heading_lines)
        widths_fit = widths_fit and (all(draw.textlength(line, font=body_face) <= width + 0.5
                                         for line in body_lines) if body_face else True)
        layout = (total, kicker_face, kicker_lines, kicker_leading, heading_face,
                  heading_lines, heading_leading, body_face, body_lines,
                  body_leading, gap_kicker, gap_body)
        return total <= available_height and widths_fit, layout

    best: tuple[Any, ...] | None = None
    low, high = 40, 100
    while low <= high:
        factor_step = (low + high) // 2
        fits, layout = measure(factor_step)
        if fits:
            best = layout
            low = factor_step + 1
        else:
            high = factor_step - 1

    if best is not None:
        (total, kicker_face, kicker_lines, kicker_leading, heading_face,
         heading_lines, heading_leading, body_face, body_lines,
         body_leading, gap_kicker, gap_body) = best
        y = top + (available_height - total) // 2
        if kicker_face:
            y = draw_lines(draw, kicker_lines, kicker_face, x, y, width,
                           kicker_leading, PAPER)
            y += gap_kicker
        y = draw_lines(draw, heading_lines, heading_face, x, y, width,
                       heading_leading, PAPER)
        if body_face:
            y += gap_body
            draw_lines(draw, body_lines, body_face, x, y, width,
                       body_leading, PAPER)
        return

    raise ValueError(
        "Text card content cannot fit safely. Shorten its heading or body, remove the "
        "watermark, or split the copy across posts."
    )


def _render_hymn(canvas: Image.Image, draw: ImageDraw.ImageDraw,
                 slide: dict[str, Any], scale: float) -> Image.Image:
    verse = str(slide.get("text", ""))
    panel_size = (round(828 * scale), round(680 * scale))
    panel = Image.new("RGBA", panel_size, (0, 3, 93, 158))
    panel_x = (canvas.width - panel.width) // 2
    panel_y = (canvas.height - panel.height) // 2
    canvas.alpha_composite(panel, (panel_x, panel_y))
    draw = ImageDraw.Draw(canvas)
    frame_x = panel_x + round(42 * scale)
    frame_y = panel_y + round(38 * scale)
    frame_width = panel.width - round(84 * scale)
    frame_height = panel.height - round(76 * scale)
    face, lines, leading = fit_block(
        draw, verse, frame_width, frame_height, round(42 * scale),
        max(18, round(24 * scale)), 1.2)
    height = block_height(face, lines, leading)
    y = frame_y + (frame_height - height) // 2
    draw_lines(draw, lines, face, frame_x, y, frame_width, leading, PAPER, "center")
    return canvas


def validate_config(config: Any, base: Path, size: int) -> list[dict[str, Any]]:
    if not isinstance(config, dict) or not isinstance(config.get("posts"), list) or not config["posts"]:
        raise ValueError("Input JSON must contain a non-empty 'posts' array.")
    if size < 512:
        raise ValueError("--size must be at least 512 pixels for legible typography.")
    posts = config["posts"]
    for index, slide in enumerate(posts, 1):
        label = f"Slide {index}"
        if not isinstance(slide, dict):
            raise ValueError(f"{label} must be a JSON object.")
        kind = slide.get("type")
        if kind not in POST_TYPES:
            raise ValueError(f"{label} has unknown type {kind!r}.")
        required_text = {"cover": "title", "text": "heading"}
        if kind in required_text and not str(slide.get(required_text[kind], "")).strip():
            raise ValueError(f"{label} ({kind}) needs a non-empty '{required_text[kind]}'.")
        if kind == "image" and not slide.get("image"):
            raise ValueError(f"{label} (image) needs an 'image' asset path.")
        for key in ("background", "image", "seal"):
            if slide.get(key):
                load_asset(base, str(slide[key]))
        if kind == "closing-a":
            load_asset(base, "alvorada-medieval-a.png")
        if kind == "closing-seal":
            load_asset(base, "brasaoalv-pixel.png")
        if kind in {"closing-chrome", "hymn"}:
            load_asset(base, "alvorada-chrome-a.png")
        if kind == "hymn" and not str(slide.get("text", "")).strip():
            raise ValueError(f"{label} (hymn) needs non-empty 'text'.")
        if "background_strength" in slide:
            try:
                strength = float(slide["background_strength"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{label} background_strength must be between 0 and 1.") from exc
            if not 0 <= strength <= 1:
                raise ValueError(f"{label} background_strength must be between 0 and 1.")
    return posts


def render_one(slide: dict[str, Any], base: Path, size: int) -> Image.Image:
    scale = size / 1080
    canvas = background(slide, base, size)
    draw = ImageDraw.Draw(canvas)
    kind = slide["type"]
    number = slide.get("number")

    if kind == "cover":
        _render_cover(canvas, draw, slide, scale)
        header_footer(canvas, draw, number, scale)

    elif kind == "image":
        art = fitted(load_asset(base, str(slide["image"])),
                     (round(908 * scale), round(800 * scale)))
        canvas.alpha_composite(art, (round(86 * scale), round(128 * scale)))
        caption = str(slide.get("caption", ""))
        if caption:
            face, lines, leading = fit_block(
                draw, caption, round(760 * scale), round(52 * scale),
                round(27 * scale), max(16, round(19 * scale)), 1.15)
            draw_lines(draw, lines, face, round(160 * scale), round(953 * scale),
                       round(760 * scale), leading, PAPER, "center")
        header_footer(canvas, draw, number, scale)

    elif kind == "text":
        _render_text_card(canvas, draw, slide, scale)
        if slide.get("seal"):
            seal = load_asset(base, str(slide["seal"]))
            max_edge = round(220 * scale)
            seal.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
            margin = round(76 * scale)
            canvas.alpha_composite(seal, (size - seal.width - margin,
                                          size - seal.height - margin))
        header_footer(canvas, draw, number, scale)

    elif kind == "closing-a":
        letter = load_asset(base, "alvorada-medieval-a.png")
        width = round(500 * scale)
        height = round(width * letter.height / letter.width)
        letter = letter.resize((width, height), Image.Resampling.LANCZOS)
        canvas.alpha_composite(letter, (size - width, size - height))
        header_footer(canvas, draw, number, scale, on_left=True)

    elif kind == "closing-seal":
        seal = load_asset(base, "brasaoalv-pixel.png")
        width = round(440 * scale)
        seal = seal.resize((width, width), Image.Resampling.NEAREST)
        canvas.alpha_composite(seal, (size - width, size - width))
        header_footer(canvas, draw, number, scale, on_left=True)

    elif kind in {"closing-chrome", "hymn"}:
        canvas = fitted(load_asset(base, "alvorada-chrome-a.png"), (size, size))
        draw = ImageDraw.Draw(canvas)
        if kind == "closing-chrome":
            header_footer(canvas, draw, number, scale, on_left=True)
        else:
            canvas = _render_hymn(canvas, draw, slide, scale)

    return canvas.convert("RGB")


def contact_sheet(images: list[Image.Image], path: Path) -> None:
    card, gutter, columns = 640, 12, 3
    rows = math.ceil(len(images) / columns)
    sheet = Image.new("RGB", (columns * (card + 2 * gutter), rows * (card + 2 * gutter)), "white")
    for index, image in enumerate(images):
        thumb = image.resize((card, card), Image.Resampling.LANCZOS)
        x = gutter + (index % columns) * (card + 2 * gutter)
        y = gutter + (index // columns) * (card + 2 * gutter)
        sheet.paste(thumb, (x, y))
    sheet.save(path, compress_level=2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON file containing a posts array")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--size", type=int, default=2160, help="Output edge in pixels, default 2160")
    args = parser.parse_args()

    try:
        config_path = args.input.resolve()
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("Input JSON must be an object containing a 'posts' array.")
        base = (config_path.parent / config.get("asset_root", "..")).resolve()
        posts = validate_config(config, base, args.size)
        if not FONT_BOOK.is_file():
            raise FileNotFoundError(f"Bundled EB Garamond font not found: {FONT_BOOK}")
        if not FONT_DISPLAY.is_file():
            raise FileNotFoundError(f"Bundled Mekzantine display font not found: {FONT_DISPLAY}")

        out = (args.output_dir or Path("build") / config_path.stem).resolve()
        # Render the whole set before writing files so a later bad slide never leaves a
        # half-updated carousel in the destination folder.
        images: list[Image.Image] = []
        for index, slide in enumerate(posts, 1):
            try:
                image = render_one(slide, base, args.size)
            except (ValueError, OSError) as exc:
                raise ValueError(f"Slide {index} ({slide['type']}): {exc}") from exc
            images.append(image)

        add_font_credit(images[-1])
        out.mkdir(parents=True, exist_ok=True)

        for index, image in enumerate(images, 1):
            image.save(out / f"slide-{index:02}.png", compress_level=2)
        contact_sheet(images, out / "grid.png")
        images[0].save(out / "carousel.pdf", "PDF", save_all=True,
                       append_images=images[1:], resolution=args.size / 15)
        print(f"Rendered {len(images)} posts to {out}")
        return 0
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"alvorada-posts: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
