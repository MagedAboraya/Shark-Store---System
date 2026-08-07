"""Build the SHARK STORE Discord Components V2 payload (flag 1<<15 = 32768)."""
import json, os

ACCENT = 0xA855F7          # purple accent bar
ACCENT_DEEP = 0x7C1FD6

# ------------------------------------------------------------ channel IDs
CH_APPLY_TEAM = "1524645415109267576"
CH_APPLY_SUPPORT = "1524645423611117658"
CH_RULES = "1534301945722966287"
CH_NEWS = "1524645355961061451"
CH_PAID_ADS = "1524645376974393436"

ASSETS = [
    "shark_cover.png", "shark_logo.png", "qr.png",
    "banner_news.png", "banner_paid_ads.png",
    "banner_apply_team.png", "banner_apply_support.png",
    "banner_rules.png", "brandbar.png",
]


def MG(*files, desc=None):
    return {"type": 12, "items": [{"media": {"url": f"attachment://{f}"},
                                   "description": desc or f.rsplit('.', 1)[0]} for f in files]}


def TD(content):
    return {"type": 10, "content": content}


def SEP(divider=True, spacing=1):
    return {"type": 14, "divider": divider, "spacing": spacing}


def SECTION(texts, thumb=None, button=None):
    s = {"type": 9, "components": [TD(t) for t in texts]}
    s["accessory"] = ({"type": 11, "media": {"url": f"attachment://{thumb}"},
                       "description": "Lorem ipsum"} if thumb else button)
    return s


def ROW(*buttons):
    return {"type": 1, "components": list(buttons)}


def BTN(label, custom_id, style=1, emoji=None):
    b = {"type": 2, "style": style, "label": label, "custom_id": custom_id}
    if emoji:
        b["emoji"] = {"name": emoji}
    return b


# ---------------------------------------------------- 1. welcome + QR
container_welcome = {
    "type": 17,
    "accent_color": ACCENT,
    "components": [
        MG("shark_cover.png", desc="Shark Store cover"),
        TD("# SHARK STORE\n"
           "Lorem ipsum dolor sit amet, **consectetur adipiscing elit**, sed do eiusmod "
           "tempor incididunt ut labore et dolore magna aliqua."),
        SEP(True, 2),
        SECTION(
            ["### Lorem Ipsum Dolor",
             "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
             "aliquip ex ea commodo consequat."],
            thumb="shark_logo.png"),
        SEP(True, 2),
        MG("qr.png", desc="Shark Store QR code"),
        TD("-# Lorem ipsum dolor sit amet · consectetur adipiscing elit"),
    ],
}

# ---------------------------------------------------- 2. news + paid ads
container_news = {
    "type": 17,
    "accent_color": ACCENT_DEEP,
    "components": [
        MG("banner_news.png", desc="News"),
        TD("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
           f"incididunt ut labore.\n> <#{CH_NEWS}>"),
        SEP(True, 2),
        MG("banner_paid_ads.png", desc="Paid ads"),
        TD("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
           f"fugiat nulla pariatur.\n> <#{CH_PAID_ADS}>"),
    ],
}

# ---------------------------------------------------- 3. applications
container_apply = {
    "type": 17,
    "accent_color": ACCENT,
    "components": [
        MG("banner_apply_team.png", desc="Apply to team"),
        TD("Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia "
           f"deserunt mollit anim id est laborum.\n> <#{CH_APPLY_TEAM}>"),
        SEP(True, 2),
        MG("banner_apply_support.png", desc="Apply to support"),
        TD("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium "
           f"doloremque laudantium.\n> <#{CH_APPLY_SUPPORT}>"),
        ROW(BTN("Apply To Team", "shark_apply_team", 1, "📋"),
            BTN("Apply To Support", "shark_apply_support", 2, "🎫")),
    ],
}

# ---------------------------------------------------- 4. rules + footer
container_rules = {
    "type": 17,
    "accent_color": ACCENT_DEEP,
    "components": [
        MG("banner_rules.png", desc="Rules"),
        TD("**01** — Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
           "**02** — Sed do eiusmod tempor incididunt ut labore et dolore.\n"
           "**03** — Ut enim ad minim veniam, quis nostrud exercitation.\n"
           "**04** — Duis aute irure dolor in reprehenderit in voluptate.\n"
           f"> <#{CH_RULES}>"),
        SEP(True, 2),
        MG("brandbar.png", desc="Shark Store"),
        TD("-# Lorem ipsum placeholder copy — SHARK STORE"),
    ],
}

payload = {
    "flags": 32768,  # IS_COMPONENTS_V2  (1 << 15)
    "components": [container_welcome, container_news, container_apply, container_rules],
    "attachments": [{"id": i, "filename": f} for i, f in enumerate(ASSETS)],
}


def count(comps):
    n = 0
    for c in comps:
        n += 1
        n += count(c.get("components", []))
        if isinstance(c.get("accessory"), dict):
            n += 1
    return n


if __name__ == "__main__":
    out = "/home/user/shark_store_welcome/"
    os.makedirs(out, exist_ok=True)
    js = json.dumps(payload, indent=2, ensure_ascii=False)
    open(out + "payload.json", "w", encoding="utf-8").write(js)
    open(out + "payload.js", "w", encoding="utf-8").write("window.SHARK_PAYLOAD = " + js + ";\n")
    print("total components:", count(payload["components"]), "(limit 40)")
    for i, c in enumerate(payload["components"], 1):
        print(f"  container {i}: {len(c['components'])} children (limit 10)")
