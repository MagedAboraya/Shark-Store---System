const fs = require('fs');
const path = require('path');

const BOT_TOKEN = process.env.BOT_TOKEN || 'YOUR_BOT_TOKEN';
const CHANNEL_ID = process.env.CHANNEL_ID || 'YOUR_CHANNEL_ID';

const FILES = [
  'shark_cover.png',
  'shark_logo.png',
  'qr.png',
  'banner_news.png',
  'banner_paid_ads.png',
  'banner_apply_team.png',
  'banner_apply_support.png',
  'banner_rules.png',
  'brandbar.png',
];

async function sendComponentsV2() {
  console.log('Reading payload.json...');
  const payloadRaw = fs.readFileSync(path.join(__dirname, 'payload.json'), 'utf-8');
  const payload = JSON.parse(payloadRaw);

  payload.attachments = FILES.map((filename, index) => ({
    id: index,
    filename: filename,
  }));

  const form = new FormData();
  form.append('payload_json', JSON.stringify(payload));

  for (let i = 0; i < FILES.length; i++) {
    const filename = FILES[i];
    const filePath = path.join(__dirname, filename);
    const fileBuffer = fs.readFileSync(filePath);
    const blob = new Blob([fileBuffer], { type: 'image/png' });
    form.append(`files[${i}]`, blob, filename);
    console.log(`Attached file[${i}]: ${filename} (${(fileBuffer.length / 1024).toFixed(1)} KB)`);
  }

  console.log(`Sending Components V2 message to Discord channel ${CHANNEL_ID}...`);

  const response = await fetch(`https://discord.com/api/v10/channels/${CHANNEL_ID}/messages`, {
    method: 'POST',
    headers: {
      Authorization: `Bot ${BOT_TOKEN}`,
      'User-Agent': 'SharkStoreBot (https://sharkstore.gg, 1.0)',
    },
    body: form,
  });

  const resText = await response.text();
  console.log(`Status: ${response.status} ${response.statusText}`);
  try {
    const resJson = JSON.parse(resText);
    console.log('Message ID:', resJson.id || 'N/A');
  } catch {
    console.log('Result:', resText.slice(0, 500));
  }
}

sendComponentsV2().catch(err => {
  console.error('Error sending message:', err);
});
