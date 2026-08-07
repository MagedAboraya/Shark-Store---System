"""Build banner_rules.png (1920x768) matching the SHARK STORE channel-banner style."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

B = "/home/user/brand/"
F = "/home/user/shark_design/fonts/"
ALDRICH = F + "Aldrich-Regular.ttf"
CAIRO = F + "Cairo.ttf"

W, H = 1920, 768
news = Image.open(B + "banner_news.png").convert("RGB")


def feather_paste(dst, src_img, box, feather=14):
    """Paste a crop of src at the same coords with soft edges."""
    x0, y0, x1, y1 = box
    crop = src_img.crop(box)
    m = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(m).rectangle([feather, feather, x1 - x0 - feather, y1 - y0 - feather], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(feather / 2))
    dst.paste(crop, (x0, y0), m)


# ---------------------------------------------------------------- background
bg = news.filter(ImageFilter.GaussianBlur(58))
a = np.asarray(bg).astype(np.float32)
r = np.random.default_rng(5)
a = np.clip(a + r.normal(0, 5.5, (H, W, 1)), 0, 255)
bg = Image.fromarray(a.astype(np.uint8)).convert("RGBA")

stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(stars)
for _ in range(240):
    x, y = int(r.integers(0, W)), int(r.integers(0, H))
    rad = int(r.choice([0, 0, 1]))
    sd.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(255, 245, 255, int(r.integers(30, 120))))
bg.alpha_composite(stars.filter(ImageFilter.GaussianBlur(0.4)))

# keep the original sharp shark badge + discord handle from the real banner
feather_paste(bg, news, (1735, 0, 1920, 135), feather=16)
feather_paste(bg, news, (795, 645, 1175, 755), feather=18)

# ------------------------------------------------------------------ 3D icon
icon = Image.open(B + "icon_rules_raw.jpeg").convert("RGB")
ia = np.asarray(icon).astype(np.float32)
lum = ia.mean(2)
alpha = np.clip((lum - 14) / 26.0, 0, 1)          # key out the black backdrop
icon = Image.fromarray(np.dstack([ia, alpha * 255]).astype(np.uint8), "RGBA")
ys, xs = np.where(alpha > 0.25)
icon = icon.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))

TARGET_H = 530
icon = icon.resize((int(icon.width * TARGET_H / icon.height), TARGET_H), Image.LANCZOS)
ix, iy = 1455 - icon.width // 2, (H - TARGET_H) // 2 + 8

glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
glow.paste(icon, (ix, iy), icon)
ga = glow.split()[3].filter(ImageFilter.GaussianBlur(70)).point(lambda v: min(255, int(v * 1.5)))
gl = Image.new("RGBA", (W, H), (168, 85, 247, 255))
gl.putalpha(ga)
bg.alpha_composite(gl)
bg.alpha_composite(icon, (ix, iy))

# --------------------------------------------------------------------- text
def fit_cap(path, text, target_h, direction=None):
    size = target_h
    for _ in range(40):
        f = ImageFont.truetype(path, size)
        bb = f.getbbox(text, direction=direction)
        h = bb[3] - bb[1]
        if abs(h - target_h) <= 1:
            return f, bb
        size = max(8, int(round(size * target_h / max(1, h))))
    f = ImageFont.truetype(path, size)
    return f, f.getbbox(text, direction=direction)


def draw_titled(img, text, font, bbox, left, top, off=7):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((left - bbox[0], top - bbox[1]), text, font=font, fill=(255, 255, 255, 255))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.paste(Image.new("RGBA", img.size, (0, 0, 0, 235)), (0, 0), lay.split()[3])
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2)), (off, off))
    img.alpha_composite(lay)
    return lay


# English title — same left edge / cap height as "News"
f_en, bb_en = fit_cap(ALDRICH, "Rules", 208)
lay_en = draw_titled(bg, "Rules", f_en, bb_en, 195, 211)
right_edge = int(np.where(np.asarray(lay_en.split()[3]) > 40)[1].max())

# Arabic subtitle — right-aligned to the English word, like الاخبار under News
ar = "القوانين"   # Pillow/raqm handles shaping + RTL ordering natively
f_ar, bb_ar = fit_cap(CAIRO, ar, 51, direction="rtl")
try:
    f_ar.set_variation_by_axes([700])
    bb_ar = f_ar.getbbox(ar, direction="rtl")
except Exception:
    pass
ar_w = bb_ar[2] - bb_ar[0]
lay_ar = Image.new("RGBA", bg.size, (0, 0, 0, 0))
ImageDraw.Draw(lay_ar).text((right_edge - ar_w - bb_ar[0], 452 - bb_ar[1]), ar,
                            font=f_ar, fill=(255, 255, 255, 255), direction="rtl")
halo = Image.new("RGBA", bg.size, (196, 132, 255, 255))
halo.putalpha(lay_ar.split()[3].filter(ImageFilter.GaussianBlur(7)).point(lambda v: min(255, v * 3)))
bg.alpha_composite(halo)
shad = Image.new("RGBA", bg.size, (14, 2, 30, 220))
shad.putalpha(lay_ar.split()[3])
bg.alpha_composite(shad.filter(ImageFilter.GaussianBlur(2)), (4, 4))
bg.alpha_composite(lay_ar)

ImageDraw.Draw(bg).rectangle([0, H - 6, W, H], fill=(124, 40, 214, 255))
bg.convert("RGB").save(B + "banner_rules.png", quality=95)
print("saved", Image.open(B + "banner_rules.png").size, "| title right edge", right_edge)
