#!/usr/bin/env python3
"""Draw the one-page newspaper for 20 November 2026.

Everything is drawn from scratch with Pillow: masthead, a navy lead
panel on the Kyiv attack, two mid-row panels (The Hague / Shenzhen),
three small panels (Anthropic / Riyadh / Hormuz), a black ticker and a
footer. The output is a deterministic 1024x1024 PNG.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (180, 35, 24)
NAVY = (27, 42, 74)
NAVY2 = (48, 68, 110)
TEAL = (14, 107, 107)
GOLD = (192, 138, 0)
PURPLE = (90, 60, 120)
WHITE = (255, 255, 255)
GREY = (90, 90, 84)
DARKGREY = (70, 70, 66)
LEAD_BODY = (168, 184, 208)
ORANGE = (232, 126, 28)
STAR_GOLD = (232, 176, 0)
FLAG_BLUE = (30, 60, 140)
FLAG_YELLOW = (245, 205, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Split text into lines that each fit max_w pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(draw, x, y, lines, fnt, fill, spacing):
    """Draw lines stacked with `spacing` between baselines."""
    for i, line in enumerate(lines):
        draw.text((x, y + i * spacing), line, font=fnt, fill=fill)
    return y + len(lines) * spacing


def rounded_panel(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def top_bar(draw, box, radius, fill):
    """A bar with rounded top corners and a square bottom edge."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=radius, fill=fill)
    top = min(y0 + radius, y1)
    draw.rectangle((x0, top, x1, y1), fill=fill)


def starburst(draw, cx, cy, outer, inner, points, fill):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        ang = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_badge(kind, diameter=40):
    """A circular flag badge: US, China or Russia."""
    img = Image.new("RGB", (diameter, diameter), WHITE)
    d = ImageDraw.Draw(img)
    if kind == "us":
        stripe = diameter / 7.0
        for i in range(7):
            y0 = int(i * stripe)
            y1 = int((i + 1) * stripe)
            d.rectangle((0, y0, diameter, y1), fill=RED if i % 2 == 0 else WHITE)
        d.rectangle((0, 0, int(diameter * 0.45), int(diameter * 0.45)),
                    fill=FLAG_BLUE)
        for sx in (6, 13):
            for sy in (5, 12):
                d.ellipse((sx - 1, sy - 1, sx + 1, sy + 1), fill=WHITE)
    elif kind == "cn":
        d.rectangle((0, 0, diameter, diameter), fill=(222, 41, 16))
        starburst(d, 13, 13, 9, 3.6, 5, FLAG_YELLOW)
    elif kind == "ru":
        third = diameter / 3.0
        d.rectangle((0, 0, diameter, int(third)), fill=WHITE)
        d.rectangle((0, int(third), diameter, int(2 * third)), fill=(0, 60, 160))
        d.rectangle((0, int(2 * third), diameter, diameter), fill=(210, 30, 30))
    mask = Image.new("L", (diameter, diameter), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, diameter, diameter), fill=255)
    img.putalpha(mask)
    return img


def draw_scales(draw, cx, top, bottom, half, color):
    """Simple line-art scales of justice centred at cx."""
    draw.line((cx, top, cx, bottom), fill=color, width=3)
    draw.line((cx - half, top + 6, cx + half, top + 6), fill=color, width=3)
    for side in (-1, 1):
        px = cx + side * half
        draw.line((px, top + 6, px - 13, top + 38), fill=color, width=2)
        draw.line((px, top + 6, px + 13, top + 38), fill=color, width=2)
        draw.arc((px - 13, top + 30, px + 13, top + 48), 0, 180,
                 fill=color, width=2)
    draw.line((cx - 20, bottom, cx + 20, bottom), fill=color, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    draw.rectangle((0, 0, W, 10), fill=RED)
    draw.text((28, 22), "THE WORLD TODAY", font=font(SERIF_B, 76), fill=INK)
    draw.line((28, 116, 996, 116), fill=INK, width=3)
    draw.text((28, 126), "FRIDAY  \u2022  20 NOVEMBER 2026",
              font=font(SANS_B, 27), fill=RED)
    draw.text((996, 128), "ONE DAY \u2014 ONE IMAGE",
              font=font(SANS_B, 22), fill=INK, anchor="ra")
    draw.line((28, 170, 996, 170), fill=INK, width=2)

    # ---- Lead panel: Kyiv -----------------------------------------
    rounded_panel(draw, (28, 182, 996, 452), 18, NAVY)
    draw.text((52, 202), "KYIV UNDER FIRE", font=font(SANS_B, 22), fill=GOLD)
    draw.text((52, 228), "RUSSIA'S BIGGEST", font=font(SERIF_B, 44), fill=WHITE)
    draw.text((52, 284), "NIGHT ATTACK", font=font(SERIF_B, 36), fill=WHITE)
    lead = ("100+ missiles and ~400 drones overnight. Three bridges "
            "damaged, eight killed, 28 hurt, power cut across the capital.")
    paragraph(draw, 52, 352, wrap(draw, lead, font(SANS, 23), 580),
              font(SANS, 23), LEAD_BODY, 30)
    starburst(draw, 900, 250, 42, 20, 12, ORANGE)
    starburst(draw, 800, 228, 22, 11, 10, STAR_GOLD)
    # Building silhouettes along the bottom-right of the panel.
    heights = [55, 80, 48, 95, 62, 88, 70]
    for i, h in enumerate(heights):
        x0 = 660 + i * 46
        draw.rectangle((x0, 452 - h, x0 + 34, 452), fill=NAVY2)

    # ---- Row 2 left: The Hague ------------------------------------
    rounded_panel(draw, (28, 470, 498, 692), 14, WHITE)
    top_bar(draw, (28, 470, 498, 514), 14, NAVY)
    draw.text((44, 482), "THE HAGUE", font=font(SANS_B, 22), fill=WHITE)
    draw.text((44, 530), "UN court: Myanmar", font=font(SERIF_B, 29), fill=INK)
    draw.text((44, 562), "committed genocide", font=font(SERIF_B, 29), fill=INK)
    hague = ("First ruling of its kind: Rohingya genocide, 10,000 killed. "
             "Myanmar calls it 'unfair'.")
    paragraph(draw, 44, 604, wrap(draw, hague, font(SANS, 19), 300),
              font(SANS, 19), DARKGREY, 24)
    draw_scales(draw, 435, 600, 678, 37, NAVY)

    # ---- Row 2 right: Shenzhen ------------------------------------
    rounded_panel(draw, (526, 470, 996, 692), 14, WHITE)
    top_bar(draw, (526, 470, 996, 514), 14, RED)
    draw.text((542, 482), "SHENZHEN", font=font(SANS_B, 22), fill=WHITE)
    draw.text((542, 530), "Trump, Xi & Putin", font=font(SERIF_B, 29), fill=INK)
    draw.text((542, 562), "first three-way summit", font=font(SERIF_B, 29), fill=INK)
    shenzhen = ("Joint declaration after 90 minutes; Europe warns of a deal "
                "over its head.")
    paragraph(draw, 542, 604, wrap(draw, shenzhen, font(SANS, 19), 260),
              font(SANS, 19), DARKGREY, 24)
    for i, kind in enumerate(("us", "cn", "ru")):
        badge = flag_badge(kind)
        img.paste(badge, (830 + i * 50, 620), badge)

    # ---- Row 3: three small panels --------------------------------
    small = [
        (28, 341, GOLD, "ANTHROPIC", "Record debut, then slide",
         "Shares fall on day two as AI stocks sell off; Japan's Nikkei down 4.8%."),
        (355, 668, PURPLE, "RIYADH", "Missile hits PIF Tower",
         "Houthi strike damages the Saudi sovereign wealth fund tower in the financial district."),
        (682, 995, TEAL, "HORMUZ", "Tanker ablaze",
         "Mine strike in the strait as the Iran war enters its ninth month; attacks on shipping grow."),
    ]
    for x0, x1, color, kicker, title, body in small:
        rounded_panel(draw, (x0, 708, x1, 898), 14, WHITE)
        top_bar(draw, (x0, 708, x1, 720), 14, color)
        draw.text((x0 + 16, 732), kicker, font=font(SANS_B, 19), fill=color)
        title_lines = wrap(draw, title, font(SERIF_B, 26), x1 - x0 - 32)
        body_y = paragraph(draw, x0 + 16, 758, title_lines,
                           font(SERIF_B, 26), INK, 28) + 8
        paragraph(draw, x0 + 16, body_y,
                  wrap(draw, body, font(SANS, 18), x1 - x0 - 32),
                  font(SANS, 18), DARKGREY, 21)

    # ---- Ticker ----------------------------------------------------
    draw.rectangle((28, 912, 996, 954), fill=INK)
    ticker = ("ALSO:  Trump pardons baseball legend Pete Rose  \u2022  "
              "EU summons Russia's envoy over Kyiv embassy damage  \u2022  "
              "Kenya discharges its last Ebola patient")
    size = 22
    while size > 8:
        fnt = font(SANS_B, size)
        if draw.textlength(ticker, font=fnt) <= 930:
            break
        size -= 1
    draw.text((512, 933), ticker, font=font(SANS_B, size), fill=WHITE,
              anchor="ma")

    # ---- Footer ----------------------------------------------------
    draw.text((512, 968), "20 NOVEMBER 2026  \u2014  THE DAY IN ONE IMAGE",
              font=font(SANS_B, 20), fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print(f"saved {out} {img.size[0]}x{img.size[1]} "
          f"{os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
