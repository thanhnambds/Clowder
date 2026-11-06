"""Builds tools/litter-box-finder.html from assets/data/litter-boxes.json.
Header and footer are copied from methodology.html. Run from the site root."""
import json, datetime, re
from html import escape as e

data = json.load(open('assets/data/litter-boxes.json'))
meth = open('methodology.html').read()
header = meth[meth.index('  <!-- HEADER -->'):meth.index('</header>') + len('</header>')]
footer = meth[meth.index('  <!-- FOOTER -->'):]
header = header.replace('<a href="/tools/litter-box-finder" class="nav-link">',
                        '<a href="/tools/litter-box-finder" class="nav-link active" aria-current="page">')
header = header.replace('<a href="/tools/litter-box-finder" class="dropdown-link">',
                        '<a href="/tools/litter-box-finder" class="dropdown-link active">')

NS = '<span class="nf-ns">Not stated by maker</span>'
DESIGN = {'drum': 'Drum', 'open-top': 'Open-top', 'open-view': 'Open-view'}

def d(iso):
    return datetime.date.fromisoformat(iso).strftime('%b %-d, %Y')

def num(v):
    return NS if v is None else e(f'{v:g}' if isinstance(v, (int, float)) else str(v))

def weight(w):
    if not w:
        return NS
    lo, hi = w
    if lo is not None and hi is not None:
        return f'{lo:g}–{hi:g} lb'
    if lo is not None:
        return f'{lo:g} lb min<br><span class="nf-ns">Max not stated by maker</span>'
    return f'<span class="nf-ns">Min not stated by maker</span><br>{hi:g} lb max'

def attr(v):
    return '' if v is None else f'{v:g}'

rows = []
for m in data:
    w = m['cat_weight_lb'] or [None, None]
    price = m.get('price_text') or f"${m['price_usd']:.2f}"
    notes = [m['notes']] if m['notes'] else []
    if m['litter'] and 'only' in m['litter']:
        notes.append(f"Litter: {m['litter']}.")
    if m['warranty'] and 'site banner' in m['warranty']:
        notes.append(f"Warranty: {m['warranty']}.")
    design = DESIGN[m['design']]
    if m.get('design_word'):
        design += f'<br><span class="nf-sub">Maker: "{e(m["design_word"])}"</span>'
    if m['page']:
        details = f'<a href="{m["page"]}">Our specs page</a>'
        for a in m['affiliate']:
            details += (f'<a href="{e(a["url"])}" target="_blank" rel="{a["rel"]}" class="nf-buy">'
                        f'{e(a["label"])} &rarr;</a>')
    else:
        details = ''.join(f'<a href="{e(a["url"])}" target="_blank" rel="{a["rel"]}" class="nf-buy">'
                          f'{e(a["label"])} &rarr;</a>' for a in m['affiliate'])
        details += (f'<a class="nf-src" href="{e(m["source"])}" rel="nofollow noopener" target="_blank">'
                    f'Source (maker\'s page, read {d(m["read"])})</a>')
    note_html = ''.join(f'<span class="nf-note">{e(n)}</span>' for n in notes)
    rows.append(f'''          <tr id="{m["id"]}" data-price="{m["price_usd"]:g}" data-design="{"drum" if m["design"] == "drum" else "open"}" data-wmin="{attr(w[0])}" data-wmax="{attr(w[1])}" data-camera="{"yes" if m["camera"] else ""}" data-waste="{attr(m["waste_l"])}">
            <th scope="row" data-label="Model"><span class="nf-model">{e(m["brand"])} {e(m["model"])}</span><span class="nf-sub">Specs read {d(m["read"])}</span>{note_html}<span class="nf-flag" hidden></span></th>
            <td data-label="Price">{e(price)}<br><span class="nf-sub">as of {d(m["price_date"])}</span></td>
            <td data-label="Design">{design}</td>
            <td data-label="Cat weight">{weight(m["cat_weight_lb"])}</td>
            <td data-label="Waste drawer (L)">{num(m["waste_l"])}</td>
            <td data-label="Entrance height (in)">{num(m["entrance_height_in"])}</td>
            <td data-label="Noise (dB)">{num(m["noise_db"])}</td>
            <td data-label="Camera">{num(m["camera"])}</td>
            <td data-label="Details" class="nf-details">{details}</td>
          </tr>''')
# wrap each <td> body in one <div> so the mobile two-column grid gets exactly label + value
rows = [re.sub(r'(<td [^>]*>)(.*?)(</td>)', r'\1<div>\2</div>\3', r) for r in rows]

TITLE = 'Automatic Litter Box Finder: Filter by Maker Specs | ClowderHub'
DESC = ("Filter 13 automatic litter boxes by cat weight, budget, design, camera and waste drawer size. "
        "Every figure comes from the maker's own product page, with the date we read it.")
URL = 'https://www.clowderhub.com/tools/litter-box-finder'

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-G1Z43N7MKG"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-G1Z43N7MKG');
  </script>
  <title>{TITLE}</title>
  <meta name="description" content="{e(DESC)}">
  <link rel="canonical" href="{URL}">
  <link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg">
  <link rel="icon" type="image/png" href="/assets/img/favicon.png">
  <link rel="stylesheet" href="/assets/style.css?v=20261017">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/pages.css?v=20261017">
  <style>
    .nf-intro{{font-size:16px;color:var(--color-slate);line-height:1.6;margin:0 0 24px;max-width:760px}}
    .nf-intro a,.nf-disclosure a,.nf-table a:not(.nf-buy){{color:var(--color-primary);text-decoration:underline}}
    .nf-filters{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;align-items:end;background:var(--pg-cream);border:1.5px solid var(--pg-line);border-radius:var(--radius-md);padding:18px;margin:0 0 14px}}
    .nf-filters label{{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;color:var(--color-dark)}}
    .nf-filters input,.nf-filters select{{font:inherit;font-size:15px;font-weight:400;min-height:44px;padding:8px 10px;border:1.5px solid var(--pg-line);border-radius:10px;background:#fff;width:100%;box-sizing:border-box}}
    .nf-reset{{font:inherit;font-size:14px;font-weight:600;min-height:44px;padding:8px 16px;border-radius:999px;border:1.5px solid var(--pg-ink);background:#fff;color:var(--pg-ink);cursor:pointer}}
    .nf-count{{font-size:15px;font-weight:600;margin:0 0 18px}}
    .nf-disclosure{{font-size:13px;color:var(--color-muted);margin:0 0 10px}}
    .nf-table{{width:100%;border-collapse:collapse;font-size:14px;line-height:1.45}}
    .nf-table th,.nf-table td{{text-align:left;vertical-align:top;padding:12px 10px;border-bottom:1px solid var(--pg-line)}}
    .nf-table thead th{{font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--color-muted);background:var(--pg-cream);position:sticky;top:0}}
    .nf-table tbody th{{font-weight:400;min-width:150px}}
    .nf-table tr[hidden]{{display:none!important}}
    .nf-model{{display:block;font-weight:700;color:var(--color-dark)}}
    .nf-sub,.nf-ns{{font-size:12.5px;color:var(--color-muted)}}
    .nf-ns{{font-style:italic}}
    .nf-sub{{display:inline-block}}
    .nf-note{{display:block;font-size:12.5px;color:var(--color-slate);margin-top:6px}}
    .nf-flag{{display:block;font-size:12.5px;color:var(--pg-muted);background:var(--pg-sand);border-radius:8px;padding:4px 8px;margin-top:6px}}
    .nf-flag[hidden]{{display:none}}
    .nf-details{{min-width:130px}}
    .nf-details a{{display:block;margin-bottom:8px}}
    .nf-table a.nf-src{{font-size:12.5px;color:var(--color-muted)}}
    .nf-buy{{display:inline-block!important;font-size:13px;font-weight:600;padding:8px 12px;border-radius:999px;background:var(--pg-teal);color:#fff;text-decoration:none;white-space:nowrap}}
    .nf-foot{{font-size:13px;color:var(--color-muted);margin:14px 0 0}}
    @media (max-width:640px){{
      .nf-table thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
      .nf-table,.nf-table tbody,.nf-table tr,.nf-table th,.nf-table td{{display:block;width:100%;box-sizing:border-box}}
      .nf-table tr{{border:1.5px solid var(--pg-line);border-radius:16px;padding:6px 14px;margin:0 0 14px;background:#fff}}
      .nf-table tbody th{{border-bottom:1px solid var(--pg-line);padding:10px 0}}
      .nf-table td{{display:grid;grid-template-columns:42% 1fr;gap:10px;padding:8px 0;border-bottom:1px solid var(--pg-line)}}
      .nf-table td:last-child{{border-bottom:0}}
      .nf-table td::before{{content:attr(data-label);font-size:12px;font-weight:600;text-transform:uppercase;color:var(--color-muted)}}
      .nf-buy{{white-space:normal}}
    }}
  </style>

  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{e(DESC)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{URL}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{TITLE}">
  <meta name="twitter:description" content="{e(DESC)}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebPage",
        "name": "Automatic litter box finder: filter by the maker's numbers",
        "description": "{e(DESC)}",
        "url": "{URL}",
        "inLanguage": "en-US",
        "dateModified": "2026-11-06",
        "publisher": {{
          "@type": "Organization",
          "name": "ClowderHub"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://www.clowderhub.com/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Litter box finder",
            "item": "{URL}"
          }}
        ]
      }}
    ]
  }}
  </script>
  <script src="/assets/nav.js?v=20261106" defer></script>
</head>
<body class="page">

{header}

  <nav class="breadcrumbs">
    <div class="container">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <span class="current">Litter box finder</span>
    </div>
  </nav>

  <main style="padding: 30px 0 80px;">
    <div class="container">
      <h1 style="font-size: 34px; font-weight: 800; line-height: 1.2; margin: 0 0 14px; color: var(--color-dark);">Automatic litter box finder: filter by the maker's numbers</h1>
      <p class="nf-intro">This tool filters {len(data)} automatic litter boxes by your cat's weight, your budget, the design, a camera and the waste drawer size. Every figure comes from the maker's own product page, and each row shows the date we read it. We do not test litter boxes. <a href="/methodology">How we compile specs</a></p>

      <form class="nf-filters" id="nf-form" onsubmit="return false">
        <label>Your cat's weight (lb)<input type="number" id="nf-weight" min="0" step="0.1" inputmode="decimal" placeholder="e.g. 14"></label>
        <label>Max budget (USD)<input type="number" id="nf-budget" min="0" step="1" inputmode="numeric" placeholder="e.g. 500"></label>
        <label>Design<select id="nf-design"><option value="">Any</option><option value="drum">Rotating drum or capsule</option><option value="open">Open-top or open-view</option></select></label>
        <label>Camera<select id="nf-camera"><option value="">Any</option><option value="yes">Must have</option></select></label>
        <label>Min waste drawer (L)<input type="number" id="nf-waste" min="0" step="0.5" inputmode="decimal" placeholder="e.g. 10"></label>
        <button type="button" class="nf-reset" id="nf-reset">Reset</button>
      </form>
      <p class="nf-count" id="nf-count" aria-live="polite">Showing {len(data)} of {len(data)} models</p>
      <p class="nf-sub" style="margin:-10px 0 18px;">Rows with missing figures stay in the results. A filter only hides a model when the maker's stated number fails it.</p>

      <p class="nf-disclosure">Some links on this page are affiliate links. We may earn a commission at no extra cost to you. <a href="/affiliate-disclosure">Details</a></p>
      <table class="nf-table" id="nf-table">
        <thead>
          <tr>
            <th scope="col">Model</th>
            <th scope="col">Price</th>
            <th scope="col">Design</th>
            <th scope="col">Cat weight</th>
            <th scope="col">Waste drawer (L)</th>
            <th scope="col">Entrance height (in)</th>
            <th scope="col">Noise (dB)</th>
            <th scope="col">Camera</th>
            <th scope="col">Details</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
      <p class="nf-foot">Prices and specs were read from each maker's site on the date shown and can change. Check the maker's page before buying.</p>
    </div>
  </main>

  <script>
    (function () {{
      const $ = id => document.getElementById(id);
      const rows = Array.from(document.querySelectorAll('#nf-table tbody tr'));
      const inputs = ['nf-weight', 'nf-budget', 'nf-design', 'nf-camera', 'nf-waste'].map($);
      const num = v => (v === '' ? null : Number(v));

      function apply() {{
        const w = num($('nf-weight').value), budget = num($('nf-budget').value);
        const design = $('nf-design').value, camera = $('nf-camera').value, waste = num($('nf-waste').value);
        let shown = 0;
        rows.forEach(tr => {{
          const d = tr.dataset, kept = [];
          const wmin = num(d.wmin), wmax = num(d.wmax), drawer = num(d.waste);
          let hide = false;
          if (w !== null) {{
            if ((wmin !== null && w < wmin) || (wmax !== null && w > wmax)) hide = true;
            else if (wmin === null || wmax === null) kept.push('cat weight limit');
          }}
          if (budget !== null && Number(d.price) > budget) hide = true;
          if (design && d.design !== design) hide = true;
          if (camera && !d.camera) kept.push('camera');
          if (waste !== null) {{
            if (drawer === null) kept.push('waste drawer size');
            else if (drawer < waste) hide = true;
          }}
          tr.hidden = hide;
          const flag = tr.querySelector('.nf-flag');
          flag.hidden = hide || !kept.length;
          flag.textContent = kept.length ? 'Kept: ' + kept.join(', ') + ' not stated by maker' : '';
          if (!hide) shown++;
        }});
        $('nf-count').textContent = 'Showing ' + shown + ' of ' + rows.length + ' models';
      }}

      // URL params: ?weight=&budget=&design=&camera=&waste= (invalid values are ignored)
      const NUM = {{ weight: ['nf-weight', 1, 40], budget: ['nf-budget', 50, 3000], waste: ['nf-waste', 1, 30] }};
      const OPT = {{ design: ['nf-design', ['drum', 'open']], camera: ['nf-camera', ['yes']] }};
      const KEYS = {{ weight: 'nf-weight', budget: 'nf-budget', design: 'nf-design', camera: 'nf-camera', waste: 'nf-waste' }};
      function readParams() {{
        const p = new URLSearchParams(location.search);
        for (const k in NUM) {{
          const [id, lo, hi] = NUM[k], v = (p.get(k) || '').trim(), n = Number(v);
          if (v !== '' && Number.isFinite(n) && n >= lo && n <= hi) $(id).value = v;
        }}
        for (const k in OPT) {{
          const [id, ok] = OPT[k];
          if (ok.includes(p.get(k))) $(id).value = p.get(k);
        }}
      }}
      function writeParams() {{
        const p = new URLSearchParams();
        for (const k in KEYS) {{
          const v = $(KEYS[k]).value.trim();
          if (v !== '') p.set(k, v);
        }}
        const q = p.toString();
        history.replaceState(null, '', location.pathname + (q ? '?' + q : '') + location.hash);
      }}

      inputs.forEach(el => el.addEventListener('input', () => {{ apply(); writeParams(); }}));
      $('nf-reset').addEventListener('click', () => {{ $('nf-form').reset(); apply(); writeParams(); }});
      readParams();
      apply();
      writeParams();
    }})();
  </script>

{footer}'''

import os
os.makedirs('tools', exist_ok=True)
open('tools/litter-box-finder.html', 'w').write(page)
print('written', len(rows), 'rows')
