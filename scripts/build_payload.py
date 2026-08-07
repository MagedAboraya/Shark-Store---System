"""Build the SHARK STORE Discord Components V2 payload (flag 1<<15 = 32768)."""
import json
import os

ACCENT = 0xA855F7  # purple accent bar
ACCENT_DEEP = 0x7C1FD6

# ------------------------------------------------------------ channel IDs
CH_APPLY_TEAM = "1524645415109267576"
CH_APPLY_SUPPORT = "1524645423611117658"
CH_RULES = "1534301945722966287"
CH_NEWS = "1524645355961061451"
CH_PAID_ADS = "1524645376974393436"

ASSETS = [
    "shark_cover.png",
    "shark_logo.png",
    "qr.png",
    "banner_news.png",
    "banner_paid_ads.png",
    "banner_apply_team.png",
    "banner_apply_support.png",
    "banner_rules.png",
    "brandbar.png",
]


def MG(*files, desc=None):
    return {
        "type": 12,
        "items": [
            {
                "media": {"url": f"attachment://{f}"},
                "description": desc or f.rsplit(".", 1)[0],
            }
            for f in files
        ],
    }


def TD(content):
    return {"type": 10, "content": content}


def SEP(divider=True, spacing=1):
    return {"type": 14, "divider": divider, "spacing": spacing}


def SECTION(texts, thumb=None, button=None):
    s = {"type": 9, "components": [TD(t) for t in texts]}
    s["accessory"] = (
        {
            "type": 11,
            "media": {"url": f"attachment://{thumb}"},
            "description": "Shark Store logo",
        }
        if thumb
        else button
    )
    return s


def ROW(*buttons):
    return {"type": 1, "components": list(buttons)}


def BTN(label, custom_id, style=1, emoji=None):
    b = {"type": 2, "style": style, "label": label, "custom_id": custom_id}
    if emoji:
        b["emoji"] = {"name": emoji}
    return b


# ---------------------------------------------------- 1. welcome + who we are + QR
container_welcome = {
    "type": 17,
    "accent_color": ACCENT,
    "components": [
        MG("shark_cover.png", desc="Shark Store cover"),
        TD(
            "## 𝐒𝐇𝐀𝐑𝐊 𝐒𝐓𝐎𝐑𝐄 ---- شـارك سـتـور\n"
            "الـسـلام عـلـيـكـم ورحـمـة الله وبـركـاتـه\n"
            "أهـلاً بـيـكـم فـي شـارك سـتـور، أكـبـر اسـتـور مـن حـيـث الـمـنـتـجـات الـمـتـاحـة\n"
            "تـقـدر تـشـتـري مـن هـنـا كـل حـاجـة انـت مـحـتـاجـهـا مـن تـصـامـيـم وخـدمـات وإلـخ..."
        ),
        SEP(True, 2),
        SECTION(
            [
                "### 𝐖𝐡𝐨 𝐚𝐫𝐞 𝐰𝐞 --- مـن نـحـن",
                "إحـنـا سـتـور مـتـمـيـز واسـمـنـا **𝐒𝐡𝐚𝐫𝐤 𝐒𝐭𝐨𝐫𝐞**\n"
                "تـم إنـشـاء الاسـتـور سـنـة **2026**",
            ],
            thumb="shark_logo.png",
        ),
        SEP(True, 2),
        MG("qr.png", desc="Shark Store QR code"),
        TD("-# 𝐒𝐇𝐀𝐑𝐊 𝐒𝐓𝐎𝐑𝐄 · شـارك سـتـور"),
    ],
}

# ---------------------------------------------------- 2. news + paid ads
container_news = {
    "type": 17,
    "accent_color": ACCENT_DEEP,
    "components": [
        MG("banner_news.png", desc="News"),
        TD(
            "### 𝐒𝐡𝐚𝐫𝐤 𝐍𝐞𝐰𝐬 --- أخـبـار الـسـيـرفـر\n"
            "تـقـدر تـشـوف كـل أخـبـار الـسـيـرفـر مـن تـحـديـثـات لـلـبـوت وكـل شـيـء مـن هـنـا\n"
            f"> <#{CH_NEWS}>"
        ),
        SEP(True, 2),
        MG("banner_paid_ads.png", desc="Paid ads"),
        TD(
            "### 𝐒𝐡𝐚𝐫𝐤 𝐀𝐝𝐬 --- شـراء إعـلانـات\n"
            "تـقـدر تـشـتـري إعـلان لـسـيـرفـرك أو مـتـجـرك مـن هـنـا\n"
            f"> <#{CH_PAID_ADS}>"
        ),
    ],
}

# ---------------------------------------------------- 3. applications
container_apply = {
    "type": 17,
    "accent_color": ACCENT,
    "components": [
        MG("banner_apply_team.png", desc="Apply to team"),
        TD(
            "### 𝐀𝐩𝐩𝐥𝐲 𝐓𝐨 𝐓𝐞𝐚𝐦 --- الـتـقـد يـم عـلـى الـسـيـلـر\n"
            "عـايـز تـبـقـى سـيـلـر وتـنـضـم لـلـتـيـم بـتـاعـنـا؟ تـنـورنـا! "
            "افـتـح تـكـت وتـأكـد مـن إﻧـك مـتـطـابـق لـكـل الـشـروط:\n"
            "• يـجـب الـتـأكـد مـن وجـود **30** فـيـدبـاك إيـجـابـي (إجـبـاريًـا)\n"
            "• يـجـب الـتـأكـد مـن وجـود مـبـلـغ ضـمـان **300m / 150 EGP / 3$**\n"
            "• نـنـبـه أنـه سـيـتـم أخـذ رقـم الـهـاتـف الـخـاص بـك كـإجـراء أمـان إجـبـاري\n"
            "• مـمـنـوع الإزعـاج بـالـمـنـشـن وسـنـقـوم بـالـرد عـلـيـك فـي أقـرب وقـت\n"
            "• يـجـب تـوفـر الـفـيـدبـاك والـضـمـان مـعـاً\n"
            f"> <#{CH_APPLY_TEAM}>"
        ),
        SEP(True, 2),
        MG("banner_apply_support.png", desc="Apply to support"),
        TD(
            "### 𝐀𝐩𝐩𝐥𝐲 𝐓𝐨 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 --- تـقـد يـم لـلإدارة\n"
            "عـايـز تـقـدم مـعـانـا فـي الإدارة؟ وتـبـنـي نـفـسـك مـعـانـا مـن الـصـفـر؟\n"
            "افـتـح تـكـت مـن هـنـا:\n"
            f"> <#{CH_APPLY_SUPPORT}>"
        ),
        ROW(
            BTN("Apply To Team", "shark_apply_team", 1, "📋"),
            BTN("Apply To Support", "shark_apply_support", 2, "🎫"),
        ),
    ],
}

# ---------------------------------------------------- 4. rules + footer
container_rules = {
    "type": 17,
    "accent_color": ACCENT_DEEP,
    "components": [
        MG("banner_rules.png", desc="Rules"),
        TD(
            "### 𝐒𝐡𝐚𝐫𝐤 𝐑𝐮𝐥𝐞𝐬 --- قـوانـيـن شـارك سـتـور\n"
            "• **مـنـع الـمـحـتـوى الـجـنـسـي الـصـريـح:** يـحـظـر نـشـر صـور أو مـحـتـوى غـيـر لـائـق "
            "فـي الـرومـات الـعـامـة ويـجـب تـحـديـد الـقـنـوات الـمـخـصـصـة لـلـبـالـغـيـن بـعـلـامـة (NSFW).\n"
            "• **عـدم إيـذاء الـنـفـس:** يـمـنـع تـشـجـيـع الانـتـحـار أو إيـذاء الـنـفـس أو الـتـلـاعـب الـعـاطـفـي.\n"
            "• **حـظـر الـتـعـدي والـمـضـايـقـة:** يـمـنـع الـتـنـمـر، والـتـهـديـد، والـتـحـرش بـالأخـريـن "
            "أو نـشـر مـعـلـومـاتـهـم الـشـخـصـيـة.\n"
            "• **مـكـافـحـة الاحـتـيـال والأمـان:** يـحـظـر نـشـر الـروابـط الـوهـمـيـة، أو الـفـيـروسـات، "
            "أو مـحـاولـات الـتـجـسـس واخـتـراق الـحـسـابـات (الـتـصـيـد الاحـتـيـالـي).\n"
            f"> <#{CH_RULES}>"
        ),
        SEP(True, 2),
        MG("brandbar.png", desc="Shark Store"),
    ],
}

payload = {
    "flags": 32768,  # IS_COMPONENTS_V2  (1 << 15)
    "components": [
        container_welcome,
        container_news,
        container_apply,
        container_rules,
    ],
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
    out = ""
    js = json.dumps(payload, indent=2, ensure_ascii=False)
    with open("payload.json", "w", encoding="utf-8") as f:
        f.write(js)
    with open("payload.js", "w", encoding="utf-8") as f:
        f.write("window.SHARK_PAYLOAD = " + js + ";\n")
    print("total components:", count(payload["components"]), "(limit 40)")
    for i, c in enumerate(payload["components"], 1):
        print(f"  container {i}: {len(c['components'])} children (limit 10)")
