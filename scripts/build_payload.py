"""Build the SHARK STORE Discord Components V2 payload (flag 1<<15 = 32768)."""
import json
import os

ACCENT = 0xA855F7  # purple accent bar
ACCENT_DEEP = 0x7C1FD6

# ------------------------------------------------------------ server custom emojis
EM_PNG = "<:PNG:1535405218051657738>"
EM_EGYPT = "<a:1202639620215537774:1525097041359802398>"
EM_NITRO = "<a:NitroActivate:1525097049387958273>"
EM_PROBOT = "<a:ProBot_icon:1525097050776272988>"
EM_LOADING = "<a:loading:1525097053674274948>"
EM_CROWN = "<a:avj_crown:1525097561998884895>"
EM_TAG111 = "<a:tag111:1525097564922183711>"
EM_HEART = "<:551465redheart:1527650669979504762>"
EM_TICK = "<a:tick:1525098506325327962>"

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
        b["emoji"] = emoji if isinstance(emoji, dict) else {"name": emoji}
    return b


# ---------------------------------------------------- 1. welcome + who we are + QR
container_welcome = {
    "type": 17,
    "accent_color": ACCENT,
    "components": [
        MG("shark_cover.png", desc="Shark Store cover"),
        TD(
            f"## {EM_PNG} ─── ✦ **SHARK STORE — شـارك سـتـور** ✦ ─── {EM_PNG}\n"
            f"الـسـلام عـلـيـكـم ورحـمـة الله وبـركـاتـه {EM_HEART}\n"
            f"> {EM_TAG111} **أهـلاً بـكـم فـي شـارك سـتـور، الاسـتـور الـمـتـكـامـل لـكـل مـا تـحـتـاجـه**\n"
            f"تـقـدر تـشـتـري مـن هـنـا كـل خـدمـاتـك وتـصـامـيـمـك بـأفـضـل جـودة وأسـرع تـسـلـيـم {EM_TICK}"
        ),
        SEP(True, 2),
        SECTION(
            [
                f"### {EM_CROWN} __Who are we — مـن نـحـن__ {EM_CROWN}",
                f"نـحـن سـتـور مـتـمـيـز يـقـدم أفـضـل الـخـدمـات والـمـنـتـجـات {EM_TAG111}\n"
                f"تـم تـأسـيـس الاسـتـور عـام **2026** {EM_TICK}",
            ],
            thumb="shark_logo.png",
        ),
        SEP(True, 2),
        MG("qr.png", desc="Shark Store QR code"),
        TD(f"-# {EM_PNG} SHARK STORE · 2026 {EM_HEART}"),
    ],
}

# ---------------------------------------------------- 2. news + paid ads
container_news = {
    "type": 17,
    "accent_color": ACCENT_DEEP,
    "components": [
        MG("banner_news.png", desc="News"),
        TD(
            f"### {EM_LOADING} ─── ✦ **Shark News — أخـبـار الـسـيـرفـر** ✦ ─── {EM_LOADING}\n"
            f"> {EM_NITRO} **تـابـع كـل جـديـد وتـحـديـثـات الـسـيـرفـر والـبـوت مـن هـنـا:**\n"
            f"> <#{CH_NEWS}>"
        ),
        SEP(True, 2),
        MG("banner_paid_ads.png", desc="Paid ads"),
        TD(
            f"### {EM_PROBOT} ─── ✦ **Shark Ads — شـراء الإعـلانـات** ✦ ─── {EM_PROBOT}\n"
            f"> {EM_TICK} **تـقـدر تـشـتـري إعـلان لـسـيـرفـرك أو مـتـجـرك بـأفـضـل الأسـعـار:**\n"
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
            f"### {EM_TAG111} ─── ✦ **Apply To Seller — الـتـقـديـم لـلـسـيـلـر** ✦ ─── {EM_TAG111}\n"
            f"> {EM_TICK} **عـايـز تـبـقـى سـيـلـر وتـنـضـم لـلـتـيـم؟ تـأكـد مـن اسـتـيـفـاء الـشـروط:**\n"
            f"• وجـود **30 فـيـدبـاك إيـجـابـي** مـوثـق كـحـد أدنـى `(إجـبـاري)` {EM_TICK}\n"
            f"• تـوفـر مـبـلـغ الـتـأمـيـن والـضـمـان: `300m / 150 EGP / 3$` {EM_EGYPT}\n"
            "• تـوثـيـق رقـم الـهـاتـف الـخـاص بـك كـإجـراء أمـان إلـزامـي\n"
            f"• مـمـنـوع تـكـرار الـمـنـشـن أو الإزعـاج — سـيـتـم الـرد عـلـيـكـم سـريـعـاً {EM_LOADING}\n"
            f"• يـشـتـرط تـوفـر الـفـيـدبـاك والـضـمـان مـعـاً {EM_HEART}\n"
            f"> <#{CH_APPLY_TEAM}>"
        ),
        SEP(True, 2),
        MG("banner_apply_support.png", desc="Apply to support"),
        TD(
            f"### {EM_CROWN} ─── ✦ **Apply To Support — الـتـقـديـم لـلإدارة** ✦ ─── {EM_CROWN}\n"
            f"> {EM_TAG111} **هـل تـمـتـلـك الـخـبـرة والـكـفـاءة لـلانـضـمـام لـطـاقـم الإدارة والـدعـم الـفـنـي؟**\n"
            f"> {EM_HEART} سـاعـدنـا فـي تـطـويـر وتـنـظـيـم الـمـجـتـمـع وابـنِ مـسـيـرتـك مـعـانـا!\n"
            f"> {EM_TICK} **لـلـتـقـديـم افـتـح تـذكـرة مـن هـنـا:**\n"
            f"> <#{CH_APPLY_SUPPORT}>"
        ),
        ROW(
            BTN("Apply To Seller", "shark_apply_team", 1, {"name": "tick", "id": "1525098506325327962", "animated": True}),
            BTN("Apply To Support", "shark_apply_support", 2, {"name": "551465redheart", "id": "1527650669979504762"}),
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
            f"### {EM_PNG} ─── ✦ **Shark Rules — قـوانـيـن شـارك سـتـور** ✦ ─── {EM_PNG}\n"
            f"> {EM_TICK} **الـرجـاء الالـتـزام بـالـقـوانـيـن الـتـالـيـة لـضـمـان بـيـئـة تـعـامـل آمـنـة لـلـجـمـيـع:**\n\n"
            "• __**مـنـع الـمـحـتـوى غـيـر الـلائـق:**__ يـحـظـر نـشـر أي صـور أو مـحـتـوى خـادش فـي الـرومـات الـعـامـة (NSFW).\n"
            "• __**عـدم إيـذاء الـنـفـس:**__ يـمـنـع مـنـعـاً بـاتـاً تـشـجـيـع إيـذاء الـنـفـس أو الاسـتـفـزاز والـتـلاعـب.\n"
            "• __**حـظـر الـتـعـدي والـتـنـمـر:**__ يـمـنـع الـسـب، والـقـذف، والـتـهـديـد أو نـشـر الـبـيـانـات الـشـخـصـيـة.\n"
            "• __**مـكـافـحـة الاحـتـيـال والأمـان:**__ يـحـظـر نـشـر الـروابـط الـمـشـبـوهـة، الـفـيـروسـات، أو الـتـصـيـد الاحـتـيـالـي.\n"
            f"> <#{CH_RULES}>"
        ),
        SEP(True, 2),
        MG("brandbar.png", desc="Shark Store"),
        TD(f"-# ✦ {EM_PNG} SHARK STORE © 2026 • جـمـيـع الـحـقـوق مـحـفـوظـة {EM_HEART} ✦"),
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
