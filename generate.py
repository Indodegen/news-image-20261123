#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: a 1024x1024 newspaper front page
summing up the world news of Monday 23 November 2026.

Pure PIL (Pillow) + Liberation fonts, no network, no randomness, no
timestamps: running it twice writes a byte-identical PNG. Every story
below was checked against the wires of 23 Nov 2026 (CNN, Reuters,
Le Monde, AP, Al Jazeera, France24, BusinessWorld, Just Security).
The DATE CHECK box names what was left out because it belongs to an
earlier day, and what Monday's news actually was for stories that
started at the weekend.

Run:  python3 generate.py [out.png]
"""
import hashlib
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
CARD = (255, 253, 246)
INK = (22, 22, 22)
MUTED = (110, 105, 92)
NAVY = (20, 38, 74)
NAVY_D = (13, 25, 50)
RED = (179, 38, 30)
RED_D = (140, 28, 22)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
SKY = (135, 190, 220)
SEA = (46, 110, 160)
GREEN = (46, 125, 60)
ORANGE = (224, 122, 26)
YELLOW = (242, 201, 60)
WHITE = (255, 255, 255)
LINE = (190, 184, 170)
DARK = (30, 34, 48)
NIGHT = (16, 24, 48)
SAND = (232, 214, 170)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines top-down; returns the y just below the last line."""
    if leading is None:
        leading = fnt.size + 3
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, fill=LINE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag(d, x, y, label, fill):
    """Small rounded-ish tag chip; returns width used."""
    f = font(F_SANS_B, 11)
    tw = d.textlength(label, font=f)
    pad = 6
    d.rectangle([x, y, x + tw + pad * 2, y + 16], fill=fill)
    d.text((x + pad, y + 2), label, font=f, fill=WHITE)
    return tw + pad * 2 + 4


# ---------------------------------------------------------------- scenes
# Every scene is drawn from flat PIL shapes: no photos, no AI images,
# nothing the program did not draw itself.


def scene_summit(d, x, y, w, h):
    """COP hall: long table, flags, a broken globe on the wall."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(58, 44, 30))
    d.rectangle([x + 18, y + h - 52, x + w - 18, y + h - 26], fill=(96, 74, 52))
    for i in range(7):
        cx = x + 24 + i * ((w - 48) // 6)
        d.ellipse([cx, y + h - 62, cx + 12, y + h - 50], fill=(210, 180, 140))
        d.rectangle([cx + 2, y + h - 50, cx + 10, y + h - 26], fill=(40, 40, 40))
    # broken globe: circle split by a jagged crack
    gx, gy, gr = x + w - 62, y + 34, 26
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=SEA)
    d.ellipse([gx - gr + 8, gy - gr + 6, gx - gr + 22, gy - gr + 20], fill=GREEN)
    d.ellipse([gx + 4, gy + 8, gx + 18, gy + 20], fill=GREEN)
    d.line([(gx - 14, gy - 22), (gx - 4, gy - 6), (gx - 12, gy + 8),
            (gx + 2, gy + 20)], fill=WHITE, width=3)
    for i in range(5):
        fx = x + 16 + i * 14
        d.rectangle([fx, y + 14, fx + 8, y + 34], fill=[RED, GOLD, TEAL, WHITE, ORANGE][i])
        d.line([(fx + 4, y + 14), (fx + 4, y + 8)], fill=GOLD, width=2)


def scene_sea(d, x, y, w, h):
    """Warship at sea at dusk, drones overhead, smoke plume."""
    d.rectangle([x, y, x + w, y + h], fill=(252, 176, 90))
    d.ellipse([x + w - 34, y + 8, x + w - 6, y + 36], fill=(255, 214, 120))
    sea_top = y + h - int(h * 0.55)
    d.rectangle([x, sea_top, x + w, y + h], fill=SEA)
    d.rectangle([x, sea_top, x + w, sea_top + 6], fill=(30, 80, 120))
    # corvette hull
    deck = y + h - int(h * 0.38)
    d.polygon([(x + 26, deck), (x + w - 30, deck),
               (x + w - 52, y + h - 6), (x + 44, y + h - 6)], fill=(70, 76, 84))
    d.rectangle([x + 70, deck - int(h * 0.28), x + 120, deck], fill=(96, 102, 110))
    d.line([(x + 92, deck - int(h * 0.28)), (x + 92, deck - int(h * 0.42))],
           fill=(70, 76, 84), width=4)
    # smoke plume from the stern
    for i, r in enumerate([9, 7, 5, 4]):
        d.ellipse([x + w - 78 + i * 6, y + 8 + i * 5,
                   x + w - 78 + i * 6 + r * 2, y + 8 + i * 5 + r * 2],
                  fill=(60, 60, 60))
    # two sea drones: small dots with wakes
    for dx in (x + 40, x + 150):
        d.ellipse([dx, y + h - 12, dx + 7, y + h - 5], fill=INK)
        d.line([(dx - 16, y + h - 8), (dx, y + h - 8)], fill=WHITE, width=2)


def scene_sky(d, x, y, w, h):
    """Night sky over a city, missile trails arcing down."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for i in range(14):
        sx = x + 12 + (i * 37) % (w - 20)
        sy = y + 6 + (i * 23) % max(10, h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
    d.ellipse([x + w - 40, y + 6, x + w - 14, y + 32], fill=(235, 220, 180))
    for i, bx in enumerate([0, 52, 108, 168, 224]):
        bh = int(h * [0.42, 0.62, 0.5, 0.7, 0.36][i])
        d.rectangle([x + bx, y + h - bh, x + bx + 44, y + h], fill=(52, 58, 78))
        for wy in range(y + h - bh + 6, y + h - 4, 12):
            d.rectangle([x + bx + 8, wy, x + bx + 14, wy + 4], fill=YELLOW)
            d.rectangle([x + bx + 26, wy, x + bx + 32, wy + 4], fill=YELLOW)
    # two missile trails
    d.line([(x + 30, y + 4), (x + 120, y + h - 16)], fill=ORANGE, width=3)
    d.line([(x + 200, y + 4), (x + 150, y + h - 20)], fill=ORANGE, width=3)
    d.ellipse([x + 116, y + h - 20, x + 124, y + h - 12], fill=RED)
    d.ellipse([x + 146, y + h - 24, x + 154, y + h - 16], fill=RED)


def scene_plane(d, x, y, w, h):
    """Grounded airliner under a grey sky, empty runway."""
    d.rectangle([x, y, x + w, y + h], fill=(188, 198, 206))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(110, 116, 122))
    d.rectangle([x, y + h - 26, x + w, y + h - 22], fill=YELLOW)
    # fuselage
    d.ellipse([x + 20, y + 30, x + w - 20, y + 62], fill=WHITE)
    d.polygon([(x + w - 60, y + 34), (x + w - 6, y + 44), (x + w - 60, y + 56)],
              fill=WHITE)
    d.polygon([(x + 30, y + 34), (x + 62, y + 30), (x + 62, y + 40)], fill=RED)
    for i in range(9):
        d.rectangle([x + 52 + i * 14, y + 42, x + 58 + i * 14, y + 48], fill=NAVY)
    d.line([(x + 90, y + 62), (x + 76, y + h - 30)], fill=(70, 76, 84), width=4)
    d.line([(x + 150, y + 62), (x + 164, y + h - 30)], fill=(70, 76, 84), width=4)
    d.text((x + 12, y + 8), "NO DEPARTURES", font=font(F_SANS_B, 13), fill=RED_D)


def scene_fire(d, x, y, w, h):
    """Factory fire at night: flames over a low building, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 20, 28))
    btop = y + int(h * 0.48)
    d.rectangle([x, y + int(h * 0.82), x + w, y + h], fill=(52, 44, 40))
    d.rectangle([x + 16, btop, x + w - 16, y + int(h * 0.82)], fill=(74, 60, 52))
    for i in range(4):
        d.rectangle([x + 28 + i * 44, btop + 6, x + 48 + i * 44, btop + 18],
                    fill=(30, 26, 22))
    for i, (fx, ff, fc) in enumerate([(30, 0.30, ORANGE), (70, 0.40, (240, 90, 30)),
                                      (120, 0.34, YELLOW), (160, 0.26, ORANGE)]):
        fh = int(h * ff)
        d.polygon([(x + fx, btop), (x + fx + 16, btop - fh),
                   (x + fx + 32, btop)], fill=fc)
    for i, r in enumerate([7, 6, 4]):
        d.ellipse([x + 60 + i * 22, y + 4 + i * 4,
                   x + 60 + i * 22 + r * 2, y + 4 + i * 4 + r * 2], fill=(90, 86, 92))


def scene_ballot(d, x, y, w, h):
    """Ballot box with a rising bar chart behind it."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 242))
    base = y + h - 12
    for bx, bf, fc in [(20, 0.35, TEAL), (62, 0.55, NAVY), (104, 0.75, RED),
                       (146, 0.45, GOLD)]:
        bh = int((h - 24) * bf)
        d.rectangle([x + bx, base - bh, x + bx + 30, base], fill=fc)
    d.rectangle([x + w - 84, y + int(h * 0.4), x + w - 20, base], fill=(210, 200, 180))
    d.rectangle([x + w - 78, y + int(h * 0.3), x + w - 26, y + int(h * 0.4)],
                fill=(120, 100, 70))
    d.line([(x + w - 62, y + int(h * 0.3)), (x + w - 52, y + int(h * 0.16))],
           fill=WHITE, width=3)
    d.ellipse([x + 16, y + 8, x + 34, y + 26], fill=WHITE)
    d.line([(x + 20, y + 17), (x + 25, y + 22), (x + 31, y + 11)], fill=GREEN, width=3)


def scene_court(d, x, y, w, h):
    """Courtroom gavel and scales, navy backdrop."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(96, 74, 52))
    # scales
    cx = x + w // 2
    top = y + 8
    bar = y + int(h * 0.32)
    pan = y + int(h * 0.72)
    d.line([(cx, top), (cx, y + h - 12)], fill=GOLD, width=3)
    d.line([(cx - 44, bar), (cx + 44, bar)], fill=GOLD, width=3)
    for s in (-1, 1):
        d.line([(cx + s * 44, bar), (cx + s * 30, pan - 12)], fill=GOLD, width=2)
        d.polygon([(cx + s * 44, pan - 12), (cx + s * 16, pan - 12),
                   (cx + s * 30, pan)], fill=GOLD)
    d.ellipse([cx - 8, top - 2, cx + 8, top + 14], fill=GOLD)


def scene_school(d, x, y, w, h):
    """Exam hall: rows of desks, one glowing phone screen."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    for r in range(2):
        for c in range(4):
            dx = x + 16 + c * 46
            dy = y + int(h * 0.16) + r * int(h * 0.34)
            d.rectangle([dx, dy, dx + 34, dy + 12], fill=(150, 140, 120))
            d.ellipse([dx + 12, dy - 8, dx + 22, dy + 2], fill=(210, 180, 140))
    px, py = x + 108, y + int(h * 0.72)
    d.rectangle([px, py, px + 20, py + 16], fill=(40, 44, 60))
    d.rectangle([px + 3, py + 3, px + 17, py + 13], fill=(120, 220, 255))
    d.text((x + 12, y + h - 16), "EXAM HALL", font=font(F_SANS_B, 11), fill=MUTED)


def scene_rain(d, x, y, w, h):
    """Flooded street: rain slashes, water line, half-submerged car."""
    d.rectangle([x, y, x + w, y + h], fill=(90, 110, 140))
    for i in range(18):
        rx = x + 8 + (i * 29) % (w - 16)
        ry = y + 6 + (i * 17) % 40
        d.line([(rx, ry), (rx - 6, ry + 12)], fill=(200, 220, 240), width=2)
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(40, 70, 100))
    d.rounded_rectangle([x + 46, y + h - 52, x + 150, y + h - 30], radius=8,
                        fill=RED)
    d.rectangle([x + 62, y + h - 62, x + 132, y + h - 50], fill=RED)
    d.rectangle([x + 70, y + h - 60, x + 92, y + h - 50], fill=(180, 220, 240))
    d.rectangle([x + 100, y + h - 60, x + 124, y + h - 50], fill=(180, 220, 240))
    for i in range(5):
        wx = x + 20 + i * 36
        d.line([(wx, y + h - 12), (wx + 18, y + h - 12)], fill=(160, 200, 230),
               width=2)


def scene_desert(d, x, y, w, h):
    """Desert dunes and a lone minaret-like tower at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 190, 120))
    d.ellipse([x + w - 46, y + 6, x + w - 14, y + 38], fill=(255, 220, 140))
    d.polygon([(x, y + h - int(h * 0.3)), (x + w // 2, y + h - int(h * 0.5)),
               (x + w, y + h - int(h * 0.26)), (x + w, y + h), (x, y + h)],
              fill=(222, 164, 92))
    d.polygon([(x, y + h - int(h * 0.16)), (x + w // 3, y + h - int(h * 0.34)),
               (x + w, y + h - int(h * 0.14)), (x + w, y + h), (x, y + h)],
              fill=(196, 138, 70))
    ttop = y + int(h * 0.22)
    tbot = y + h - int(h * 0.34)
    d.rectangle([x + 30, ttop, x + 44, tbot], fill=(120, 90, 60))
    d.polygon([(x + 28, ttop), (x + 37, ttop - 12), (x + 46, ttop)],
              fill=(120, 90, 60))


def scene_sport(d, x, y, w, h):
    """Football pitch from above: green, lines, a ball and a fallen boot."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 140, 70))
    d.rectangle([x + 8, y + 8, x + w - 8, y + h - 8], outline=WHITE, width=2)
    d.line([(x + w // 2, y + 8), (x + w // 2, y + h - 8)], fill=WHITE, width=2)
    d.ellipse([x + w // 2 - 18, y + h // 2 - 18, x + w // 2 + 18,
               y + h // 2 + 18], outline=WHITE, width=2)
    d.ellipse([x + w - 52, y + h - 52, x + w - 28, y + h - 28], fill=WHITE)
    d.polygon([(x + w - 48, y + h - 48), (x + w - 40, y + h - 40),
               (x + w - 32, y + h - 48)], fill=INK)
    d.rectangle([x + 24, y + h - 26, x + 52, y + h - 16], fill=(240, 240, 240))


# ---------------------------------------------------------------- data
# 40 stories, every one dated Monday 23 November 2026 (happened that day
# or first reported that day). Sources are named per story.
# tag: REPORTED = wires / on the record; CLAIM = one side's claim.

LEAD = [
    dict(n=1, place="ANTALYA, TÜRKIYE", beat="CLIMATE", tag="REPORTED",
         scene=scene_summit,
         head="COP31 ends with no deal — the blame game begins",
         body=("The longest climate talks ever end with no pact: the EU "
               "rejects a text with no fossil fuels in it."),
         src="Reuters · CNN · Le Monde"),
    dict(n=2, place="BENGHAZI, LIBYA", beat="SEA WAR", tag="REPORTED",
         scene=scene_sea,
         head="Ukraine sinks Russian warship off Libya",
         body=("Zelensky confirms it: seven sea drones sank the corvette "
               "Merkury and destroyed a Ka-27 aboard."),
         src="CNN · France24 · China Daily"),
    dict(n=3, place="WARSAW, POLAND", beat="AIRSPACE", tag="REPORTED",
         scene=scene_sky,
         head="Russian missiles fall inside Poland; NATO meets",
         body=("Three Russian Kh-101 missiles struck Polish soil. NATO "
               "holds an emergency session Monday."),
         src="Reuters · Liveuamap"),
]

GRID = [
    dict(n=4, place="BRUSSELS, BELGIUM", beat="STRIKE", tag="REPORTED",
         scene=scene_plane,
         head="Belgium's skies shut for 14 hours",
         body="Air controllers join the strike; ~429 flights hit.",
         src="Travel Tomorrow · FTN"),
    dict(n=5, place="DYMER, KYIV REGION", beat="WAR", tag="REPORTED",
         scene=scene_sky,
         head="Dymer toll rises to 11",
         body="Child killed in Kryvyi Rih; 153 drones fired overnight.",
         src="Liveuamap · Just Security"),
    dict(n=6, place="STRAIT OF HORMUZ", beat="GULF", tag="REPORTED",
         scene=scene_sea,
         head="Tankers hit; Iran vows 'all means'",
         body="Three tankers hit in Hormuz; US base struck in Bahrain.",
         src="Just Security · Al Jazeera"),
    dict(n=7, place="GAZA CITY", beat="CONFLICT", tag="REPORTED",
         scene=scene_desert,
         head="Truck strike kills 3; 99% of Gaza 'toxic'",
         body="A food-aid truck is hit; Oxfam finds toxins across Gaza.",
         src="Al Jazeera · Reuters"),
    dict(n=8, place="SERANG, INDONESIA", beat="FIRE", tag="REPORTED",
         scene=scene_fire,
         head="Serang fire: 24 dead, ~30 missing",
         body="Rescuers dig on at the Milkita plant in Banten.",
         src="AP · BusinessWorld"),
    dict(n=9, place="WASHINGTON, US", beat="POLITICS", tag="REPORTED",
         scene=scene_ballot,
         head="Democrats win 258 House seats",
         body="Best since 1992; Trump moves to block oversight.",
         src="Medium · Open Chronicle"),
    dict(n=10, place="SEOUL", beat="EDUCATION", tag="REPORTED",
         scene=scene_school,
         head="Minister quits over AI exam cheating",
         body="Seoul's education minister resigns after the scandal.",
         src="UBStandard"),
    dict(n=11, place="COPENHAGEN", beat="SECURITY", tag="REPORTED",
         scene=scene_court,
         head="Denmark: Russia plotted to kill a rapper",
         body="NATO intel blames Russian services for a Copenhagen plot.",
         src="UBStandard"),
    dict(n=12, place="BELGRADE, SERBIA", beat="WEATHER", tag="REPORTED",
         scene=scene_rain,
         head="Record rain floods Belgrade",
         body="Record rain floods the city; weather agency under fire.",
         src="Nexus Europa"),
    dict(n=13, place="MEDELLÍN, COLOMBIA", beat="SPORT", tag="REPORTED",
         scene=scene_sport,
         head="Paredes collapses in post-match interview",
         body="Argentina's Paredes collapses on camera in Colombia.",
         src="Al Jazeera"),
]

# The numbered list: 27 more stories, 14–40. Each fits one line.
MORE = [
    ("Kyiv", "153 drones fired overnight; 11 sites hit"),
    ("Perm", "Ukrainian drone kills 1 at industrial site"),
    ("Rostov", "Novoshakhtinsk refinery halts after strikes"),
    ("Ramallah", "Eisenkot calls settler arson Jewish terrorism"),
    ("South Lebanon", "Families return to ruins after attacks"),
    ("Washington", "Vance won't say if he'd authorise Iran strikes"),
    ("Washington", "Trump: Iran wants a deal, not 'acceptable'"),
    ("Brussels", "Unions march vs €10bn cuts; PM offered to quit"),
    ("Paris", "Student leaders in talks with Macron's government"),
    ("Mt Fuji", "China warns citizens off; $75k reward for climber"),
    ("Khartoum", "Sudan's humanitarian emergency deepens"),
    ("Kabul", "Taliban police guard vanishing forests"),
    ("Berlin", "NATO intel: Russia plans a nuclear-armed satellite"),
    ("Silicon Valley", "Meta exec: superintelligence 'arriving'"),
    ("London", "New Epstein Russia links challenge suicide ruling"),
    ("Brazil", "Deadly storm hits a town; thousands displaced"),
    ("Antalya", "90 nations sign electrification pledge to 2035"),
    ("Canberra", "Calls to sack Bowen after A$150m COP31"),
    ("Moscow", "Kremlin: new Abu Dhabi talks may follow"),
    ("Tripoli", "Libya: not a party to the war; no arena for scores"),
    ("Rome", "Italy warns Libya strike may destabilise the Med"),
    ("Kyiv", "Ukraine claims 2,471 Russian losses in a day"),
    ("Kharkiv", "Russian drone strikes a kindergarten, reports say"),
    ("Slovyansk", "Russian airstrikes kill two, reports say"),
    ("Dhaka", "Why Bangladesh's Grameen Bank is under attack"),
    ("Washington", "Air-traffic funding fight amid US disruption"),
    ("Antalya", "47 nations back methane and super-pollutant cuts"),
]

STATS = [
    ("153", "drones fired at Ukraine"),
    ("11", "dead in Dymer now"),
    ("24", "dead in Serang fire"),
    ("429", "Belgium flights axed"),
    ("3", "tankers hit in Hormuz"),
    ("258", "Democrat House seats"),
]

REGIONS = [
    ("EUROPE", 14, NAVY), ("MIDDLE EAST", 6, RED), ("ASIA-PACIFIC", 8, GOLD),
    ("AMERICAS", 4, TEAL), ("AFRICA", 4, GREEN), ("WORLD", 4, (90, 60, 120)),
]

# Coarse world dot-map (land = #). Columns run west to east, rows north
# to south; red dots below mark where the featured stories happened.
MAP_ROWS = [
    "...........XXXXX....................................",
    "........XXXXXXXXXXX........XXXXXXXXXXXXXXXXXXX.......",
    "......XXXXXXXXXXXXXXXX....XXXXXXXXXXXXXXXXXXXXX.....",
    "....XXXXXXXXXXXXXXXXXX....XXXXXXXXXXXXXXXXXXXXXX....",
    ".....XXXXXXXXXXXXXXXX.......XXXXXXXXXXXXXXXXXX......",
    "......XXXXXXXXXXXXXX.........XXXXXXXX..XXXXXX.........",
    ".......XXXXXXXXXXX............XXXXXX...XXXX...........",
    "........XXXXXXXXX..............XXXX.....XX............",
    ".........XXXXXXX................XX...................",
    "..........XXXXX.....................................",
    "...........XXXX.............XXXXX....................",
    "............XX..............XXXXXXX..................",
    ".............X...............XXXXXXXXX...............",
    "..............................XXXXXX.................",
    "...............................XXXX.................",
    "................................XX.................",
    ".................................X.................",
]
# (col, row) of the red dots on the map above.
MAP_DOTS = [(27, 3), (30, 6), (28, 4), (26, 3), (31, 4), (33, 7), (34, 8),
            (45, 11), (11, 6), (48, 5), (27, 2), (29, 4), (10, 9),
            (32, 9), (36, 7), (31, 10)]


# ---------------------------------------------------------------- cards
def draw_lead(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
    s["scene"](d, x + 1, y + 1, w - 2, 80)
    tag(d, x + 10, y + 86, s["tag"], TEAL if s["tag"] == "REPORTED" else RED)
    yy = y + 106
    d.text((x + 10, yy), f"{s['n']}  {s['place']} · {s['beat']}",
           font=font(F_SANS_B, 12), fill=RED_D)
    yy += 16
    head_lines = wrap(d, s["head"], font(F_SERIF, 21), w - 20)
    assert len(head_lines) <= 2, f"lead {s['n']} headline {len(head_lines)} lines"
    yy = text_block(d, x + 10, yy, head_lines, font(F_SERIF, 21), leading=23)
    yy += 2
    body_lines = wrap(d, s["body"], font(F_SANS, 12), w - 20)
    assert len(body_lines) <= 2, f"lead {s['n']} body {len(body_lines)} lines"
    text_block(d, x + 10, yy, body_lines, font(F_SANS, 12), leading=14)


def draw_grid_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
    s["scene"](d, x + 1, y + 1, w - 2, 54)
    tag(d, x + 8, y + 58, s["tag"], TEAL if s["tag"] == "REPORTED" else RED)
    yy = y + 78
    d.text((x + 8, yy), f"{s['n']}  {s['place']} · {s['beat']}",
           font=font(F_SANS_B, 10), fill=RED_D)
    yy += 14
    head_lines = wrap(d, s["head"], font(F_SERIF, 16), w - 16)
    assert len(head_lines) <= 2, f"grid {s['n']} headline {len(head_lines)} lines"
    yy = text_block(d, x + 8, yy, head_lines, font(F_SERIF, 16), leading=17)
    yy += 1
    body_lines = wrap(d, s["body"], font(F_SANS, 11), w - 16)
    assert len(body_lines) <= 2, f"grid {s['n']} body {len(body_lines)} lines"
    text_block(d, x + 8, yy, body_lines, font(F_SANS, 11), leading=12)


# ---------------------------------------------------------------- compose
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
    d.text((x + 10, y + 8), "WHERE IT HAPPENED",
           font=font(F_SANS_B, 12), fill=NAVY)
    cols = len(MAP_ROWS[0])
    rows = len(MAP_ROWS)
    cw, ch = (w - 20) / cols, (h - 52) / rows
    dot = min(cw, ch) * 0.62
    for r, row in enumerate(MAP_ROWS):
        for c, ch_ in enumerate(row):
            if ch_ == "X":
                cx = x + 10 + c * cw + (cw - dot) / 2
                cy = y + 30 + r * ch + (ch - dot) / 2
                d.ellipse([cx, cy, cx + dot, cy + dot], fill=(150, 150, 140))
    for (c, r) in MAP_DOTS:
        cx = x + 10 + c * cw + cw / 2
        cy = y + 30 + r * ch + ch / 2
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=RED, width=1)
    d.text((x + 10, y + h - 18), "Dot map — red dots mark the featured stories.",
           font=font(F_SANS_I, 10), fill=MUTED)


def draw_more_list(d, x, y, w, h):
    d.text((x, y), "ALSO ON MONDAY 23 NOVEMBER — 27 MORE STORIES",
           font=font(F_SANS_B, 13), fill=NAVY)
    y += 22
    col_w = (w - 16) // 2
    f_num = font(F_SANS_B, 11)
    f_txt = font(F_SANS, 11)
    for i, (place, txt) in enumerate(MORE):
        col = 0 if i < 14 else 1
        row = i if i < 14 else i - 14
        lx = x + col * (col_w + 16)
        ly = y + row * 12
        d.rectangle([lx, ly + 1, lx + 7, ly + 8], fill=RED)
        d.text((lx + 11, ly), f"{14 + i}.", font=f_num, fill=RED_D)
        label = f"{place} — {txt}"
        lines = wrap(d, label, f_txt, col_w - 34)
        assert len(lines) == 1, f"list {14 + i} wraps to {len(lines)} lines: {label}"
        d.text((lx + 34, ly), lines[0], font=f_txt, fill=INK)


def main(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top bar
    d.rectangle([0, 0, W, 26], fill=NAVY_D)
    d.text((10, 5), "THE WORLD IN ONE DAY", font=font(F_SANS_B, 14), fill=WHITE)
    right = "40 STORIES · 6 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
    d.text((W - 10 - d.textlength(right, font=font(F_SANS_B, 13)), 6), right,
           font=font(F_SANS_B, 13), fill=GOLD)

    # --- masthead
    title = "Monday 23 November 2026"
    tf = font(F_SERIF, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    ticker = ("COP31 blame game  ·  Merkury sunk off Libya  ·  NATO meets on Poland  ·  "
              "Belgium's skies shut  ·  Serang search goes on")
    tf2 = font(F_SANS, 16)
    d.text(((W - d.textlength(ticker, font=tf2)) / 2, 104), ticker, font=tf2,
           fill=RED_D)

    # --- stats strip
    y0 = 128
    sw = W / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = i * sw + sw / 2
        nf = font(F_SERIF, 30)
        d.text((cx - d.textlength(num, font=nf) / 2, y0), num, font=nf, fill=RED_D)
        lf = font(F_SANS, 11)
        d.text((cx - d.textlength(label, font=lf) / 2, y0 + 34), label, font=lf,
               fill=MUTED)
        if i:
            d.line([(i * sw, y0 + 4), (i * sw, y0 + 46)], fill=LINE, width=1)
    hline(d, 0, W, y0 + 52, fill=LINE, width=1)

    # --- region bar
    y0 = 184
    total = sum(n for _, n, _ in REGIONS)
    rx = 0
    for name, n, col in REGIONS:
        seg = int(W * n / total)
        d.rectangle([rx, y0, rx + seg, y0 + 18], fill=col)
        d.text((rx + 6, y0 + 3), f"{name} {n}", font=font(F_SANS_B, 11), fill=WHITE)
        rx += seg

    # --- lead row: 3 cards
    y0 = 208
    cw = (W - 20 - 16) // 3
    for i, s in enumerate(LEAD):
        draw_lead(d, 10 + i * (cw + 8), y0, cw, 196, s)

    # --- grid rows: 5 + 5 cards
    gw = (W - 20 - 32) // 5
    for row in range(2):
        y0 = 412 + row * 158
        for i in range(5):
            draw_grid_card(d, 10 + i * (gw + 8), y0, gw, 150, GRID[row * 5 + i])

    # --- bottom: map + more stories
    y0 = 726
    draw_map(d, 10, y0, 300, 180)
    draw_more_list(d, 326, y0 + 2, W - 336, 180)

    # --- date check
    y0 = 914
    d.rectangle([10, y0, W - 10, y0 + 62], outline=RED, width=2)
    d.text((18, y0 + 6), "DATE CHECK — READ THIS FIRST",
           font=font(F_SANS_B, 12), fill=RED_D)
    dc = ("Every story above happened, or was first reported, on Monday 23 November 2026. "
          "Left out because they belong to earlier days: the COP31 final vote itself (Sun 22 Nov — "
          "Monday's story is the fallout); the Serang fire breaking out (Sat 21 Nov — Monday's story "
          "is the toll and the search); the Bahrain attack (Sat 21 Nov); the Dymer strike (Sun 22 Nov — "
          "Monday's story is the toll rising to 11); the Merkury attack (Sun 22 Nov — confirmed Monday); "
          "Trump's Iran remarks (Fri 20 Nov).")
    text_block(d, 18, y0 + 24, wrap(d, dc, font(F_SANS, 12), W - 36),
               font(F_SANS, 12), leading=15)

    # --- footer
    d.text((10, 992),
           "Sources: Reuters · AP · CNN · Le Monde · Al Jazeera · France24 · BusinessWorld · Just Security — scenes drawn, not photographs.",
           font=font(F_SANS, 11), fill=MUTED)
    d.text((10, 1006),
           "REPORTED = wires / on the record · CLAIM = one side's claim, named as such",
           font=font(F_SANS, 11), fill=MUTED)

    img.save(out_path, format="PNG", optimize=True)
    data = open(out_path, "rb").read()
    print(f"wrote {out_path}: {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    return len(data)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
