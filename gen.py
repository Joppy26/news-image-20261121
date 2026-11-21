#!/usr/bin/env python3
"""Render 'THE WORLD IN ONE PAGE' — a 1024x1024 broadsheet summing up the
world news of Saturday 21 November 2026.

Drawn entirely with PIL primitives and the DejaVu fonts shipped on the
system. No network, no randomness, no timestamps: running this file twice
produces byte-identical output.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 227)      # newsprint cream
INK = (20, 20, 20)           # near-black
RED = (176, 30, 30)          # accent red
BLUE = (29, 78, 137)         # accent blue
GREY = (90, 88, 80)
NIGHT = (28, 38, 66)         # night sky for the lead illustration
GOLD = (212, 160, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)       # noqa: E731


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=1.25):
    """Draw wrapped lines; returns the y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- illustrations
def draw_lead_art(draw, x0, y0, x1, y1):
    """Night sky over a city: missile arcs and one burst."""
    draw.rectangle([x0, y0, x1, y1], fill=NIGHT)
    # stars
    for sx, sy in [(x0 + 30, y0 + 18), (x0 + 90, y0 + 40), (x0 + 150, y0 + 14),
                   (x0 + 210, y0 + 34), (x0 + 260, y0 + 16), (x0 + 300, y0 + 48),
                   (x0 + 60, y0 + 62), (x0 + 180, y0 + 58), (x0 + 240, y0 + 70)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(240, 240, 220))
    # missile arcs (white trails with a bright head)
    for (ax, ay, bx, by) in [(x0 + 20, y1 - 30, x0 + 150, y0 + 70),
                             (x0 + 90, y1 - 10, x0 + 220, y0 + 50),
                             (x0 + 180, y1 - 40, x0 + 300, y0 + 90)]:
        mx, my = (ax + bx) // 2, min(ay, by) - 40
        draw.arc([ax, my - 60, bx, by + 60], start=200, end=340,
                 fill=(235, 235, 235), width=3)
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 210, 90))
    # explosion burst
    cx, cy = x0 + 250, y0 + 150
    for r, col in [(46, (255, 140, 40)), (32, (255, 190, 70)), (18, (255, 230, 150))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # city skyline silhouette
    base = y1
    for i, (bx, bw, bh) in enumerate([(0, 44, 70), (48, 36, 110), (88, 52, 80),
                                      (144, 40, 130), (188, 46, 90), (238, 38, 120),
                                      (280, 44, 84), (x1 - x0 - 40, 40, 100)]):
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(12, 16, 30))
        for wy in range(base - bh + 12, base - 10, 22):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 6, 16):
                draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 200, 90))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_market_art(draw, x0, y0, x1, y1):
    """A falling market line on a chart grid."""
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    for gy in range(y0 + 24, y1 - 8, 28):
        draw.line([(x0 + 6, gy), (x1 - 6, gy)], fill=(220, 220, 215), width=1)
    pts = [(x0 + 10, y0 + 26), (x0 + 28, y0 + 36), (x0 + 46, y0 + 34),
           (x0 + 62, y0 + 62), (x0 + 78, y0 + 82), (x0 + 92, y0 + 112),
           (x0 + 100, y0 + 138)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.polygon([(x0 + 100, y0 + 138), (x0 + 104, y0 + 128), (x0 + 108, y0 + 140)],
                 fill=RED)
    draw.text((x0 + 8, y0 + 4), "-3.7%", font=SANS_B(16), fill=RED)


def draw_justice_art(draw, x0, y0, x1, y1):
    """Scales of justice."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 234, 222))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    cx = (x0 + x1) // 2
    top = y0 + 22
    draw.line([(cx, top), (cx, y1 - 30)], fill=INK, width=5)
    draw.line([(x0 + 22, top + 14), (x1 - 22, top + 14)], fill=INK, width=5)
    draw.ellipse([cx - 8, top - 10, cx + 8, top + 6], fill=GOLD)
    for px in (x0 + 22, x1 - 22):
        draw.line([(px, top + 14), (px, top + 52)], fill=INK, width=3)
        draw.polygon([(px - 26, top + 52), (px + 26, top + 52), (px, top + 86)],
                     outline=INK, width=3)
    draw.rectangle([cx - 30, y1 - 30, cx + 30, y1 - 18], fill=INK)


def draw_climate_art(draw, x0, y0, x1, y1):
    """Sun behind a smoking factory."""
    draw.rectangle([x0, y0, x1, y1], fill=(222, 236, 244))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    sx, sy = x0 + 46, y0 + 44
    draw.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(240, 180, 60))
    for ang in range(0, 360, 45):
        import math
        dx = int(34 * math.cos(math.radians(ang)))
        dy = int(34 * math.sin(math.radians(ang)))
        draw.line([(sx + dx, sy + dy), (sx + int(42 * math.cos(math.radians(ang)))),
                   (sy + int(42 * math.sin(math.radians(ang))))], fill=(240, 180, 60), width=4)
    # factory
    draw.rectangle([x0 + 30, y1 - 62, x1 - 24, y1 - 12], fill=(70, 76, 84))
    draw.rectangle([x0 + 44, y1 - 108, x0 + 60, y1 - 62], fill=(70, 76, 84))
    draw.rectangle([x0 + 76, y1 - 96, x0 + 90, y1 - 62], fill=(70, 76, 84))
    for i, (px, py, r) in enumerate([(x0 + 52, y1 - 122, 10), (x0 + 66, y1 - 138, 13),
                                     (x0 + 84, y1 - 112, 9), (x0 + 96, y1 - 126, 12)]):
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(150, 150, 145))
    draw.rectangle([x0 + 40, y1 - 52, x0 + 56, y1 - 36], fill=(255, 220, 120))


def draw_politics_art(draw, x0, y0, x1, y1):
    """Two flags side by side: UK cross and EU circle of stars."""
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # UK flag (simplified): blue field, white diagonals, red cross
    ux0, uy0, ux1, uy1 = x0 + 6, y0 + 28, x0 + 52, y0 + 78
    draw.rectangle([ux0, uy0, ux1, uy1], fill=(20, 40, 90))
    draw.line([(ux0, uy0), (ux1, uy1)], fill=(255, 255, 255), width=7)
    draw.line([(ux0, uy1), (ux1, uy0)], fill=(255, 255, 255), width=7)
    draw.line([(ux0, uy0), (ux1, uy1)], fill=(200, 30, 30), width=3)
    draw.line([(ux0, uy1), (ux1, uy0)], fill=(200, 30, 30), width=3)
    draw.line([((ux0 + ux1) // 2, uy0), ((ux0 + ux1) // 2, uy1)],
              fill=(255, 255, 255), width=11)
    draw.line([(ux0, (uy0 + uy1) // 2), (ux1, (uy0 + uy1) // 2)],
              fill=(255, 255, 255), width=11)
    draw.line([((ux0 + ux1) // 2, uy0), ((ux0 + ux1) // 2, uy1)],
              fill=(200, 30, 30), width=5)
    draw.line([(ux0, (uy0 + uy1) // 2), (ux1, (uy0 + uy1) // 2)],
              fill=(200, 30, 30), width=5)
    # EU flag: blue field, circle of gold stars
    ex0, ey0, ex1, ey1 = x0 + 58, y0 + 28, x0 + 104, y0 + 78
    draw.rectangle([ex0, ey0, ex1, ey1], fill=(0, 40, 120))
    import math
    ecx, ecy = (ex0 + ex1) // 2, (ey0 + ey1) // 2
    for k in range(12):
        ang = math.radians(k * 30 - 90)
        px = ecx + int(13 * math.cos(ang))
        py = ecy + int(13 * math.sin(ang))
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 210, 60))
    draw.line([(x0 + 6, y0 + 92), (x1 - 6, y0 + 92)], fill=GREY, width=2)
    draw.text((x0 + 6, y0 + 98), "LONDON · BRUSSELS", font=SANS_B(10), fill=GREY)


def draw_health_art(draw, x0, y0, x1, y1):
    """A capsule beside cells fading away."""
    draw.rectangle([x0, y0, x1, y1], fill=(240, 240, 232))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # capsule: white right half, red left half, thick outline
    cx, cy = x0 + 66, y0 + 45
    draw.ellipse([cx - 48, cy - 18, cx + 48, cy + 18], fill=(250, 250, 250))
    draw.pieslice([cx - 48, cy - 18, cx + 4, cy + 18], start=90, end=270, fill=RED)
    draw.ellipse([cx - 48, cy - 18, cx + 48, cy + 18], outline=INK, width=3)
    draw.line([(cx - 48, cy), (cx + 48, cy)], fill=INK, width=2)
    # fading cells to the right of the capsule
    for px, py, r in [(x0 + 140, y0 + 26, 10), (x0 + 160, y0 + 52, 7),
                      (x0 + 142, y0 + 76, 5)]:
        draw.ellipse([px - r, py - r, px + r, py + r],
                     outline=(150, 60, 60), width=2)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead
    title = "THE WORLD IN ONE PAGE"
    tf = SERIF_B(54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 14), title, font=tf, fill=INK)
    rule(d, 24, W - 24, 84, width=3)
    rule(d, 24, W - 24, 90, width=1)
    date = "SATURDAY 21 NOVEMBER 2026"
    df = SANS_B(29)
    d.text(((W - d.textlength(date, font=df)) / 2, 98), date, font=df, fill=RED)
    d.text((24, 104), "ONE DAY", font=SANS_B(14), fill=GREY)
    d.text((W - 24 - d.textlength("SIX STORIES", font=SANS_B(14)), 104),
           "SIX STORIES", font=SANS_B(14), fill=GREY)

    # --- lead story: Russia strikes Ukraine; missiles land in Poland
    ly0, ly1 = 140, 396
    draw_lead_art(d, 16, ly0, 360, ly1)
    tx = 380
    d.text((tx, ly0 + 2), "WAR IN EUROPE  •  KYIV AND POLAND", font=SANS_B(16), fill=RED)
    headline = "RUSSIA'S BIGGEST STRIKE YET; MISSILES LAND IN POLAND"
    hf = SERIF_B(32)
    y = draw_lines(d, wrap(headline, hf, 628, d), tx, ly0 + 28, hf, leading=1.12)
    summary = ("More than 400 drones and 110 missiles hit Ukraine overnight; at "
               "least eight people were killed in Kyiv as bridges and railway "
               "stations burned. Two missiles and a suspected drone came down "
               "in Poland. Prime Minister Tusk called it a deliberate provocation.")
    draw_lines(d, wrap(summary, SANS(19), 628, d), tx, y + 8, SANS(19), leading=1.3)

    rule(d, 16, W - 16, 410, width=2)

    # --- grid: four stories, two by two
    grid = [
        ("MARKETS", "AI SELLOFF PUSHES S&P 500 INTO CORRECTION",
         "US stocks fell 3.7% as AI and chip shares sank; the Nasdaq lost "
         "5.3% and Tokyo's Nikkei 5.1%.", draw_market_art),
        ("JUSTICE", "COURT: MYANMAR COMMITTED ROHINGYA GENOCIDE",
         "The International Court of Justice found Myanmar responsible for "
         "genocide against the Rohingya people.", draw_justice_art),
        ("CLIMATE  •  ANTALYA", "COP31 DEADLOCK OVER FOSSIL FUELS",
         "UN climate talks ran past their deadline as nearly 200 nations "
         "failed to agree on phasing out fossil fuels.", draw_climate_art),
        ("POLITICS  •  BRUSSELS", "UK AND EU SIGN BIGGEST POST-BREXIT DEAL",
         "Three agreements on food exports, carbon markets and youth "
         "mobility — the deepest reset since Brexit.", draw_politics_art),
    ]
    cell_w, cell_h = 488, 204
    origins = [(16, 424), (520, 424), (16, 640), (520, 640)]
    for (kicker, head, summ, art), (cx, cy) in zip(grid, origins):
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], outline=INK, width=2)
        art(d, cx + 8, cy + 8, cx + 118, cy + cell_h - 8)
        tx2 = cx + 130
        d.text((tx2, cy + 10), kicker, font=SANS_B(14), fill=RED)
        y = draw_lines(d, wrap(head, SERIF_B(23), cell_w - 142, d),
                       tx2, cy + 32, SERIF_B(23), leading=1.12)
        draw_lines(d, wrap(summ, SANS(16), cell_w - 142, d),
                   tx2, y + 6, SANS(16), leading=1.28)

    rule(d, 16, W - 16, 858, width=2)

    # --- bottom band: health breakthrough
    by0, by1 = 872, 962
    draw_health_art(d, 16, by0, 196, by1)
    tx3 = 212
    d.text((tx3, by0 + 2), "HEALTH  •  A TRIAL RESULT", font=SANS_B(15), fill=RED)
    y = draw_lines(d, wrap("A PILL THAT MAKES TUMOURS VANISH", SERIF_B(26), 780, d),
                   tx3, by0 + 24, SERIF_B(26), leading=1.12)
    draw_lines(d, wrap("In a pancreatic cancer trial, the pill daraxonrasib made "
                       "tumours undetectable on scans in one in twelve patients.",
                       SANS(18), 780, d), tx3, y + 4, SANS(18), leading=1.3)

    # --- footer ticker
    rule(d, 16, W - 16, 976, width=2)
    ticker = ("ALSO:  PERU 6.9 QUAKE  •  FBI AND US AGRICULTURE DEPT HACKED  •  "
              "GEN Z PROTESTS IN 25 NATIONS")
    tf2 = SANS_B(15)
    d.text(((W - d.textlength(ticker, font=tf2)) / 2, 984), ticker, font=tf2, fill=INK)

    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
