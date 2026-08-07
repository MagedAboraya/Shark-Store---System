"""SHARK STORE — Discord section banners generator."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

UP = "/home/user/.uploads/"
F = "/home/user/shark_design/fonts/"
OUT = "/home/user/shark_design/assets/"
import os
os.makedirs(OUT, exist_ok=True)

ANTON = F + "Anton-Regular.ttf"
ARCHIVO = F + "ArchivoBlack-Regular.ttf"
BEBAS = F + "BebasNeue-Regular.ttf"
OSWALD = F + "Oswald.ttf"

SRC_BANNER = Image.open(UP + "pasted-image-image-1786127768637.png").convert("RGB")
SHARK = Image.open(UP + "pasted-image-image-1786127608697.png").convert("RGBA")

rng = np.random.default_rng(7)


def base_texture(w, h, dark=0.55, seed=0):
    """Purple grunge cloudscape derived from the brand banner + procedural grunge."""
    r = np.random.default_rng(seed)
    # 1. blurred crop of the real brand artwork -> authentic purple clouds
    sw, sh = SRC_BANNER.size
    cw = min(sw, int(sh * w / h))
    ch = int(cw * h / w)
    x0 = r.integers(0, max(1, sw - cw))
    y0 = r.integers(0, max(1, sh - ch))
    tex = SRC_BANNER.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.LANCZOS)
    tex = tex.filter(ImageFilter.GaussianBlur(radius=max(18, w // 26)))

    a = np.asarray(tex).astype(np.float32)
    # push toward brand purple
    a[..., 0] *= 0.95
    a[..., 1] *= 0.62
    a[..., 2] *= 1.12

    # 2. fractal grunge noise
    noise = np.zeros((h, w), np.float32)
    amp = 1.0
    for oct_ in range(5):
        s = 2 ** (oct_ + 1)
        n = r.random((max(2, h // (2 ** (4 - oct_) + 1) + 2), max(2, w // (2 ** (4 - oct_) + 1) + 2))).astype(np.float32)
        n = np.array(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255.0
        noise += n * amp
        amp *= 0.55
    noise = (noise - noise.min()) / (noise.ptp() + 1e-6)

    a[..., 0] += (noise - 0.5) * 70
    a[..., 1] += (noise - 0.5) * 34
    a[..., 2] += (noise - 0.5) * 90
    a = np.clip(a, 0, 255)

    img = Image.fromarray(a.astype(np.uint8))
    # 3. vignette + darkening so white text pops
    vg = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(vg)
    d.ellipse((-w * 0.35, -h * 1.2, w * 1.35, h * 2.2), fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(w // 8))
    dark_layer = Image.new("RGB", (w, h), (18, 3, 38))
    img = Image.composite(img, Image.blend(img, dark_layer, 0.75), vg)
    img = Image.blend(img, dark_layer, dark)
    img = ImageEnhance.Color(img).enhance(1.35)
    return img.convert("RGBA")


def scratch_overlay(w, h, seed=1, density=26, alpha=70):
    """Light diagonal scratches / paint streaks like the reference art."""
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    r = np.random.default_rng(seed)
    for _ in range(density):
        x = r.integers(-h, w)
        y = r.integers(0, h)
        ln = r.integers(w // 12, w // 3)
        wd = int(r.integers(1, 4))
        col = (255, 255, 255, int(r.integers(alpha // 3, alpha)))
        d.line([(x, y), (x + ln, y - int(ln * 0.45))], fill=col, width=wd)
    return lay.filter(ImageFilter.GaussianBlur(0.6))


def text_layer(size, text, font, fill=(255, 255, 255, 255), track=0, anchor_xy=None, align_center=True):
    """Render text with letter tracking on a transparent layer; returns (layer, bbox)."""
    w, h = size
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    widths = [d.textlength(c, font=font) + track for c in text]
    total = sum(widths) - track
    asc, desc = font.getmetrics()
    x = (w - total) / 2 if align_center else anchor_xy[0]
    y = anchor_xy[1] if anchor_xy else (h - (asc + desc)) / 2
    if align_center and anchor_xy:
        y = anchor_xy[1]
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill)
        x += cw
    return lay, total


def glow(layer, radius, color, strength=1.0):
    a = layer.split()[3]
    g = Image.new("RGBA", layer.size, color)
    ga = a.filter(ImageFilter.GaussianBlur(radius))
    ga = ga.point(lambda v: min(255, int(v * strength)))
    g.putalpha(ga)
    return g


def outline(layer, px, color):
    a = layer.split()[3]
    grown = a.filter(ImageFilter.MaxFilter(px * 2 + 1 if px * 2 + 1 <= 9 else 9))
    for _ in range(max(0, px // 4)):
        grown = grown.filter(ImageFilter.MaxFilter(9))
    o = Image.new("RGBA", layer.size, color)
    o.putalpha(grown)
    return o


def frame_corners(img, pad=18, ln=None, col=(214, 175, 255, 190), wdt=3):
    w, h = img.size
    ln = ln or int(w * 0.09)
    d = ImageDraw.Draw(img)
    d.line([(pad, pad), (pad + ln, pad)], fill=col, width=wdt)
    d.line([(pad, pad), (pad, pad + int(h * 0.28))], fill=col, width=wdt)
    d.line([(w - pad, h - pad), (w - pad - ln, h - pad)], fill=col, width=wdt)
    d.line([(w - pad, h - pad), (w - pad, h - pad - int(h * 0.28))], fill=col, width=wdt)
    return img



def fit_font(font_path, text, max_w, start_size, track_ratio=0.05):
    """Shrink font size until the tracked text fits max_w."""
    from PIL import ImageDraw, Image as _I
    d = ImageDraw.Draw(_I.new("RGB", (10, 10)))
    size = start_size
    while size > 8:
        f = ImageFont.truetype(font_path, size)
        track = size * track_ratio
        total = sum(d.textlength(c, font=f) + track for c in text) - track
        if total <= max_w:
            return f, int(track)
        size -= 2
    return ImageFont.truetype(font_path, 8), 0

# ---------------------------------------------------------------- MAIN HEADER
def make_hero(path, big="GET STARTING", small="ABOUT US", w=1200, h=330, seed=3):
    img = base_texture(w, h, dark=0.42, seed=seed)
    img.alpha_composite(scratch_overlay(w, h, seed=seed + 9))

    fbig, tk = fit_font(ARCHIVO, big, w * 0.86, int(h * 0.42), 0.11)
    lay, tw = text_layer((w, h), big, fbig, track=tk, anchor_xy=(0, int(h * 0.13)))
    # shadow
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh.alpha_composite(glow(lay, 14, (10, 0, 25, 255), 1.6))
    img.alpha_composite(sh)
    img.alpha_composite(glow(lay, 26, (170, 60, 255, 255), 1.1))
    img.alpha_composite(outline(lay, 4, (24, 4, 48, 255)))
    img.alpha_composite(lay)

    fsm, tk2 = fit_font(ANTON, small, w * 0.80, int(h * 0.30), 0.33)
    lay2, _ = text_layer((w, h), small, fsm, track=tk2, anchor_xy=(0, int(h * 0.50)))
    img.alpha_composite(glow(lay2, 18, (12, 0, 28, 255), 1.8))
    img.alpha_composite(outline(lay2, 5, (30, 6, 60, 255)))
    grad = Image.new("RGBA", (w, h))
    gp = grad.load()
    for y in range(h):
        t = y / h
        gp_col = (int(255 - 40 * t), int(235 - 90 * t), 255, 255)
        for x in range(w):
            gp[x, y] = gp_col
    grad.putalpha(lay2.split()[3])
    img.alpha_composite(grad)

    # underline bar
    d = ImageDraw.Draw(img)
    by = int(h * 0.88)
    d.rounded_rectangle([w * 0.30, by, w * 0.70, by + 7], radius=4, fill=(196, 120, 255, 210))
    frame_corners(img)
    img.convert("RGB").save(path, quality=95)
    return path


# ------------------------------------------------------------- SECTION TITLES
def make_section(path, text, w=1100, h=140, seed=11):
    img = base_texture(w, h, dark=0.5, seed=seed)
    img.alpha_composite(scratch_overlay(w, h, seed=seed + 4, density=14, alpha=55))
    f, tk = fit_font(ARCHIVO, text, w * 0.86, int(h * 0.46), 0.16)
    lay, _ = text_layer((w, h), text, f, track=tk, anchor_xy=(0, int(h * 0.20)))
    img.alpha_composite(glow(lay, 12, (8, 0, 22, 255), 1.7))
    img.alpha_composite(glow(lay, 22, (160, 70, 255, 255), 0.9))
    img.alpha_composite(outline(lay, 3, (26, 5, 52, 255)))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 8, h], fill=(178, 96, 255, 235))
    d.rectangle([w - 8, 0, w, h], fill=(178, 96, 255, 235))
    img.convert("RGB").save(path, quality=95)
    return path


# ---------------------------------------------------------------- FOOTER HERO
def make_footer(path, big="AND THAT'S IT", small="HAVE A GREAT DAY WITH SHARK STORE", w=1200, h=300, seed=21):
    img = base_texture(w, h, dark=0.40, seed=seed)
    img.alpha_composite(scratch_overlay(w, h, seed=seed + 3))
    f1, tk = fit_font(ARCHIVO, big, w * 0.86, int(h * 0.40), 0.12)
    lay, _ = text_layer((w, h), big, f1, track=tk, anchor_xy=(0, int(h * 0.16)))
    img.alpha_composite(glow(lay, 14, (8, 0, 22, 255), 1.7))
    img.alpha_composite(glow(lay, 26, (170, 60, 255, 255), 1.0))
    img.alpha_composite(outline(lay, 4, (24, 4, 48, 255)))
    img.alpha_composite(lay)
    f2, tk2 = fit_font(ANTON, small, w * 0.80, int(h * 0.17), 0.10)
    lay2, _ = text_layer((w, h), small, f2, track=tk2, anchor_xy=(0, int(h * 0.58)))
    img.alpha_composite(glow(lay2, 10, (8, 0, 22, 255), 1.8))
    img.alpha_composite(outline(lay2, 3, (30, 6, 60, 255)))
    tint = Image.new("RGBA", (w, h), (226, 205, 255, 255))
    tint.putalpha(lay2.split()[3])
    img.alpha_composite(tint)
    frame_corners(img)
    img.convert("RGB").save(path, quality=95)
    return path


# ------------------------------------------------------------------ BRAND BAR
def make_brandbar(path, w=1100, h=64):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    grad = Image.new("RGBA", (w, h))
    p = grad.load()
    for x in range(w):
        t = abs(x / w - 0.5) * 2
        c = (int(126 + 70 * (1 - t)), int(24 + 40 * (1 - t)), int(214 + 41 * (1 - t)), 255)
        for y in range(h):
            p[x, y] = c
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=255)
    grad.putalpha(mask)
    img.alpha_composite(grad)
    f, tk = fit_font(ARCHIVO, "SHARK   STORE", w * 0.80, int(h * 0.42), 0.38)
    lay, _ = text_layer((w, h), "SHARK   STORE", f, track=tk, anchor_xy=(0, int(h * 0.24)))
    img.alpha_composite(glow(lay, 8, (40, 0, 80, 255), 1.5))
    img.alpha_composite(lay)
    Image.alpha_composite(Image.new("RGBA", (w, h), (12, 4, 26, 255)), img).convert("RGB").save(path)
    return path


# --------------------------------------------------------------- SERVER COVER
def make_cover(path, w=1200, h=420, seed=33):
    img = base_texture(w, h, dark=0.30, seed=seed)
    img.alpha_composite(scratch_overlay(w, h, seed=seed + 2, density=34))

    # giant SHARK wordmark
    f, tk = fit_font(ARCHIVO, "SHARK", w * 0.92, int(h * 0.72), 0.03)
    lay, _ = text_layer((w, h), "SHARK", f, track=tk, anchor_xy=(0, int(h * 0.10)))
    img.alpha_composite(glow(lay, 24, (6, 0, 18, 255), 1.9))
    img.alpha_composite(outline(lay, 5, (20, 3, 42, 255)))
    wm = Image.new("RGBA", (w, h))
    p = wm.load()
    for y in range(h):
        t = min(1, max(0, (y - h * 0.15) / (h * 0.7)))
        c = (255, int(255 - 55 * t), 255, 255)
        for x in range(w):
            p[x, y] = c
    wm.putalpha(lay.split()[3])
    img.alpha_composite(wm)

    # shark artwork on top of the wordmark
    sk = SHARK.copy()
    tw = int(w * 0.60)
    sk = sk.resize((tw, int(sk.height * tw / sk.width)), Image.LANCZOS)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sx, sy = int(w * 0.22), int(h * 0.02)
    shadow.paste(sk, (sx, sy), sk)
    img.alpha_composite(glow(shadow, 18, (8, 0, 20, 255), 1.6))
    img.alpha_composite(shadow)

    # tagline left
    f2 = ImageFont.truetype(ANTON, int(h * 0.13))
    d = ImageDraw.Draw(img)
    for i, word in enumerate(["Dive", "Into", "Quality"]):
        y = int(h * 0.16 + i * h * 0.20)
        d.text((int(w * 0.045) + 3, y + 3), word, font=f2, fill=(10, 0, 24, 220))
        d.text((int(w * 0.045), y), word, font=f2, fill=(233, 215, 255, 255))

    # bottom trust row
    f3 = ImageFont.truetype(ARCHIVO, int(h * 0.062))
    bar_y = int(h * 0.845)
    d.rectangle([0, bar_y, w, h], fill=(28, 6, 56, 165))
    items = ["SAFETY", "SPEED", "GUARANTEE"]
    for i, it in enumerate(items):
        cx = int(w * (0.22 + i * 0.28))
        tl = d.textlength(it, font=f3)
        d.text((cx - tl / 2, bar_y + h * 0.035), it, font=f3, fill=(255, 255, 255, 255))
        if i:
            d.line([(cx - w * 0.145, bar_y + h * 0.03), (cx - w * 0.145, h - h * 0.03)], fill=(180, 120, 255, 140), width=2)
    f4 = ImageFont.truetype(OSWALD, int(h * 0.05))
    lay4, _ = text_layer((w, h), "L O R E M   I P S U M   S T O R E", f4, track=2, anchor_xy=(0, int(h * 0.775)))
    img.alpha_composite(glow(lay4, 8, (10, 0, 24, 255), 1.6))
    img.alpha_composite(lay4)
    img.convert("RGB").save(path, quality=95)
    return path


if __name__ == "__main__":
    make_cover(OUT + "cover.png")
    make_hero(OUT + "hero_getstarting.png", "GET STARTING", "ABOUT US", seed=3)
    make_section(OUT + "sec_information.png", "INFORMATION:", seed=12)
    make_section(OUT + "sec_contact.png", "CONTACT WITH US:", seed=17)
    make_section(OUT + "sec_support.png", "JOIN OUR SUPPORT TEAM:", seed=23)
    make_section(OUT + "sec_rules.png", "LOREM IPSUM RULES:", seed=29)
    make_footer(OUT + "footer_thatsit.png")
    make_brandbar(OUT + "brandbar.png")
    print("done", os.listdir(OUT))
