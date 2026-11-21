# generate_image.py — draws entry.png (1024x1024) for the
# make.fun bounty "Sum up 20 November's world news in one image".
# Run: python3 generate_image.py  -> writes entry.png next to this file.
# The entry program (main.ts) only copies entry.png to /output/entry.png,
# so the PNG bytes here are exactly what the judge sees.
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
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

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, box, fill, outline=INK, width=2):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def burst(draw, cx, cy, r, fill):
    """Starburst: alternating long/short spikes."""
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_circle(draw, cx, cy, r, kind):
    """A round flag badge: US / CN / RU, drawn from simple shapes."""
    mask = Image.new("L", (r * 2 + 4, r * 2 + 4), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((2, 2, r * 2 + 2, r * 2 + 2), fill=255)
    layer = Image.new("RGB", (r * 2 + 4, r * 2 + 4), WHITE)
    ld = ImageDraw.Draw(layer)
    if kind == "US":
        for i in range(7):
            ld.rectangle((0, i * (r * 2 + 4) // 7, r * 2 + 4,
                          (i + 1) * (r * 2 + 4) // 7),
                         fill=RED if i % 2 == 0 else WHITE)
        ld.rectangle((0, 0, (r * 2 + 4) * 0.45, (r * 2 + 4) * 0.55), fill=NAVY)
        for sx in (8, 26, 44):
            for sy in (8, 22):
                ld.ellipse((sx, sy, sx + 6, sy + 6), fill=WHITE)
    elif kind == "CN":
        ld.rectangle((0, 0, r * 2 + 4, r * 2 + 4), fill=(222, 41, 16))
        ld.ellipse((r * 0.45, r * 0.45, r * 0.95, r * 0.95), fill=(255, 222, 0))
        for sx, sy in ((r * 1.35, r * 0.35), (r * 1.55, r * 0.7), (r * 1.5, r * 1.1)):
            ld.ellipse((sx, sy, sx + 8, sy + 8), fill=(255, 222, 0))
    else:  # RU
        h = (r * 2 + 4) / 3
        ld.rectangle((0, 0, r * 2 + 4, h), fill=WHITE)
        ld.rectangle((0, h, r * 2 + 4, 2 * h), fill=(0, 57, 166))
        ld.rectangle((0, 2 * h, r * 2 + 4, 3 * h), fill=(213, 0, 50))
    img.paste(layer, (cx - r - 2, cy - r - 2), mask)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=WHITE, width=3)


img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img)

# ---- top rule + masthead -----------------------------------------------
draw.rectangle((0, 0, W, 10), fill=RED)
draw.text((28, 22), "THE WORLD TODAY", font=font(SERIF, 76), fill=INK)
draw.line((28, 116, W - 28, 116), fill=INK, width=3)
draw.text((28, 126), "FRIDAY  •  20 NOVEMBER 2026",
          font=font(SANS_B, 27), fill=RED)
draw.text((W - 28, 128), "ONE DAY — ONE IMAGE",
          font=font(SANS_B, 22), fill=INK, anchor="ra")
draw.line((28, 170, W - 28, 170), fill=INK, width=1)

# ---- lead story: Kyiv under fire ----------------------------------------
panel(draw, (28, 182, 996, 452), NAVY)
draw.text((52, 202), "KYIV UNDER FIRE", font=font(SANS_B, 22), fill=(255, 214, 90))
draw.text((52, 228), "RUSSIA'S BIGGEST", font=font(SERIF, 44), fill=WHITE)
draw.text((52, 284), "NIGHT ATTACK", font=font(SERIF, 36), fill=WHITE)
para(draw, (52, 352),
     "100+ missiles and ~400 drones overnight. Three bridges damaged, "
     "eight killed, 28 hurt, power cut across the capital.",
     font(SANS, 23), (220, 228, 240), 580, 30)
# explosion burst, top right, clear of the headline (ends x~640 at 44px)
burst(draw, 900, 250, 42, (255, 170, 0))
burst(draw, 800, 228, 22, (255, 214, 90))
# Kyiv skyline along the bottom right
for i, hgt in enumerate((40, 66, 50, 80, 56, 70, 44)):
    x0 = 660 + i * 46
    draw.rectangle((x0, 452 - 12 - hgt, x0 + 34, 452 - 12), fill=NAVY2)

# ---- row 2: ICJ Myanmar + Shenzhen summit -------------------------------
# Myanmar (scales-of-justice motif in the bottom-right corner)
panel(draw, (28, 470, 498, 692), WHITE)
draw.rectangle((28, 470, 498, 514), fill=NAVY)
draw.text((46, 478), "THE HAGUE", font=font(SANS_B, 22), fill=WHITE)
draw.text((46, 526), "UN court: Myanmar", font=font(SERIF, 29), fill=INK)
draw.text((46, 560), "committed genocide", font=font(SERIF, 29), fill=INK)
para(draw, (46, 602),
     "First ruling of its kind: Rohingya genocide, 10,000 killed. "
     "Myanmar calls it 'unfair'.",
     font(SANS, 19), INK, 300, 24)
draw.line((430, 640, 430, 676), fill=INK, width=4)
draw.line((392, 640, 468, 640), fill=INK, width=4)
draw.line((392, 640, 380, 668), fill=INK, width=3)
draw.line((392, 640, 404, 668), fill=INK, width=3)
draw.line((468, 640, 456, 668), fill=INK, width=3)
draw.line((468, 640, 480, 668), fill=INK, width=3)
draw.arc((372, 660, 412, 686), start=0, end=180, fill=INK, width=3)
draw.arc((448, 660, 488, 686), start=0, end=180, fill=INK, width=3)
# Shenzhen summit
panel(draw, (526, 470, 996, 692), WHITE)
draw.rectangle((526, 470, 996, 514), fill=(120, 40, 30))
draw.text((544, 478), "SHENZHEN", font=font(SANS_B, 22), fill=WHITE)
draw.text((544, 526), "Trump, Xi & Putin", font=font(SERIF, 29), fill=INK)
draw.text((544, 560), "first three-way summit", font=font(SERIF, 29), fill=INK)
para(draw, (544, 602),
     "Joint declaration after 90 minutes; Europe warns of "
     "a deal over its head.",
     font(SANS, 19), INK, 260, 24)
for cx, kind in ((850, "US"), (900, "CN"), (950, "RU")):
    flag_circle(draw, cx, 640, 20, kind)

# ---- row 3: Anthropic / Riyadh / Hormuz ---------------------------------
cols = [
    ("ANTHROPIC", GOLD, "Record debut, then slide",
     "Shares fall on day two as AI stocks sell off; Japan's Nikkei "
     "down 4.8%."),
    ("RIYADH", PURPLE, "Missile hits PIF Tower",
     "Houthi strike damages the Saudi sovereign wealth fund tower "
     "in the financial district."),
    ("HORMUZ", TEAL, "Tanker ablaze",
     "Mine strike in the strait as the Iran war enters its ninth "
     "month; attacks on shipping grow."),
]
xs = [(28, 341), (355, 668), (682, 995)]
for (x0, x1), (kick, col, head, body) in zip(xs, cols):
    panel(draw, (x0, 708, x1, 898), WHITE)
    draw.rectangle((x0, 708, x1, 716), fill=col)
    draw.text((x0 + 16, 728), kick, font=font(SANS_B, 19), fill=col)
    y = para(draw, (x0 + 16, 756), head, font(SERIF, 26), INK, x1 - x0 - 32, 31)
    para(draw, (x0 + 16, y + 6), body, font(SANS, 18), (60, 60, 60),
         x1 - x0 - 32, 22)

# ---- ticker + footer ------------------------------------------------------
draw.rectangle((28, 912, 996, 954), fill=INK)
ticker = ("ALSO:  Trump pardons baseball legend Pete Rose  •  "
          "EU summons Russia's envoy over Kyiv embassy damage  •  "
          "Kenya discharges its last Ebola patient")
tf = font(SANS_B, 19)
while draw.textlength(ticker, font=tf) > 930:
    tf = font(SANS_B, tf.size - 1)
draw.text((46, 922), ticker, font=tf, fill=WHITE)
draw.text((W // 2, 968), "20 NOVEMBER 2026  —  THE DAY IN ONE IMAGE",
          font=font(SANS_B, 20), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, len(open("entry.png", "rb").read()), "bytes")
