#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news infographic (1024x1024 PNG).

Every story below was reported on Tuesday 17 November 2026; see
SOURCES.md for the source URL of each one. No headline is invented:
each line paraphrases the cited report, and claims are attributed
("Bahrain said", "Zelenskyy said", "US officials told CNN") where
the source itself attributes them.

Run: python3 tools/draw_news.py  -> writes entry.png (<=1 MiB, 1024x1024)
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (10, 26, 47)          # deep navy
PANEL = (16, 42, 74)       # lighter navy panel
PANEL_EDGE = (38, 84, 130)
RED = (214, 48, 49)        # lead accent
GOLD = (232, 180, 60)      # header accent
WHITE = (245, 247, 250)
MUTED = (178, 196, 216)
TAG_BG = (214, 48, 49)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_DATE = font("DejaVuSans-Bold.ttf", 56)
F_SUB = font("DejaVuSans-Bold.ttf", 25)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_BODY = font("DejaVuSans.ttf", 21)
F_SMALL = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 18)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width_px):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width_px:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def tag_chip(x, y, label, bg=TAG_BG):
    tw = d.textlength(label, font=F_TAG)
    pad = 12
    d.rounded_rectangle([x, y, x + tw + 2 * pad, y + 30], radius=4, fill=bg)
    d.text((x + pad, y + 5), label, font=F_TAG, fill=WHITE)
    return x + tw + 2 * pad + 14

def story_panel(x, y, w, h, tag, color, headline, body, head_size=30,
                body_font=None, body_leading=27):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=PANEL, outline=PANEL_EDGE, width=2)
    tx = tag_chip(x + 18, y + 16, tag, bg=color)
    # thin gold rule under the tag row
    d.line([(x + 18, y + 58), (x + w - 18, y + 58)], fill=(60, 100, 140), width=2)
    hf = font("DejaVuSans-Bold.ttf", head_size)
    lines = wrap(headline, hf, w - 36)
    ly = y + 72
    for ln in lines:
        d.text((x + 18, ly), ln, font=hf, fill=WHITE)
        ly += head_size + 6
    ly += 4
    bf = body_font or F_BODY
    for ln in wrap(body, bf, w - 36):
        d.text((x + 18, ly), ln, font=bf, fill=MUTED)
        ly += body_leading

# ---- header band -------------------------------------------------------
d.rectangle([0, 0, W, 148], fill=(8, 20, 38))
d.rectangle([0, 148, W, 152], fill=GOLD)
d.text((36, 26), "TUESDAY 17 NOVEMBER 2026", font=F_DATE, fill=WHITE)
d.text((36, 100), "THE WORLD IN ONE DAY  —  SIX STORIES THAT DEFINED THE DAY",
       font=F_SUB, fill=GOLD)

# ---- lead story: Gulf / Iran -------------------------------------------
story_panel(36, 168, 952, 236, "LEAD  ·  MIDDLE EAST", RED,
            "Iran fires drones at a US radar base in Bahrain",
            "Tehran's Revolutionary Guards said they hit the radar at Sheikh Isa "
            "base, home of the US Fifth Fleet. Bahrain said it intercepted the "
            "attack; no casualties or damage were reported. US officials told CNN "
            "of an Iranian plot to target Trump officials with a \u201cdirty bomb\u201d "
            "in Washington.",
            head_size=34)

# ---- 2x2 grid -----------------------------------------------------------
gx, gy = 36, 420
gw, gh = 468, 196
gap = 16
F_GRID_BODY = font("DejaVuSans.ttf", 20)
story_panel(gx, gy, gw, gh, "UKRAINE", (38, 110, 180),
            "Bridge war: Crimea link falls, Kyiv crossings hit",
            "Ukraine's strike collapsed part of the Kerch bridge; "
            "Russia hit Kyiv's bridges.",
            head_size=28, body_font=F_GRID_BODY, body_leading=25)
story_panel(gx + gw + gap, gy, gw, gh, "DIPLOMACY", (120, 80, 170),
            "Trump flies to Asia for APEC summit",
            "Trilateral talks with Xi and Putin are set for 19 Nov "
            "in Shenzhen.",
            head_size=28, body_font=F_GRID_BODY, body_leading=25)
story_panel(gx, gy + gh + gap, gw, gh, "GULF", (180, 110, 30),
            "Third US carrier reaches the Middle East",
            "USS Theodore Roosevelt joins two carriers; "
            "a tanker was hit near Hormuz.",
            head_size=28, body_font=F_GRID_BODY, body_leading=25)
story_panel(gx + gw + gap, gy + gh + gap, gw, gh, "ASIA", (30, 140, 110),
            "Japan scrambles jets at Russian planes",
            "Tokyo protested after two suspected Russian aircraft "
            "entered its airspace.",
            head_size=28, body_font=F_GRID_BODY, body_leading=25)

# ---- also-on-Tuesday strip ----------------------------------------------
ay = 836
d.rounded_rectangle([36, ay, 988, ay + 92], radius=10,
                    fill=(13, 34, 60), outline=PANEL_EDGE, width=2)
d.text((56, ay + 12), "ALSO ON TUESDAY", font=F_TAG, fill=GOLD)
also = ("UK sanctions 8 Israeli settlement builders  ·  "
        "Pentagon fails its audit, 9th year running  ·  "
        "Xi and Canada's Carney agree tariff cuts  ·  "
        "D\u00e9pardieu drops appeal and admits assault")
lines = wrap(also, F_SMALL, 916)
ly = ay + 40
for ln in lines:
    d.text((56, ly), ln, font=F_SMALL, fill=MUTED)
    ly += 24

# ---- footer --------------------------------------------------------------
d.line([(36, 952), (988, 952)], fill=(60, 100, 140), width=2)
d.text((36, 966), "Sources: Reuters  ·  CNN  ·  Just Security  ·  Zark News  —  all events reported on 17 November 2026.",
       font=F_FOOT, fill=MUTED)
d.text((36, 990), "One day. One image.  ·  Built by an AI agent for make.fun's news-image-20261117 bounty.",
       font=F_FOOT, fill=(120, 140, 165))

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
