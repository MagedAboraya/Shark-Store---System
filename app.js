/* Renders a Discord Components V2 payload (flag 1<<15) into HTML. */

const P = window.SHARK_PAYLOAD;
const url = u => (u || '').replace('attachment://', '');

// ---- tiny markdown subset used by Text Display -------------------------
function md(t) {
  const esc = t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return esc
    .split('\n')
    .map(line => {
      if (line.startsWith('### ')) return `<h3>${inline(line.slice(4))}</h3>`;
      if (line.startsWith('## ')) return `<h2>${inline(line.slice(3))}</h2>`;
      if (line.startsWith('# ')) return `<h1>${inline(line.slice(2))}</h1>`;
      if (line.startsWith('-# ')) return `<p class="subtext">${inline(line.slice(3))}</p>`;
      if (line.startsWith('&gt; ')) return `<blockquote>${inline(line.slice(5))}</blockquote>`;
      return `<p>${inline(line)}</p>`;
    })
    .join('');
}
function inline(s) {
  return s
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a class="lnk" href="$2">$1</a>')
    .replace(/&lt;:([a-zA-Z0-9_]+):(\d+)&gt;/g, '<span class="emoji-tag" title="$1">:$1:</span>')
    .replace(/:(PNG|NitroActivate|ProBot_icon|loading|avj_crown|tag111|551465redheart|tick):/g, '<span class="emoji-tag">:$1:</span>')
    .replace(/__([^_]+)__/g, '<u>$1</u>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code class="code">$1</code>')
    .replace(/&lt;#(\d+)&gt;/g, (_, id) => `<span class="chan">#${CHANNELS[id] || id}</span>`);
}

const CHANNELS = {
  '1524645415109267576': 'apply-to-team',
  '1524645423611117658': 'apply-to-support',
  '1534301945722966287': 'rules',
  '1524645355961061451': 'news',
  '1524645376974393436': 'paid-ads',
};

const BTN_STYLE = { 1: 'btn-primary', 2: 'btn-secondary', 3: 'btn-success', 4: 'btn-danger', 5: 'btn-link' };

// ---- component renderers ----------------------------------------------
function render(c) {
  switch (c.type) {
    case 17: { // CONTAINER
      const accent = '#' + (c.accent_color ?? 0x4f545c).toString(16).padStart(6, '0');
      return `<div class="v2-container" style="--accent:${accent}">
                ${c.components.map(render).join('')}
              </div>`;
    }
    case 12: { // MEDIA GALLERY
      const n = c.items.length;
      return `<div class="v2-gallery" data-n="${n}">
                ${c.items.map(i => `<img src="${url(i.media.url)}" alt="${i.description || ''}" loading="lazy">`).join('')}
              </div>`;
    }
    case 10: { // TEXT DISPLAY
      const rtl = /[\u0600-\u06FF]/.test(c.content);
      return `<div class="v2-text${rtl ? ' rtl' : ''}">${md(c.content)}</div>`;
    }
    case 14: // SEPARATOR
      return `<div class="v2-sep ${c.spacing === 2 ? 'sep-lg' : 'sep-sm'} ${c.divider === false ? 'no-line' : ''}"></div>`;
    case 9: { // SECTION
      const a = c.accessory || {};
      const acc = a.type === 11
        ? `<img class="v2-thumb" src="${url(a.media.url)}" alt="${a.description || ''}" loading="lazy">`
        : a.type === 2 ? render(a) : '';
      return `<div class="v2-section">
                <div class="min-w-0">${c.components.map(render).join('')}</div>
                ${acc}
              </div>`;
    }
    case 1: // ACTION ROW
      return `<div class="v2-row">${c.components.map(render).join('')}</div>`;
    case 2: // BUTTON
      return `<span class="v2-btn ${BTN_STYLE[c.style] || 'btn-secondary'}">
                ${c.emoji ? `<span>${c.emoji.name}</span>` : ''}${c.label || ''}
                ${c.style === 5 ? '<span class="ext">↗</span>' : ''}
              </span>`;
    default:
      return '';
  }
}

function countComponents(list) {
  return list.reduce((n, c) => n + 1 + countComponents(c.components || []) +
    (c.accessory && typeof c.accessory === 'object' ? 1 : 0), 0);
}

// ---- assets tab --------------------------------------------------------
const ASSETS = [
  ['shark_cover.png', 'Server Cover', '1920 × 1080'],
  ['shark_logo.png', 'Logo / Thumbnail', '1080 × 1080'],
  ['qr.png', 'QR Code', '1080 × 1080'],
  ['banner_news.png', 'News — #news', '1920 × 768'],
  ['banner_paid_ads.png', 'Paid ads — #paid-ads', '1920 × 768'],
  ['banner_apply_team.png', 'Apply To Team — #apply-to-team', '1920 × 768'],
  ['banner_apply_support.png', 'Apply To Support — #apply-to-support', '1920 × 768'],
  ['banner_rules.png', 'Rules — #rules', '1920 × 768'],
  ['brandbar.png', 'Brand Bar', '960 × 50'],
];

function init() {
  document.getElementById('v2-root').innerHTML = P.components.map(render).join('');

  document.querySelector('#tab-assets .card-grid').innerHTML = ASSETS.map(
    ([f, t, s]) => `<figure class="asset"><img src="${f}" alt="${t}" loading="lazy">
      <figcaption><span>${t}</span><span>${s}</span></figcaption></figure>`).join('');

  const json = JSON.stringify(P, null, 2);
  document.getElementById('json-out').textContent = json;
  document.getElementById('comp-count').textContent = countComponents(P.components);
  document.getElementById('copy-json').addEventListener('click', e => {
    navigator.clipboard?.writeText(json);
    e.target.textContent = 'Copied ✓';
    setTimeout(() => (e.target.textContent = 'Copy JSON'), 1500);
  });

  const btns = document.querySelectorAll('.tab-btn[data-tab]');
  btns.forEach(b => b.addEventListener('click', () => {
    btns.forEach(x => x.classList.remove('tab-active'));
    b.classList.add('tab-active');
    ['preview', 'assets', 'json'].forEach(t =>
      document.getElementById('tab-' + t).classList.toggle('hidden', t !== b.dataset.tab));
  }));
}

init();
