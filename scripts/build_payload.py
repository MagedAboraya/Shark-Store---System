"""Build the SHARK STORE Discord Components V2 payload (flag 1<<15 = 32768)."""
import json, os

ACCENT = 0xA855F7          # purple accent bar
ACCENT_DEEP = 0x7C1FD6

def MG(*files, desc=None):
    return {"type": 12, "items": [{"media": {"url": f"attachment://{f}"},
                                   "description": desc or f.rsplit('.', 1)[0]} for f in files]}

def TD(content):
    return {"type": 10, "content": content}

def SEP(divider=True, spacing=1):
    return {"type": 14, "divider": divider, "spacing": spacing}

def SECTION(texts, thumb=None, button=None):
    s = {"type": 9, "components": [TD(t) for t in texts]}
    if thumb:
        s["accessory"] = {"type": 11, "media": {"url": f"attachment://{thumb}"}, "description": "Lorem ipsum"}
    else:
        s["accessory"] = button
    return s

def ROW(*buttons):
    return {"type": 1, "components": list(buttons)}

def LINK(label, url, emoji=None):
    b = {"type": 2, "style": 5, "label": label, "url": url}
    if emoji: b["emoji"] = {"name": emoji}
    return b

def BTN(label, custom_id, style=1, emoji=None):
    b = {"type": 2, "style": style, "label": label, "custom_id": custom_id}
    if emoji: b["emoji"] = {"name": emoji}
    return b


container_welcome = {
    "type": 17,
    "accent_color": ACCENT,
    "components": [
        MG("cover.png", desc="Shark Store cover"),
        MG("hero_getstarting.png", desc="Get starting - about us"),
        TD("## Hi everyone 👋\n"
           "Lorem ipsum dolor sit amet, **consectetur adipiscing elit**. "
           "Here is a link to this server: [Lorem Ipsum](https://discord.gg/lorem)."),
        SEP(True, 2),
        MG("sec_information.png", desc="Information"),
        TD("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
           "incididunt ut labore et dolore magna aliqua.\n"
           "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip "
           "ex ea commodo consequat.\n"
           "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore."),
        SEP(True, 1),
        TD("-# Lorem ipsum dolor sit amet · consectetur adipiscing elit"),
    ],
}

container_rules = {
    "type": 17,
    "accent_color": ACCENT_DEEP,
    "components": [
        MG("sec_rules.png", desc="Lorem ipsum rules"),
        TD("**01** — Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
           "**02** — Sed do eiusmod tempor incididunt ut labore et dolore.\n"
           "**03** — Ut enim ad minim veniam, quis nostrud exercitation.\n"
           "**04** — Duis aute irure dolor in reprehenderit in voluptate velit."),
        SEP(True, 2),
        MG("sec_contact.png", desc="Contact with us"),
        TD("Lorem ipsum, you can send an email here `lorem@ipsum.dolor` or DM us here.\n"
           "You can also send your problem on our socials below."),
        ROW(LINK("Lorem", "https://example.com/lorem"),
            LINK("Ipsum", "https://example.com/ipsum"),
            LINK("Dolor", "https://example.com/dolor")),
        SEP(True, 2),
        MG("sec_support.png", desc="Join our support team"),
        TD("Lorem ipsum dolor sit amet, consectetur adipiscing elit — "
           "sed do eiusmod tempor incididunt ut labore. Apply below 👇"),
        ROW(BTN("Open Ticket", "shark_open_ticket", 1, "🎫"),
            BTN("Lorem Ipsum", "shark_lorem", 2)),
    ],
}

container_footer = {
    "type": 17,
    "accent_color": ACCENT,
    "components": [
        SECTION(
            ["### Lorem Ipsum Dolor",
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
             "incididunt ut labore et dolore magna aliqua."],
            thumb="qr.png"),
        SEP(True, 1),
        MG("footer_thatsit.png", desc="And that's it"),
        MG("brandbar.png", desc="Shark Store"),
        TD("-# Lorem ipsum placeholder copy — SHARK STORE"),
    ],
}

payload = {
    "flags": 32768,  # IS_COMPONENTS_V2  (1 << 15)
    "components": [container_welcome, container_rules, container_footer],
    "attachments": [
        {"id": i, "filename": f} for i, f in enumerate([
            "cover.png", "hero_getstarting.png", "sec_information.png", "sec_rules.png",
            "sec_contact.png", "sec_support.png", "footer_thatsit.png", "brandbar.png", "qr.png"])
    ],
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
    open(out + "payload.json", "w").write(js)
    open(out + "payload.js", "w").write("window.SHARK_PAYLOAD = " + js + ";\n")
    print("total components:", count(payload["components"]), "(limit 40)")
    for c in payload["components"]:
        print("  container children:", len(c["components"]), "(limit 10)")
