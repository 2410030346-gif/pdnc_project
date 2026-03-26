"""Handwriting synthesis helpers.

This starter module provides a simple text-to-image generator that mimics
handwritten output using an italic font when available.
"""

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


def build_synthesis_model():
    """Return a lightweight synthesis descriptor for the starter pipeline."""
    return {"type": "text_renderer", "version": "starter-v1"}


def _get_style_fonts(handwriting_style: str) -> list[str]:
    """Return candidate font names for each handwriting style."""
    styles = {
        "cursive": ["segoesc.ttf", "BRUSHSCI.TTF", "ariali.ttf"],
        "neat": ["calibri.ttf", "segoeui.ttf", "arial.ttf"],
        "marker": ["comicbd.ttf", "comic.ttf", "arialbd.ttf"],
        "mono": ["consola.ttf", "cour.ttf", "lucon.ttf"],
        "signature": ["segoesc.ttf", "BRUSHSCI.TTF", "script.ttf"],
    }
    return styles.get(handwriting_style, styles["cursive"])


def _load_font(font_size: int, handwriting_style: str) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load style-specific font if available, otherwise use default font."""
    candidate_fonts = _get_style_fonts(handwriting_style)
    for font_name in candidate_fonts:
        try:
            return ImageFont.truetype(font_name, font_size)
        except OSError:
            continue
    return ImageFont.load_default()


def _get_style_settings(handwriting_style: str) -> dict[str, object]:
    """Return rendering settings for handwriting style."""
    settings = {
        "cursive": {"scale": 1.0, "ink": (35, 35, 35), "line_space": 1.25},
        "neat": {"scale": 0.85, "ink": (38, 50, 72), "line_space": 1.35},
        "marker": {"scale": 0.95, "ink": (28, 28, 28), "line_space": 1.2},
        "mono": {"scale": 0.82, "ink": (34, 44, 64), "line_space": 1.3},
        "signature": {"scale": 1.05, "ink": (25, 25, 25), "line_space": 1.3},
    }
    return settings.get(handwriting_style, settings["cursive"])


def _paper_base_color(paper_style: str) -> tuple[int, int, int]:
    """Return base paper color by style."""
    if paper_style == "lines":
        paper_style = "ruled"
    palette = {
        "plain": (255, 255, 250),
        "warm": (255, 246, 226),
        "blue": (244, 249, 255),
        "ruled": (252, 252, 252),
        "grid": (252, 252, 252),
        "dots": (252, 252, 252),
    }
    return palette.get(paper_style, palette["plain"])


def _apply_paper_pattern(draw: ImageDraw.ImageDraw, width: int, height: int, paper_style: str) -> None:
    """Draw paper-like background pattern based on selected style."""
    if paper_style == "lines":
        paper_style = "ruled"

    if paper_style == "ruled":
        for y in range(32, height, 24):
            draw.line([(0, y), (width, y)], fill=(216, 227, 247), width=1)
    elif paper_style == "grid":
        for y in range(28, height, 28):
            draw.line([(0, y), (width, y)], fill=(226, 234, 244), width=1)
        for x in range(28, width, 28):
            draw.line([(x, 0), (x, height)], fill=(232, 238, 246), width=1)
    elif paper_style == "dots":
        for y in range(24, height, 24):
            for x in range(24, width, 24):
                draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(206, 214, 226))


def generate_handwriting(
    text: str,
    output_path: Optional[str] = None,
    width: int = 900,
    height: int = 220,
    font_size: int = 56,
    paper_style: str = "plain",
    handwriting_style: str = "cursive",
) -> Image.Image:
    """Render input text into a handwriting-style image.

    Args:
        text: Text to render.
        output_path: Optional file path to save generated image.
        width: Canvas width in pixels.
        height: Canvas height in pixels.
        font_size: Font size for rendering.
        paper_style: Background style (plain, warm, blue, ruled, grid, dots).
        handwriting_style: Handwriting style preset (cursive, neat, marker, mono, signature).

    Returns:
        PIL Image object containing generated text.
    """
    if not text or not text.strip():
        raise ValueError("Input text must not be empty.")

    style_settings = _get_style_settings(handwriting_style)
    scaled_font_size = max(18, int(font_size * float(style_settings["scale"])))
    font = _load_font(scaled_font_size, handwriting_style)
    side_padding = 40
    top_padding = 30
    bottom_padding = 30
    max_text_width = max(120, width - (2 * side_padding))

    # Use a temporary drawing context for line measurement.
    measure_image = Image.new("RGB", (width, 200), color=_paper_base_color(paper_style))
    measure_draw = ImageDraw.Draw(measure_image)

    def wrap_line(line: str) -> list[str]:
        words = line.split()
        if not words:
            return [""]

        wrapped: list[str] = []
        current = words[0]

        for word in words[1:]:
            candidate = f"{current} {word}"
            if measure_draw.textlength(candidate, font=font) <= max_text_width:
                current = candidate
            else:
                wrapped.append(current)
                current = word
        wrapped.append(current)
        return wrapped

    lines: list[str] = []
    for raw_line in text.strip().splitlines():
        lines.extend(wrap_line(raw_line))

    if not lines:
        lines = [text.strip()]

    line_height = int(scaled_font_size * float(style_settings["line_space"]))
    required_height = top_padding + bottom_padding + (line_height * len(lines))
    final_height = max(height, required_height)

    image = Image.new("RGB", (width, final_height), color=_paper_base_color(paper_style))
    draw = ImageDraw.Draw(image)
    _apply_paper_pattern(draw, width, final_height, paper_style)

    y = top_padding
    for line in lines:
        draw.text((side_padding, y), line, fill=style_settings["ink"], font=font)
        y += line_height

    if output_path:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        image.save(out_file)

    return image
