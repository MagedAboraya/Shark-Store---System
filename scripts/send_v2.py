"""
SHARK STORE — send the Components V2 welcome message.

Requirements:
  pip install requests
Put the PNGs from this pack in the same folder as this file.

The IS_COMPONENTS_V2 flag (1 << 15 = 32768) is REQUIRED.
With it, `content` and `embeds` are disabled — everything lives in `components`.
"""
import json
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "YOUR_CHANNEL_ID"

FILES = [
    "cover.png", "hero_getstarting.png", "sec_information.png", "sec_rules.png",
    "sec_contact.png", "sec_support.png", "footer_thatsit.png", "brandbar.png", "qr.png",
]

payload = json.load(open("payload.json", encoding="utf-8"))

# attachment ids must match the multipart file indexes (files[0], files[1], ...)
payload["attachments"] = [{"id": i, "filename": f} for i, f in enumerate(FILES)]

multipart = {"payload_json": (None, json.dumps(payload), "application/json")}
for i, f in enumerate(FILES):
    multipart[f"files[{i}]"] = (f, open(f, "rb"), "image/png")

r = requests.post(
    f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
    headers={"Authorization": f"Bot {BOT_TOKEN}"},
    files=multipart,
    timeout=60,
)
print(r.status_code)
print(r.text[:1500])

# ---------------------------------------------------------------------------
# discord.py (2.4+) equivalent:
#
# import discord
# files = [discord.File(f) for f in FILES]
# await channel.send(files=files, view=discord.ui.LayoutView.from_dict(payload))
#
# discord.js (v14.16+) equivalent:
#
# const { MessageFlags } = require('discord.js');
# channel.send({
#   flags: MessageFlags.IsComponentsV2,
#   components: payload.components,
#   files: FILES,
# });
# ---------------------------------------------------------------------------
