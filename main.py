#!/usr/bin/env python3
"""The Perpetual Power Strip.

A catalogue photograph of an impossible gadget: a white power strip that
plugs into itself, delivering power from nothing. Rendered with PIL only,
deterministic, no network, no external files besides system fonts.
Writes /output/entry.png (1024x1024).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
OUT = "/output/entry.png"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FLOOR_Y = 737


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, top_c, bot_c):
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        draw.line([(x0, y), (x1, y)], fill=lerp(top_c, bot_c, (y - y0) / span))


# ---------------------------------------------------------------- background
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
top_c = (239, 236, 230)
mid_c = (223, 219, 212)
bot_c = (196, 191, 184)
for y in range(H):
    t = y / (H - 1)
    if t < 0.72:
        c = lerp(top_c, mid_c, t / 0.72)
    else:
        c = lerp(mid_c, bot_c, (t - 0.72) / 0.28)
    d.line([(0, y), (W, y)], fill=c)
# faint floor seam
d.line([(0, FLOOR_Y), (W, FLOOR_Y)], fill=(188, 183, 176), width=2)

# soft key-light glow, top-left
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-260, -260, 620, 520], fill=(255, 255, 255, 46))
img = Image.alpha_composite(img.convert("RGBA"),
                            glow.filter(ImageFilter.GaussianBlur(90)))
d = ImageDraw.Draw(img)

# ------------------------------------------------------- contact shadows
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sh)
sd.ellipse([95, 706, 680, 752], fill=(40, 36, 30, 110))
sd.ellipse([790, 722, 965, 752], fill=(40, 36, 30, 100))
img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(14)))
d = ImageDraw.Draw(img)

# ------------------------------------------------------------- cable loop
# Thick black cable: exits the strip's right end, sweeps up and around in a
# big loop, and ends in the plug seated in the strip's own first socket.
cable_pts = [
    (648, 628), (712, 610), (762, 540), (756, 452),
    (700, 386), (560, 348), (400, 340), (268, 352),
    (196, 392), (182, 436),
]
d.line(cable_pts, fill=(28, 26, 24), width=17, joint="curve")
d.line([(x, y - 4) for x, y in cable_pts], fill=(74, 70, 66), width=5,
       joint="curve")

# ------------------------------------------------------------- power strip
# Body: chunky rounded rectangle, cream-white, top-lit.
body = (110, 520, 650, 700)
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle(body, radius=30, fill=255)
body_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(body_img)
vgrad(bd, body, (252, 250, 246), (214, 210, 202))
img = Image.alpha_composite(img, Image.composite(
    body_img, Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask))
d = ImageDraw.Draw(img)
# top highlight + bottom shade on the body
d.rounded_rectangle([110, 520, 650, 548], radius=14, fill=(255, 255, 255, 90))
d.rounded_rectangle([110, 686, 650, 700], radius=14, fill=(120, 114, 106, 60))
d.rounded_rectangle(body, radius=30, outline=(150, 144, 136), width=2)

# Four dark socket faces on the upper front of the strip.
socket_centres = [185, 295, 405, 515]
for cx in socket_centres:
    d.rounded_rectangle([cx - 40, 540, cx + 40, 622], radius=12,
                        fill=(52, 50, 48))
    d.rounded_rectangle([cx - 40, 540, cx + 40, 622], radius=12,
                        outline=(30, 28, 26), width=2)
    d.rounded_rectangle([cx - 40, 540, cx + 40, 556], radius=8,
                        fill=(88, 84, 80))
    # two slots + round ground hole
    d.rounded_rectangle([cx - 20, 566, cx - 8, 596], radius=4,
                        fill=(16, 15, 14))
    d.rounded_rectangle([cx + 8, 566, cx + 20, 596], radius=4,
                        fill=(16, 15, 14))
    d.ellipse([cx - 7, 600, cx + 7, 614], fill=(16, 15, 14))

# Red rocker switch, right end of the strip.
d.rounded_rectangle([572, 556, 626, 622], radius=9, fill=(178, 32, 28))
d.rounded_rectangle([572, 556, 626, 622], radius=9,
                    outline=(120, 20, 16), width=2)
d.rounded_rectangle([572, 556, 626, 578], radius=8, fill=(226, 84, 76))
d.line([(582, 612), (616, 612)], fill=(255, 255, 255), width=4)

# Glowing green LED next to the switch.
led_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(led_glow)
ld.ellipse([540, 640, 566, 666], fill=(90, 220, 110, 130))
img = Image.alpha_composite(img, led_glow.filter(ImageFilter.GaussianBlur(6)))
d = ImageDraw.Draw(img)
d.ellipse([545, 645, 561, 661], fill=(46, 190, 80))
d.ellipse([548, 647, 555, 654], fill=(190, 255, 200))

# Printed text on the strip body (product labelling only).
f_bold = font("DejaVuSans-Bold.ttf", 30)
f_reg = font("DejaVuSans.ttf", 19)
f_tiny = font("DejaVuSans.ttf", 14)
d.text((140, 640), "PERPETUAL", font=f_bold, fill=(74, 70, 64))
d.text((420, 650), "MODEL \u221e-1", font=f_reg, fill=(110, 104, 96))
d.text((140, 672), "N O   O U T L E T   R E Q U I R E D", font=f_tiny,
       fill=(88, 82, 74))

# ------------------------------------------------- plug in the first socket
# Two metal prongs rising out of socket 1, plug body above them.
d.rectangle([172, 500, 182, 542], fill=(168, 166, 160))
d.rectangle([188, 500, 198, 542], fill=(168, 166, 160))
d.rounded_rectangle([150, 428, 222, 504], radius=16, fill=(238, 236, 231))
d.rounded_rectangle([150, 428, 222, 504], radius=16,
                    outline=(160, 154, 146), width=2)
d.rounded_rectangle([150, 428, 222, 452], radius=12, fill=(255, 255, 255))
# cable meets the top of the plug
d.ellipse([176, 424, 196, 444], fill=(28, 26, 24))

# ------------------------------------------------------- accessory: phone
# Exactly one accessory: a smartphone standing upright, screen lit at 100%,
# fed by a thin charging cable from the strip.
phone = (800, 372, 950, 737)
d.rounded_rectangle(phone, radius=26, fill=(34, 34, 38))
d.rounded_rectangle(phone, radius=26, outline=(12, 12, 14), width=2)
d.rounded_rectangle([800, 372, 950, 404], radius=13, fill=(74, 74, 80))
# screen
scr = (812, 388, 938, 722)
smask = Image.new("L", (W, H), 0)
smd = ImageDraw.Draw(smask)
smd.rounded_rectangle(scr, radius=16, fill=255)
scr_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd2 = ImageDraw.Draw(scr_img)
vgrad(sd2, scr, (226, 250, 228), (150, 215, 165))
img = Image.alpha_composite(img, Image.composite(
    scr_img, Image.new("RGBA", (W, H), (0, 0, 0, 0)), smask))
d = ImageDraw.Draw(img)
d.rounded_rectangle(scr, radius=16, outline=(20, 60, 30), width=2)
# glossy diagonal sheen on the screen
sheen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shd = ImageDraw.Draw(sheen)
shd.polygon([(812, 722), (880, 388), (930, 388), (862, 722)],
            fill=(255, 255, 255, 34))
img = Image.alpha_composite(img, sheen)
d = ImageDraw.Draw(img)
# charging bolt
bolt = [(884, 420), (856, 500), (876, 500), (862, 580),
        (908, 492), (886, 492)]
d.polygon(bolt, fill=(250, 196, 20), outline=(200, 150, 10))
# big 100% readout
f_big = font("DejaVuSans-Bold.ttf", 38)
d.text((875, 596), "100%", font=f_big, fill=(18, 70, 34), anchor="ma")
f_small = font("DejaVuSans-Bold.ttf", 17)
d.text((875, 664), "CHARGING", font=f_small, fill=(30, 110, 55),
       anchor="ma")

# thin charging cable: strip's right end -> phone base
d.line([(646, 676), (716, 706), (792, 726), (828, 724)],
       fill=(60, 58, 56), width=5, joint="curve")

# ------------------------------------------------------------- save + check
os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.convert("RGB").save(OUT, format="PNG")
size = os.path.getsize(OUT)
print(f"wrote {OUT}: {W}x{H}, {size} bytes")
assert size <= 1048576, "image over 1 MiB"
assert W <= 1024 and H <= 1024, "image over 1024 px"
print("OK: within size and dimension limits")
