# 🦈 Shark Store — Discord Components V2 System

Purple shark-themed Discord welcome message built on **Discord Components V2**
(`IS_COMPONENTS_V2`, message flag `1 << 15` = `32768`), plus the generated banner
artwork and the Python scripts that produce both.

![Cover](cover.png)

---

## What's in here

| File | Purpose |
| --- | --- |
| `index.html` | Live preview — renders the real V2 payload as Discord would |
| `styles.css` | Discord V2 container / gallery / section / button styling |
| `app.js` | Components V2 renderer (types 17, 12, 10, 9, 11, 14, 1, 2) |
| `payload.json` | The Discord message payload — this is the source of truth |
| `payload.js` | Same payload wrapped for the browser preview |
| `scripts/build_payload.py` | Generates `payload.json` |
| `scripts/make_banners.py` | Generates every PNG banner with Pillow |
| `scripts/send_v2.py` | Posts the message to a channel via the Discord REST API |
| `*.png` | Banner assets |

---

## Components V2 quick reference

| Type | Component | Used for |
| --- | --- | --- |
| `17` | Container | The 3 purple boxes (with `accent_color`) |
| `12` | Media Gallery | All banner images |
| `10` | Text Display | Markdown body copy |
| `9` | Section | Text + thumbnail row |
| `11` | Thumbnail | QR accessory inside the Section |
| `14` | Separator | Dividers (`spacing` 1 = small, 2 = large) |
| `1` | Action Row | Button rows |
| `2` | Button | Link + ticket buttons |

**Rules to keep in mind**

- `flags: 32768` is **required**, and it can never be removed from a sent message.
- `content` and `embeds` stop working — everything goes in `components`.
- Max **40 components** per message, max **10 children** per container.
- Attachments are not shown automatically — expose them through components.
- `poll` and `stickers` are disabled.

Current payload: **34 components** across **3 containers** (8 / 10 / 5 children).

---

## Layout

| Container | Accent | Contents |
| --- | --- | --- |
| 1 — Welcome | `#A855F7` | Cover · GET STARTING · intro · INFORMATION · subtext |
| 2 — Rules & Contact | `#7C1FD6` | RULES · CONTACT + 3 link buttons · SUPPORT + ticket button |
| 3 — Footer | `#A855F7` | QR section · AND THAT'S IT · brand bar |

---

## Preview it locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Three tabs: **Preview** (Discord render), **Assets** (banner gallery),
**V2 Payload** (raw JSON + copy button).

---

## Send it to Discord

```bash
pip install requests
# edit BOT_TOKEN and CHANNEL_ID in scripts/send_v2.py
python3 scripts/send_v2.py
```

Images are referenced as `attachment://cover.png`, so the PNGs must be uploaded
in the same request under the same filenames. Swap them for CDN URLs if you'd
rather host them elsewhere.

### discord.js

```js
const { MessageFlags } = require('discord.js');
const payload = require('./payload.json');

channel.send({
  flags: MessageFlags.IsComponentsV2,
  components: payload.components,
  files: ['cover.png', 'hero_getstarting.png', /* ... */],
});
```

---

## Regenerate the artwork

```bash
pip install pillow numpy
python3 scripts/make_banners.py    # rebuilds every PNG
python3 scripts/build_payload.py   # rebuilds payload.json + payload.js
```

Fonts used: Anton, Archivo Black, Bebas Neue, Oswald (Google Fonts, OFL).
`make_banners.py` expects them in `fonts/` — see the `F` constant at the top.

---

## Editing the copy

All text is **Lorem Ipsum** placeholder. Change it in
`scripts/build_payload.py` (the `TD(...)` strings), then re-run
`build_payload.py`. Text Display supports normal Discord markdown:
`#`/`##`/`###` headings, `**bold**`, `` `code` ``, `[links](url)`, and `-# subtext`.
