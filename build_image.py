#!/usr/bin/env python3
"""Build v2 of the entry image for make.fun bounty news-image-20261118.

One-page newspaper digest of Wednesday 18 November 2026:
52 stories, 7 regions, 2 drawn lead scenes, a westward day-timeline.
Every story reported on the day itself. Deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (255, 253, 245)
INK = (22, 22, 22)
GRAY = (90, 90, 90)
RULE = (40, 40, 40)
DATE_RED = (157, 2, 8)
LEAD_BG = (243, 238, 224)
WHITE = (255, 255, 255)

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
     "arrived for APEC. Their first three-way summit is set for Thursday, with "
     "Ukraine, Iran and trade on the table."),
    ("THE GULF · IRAN–US CLASHES", (179, 84, 30),
     "Drones, intercepts & struck tankers",
     "Iranian drones targeted a US base in Kuwait and, Tehran said, US forces "
     "in Jordan; Bahrain intercepted attacks before dawn; US jets hit a "
     "missile site on Qeshm Island. Oil held near $93."),
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
        ("Slovaks protest the Fico government",
         "Thousands marched in Bratislava against the PM's stance on Russia and Ukraine."),
        ("Italy passes its antisemitism law",
         "Final parliamentary approval, amid debate over free-expression limits."),
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
        ("Ceasefire monitors sound the alarm",
         "The US-backed Board of Peace warned the Gaza truce could collapse without action."),
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
        ("Rare contact with isolated Amazon people",
         "Brazil reports raised disease and land-rights alarms for an uncontacted community."),
    ]),
    "AFRICA": ((166, 124, 0), [
        ("Sudan's army advances in West Kordofan",
         "Army gains piled pressure on the RSF as the humanitarian crisis deepened."),
        ("Chad closes its border with Sudan",
         "N'Djamena shut the frontier as fighting across the border in Sudan intensified."),
        ("Nigeria votes to allow state police",
         "Landmark reform would let states raise their own police forces for the first time."),
        ("Ebola vaccines reach Phase 2 in DR Congo",
         "Two candidates will be tested for safety and immune response."),
    ]),
    "OCEANIA": ((0, 131, 143), [
        ("Australia sanctions West Bank settlers",
         "Canberra targeted 3 people and 4 groups over settlement violence (FM Penny Wong)."),
        ("Australia's pay gap hits a record low",
         "The national gender pay gap fell to its smallest ever recorded."),
        ("New Zealand tsunami warning withdrawn",
         "The alert was lifted after offshore activity off the North Island."),
    ]),
    "CLIMATE · TECH · SPORT · CULTURE": ((106, 27, 154), [
        ("COP31 talks enter their decisive phase",
         "Antalya negotiators faced a draft text with 144 disputed items before Friday's deadline."),
        ("Nvidia board: no return for Huang",
         "Directors ruled out reinstating Jensen Huang as CEO; the chip forecast still beat hopes."),
        ("Measles is back: US loses elimination status",
         "UNICEF warned of a global resurgence as vaccination gaps widened."),
        ("F1 to broadcast drivers' heartbeats",
         "A four-year WHOOP deal, unveiled in Las Vegas, puts live health data on screen from 2027."),
        ("EU–Indonesia trade deal gets green light",
         "The EU Council approved signing the CEPA trade and investment agreements."),
    ]),
}

BRIEFS = [
    ("THAI–MYANMAR", "Villages fear arsenic in border rivers"),
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
    ("EU", "Brussels moves against Temu over illegal goods"),
    ("PAKISTAN", "Petrol cut by Rs3 to Rs325 a litre"),
    ("NETHERLANDS", "Youngest, first openly gay PM sworn in"),
]

TOTAL = len(LEADS) + sum(len(v[1]) for v in REGIONS.values()) + len(BRIEFS)
print("story count:", TOTAL)
assert TOTAL == 52, TOTAL

# ---------------------------------------------------------------- masthead
center("THE WHOLE DAY'S WORLD NEWS IN A SINGLE IMAGE", F(SANS_B, 12), 10, GRAY)
center("THE WORLD TODAY", F(SERIF_B, 50), 26)
d.line([(MX, 86), (W - MX, 86)], fill=RULE, width=3)
center("Wednesday 18 November 2026", F(SERIF_B, 36), 92, DATE_RED)
center("52 stories  ·  7 regions  ·  2 drawn scenes  ·  every story reported on the day itself, date-checked",
       F(SANS, 14), 136, GRAY)
d.line([(MX, 160), (W - MX, 160)], fill=RULE, width=1)

# ---------------------------------------------------------------- lead scenes
def scene_apec(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(173, 206, 235))
    d.ellipse([x + w - 34, y + 8, x + w - 10, y + 32], fill=(250, 204, 60))
    base = y + h
    for bx, bw, bh in [(2, 20, 44), (24, 16, 60), (42, 22, 36), (66, 15, 52), (83, 20, 40), (100, 16, 58)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(43, 62, 92))
    for px, flag in [(18, "cn"), (52, "ru"), (86, "us")]:
        d.line([(x + px, base), (x + px, base - 78)], fill=(30, 30, 30), width=2)
        fx, fy = x + px + 2, base - 78
        if flag == "cn":
            d.rectangle([fx, fy, fx + 24, fy + 15], fill=(222, 41, 16))
            for sx, sy in [(3, 3), (8, 2), (9, 5), (8, 8), (3, 10)]:
                d.point((fx + sx, fy + sy), fill=(255, 222, 0))
                d.rectangle([fx + sx, fy + sy, fx + sx + 1, fy + sy + 1], fill=(255, 222, 0))
        elif flag == "ru":
            d.rectangle([fx, fy, fx + 24, fy + 5], fill=WHITE)
            d.rectangle([fx, fy + 5, fx + 24, fy + 10], fill=(0, 57, 166))
            d.rectangle([fx, fy + 10, fx + 24, fy + 15], fill=(213, 43, 30))
        else:
            for i in range(5):
                d.rectangle([fx, fy + i * 3, fx + 24, fy + i * 3 + 2],
                            fill=(178, 34, 52) if i % 2 == 0 else WHITE)
            d.rectangle([fx, fy, fx + 11, fy + 8], fill=(60, 59, 110))

def scene_gulf(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 224, 178))
    d.rectangle([x, y + int(h * 0.45), x + w, y + h], fill=(38, 110, 138))
    d.ellipse([x + 10, y + 8, x + 34, y + 32], fill=(244, 164, 40))
    # tanker
    ty = y + int(h * 0.62)
    d.polygon([(x + 14, ty), (x + w - 12, ty), (x + w - 24, ty + 16), (x + 24, ty + 16)], fill=(35, 35, 40))
    d.rectangle([x + 26, ty - 7, x + w - 30, ty], fill=(90, 90, 96))
    d.rectangle([x + w - 40, ty - 20, x + w - 28, ty - 7], fill=(60, 60, 66))
    d.rectangle([x + w - 36, ty - 26, x + w - 32, ty - 20], fill=(178, 34, 52))
    # drones
    for cx, cy in [(x + 34, y + 16), (x + 66, y + 10)]:
        d.line([(cx - 6, cy - 4), (cx + 6, cy + 4)], fill=(30, 30, 30), width=2)
        d.line([(cx - 6, cy + 4), (cx + 6, cy - 4)], fill=(30, 30, 30), width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(30, 30, 30))
    # intercept arc
    d.arc([x + 40, y + 18, x + w - 6, y + 74], start=200, end=320, fill=(178, 34, 52), width=2)

LY = 170
LW = (CW - 16) // 2
LH = 126
for i, (kick, col, head, body) in enumerate(LEADS):
    x = MX + i * (LW + 16)
    d.rectangle([x, LY, x + LW, LY + LH], fill=LEAD_BG)
    d.rectangle([x, LY, x + LW, LY + 5], fill=col)
    if i == 0:
        scene_apec(x + 10, LY + 12, 118, LH - 22)
    else:
        scene_gulf(x + 10, LY + 12, 118, LH - 22)
    tx = x + 140
    d.text((tx, LY + 11), kick, font=F(SANS_B, 12), fill=col)
    d.text((tx, LY + 27), head, font=F(SERIF_B, 19), fill=INK)
    yy = LY + 54
    for ln in wrap(body, F(SANS, 11), LW - 152):
        d.text((tx, yy), ln, font=F(SANS, 11), fill=(45, 45, 45))
        yy += 14

# ---------------------------------------------------------------- timeline
TY = LY + LH + 8
d.rectangle([MX, TY, W - MX, TY + 24], fill=INK)
TL = ("ONE DAY, WESTWARD  »  SHENZHEN: APEC opens  »  MANILA: Quad meets  »  ANTALYA: COP31 endgame  »  "
      "KYIV: drone night  »  GAZA: winter warning  »  RIYADH: missile downed  »  ALASKA: Senate flips")
_tlf = F(SANS_B, 10)
while text_w(TL, _tlf) > CW - 20:
    _tlf = F(SANS_B, _tlf.size - 1)
d.text((MX + 10, TY + 5), TL, font=_tlf, fill=WHITE)

# ---------------------------------------------------------------- regions
LEFT = ["ASIA-PACIFIC", "EUROPE & UKRAINE", "MIDDLE EAST"]
RIGHT = ["AMERICAS", "AFRICA", "OCEANIA", "CLIMATE · TECH · SPORT · CULTURE"]

HF = F(SANS_B, 12)
BF = F(SANS, 10)
SF = F(SANS_B, 13)
HLH, BLH = 12, 10
COLW = (CW - 20) // 2
TOP = TY + 32
BOTTOM = 850

def region_height(name):
    col, stories = REGIONS[name]
    h = 21
    for head, body in stories:
        h += HLH + len(wrap(body, BF, COLW - 10)) * BLH + 1
    return h + 2

def draw_region(name, x, y):
    col, stories = REGIONS[name]
    d.rectangle([x, y, x + COLW, y + 18], fill=col)
    d.text((x + 8, y + 2), name, font=SF, fill=WHITE)
    yy = y + 21
    for head, body in stories:
        d.rectangle([x + 1, yy + 3, x + 5, yy + 10], fill=col)
        d.text((x + 10, yy), head, font=HF, fill=INK)
        yy += HLH
        for ln in wrap(body, BF, COLW - 10):
            d.text((x + 10, yy), ln, font=BF, fill=(60, 60, 60))
            yy += BLH
        yy += 1
    return yy + 2

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
BY = 856
d.rectangle([MX, BY, W - MX, BY + 18], fill=RULE)
d.text((MX + 8, BY + 2), "IN BRIEF — 15 MORE STORIES FROM THE DAY", font=F(SANS_B, 13), fill=WHITE)
BCOLW = (CW - 2 * 14) // 3
BF2 = F(SANS_B, 10)
yy = BY + 26
for row in range(5):
    for cidx in range(3):
        tag, txt = BRIEFS[row * 3 + cidx]
        x = MX + cidx * (BCOLW + 14)
        d.rectangle([x + 1, yy + 3, x + 5, yy + 10], fill=RULE)
        line = tag + " · " + txt
        assert text_w(line, BF2) <= BCOLW - 10, line
        d.text((x + 10, yy), line, font=BF2, fill=INK)
    yy += 16

# ---------------------------------------------------------------- footer
FY = 972
d.line([(MX, FY), (W - MX, FY)], fill=RULE, width=2)
center("Every story happened, or was first reported, on Wednesday 18 November 2026 in some time zone. Contested claims are attributed as reported.",
       F(SANS_I, 11), FY + 7, GRAY)
center("Sources: Reuters · Associated Press · AFP · Al Jazeera · UN agencies · Yonhap · ABC · The Hindu · Geo News · official statements",
       F(SANS, 10), FY + 24, GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_v2.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
