#!/usr/bin/env python3
"""Build v3 of the entry image for make.fun bounty news-image-20261118.

One-page newspaper digest of Wednesday 18 November 2026:
52 stories, 7 regions, 3 drawn lead scenes (incl. Voyager 1), a drawn
dot world map with the day's places marked, a Day in Numbers panel,
a date-check stamp and a UTC clock timeline anchored to reported times.
Every story reported on the day itself. Deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont
import os, random

W, H = 1024, 1024
PAPER = (255, 253, 245)
INK = (22, 22, 22)
GRAY = (90, 90, 90)
RULE = (40, 40, 40)
DATE_RED = (157, 2, 8)
LEAD_BG = (243, 238, 224)
WHITE = (255, 255, 255)
MAP_BG = (233, 238, 242)
LAND = (105, 128, 152)
MARK = (178, 34, 52)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def center(s, font, y, fill=INK):
    d.text(((W - text_w(s, font)) / 2, y), s, font=font, fill=fill)

MX = 26
CW = W - 2 * MX

# ---------------------------------------------------------------- data
LEADS = [
    ("SHENZHEN · APEC SUMMIT", (29, 78, 137),
     "Xi & Putin meet as Trump lands",
     "Xi Jinping and Vladimir Putin opened talks in Shenzhen as Donald Trump "
     "arrived for APEC. First three-way summit set for Thursday. (AFP/AP)"),
    ("THE GULF · IRAN–US CLASHES", (179, 84, 30),
     "Drones, intercepts & struck tankers",
     "Iranian drones targeted a US base in Kuwait; Bahrain intercepted attacks "
     "before dawn; US jets hit a missile site on Qeshm Island. Oil near $93. (Reuters)"),
    ("DEEP SPACE · VOYAGER 1", (40, 40, 120),
     "One light-day from home",
     "At 10:16 UTC, NASA's Voyager 1 became the first human-made object one "
     "light-day from Earth: 25.9 billion km. A command now takes a day to arrive. (NASA)"),
]

REGIONS = {
    "ASIA-PACIFIC": ((29, 111, 184), [
        ("Quad leaders meet in Manila",
         "First leader-level Quad in over two years; Trump announced a US–Philippines trade deal."),
        ("Seoul reaches out to Beijing",
         "President Lee Jae Myung used APEC to seek China's help on Korean Peninsula stability."),
        ("ASEAN talks on a South China Sea code",
         "Regional governments kept negotiating a code of conduct for the disputed sea."),
        ("Russian bombers shadow Japan & Taiwan",
         "Japan reported an airspace violation off Fukuoka; Taiwan logged 10 PLA sorties, 11 ships."),
        ("Cyclone Akvan bears down on Odisha",
         "Severe storm put India's south Odisha coast on high alert; evacuations began, schools shut."),
        ("Afghan earthquake kills more than 600",
         "Rescuers dug through rubble in the east as the reported death toll kept climbing."),
    ]),
    "EUROPE & UKRAINE": ((68, 86, 168), [
        ("Ukraine hits the Kerch Bridge again",
         "A second night of strikes shut the Crimea bridge; Russia hit two Ukrainian bridges in reply."),
        ("141 drones in one night over Ukraine",
         "Kyiv said 126 were downed or suppressed by morning; six people were injured in Dnipro."),
        ("Allies weigh more jets for Kyiv",
         "Ramstein group met as Ukraine asked for fighters and air defence; France to send more Mirages."),
        ("EU proposes €45bn loan for Ukraine",
         "Commission plan for 2027: €25bn in military aid plus €20bn of budget support."),
    ]),
    "MIDDLE EAST": ((179, 84, 30), [
        ("Tanker hit near Hormuz; crewman missing",
         "ADNOC-linked vessel struck by a projectile: 11 crew injured, one missing (Reuters)."),
        ("US says five Iranian tankers destroyed",
         "Washington said the sinkings answered IRGC attacks on a US warship; Iran said it hit 10 ships."),
        ("Saudi intercepts missile bound for Riyadh",
         "The kingdom said it destroyed a Houthi cruise missile aimed at the capital region."),
        ("Gaza's displaced face a fourth winter",
         "WHO: 950,000 people in flood-prone ground; the UN warned of deaths from cold and hunger."),
    ]),
    "AMERICAS": ((46, 125, 50), [
        ("Peltola's Alaska upset flips the Senate",
         "Democrat beat Sen. Sullivan — the first Alaska Native senator; Democrats projected 56–44."),
        ("US probes a day of tech failures",
         "Microsoft 365, the FAA and an NSA network went down; Rubio saw no sign of a cyberattack."),
        ("27 years for the Iran-linked Trump plot",
         "A Pakistani man was sentenced over the alleged Tehran-backed assassination scheme."),
        ("Carney takes Canada's trade pitch to Asia",
         "Ottawa courted Asian markets to cut the country's reliance on the United States."),
        ("Haiti signs security pact with El Salvador",
         "Salvadoran personnel to help fight gangs after 4,595 violence deaths in 10 months (UN)."),
    ]),
    "AFRICA": ((166, 124, 0), [
        ("Sudan's army advances in West Kordofan",
         "Army gains piled pressure on the RSF as the humanitarian crisis deepened."),
        ("Chad closes its border with Sudan",
         "N'Djamena shut the frontier as fighting across the border in Sudan intensified."),
        ("Nigeria votes to allow state police",
         "Landmark reform would let states raise their own police forces for the first time."),
    ]),
    "OCEANIA": ((0, 131, 143), [
        ("Australia sanctions West Bank settlers",
         "Canberra targeted 3 people and 4 groups over settlement violence (FM Penny Wong)."),
        ("Australia's pay gap hits a record low",
         "The national gender pay gap fell to its smallest ever recorded."),
    ]),
    "CLIMATE · TECH · SPORT · CULTURE": ((106, 27, 154), [
        ("COP31 talks enter their decisive phase",
         "Antalya negotiators faced a draft text with 144 disputed items before Friday's deadline."),
        ("Nvidia board: no return for Huang",
         "Directors ruled out reinstating Jensen Huang as CEO; the chip forecast still beat hopes."),
        ("Measles is back: US loses elimination status",
         "UNICEF warned of a global resurgence as vaccination gaps widened."),
    ]),
}

BRIEFS = [
    ("THAI–MYANMAR", "Villages fear arsenic in border rivers"),
    ("SLOVAKIA", "Thousands protest the Fico government"),
    ("ITALY", "Antisemitism law passes parliament"),
    ("GAZA", "Board of Peace warns truce may collapse"),
    ("BRAZIL", "Rare contact with isolated Amazon people"),
    ("DR CONGO", "Ebola vaccine candidates reach Phase 2"),
    ("NEW ZEALAND", "Tsunami warning withdrawn"),
    ("EU–INDONESIA", "CEPA trade deal gets green light"),
    ("UKRAINE", "Kyiv's drones hit Russian oil refineries"),
    ("IRAN", "Army helicopter crash kills four in Isfahan"),
    ("IRAQ", "Baghdad's ultimatum to a militia is rejected"),
    ("CANADA", "More aid pledged; sanctions on Russia stay"),
    ("US", "Supreme Court acts on Trump's anti-DEI push"),
    ("US", "New York orders travel ban as storm hits"),
    ("NIGERIA", "Abuja bids for a UN Human Rights Council seat"),
    ("PAKISTAN", "Building blast death toll rises to 16"),
    ("SPORT", "Pakistan edge India in blind-cricket thriller"),
    ("FILM", "Robert Pattinson named the new James Bond"),
    ("TECH", "Waymo pauses driverless freeway runs"),
    ("F1", "Drivers' heartbeats on TV from 2027"),
    ("NETHERLANDS", "Youngest, first openly gay PM sworn in"),
    ("PAKISTAN", "Petrol cut by Rs3 to Rs325 a litre"),
]

NUMBERS = [
    ("141", "drones over Ukraine in one night — 126 downed by morning"),
    ("950,000", "displaced people in Gaza on flood-prone ground (WHO)"),
    ("€45bn", "EU loan proposed for Ukraine: arms and budget support"),
    ("56–44", "projected US Senate split after the Alaska upset"),
    ("$93", "oil, per barrel, as tankers are struck near Hormuz"),
    ("25.9bn km", "Voyager 1's distance from Earth — one light-day (NASA)"),
]

TOTAL = len(LEADS) + sum(len(v[1]) for v in REGIONS.values()) + len(BRIEFS)
print("story count:", TOTAL)
assert TOTAL == 52, TOTAL

# ---------------------------------------------------------------- masthead
center("THE WHOLE DAY'S WORLD NEWS IN A SINGLE IMAGE", F(SANS_B, 11), 8, GRAY)
center("THE WORLD TODAY", F(SERIF_B, 44), 22)
d.line([(MX, 74), (W - MX, 74)], fill=RULE, width=3)
center("Wednesday 18 November 2026", F(SERIF_B, 32), 80, DATE_RED)
center("52 stories  ·  7 regions  ·  drawn map & scenes  ·  every story reported on the day itself, date-checked",
       F(SANS, 13), 118, GRAY)
d.line([(MX, 140), (W - MX, 140)], fill=RULE, width=1)

# date-check stamp (drawn on its own layer, rotated, pasted)
stamp = Image.new("RGBA", (176, 48), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([2, 2, 173, 45], outline=(178, 34, 52, 255), width=3)
sd.text((88 - sd.textlength("DATE-CHECKED", font=F(SANS_B, 16)) / 2, 5),
        "DATE-CHECKED", font=F(SANS_B, 16), fill=(178, 34, 52, 255))
sd.text((88 - sd.textlength("WED 18 NOV 2026", font=F(SANS_B, 11)) / 2, 27),
        "WED 18 NOV 2026", font=F(SANS_B, 11), fill=(178, 34, 52, 255))
img.paste(stamp.rotate(8, expand=True, resample=Image.BILINEAR), (836, 12), stamp.rotate(8, expand=True, resample=Image.BILINEAR))
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- lead scenes
def scene_apec(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(173, 206, 235))
    d.ellipse([x + w - 26, y + 6, x + w - 6, y + 26], fill=(250, 204, 60))
    base = y + h
    for fx_, bw, bh in [(0.02, 0.16, 0.42), (0.20, 0.13, 0.58), (0.35, 0.18, 0.35),
                        (0.55, 0.12, 0.50), (0.69, 0.16, 0.38), (0.86, 0.13, 0.55)]:
        bx = x + int(fx_ * w)
        d.rectangle([bx, base - int(bh * h), bx + int(bw * w), base], fill=(43, 62, 92))
    for pf, flag in [(0.16, "cn"), (0.47, "ru"), (0.78, "us")]:
        px = x + int(pf * w)
        d.line([(px, base), (px, base - int(0.80 * h))], fill=(30, 30, 30), width=2)
        fx, fy = px + 2, base - int(0.80 * h)
        fw, fh = int(0.24 * w), int(0.15 * h)
        if flag == "cn":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            d.rectangle([fx + 3, fy + 3, fx + 6, fy + 6], fill=(255, 222, 0))
        elif flag == "ru":
            d.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=WHITE)
            d.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(0, 57, 166))
            d.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(213, 43, 30))
        else:
            for i in range(5):
                d.rectangle([fx, fy + i * fh // 5, fx + fw, fy + (i + 1) * fh // 5],
                            fill=(178, 34, 52) if i % 2 == 0 else WHITE)
            d.rectangle([fx, fy, fx + fw // 2, fy + fh // 2], fill=(60, 59, 110))

def scene_gulf(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 224, 178))
    d.rectangle([x, y + int(h * 0.45), x + w, y + h], fill=(38, 110, 138))
    d.ellipse([x + 8, y + 6, x + 28, y + 26], fill=(244, 164, 40))
    ty = y + int(h * 0.62)
    d.polygon([(x + 10, ty), (x + w - 8, ty), (x + w - 18, ty + 13), (x + 18, ty + 13)], fill=(35, 35, 40))
    d.rectangle([x + 20, ty - 6, x + w - 22, ty], fill=(90, 90, 96))
    d.rectangle([x + w - 30, ty - 16, x + w - 20, ty - 6], fill=(60, 60, 66))
    d.rectangle([x + w - 27, ty - 21, x + w - 23, ty - 16], fill=(178, 34, 52))
    for cf in [(0.34, 0.16), (0.62, 0.10)]:
        cx, cy = x + int(cf[0] * w), y + int(cf[1] * h)
        d.line([(cx - 5, cy - 3), (cx + 5, cy + 3)], fill=(30, 30, 30), width=2)
        d.line([(cx - 5, cy + 3), (cx + 5, cy - 3)], fill=(30, 30, 30), width=2)
    d.arc([x + int(0.30 * w), y + int(0.14 * h), x + w - 4, y + int(0.72 * h)],
          start=200, end=320, fill=(178, 34, 52), width=2)

def scene_voyager(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 44))
    rng = random.Random(20261118)
    for _ in range(46):
        sx, sy = x + rng.randint(2, w - 3), y + rng.randint(2, h - 3)
        c = (255, 255, 255) if rng.random() < 0.7 else (255, 230, 150)
        d.point((sx, sy), fill=c)
        if rng.random() < 0.3:
            d.point((sx + 1, sy), fill=c)
    # Earth, bottom left
    ex, ey = x + 13, y + h - 14
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(70, 130, 220))
    d.ellipse([ex - 3, ey - 4, ex + 1, ey], fill=(90, 190, 110))
    # dashed signal arc Earth -> probe
    import math
    px_, py_ = x + int(0.60 * w), y + int(0.34 * h)
    for t in [i / 26 for i in range(27)]:
        if int(t * 26) % 2 == 0:
            continue
        cx = ex + (px_ - ex) * t
        cy = ey + (py_ - ey) * t - 16 * math.sin(math.pi * t)
        d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=(140, 200, 255))
    # probe: dish, bus, boom
    d.ellipse([px_ - 13, py_ - 10, px_ + 13, py_ + 10], fill=(225, 230, 240), outline=(150, 160, 180))
    d.ellipse([px_ - 4, py_ - 3, px_ + 4, py_ + 3], fill=(170, 178, 195))
    d.line([(px_, py_), (px_ + 10, py_ + 8)], fill=(200, 205, 215), width=2)
    d.rectangle([px_ + 9, py_ + 7, px_ + 17, py_ + 15], fill=(212, 175, 55))
    d.line([(px_, py_), (px_ - 14, py_ - 12)], fill=(200, 205, 215), width=2)
    d.rectangle([px_ - 19, py_ - 16, px_ - 13, py_ - 10], fill=(120, 120, 130))

LY = 148
LW = (CW - 2 * 12) // 3
LH = 108
for i, (kick, col, head, body) in enumerate(LEADS):
    x = MX + i * (LW + 12)
    d.rectangle([x, LY, x + LW, LY + LH], fill=LEAD_BG)
    d.rectangle([x, LY, x + LW, LY + 5], fill=col)
    if i == 0:
        scene_apec(x + 8, LY + 8, 84, LH - 16)
    elif i == 1:
        scene_gulf(x + 8, LY + 8, 84, LH - 16)
    else:
        scene_voyager(x + 8, LY + 8, 84, LH - 16)
    tx = x + 100
    d.text((tx, LY + 8), kick, font=F(SANS_B, 11), fill=col)
    yy = LY + 23
    for ln in wrap(head, F(SERIF_B, 15), LW - 108):
        d.text((tx, yy), ln, font=F(SERIF_B, 15), fill=INK)
        yy += 17
    yy += 2
    for ln in wrap(body, F(SANS, 10), LW - 108):
        d.text((tx, yy), ln, font=F(SANS, 10), fill=(45, 45, 45))
        yy += 11.5

# ---------------------------------------------------------------- map + numbers
MY = LY + LH + 8
MH = 168
MAPW = 596
d.rectangle([MX, MY, MX + MAPW, MY + 16], fill=RULE)
d.text((MX + 8, MY + 2), "THE DAY ON THE MAP — WHERE WEDNESDAY HAPPENED", font=F(SANS_B, 12), fill=WHITE)
d.rectangle([MX, MY + 16, MX + MAPW, MY + MH], fill=MAP_BG)

LAND_SPANS = {
    0: [(3, 6), (11, 16), (26, 29), (47, 60), (64, 78)],
    1: [(1, 8), (10, 21), (25, 28), (37, 37), (43, 46), (48, 79)],
    2: [(9, 22), (39, 40), (41, 46), (47, 78)],
    3: [(8, 23), (38, 45), (47, 56), (57, 67), (71, 73)],
    4: [(8, 23), (38, 39), (42, 43), (44, 47), (48, 50), (51, 55), (58, 67), (68, 69), (70, 72)],
    5: [(9, 20), (13, 17), (37, 46), (47, 49), (50, 52), (53, 55), (56, 58), (59, 66)],
    6: [(12, 16), (36, 47), (48, 51), (56, 59), (60, 62), (63, 66), (67, 67), (68, 69)],
    7: [(14, 15), (36, 47), (48, 50), (56, 58), (59, 62), (67, 68)],
    8: [(23, 28), (36, 48), (49, 50), (57, 57), (59, 61), (62, 65)],
    9: [(23, 29), (37, 46), (60, 68)],
    10: [(23, 30), (37, 45), (62, 67), (69, 71)],
    11: [(24, 31), (38, 44), (66, 72)],
    12: [(24, 30), (38, 43), (46, 46), (64, 74)],
    13: [(25, 29), (38, 41), (63, 73)],
    14: [(25, 28), (38, 39), (67, 73)],
    15: [(25, 26), (78, 80)],
    16: [(25, 26), (77, 78)],
    17: [(25, 25)],
}
MARKS = [
    (66, 6, "SHENZHEN", "l", 0), (68, 7, "MANILA", "r", 0), (59, 7, None, None, 0),
    (47, 3, "KYIV", "l", 0), (46, 4, None, None, 0), (48, 5, "GAZA", "r", 0),
    (53, 6, "HORMUZ", "r", 11), (50, 6, None, None, 0), (47, 7, None, None, 0),
    (7, 1, "ALASKA", "r", 0), (23, 4, "WASHINGTON", "l", 0), (23, 3, None, None, 0),
    (30, 12, None, None, 0), (73, 14, "CANBERRA", "l", 0), (80, 15, None, None, 0),
]
GX, GY = MX + 11, MY + 24
SX, SY = 7.0, 7.2
for row, spans in LAND_SPANS.items():
    for c0, c1 in spans:
        for c in range(c0, c1 + 1):
            cx, cy = GX + c * SX, GY + row * SY
            d.ellipse([cx - 2.2, cy - 2.2, cx + 2.2, cy + 2.2], fill=LAND)
LF = F(SANS_B, 9)
for c, r, label, side, dy in MARKS:
    cx, cy = GX + c * SX, GY + r * SY
    d.ellipse([cx - 4.5, cy - 4.5, cx + 4.5, cy + 4.5], fill=WHITE)
    d.ellipse([cx - 3.2, cy - 3.2, cx + 3.2, cy + 3.2], fill=MARK)
    if label:
        tw = text_w(label, LF)
        lx = cx + 7 if side == "r" else cx - 7 - tw
        d.text((lx, cy - 5 + dy), label, font=LF, fill=INK, stroke_width=2, stroke_fill=MAP_BG)

NX = MX + MAPW + 12
NW = W - MX - NX
d.rectangle([NX, MY, NX + NW, MY + 16], fill=RULE)
d.text((NX + 8, MY + 2), "THE DAY IN NUMBERS", font=F(SANS_B, 12), fill=WHITE)
d.rectangle([NX, MY + 16, NX + NW, MY + MH], fill=LEAD_BG)
NF = F(SERIF_B, 19)
NL = F(SANS, 9)
cell_w = (NW - 24) // 2
for i, (num, lab) in enumerate(NUMBERS):
    cx = NX + 10 + (i % 2) * (cell_w + 8)
    cy = MY + 24 + (i // 2) * 50
    d.text((cx, cy), num, font=NF, fill=DATE_RED)
    yy = cy + 23
    for ln in wrap(lab, NL, cell_w):
        d.text((cx, yy), ln, font=NL, fill=(45, 45, 45))
        yy += 10.5

# ---------------------------------------------------------------- timeline
TY = MY + MH + 8
d.rectangle([MX, TY, W - MX, TY + 24], fill=INK)
TL = ("BY THE CLOCK (UTC)  »  before dawn: Bahrain intercepts  »  by 08:00: 126 of 141 drones downed  »  "
      "10:16: Voyager 1 crosses one light-day  »  all day: APEC + Quad sit")
_tlf = F(SANS_B, 10)
while text_w(TL, _tlf) > CW - 20:
    _tlf = F(SANS_B, _tlf.size - 1)
d.text((MX + 10, TY + 5), TL, font=_tlf, fill=WHITE)

# ---------------------------------------------------------------- regions
LEFT = ["ASIA-PACIFIC", "EUROPE & UKRAINE", "MIDDLE EAST"]
RIGHT = ["AMERICAS", "AFRICA", "OCEANIA", "CLIMATE · TECH · SPORT · CULTURE"]

HF = F(SANS_B, 11)
BF = F(SANS, 9)
SF = F(SANS_B, 12)
HLH, BLH = 11, 10
COLW = (CW - 20) // 2
TOP = TY + 32
BOTTOM = 846

def region_height(name):
    col, stories = REGIONS[name]
    h = 19
    for head, body in stories:
        h += HLH + len(wrap(body, BF, COLW - 10)) * BLH + 1
    return h + 1

def draw_region(name, x, y):
    col, stories = REGIONS[name]
    d.rectangle([x, y, x + COLW, y + 17], fill=col)
    d.text((x + 8, y + 2), name, font=SF, fill=WHITE)
    yy = y + 19
    for head, body in stories:
        d.rectangle([x + 1, yy + 3, x + 5, yy + 9], fill=col)
        d.text((x + 10, yy), head, font=HF, fill=INK)
        yy += HLH
        for ln in wrap(body, BF, COLW - 10):
            d.text((x + 10, yy), ln, font=BF, fill=(60, 60, 60))
            yy += BLH
        yy += 1
    return yy + 1

lh = sum(region_height(r) for r in LEFT)
rh = sum(region_height(r) for r in RIGHT)
print("left col height:", lh, "right col height:", rh, "available:", BOTTOM - TOP)
assert lh <= BOTTOM - TOP and rh <= BOTTOM - TOP, "region overflow"

y = TOP
for r in LEFT:
    y = draw_region(r, MX, y)
y = TOP
for r in RIGHT:
    y = draw_region(r, MX + COLW + 20, y)

# ---------------------------------------------------------------- in brief
BY = 850
d.rectangle([MX, BY, W - MX, BY + 17], fill=RULE)
d.text((MX + 8, BY + 2), "IN BRIEF — 22 MORE STORIES FROM THE DAY", font=F(SANS_B, 12), fill=WHITE)
BCOLW = (CW - 2 * 14) // 3
BF2 = F(SANS_B, 9)
yy = BY + 23
rows = (len(BRIEFS) + 2) // 3
for row in range(rows):
    for cidx in range(3):
        k = row * 3 + cidx
        if k >= len(BRIEFS):
            break
        tag, txt = BRIEFS[k]
        x = MX + cidx * (BCOLW + 14)
        d.rectangle([x + 1, yy + 3, x + 5, yy + 9], fill=RULE)
        line = tag + " · " + txt
        assert text_w(line, BF2) <= BCOLW - 10, line
        d.text((x + 10, yy), line, font=BF2, fill=INK)
    yy += 14

# ---------------------------------------------------------------- footer
FY = 989
d.line([(MX, FY), (W - MX, FY)], fill=RULE, width=2)
center("Every story happened, or was first reported, on Wednesday 18 November 2026 in some time zone. Contested claims are attributed as reported.",
       F(SANS_I, 10), FY + 5, GRAY)
center("Sources: Reuters · Associated Press · AFP · Al Jazeera · UN agencies · NASA/JPL · Yonhap · ABC · The Hindu · Geo News · official statements",
       F(SANS, 9), FY + 20, GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_v3.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
