#!/usr/bin/env python3
"""Build the entry image for make.fun bounty news-image-20261118:
'Sum up 18 November's world news in one image.'

Renders a one-page newspaper digest of Wednesday 18 November 2026:
40 stories, 7 regions, every story reported on the day itself.
Deterministic: same input data -> same PNG bytes.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
PAPER = (255, 253, 245)
INK = (22, 22, 22)
GRAY = (90, 90, 90)
RULE = (40, 40, 40)
DATE_RED = (157, 2, 8)
LEAD_BG = (243, 238, 224)

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

# ---------------------------------------------------------------- masthead
MX = 26                      # side margin
CW = W - 2 * MX              # content width

center("THE WHOLE DAY'S WORLD NEWS IN A SINGLE IMAGE", F(SANS_B, 14), 14, GRAY)
center("THE WORLD TODAY", F(SERIF_B, 58), 32)
d.line([(MX, 100), (W - MX, 100)], fill=RULE, width=3)
center("Wednesday 18 November 2026", F(SERIF_B, 41), 106, DATE_RED)
center("41 stories  ·  7 regions  ·  every story reported on the day itself, date-checked",
       F(SANS, 15), 156, GRAY)
d.line([(MX, 182), (W - MX, 182)], fill=RULE, width=1)

# ---------------------------------------------------------------- lead band
LY = 192
LW = (CW - 16) // 2
LEADS = [
    ("SHENZHEN · APEC SUMMIT", (29, 78, 137),
     "Xi & Putin meet as Trump lands",
     "Xi Jinping and Vladimir Putin opened talks in Shenzhen as Donald Trump "
     "arrived for APEC. Their first three-way summit is set for Thursday, with "
     "Ukraine, Iran and trade on the table."),
    ("THE GULF · IRAN–US CLASHES", (179, 84, 30),
     "Drones, intercepts & struck tankers",
     "Iranian drones targeted a US base in Kuwait; Bahrain intercepted "
     "attacks before dawn; US jets hit a missile site on Qeshm Island and "
     "ships were struck near Hormuz. Oil held near $93."),
]
for i, (kick, col, head, body) in enumerate(LEADS):
    x = MX + i * (LW + 16)
    d.rectangle([x, LY, x + LW, LY + 112], fill=LEAD_BG)
    d.rectangle([x, LY, x + LW, LY + 5], fill=col)
    d.text((x + 12, LY + 10), kick, font=F(SANS_B, 12), fill=col)
    d.text((x + 12, LY + 26), head, font=F(SERIF_B, 21), fill=INK)
    yy = LY + 53
    for ln in wrap(body, F(SANS, 12), LW - 24):
        d.text((x + 12, yy), ln, font=F(SANS, 12), fill=(45, 45, 45))
        yy += 15

# ---------------------------------------------------------------- stories
# (headline, one-line summary) per region
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
        ("Arsenic fears on the Thai–Myanmar border",
         "Villages sought safe water as officials traced contamination in cross-border rivers."),
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

LEFT = ["ASIA-PACIFIC", "EUROPE & UKRAINE", "MIDDLE EAST"]
RIGHT = ["AMERICAS", "AFRICA", "OCEANIA", "CLIMATE · TECH · SPORT · CULTURE"]

HF = F(SANS_B, 13)      # story headline
BF = F(SANS, 11)        # story summary
SF = F(SANS_B, 14)      # section header
HLH, BLH = 14, 12       # line heights
COLW = (CW - 20) // 2
TOP = 318
BOTTOM = 940

def region_height(name):
    col, stories = REGIONS[name]
    h = 24
    for head, body in stories:
        h += HLH + len(wrap(body, BF, COLW - 10)) * BLH + 3
    return h + 4

def draw_region(name, x, y):
    col, stories = REGIONS[name]
    d.rectangle([x, y, x + COLW, y + 20], fill=col)
    d.text((x + 8, y + 2), name, font=SF, fill=(255, 255, 255))
    yy = y + 24
    for head, body in stories:
        d.rectangle([x + 1, yy + 3, x + 5, yy + 11], fill=col)
        d.text((x + 10, yy), head, font=HF, fill=INK)
        yy += HLH
        for ln in wrap(body, BF, COLW - 10):
            d.text((x + 10, yy), ln, font=BF, fill=(60, 60, 60))
            yy += BLH
        yy += 3
    return yy + 4

# balance check
lh = sum(region_height(r) for r in LEFT)
rh = sum(region_height(r) for r in RIGHT)
print("left col height:", lh, "right col height:", rh, "available:", BOTTOM - TOP)

y = TOP
for r in LEFT:
    y = draw_region(r, MX, y)
y = TOP
for r in RIGHT:
    y = draw_region(r, MX + COLW + 20, y)

# ---------------------------------------------------------------- footer
FY = 946
d.line([(MX, FY), (W - MX, FY)], fill=RULE, width=2)
center("ALSO THIS DAY — Pakistan cuts petrol by Rs3 to Rs325 a litre · EU moves against Temu over illegal goods · Waymo pauses driverless freeway runs",
       F(SANS_B, 12), FY + 7)
center("Robert Pattinson named the new James Bond · Libya seizes a cocaine-and-pills haul in the east",
       F(SANS_B, 12), FY + 23)
center("Every story happened, or was first reported, on Wednesday 18 November 2026 in some time zone. Contested claims are attributed as reported.",
       F(SANS_I, 12), FY + 41, GRAY)
center("Sources: Reuters · Associated Press · AFP · Al Jazeera · UN agencies · Yonhap · ABC · The Hindu · official statements",
       F(SANS, 11), FY + 58, GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
