#!/usr/bin/env python3
"""Draw the Spotlight @crisxai5 card (1080x1350) and save it as card.png
in the same directory as this script. Pillow only; DejaVu Sans with a
fallback to PIL's built-in default font."""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1350

NAVY_TOP = (6, 12, 32)
NAVY_BOTTOM = (18, 42, 84)
CYAN = (34, 211, 238)
WHITE = (255, 255, 255)
MUTED = (148, 168, 198)
GREEN = (46, 204, 113)
MAGENTA = (219, 39, 119)


def load_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = os.path.join("/usr/share/fonts/truetype/dejavu", name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default(size=size)


def gradient_background():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        r = round(NAVY_TOP[0] + (NAVY_BOTTOM[0] - NAVY_TOP[0]) * t)
        g = round(NAVY_TOP[1] + (NAVY_BOTTOM[1] - NAVY_TOP[1]) * t)
        b = round(NAVY_TOP[2] + (NAVY_BOTTOM[2] - NAVY_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img


def draw_grid(base):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(0, W + 1, 90):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H + 1, 90):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)
    base.alpha_composite(overlay)


def draw_chart_corner(base):
    # Faint thin cyan rising line, tucked in the top-right corner only.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    points = [
        (815, 150), (845, 138), (870, 142), (900, 118),
        (925, 122), (955, 96), (980, 100), (1010, 66),
    ]
    d.line(points, fill=(34, 211, 238, 70), width=3, joint="curve")
    for x, y in points:
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(34, 211, 238, 70))
    base.alpha_composite(overlay)


def centered_text(draw, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=font, fill=fill)
    return tw


def main():
    img = gradient_background().convert("RGBA")
    draw_grid(img)
    draw_chart_corner(img)
    draw = ImageDraw.Draw(img)

    eyebrow_font = load_font(True, 27)
    headline_font = load_font(True, 86)
    handle_font = load_font(True, 62)
    body_font = load_font(False, 34)
    title_font = load_font(True, 40)
    sub_font = load_font(False, 30)
    pill_font = load_font(True, 44)

    # Eyebrow, top left.
    draw.text((80, 64), "S P O T L I G H T   \u2022   A I  \u00d7  C R Y P T O",
              font=eyebrow_font, fill=CYAN + (255,))

    # Headline, two lines.
    draw.text((80, 170), "Your feed needs", font=headline_font, fill=WHITE + (255,))
    draw.text((80, 268), "more signal.", font=headline_font, fill=WHITE + (255,))

    # Handle banner: rounded rect, cyan outline, translucent cyan fill.
    banner = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(banner)
    bd.rounded_rectangle([80, 420, 1000, 530], radius=24,
                         fill=(34, 211, 238, 28), outline=CYAN + (255,), width=3)
    img.alpha_composite(banner)
    draw = ImageDraw.Draw(img)
    centered_text(draw, 440, "@crisxai5", handle_font, CYAN + (255,))

    # Supporting lines.
    draw.text((80, 578), "The sharpest voice in AI & crypto \u2014",
              font=body_font, fill=MUTED + (255,))
    draw.text((80, 626), "practical insights, no noise.",
              font=body_font, fill=MUTED + (255,))

    # Four feature rows.
    rows = [
        ("AI agents", "what's actually shipping"),
        ("Crypto alpha", "signal before the crowd"),
        ("Web3 tooling", "the stack that works"),
        ("On-chain automation", "bots that do the work"),
    ]
    y = 728
    for title, sub in rows:
        draw.ellipse([88, y + 14, 106, y + 32], fill=GREEN + (255,))
        draw.text((130, y), title, font=title_font, fill=WHITE + (255,))
        draw.text((130, y + 50), sub, font=sub_font, fill=MUTED + (255,))
        y += 112

    # Follow pill near the bottom: magenta, spanning most of the width.
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([80, 1196, 1000, 1290], radius=47,
                         fill=MAGENTA + (255,))
    img.alpha_composite(pill)
    draw = ImageDraw.Draw(img)
    centered_text(draw, 1218, "Follow  \u2192  x.com/crisxai5",
                  pill_font, WHITE + (255,))

    out_path = os.path.join(HERE, "card.png")
    img.convert("RGB").save(out_path, "PNG")
    print(f"Saved {out_path} ({W}x{H})")


if __name__ == "__main__":
    main()
