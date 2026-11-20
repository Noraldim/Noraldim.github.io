#!/usr/bin/env python3
"""Regenerate the main content of /projects/index.html from the PROJECT data below.

    python3 tools/build-projects.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'projects' / 'index.html'
GH = 'https://github.com/Noraldim/'

HIGHLIGHTS = [
    ('3', 'production platforms live, used by schools, merchants and healthcare staff'),
    ('120+', 'active users on a government health-education platform I delivered'),
    ('5', 'research papers, including a TÜBİTAK 2209-A project'),
    ('Finalist', 'at TEKNOFEST, Türkiye&rsquo;s national technology competition'),
]

# kind: live | paper | code | demo | article
FEATURED = [
    dict(cat='web', cover='/projects/covers/madaries.jpg',
         alt='The Madaries landing page in Arabic: one platform that runs many schools',
         meta='2025 &middot; Multi-tenant SaaS &middot; Web + Android',
         title='Madaries &mdash; School Management Platform',
         pitch='One platform that runs many schools: student records, grades, attendance, timetables, finance and reports, with every school&rsquo;s data kept completely separate.',
         points=[
             'Multi-tenant architecture on <b>Next.js</b> and <b>PostgreSQL</b>: many schools run from a single deployment with per-school data isolation.',
             '<b>Eight permission-scoped roles</b> across student records, grading, attendance, timetabling and finance.',
             '<b>Redis</b> caching in front of PostgreSQL keeps response times steady under concurrent load.',
             'Two-factor authentication, full activity logging and automated backups. Released in Arabic and English (RTL) on the web and <b>Google Play</b>.',
         ],
         tags=['Next.js', 'PostgreSQL', 'Redis', 'Multi-tenancy', 'RBAC', '2FA', 'Arabic / RTL'],
         links=[('live', 'https://madaries.com', 'madaries.com')]),
    dict(cat='web', cover='/projects/covers/elsiraj.jpg',
         alt='The Elsiraj landing page: a digital intermediary connecting trusted merchants with customers',
         meta='2026 &middot; Fintech marketplace',
         title='Elsiraj &mdash; Currency-Exchange Marketplace',
         pitch='A digital intermediary between customers and verified currency merchants: a clear order, evidence kept on record, and a full history from the first step to the money arriving.',
         points=[
             'Merchant storefronts publish <b>live rates and limits</b> before anyone places an order.',
             'Orders are created against a <b>locked-in rate</b>, so the customer sees the applied rate and exact payout before confirming.',
             '<b>Payment-proof uploads</b> and merchant verification, with an auditable history for every transaction.',
             'One customer account across every merchant. Bilingual Arabic / English with full right-to-left support, installable as a <b>PWA</b>.',
         ],
         tags=['Next.js', 'PostgreSQL', 'PWA', 'Fintech', 'Arabic / RTL', 'i18n'],
         links=[('live', 'https://elsiraj.com', 'elsiraj.com')]),
    dict(cat='web', cover='/projects/covers/health-education.jpg',
         alt='The SEP sign-in page: a modern training platform for healthcare professionals',
         meta='2026 &middot; Baynal Group &middot; Government contract',
         title='SEP &mdash; National Healthcare Education Platform',
         pitch='A training platform delivered for the <b>Bilecik Provincial Health Directorate</b>. Healthcare staff take mandatory and elective trainings, earn digital certificates and track their progress.',
         points=[
             'Built the <b>web application</b>, its <b>REST APIs</b> and the companion <b>cross-platform mobile app</b> end-to-end.',
             'Online trainings, instant digital certificates, real-time progress reporting and mobile notifications.',
             'Sign-in by email or Turkish ID number, with Turkish and English throughout.',
             'In production: the live site reports <b>120+ active users</b>, 40+ trainings and 6 departments.',
         ],
         tags=['React', 'Next.js', 'REST API', 'Mobile app', 'i18n'],
         links=[('live', 'https://saglikegitimplatformu.com.tr/', 'saglikegitimplatformu.com.tr')]),
    dict(cat='ai', cover='/papers/covers/urban-planner.jpg',
         alt='A satellite tile, its buildable-land mask, and the city plan generated on top of it',
         meta='2025 &ndash; 2026 &middot; Senior capstone &middot; Computer vision',
         title='AI-Driven Urban Planner',
         pitch='From satellite pixels to a city plan. Deep segmentation finds land that is free to build on, then an automated planner lays out a whole district on top of it.',
         points=[
             'Segments 10&nbsp;m <b>Sentinel-2</b> imagery. Seven <b>U-Net</b> and <b>DeepLabV3+</b> models are compared on a binary open-land dataset derived from PASTIS.',
             'The best model (DeepLabV3+ with ResNet-101) reaches a <b>0.942</b> overall score and 0.937 Dice, well above the 0.725 of a trivial baseline.',
             'A rule-based, conflict-free planner places hospitals, stadiums, malls, apartments and houses. A <b>236-building plan</b> fits completely on 84% of tiles.',
             'Results are rendered as an interactive 3D web visualization.',
         ],
         tags=['Python', 'TensorFlow / Keras', 'U-Net', 'DeepLabV3+', 'Sentinel-2', 'JavaScript'],
         links=[('paper', '/papers/urban-planner/', 'Read the paper'), ('code', GH + 'Urban-Planner', 'Source code')]),
    dict(cat='ai', cover='/projects/covers/drone-fire.jpg',
         alt='Illustration of a drone camera view detecting a fire in a field, with a GPS lock',
         meta='2023 &middot; TEKNOFEST national finalist',
         title='Drone-Based Fire Detection System',
         pitch='A drone that finds fires in the field and tells the ground team exactly where they are.',
         points=[
             'A drone-mounted system that <b>detects fire from the air</b>.',
             'Streams <b>real-time imagery with GPS coordinates</b> to a ground control station.',
             'Advanced to the <b>national finals of TEKNOFEST</b>, Türkiye&rsquo;s largest aerospace and technology competition.',
         ],
         tags=['Computer Vision', 'UAV', 'Telemetry', 'GPS'],
         links=[]),
]

MORE = [
    dict(cat='infra', icon='fa-network-wired', year='2024 &ndash; 2025',
         title='Campus Network &amp; Container Infrastructure', meta='Bilecik &Scedil;eyh Edebali University &middot; Network Engineer',
         desc='Ran the university-wide server, switch and DNS infrastructure. Moved internal services onto Docker and Kubernetes, set up Graylog for centralized logging, and hardened Linux and network systems across campus.',
         tags=['Docker', 'Kubernetes', 'DNS', 'Graylog', 'Linux hardening'], links=[]),
    dict(cat='ai', icon='fa-crosshairs', year='2024',
         title='ASTRON &mdash; Drone Detection &amp; Tracking', meta='YOLOv8 &middot; Kalman filter',
         desc='Real-time drone detection and trajectory prediction. A custom YOLOv8 detector (0.956 mAP@0.5, 3.0&nbsp;M parameters) is paired with a constant-velocity Kalman filter, and tuning cut the forecast error from 10.7 to 5.7&nbsp;px.',
         tags=['Python', 'YOLOv8', 'OpenCV', 'Kalman Filter'],
         links=[('paper', '/papers/astron/', 'Paper'), ('code', GH + 'ASTRON', 'Code')]),
    dict(cat='ai', icon='fa-brain', year='2025',
         title='Alpha Research &mdash; LLM Customer Insight Engine', meta='Data + LLM',
         desc='Customer data-analysis algorithms wired into a large language model, so answers are grounded in real customer data instead of generic model output.',
         tags=['Python', 'LLM', 'pandas'],
         links=[('live', 'https://alpharesearch.me', 'alpharesearch.me')]),
    dict(cat='ai', icon='fa-leaf', year='2025',
         title='Plant Leaf Disease Diagnosis', meta='Image processing &middot; Neural network',
         desc='A full pipeline from garden phone photos and the PlantVillage dataset: preprocessing, region-of-interest features (edge density, histograms, contours) and a neural-network classifier.',
         tags=['Python', 'OpenCV', 'NumPy', 'Neural Networks'],
         links=[('paper', '/papers/plant-leaf-disease/', 'Paper'), ('code', GH + 'Training-CNN-Models', 'Code')]),
    dict(cat='systems', icon='fa-microchip', year='2024 &ndash; 2025',
         title='BCD to Binary Converter', meta='C &middot; IA-32 &middot; x86-64',
         desc='Decimal-to-binary conversion analysed from the maths down to the machine code GCC emits for IA-32 and x86-64, plus a browser-based binary calculator and an exact, integer-only fix.',
         tags=['C', 'Assembly', 'x86-64', 'JavaScript'],
         links=[('paper', '/papers/bcd-radix/', 'Paper'), ('demo', 'https://www.binary.alpharesearch.me/', 'Demo'), ('code', GH + 'BM_Architecture', 'Code')]),
    dict(cat='systems', icon='fa-comments', year='2023',
         title='Telegram Chatbot from My Chat History', meta='Python &middot; PostgreSQL',
         desc='A bot that answers in my own voice: regex-based cleaning of chat exports, UTF-8-safe storage in PostgreSQL via psycopg2, and replies through the Telegram Bot API.',
         tags=['Python', 'PostgreSQL', 'Telegram Bot API'],
         links=[('article', '/posts/cat/', 'Article'), ('code', GH + 'CHAT-BOT', 'Code')]),
    dict(cat='infra', icon='fa-shield-halved', year='2023 &ndash; 2025',
         title='Server Provisioning &amp; Hardening', meta='Bash &middot; Ansible',
         desc='Brings a fresh server to a safe baseline: package updates, rsync, git and ufw, a configured firewall and key-based root access instead of a password. The same setup is automated with Ansible playbooks and inventory.',
         tags=['Bash', 'Ansible', 'ufw', 'SSH', 'Linux'],
         links=[('code', GH + 'Server_setUp', 'Bash script'), ('code', GH + 'Ansible_confing', 'Ansible')]),
    dict(cat='web', icon='fa-chart-line', year='2024',
         title='D3 Data Visualization', meta='Internet programming',
         desc='Interactive browser visualizations built with D3: data binding, scales and transitions across three exercises.',
         tags=['D3.js', 'JavaScript', 'SVG'],
         links=[('code', GH + 'D3_project', 'Code')]),
    dict(cat='systems', icon='fa-code', year='2025',
         title='Competitive Programming', meta='Codeforces',
         desc='Codeforces solutions in Python, kept as a running log of algorithm and data-structure practice.',
         tags=['Python', 'Algorithms', 'Data Structures'],
         links=[('code', GH + 'Code-Forces', 'Code')]),
]

CATS = [('all', 'All'), ('web', 'Web &amp; product'), ('ai', 'AI &amp; research'),
        ('infra', 'Cloud &amp; infrastructure'), ('systems', 'Systems &amp; tools')]

ICON = {'live': 'fas fa-arrow-up-right-from-square', 'paper': 'fas fa-file-lines', 'code': 'fab fa-github',
        'demo': 'fas fa-play', 'article': 'fas fa-pen-nib'}


def link(kind, url, label, primary=False):
    ext = url.startswith('http')
    attrs = ' target="_blank" rel="noopener noreferrer"' if ext else ''
    cls = 'nk-btn nk-btn-primary' if primary else 'nk-btn'
    return f'<a class="{cls}" href="{url}"{attrs}><i class="{ICON[kind]} fa-fw" aria-hidden="true"></i>{label}</a>'


def tags(ts):
    return '<div class="nk-tags">' + ''.join(f'<span>{t}</span>' for t in ts) + '</div>'


def featured(p):
    first = p['links'][0][1] if p['links'] else None
    img = f'<img src="{p["cover"]}" alt="{p["alt"]}" width="1200" height="675" loading="lazy">'
    media = (f'<a class="nk-feature-media" href="{first}"' + (' target="_blank" rel="noopener noreferrer"' if first.startswith('http') else '') + f'>{img}</a>'
             if first else f'<div class="nk-feature-media">{img}</div>')
    pts = ''.join(f'<li>{x}</li>' for x in p['points'])
    acts = ''.join(link(k, u, l, primary=(i == 0)) for i, (k, u, l) in enumerate(p['links']))
    return f'''<article class="nk-feature" data-cat="{p['cat']}">
  {media}
  <div class="nk-feature-body">
    <p class="nk-role">{p['meta']}</p>
    <h3>{p['title']}</h3>
    <p class="nk-feature-pitch">{p['pitch']}</p>
    <ul class="nk-feature-points">{pts}</ul>
    {tags(p['tags'])}
    {'<div class="nk-actions">' + acts + '</div>' if acts else ''}
  </div>
</article>'''


def more(p):
    links = ''.join(
        f'<a href="{u}"' + (' target="_blank" rel="noopener noreferrer"' if u.startswith('http') else '') +
        f'><i class="{ICON[k]} fa-fw" aria-hidden="true"></i>{l}</a>' for k, u, l in p['links'])
    return f'''<article class="nk-card nk-proj" data-cat="{p['cat']}">
  <div class="nk-proj-head"><span class="nk-proj-icon"><i class="fas {p['icon']} fa-fw" aria-hidden="true"></i></span><span class="nk-date">{p['year']}</span></div>
  <h3>{p['title']}</h3>
  <p class="nk-role">{p['meta']}</p>
  <p class="nk-desc">{p['desc']}</p>
  {tags(p['tags'])}
  {'<div class="nk-links">' + links + '</div>' if links else ''}
</article>'''


SCRIPT = '''<script type="text/javascript">
(function () {
  var buttons = document.querySelectorAll('.nk-filter button');
  if (!buttons.length) return;
  function apply(cat) {
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.cat === cat)); });
    document.querySelectorAll('.nk-projects [data-cat]').forEach(function (el) {
      if (el.tagName === 'BUTTON') return;
      el.hidden = !(cat === 'all' || el.dataset.cat === cat);
    });
    document.querySelectorAll('.nk-projects [data-section]').forEach(function (sec) {
      sec.hidden = !sec.querySelector('[data-cat]:not([hidden])');
    });
  }
  buttons.forEach(function (b) { b.addEventListener('click', function () { apply(b.dataset.cat); }); });
})();
</script>'''


def build():
    hl = ''.join(f'<div class="nk-highlight"><b>{v}</b><span>{l}</span></div>' for v, l in HIGHLIGHTS)
    chips = ''.join(f'<button type="button" data-cat="{c}" aria-pressed="{str(c == "all").lower()}">{n}</button>' for c, n in CATS)
    main = ('<div class="page archive nk-wide nk-projects">'
            '<h2 class="single-title animate__animated animate__pulse animate__faster">Projects</h2>'
            '<p class="nk-lead">Software I have designed, built and shipped: production platforms used every day by schools, '
            'merchants and healthcare staff, research in computer vision, and the infrastructure underneath it all.</p>'
            f'<div class="nk-highlights">{hl}</div>'
            f'<div class="nk-filter" role="group" aria-label="Filter projects">{chips}</div>'
            '<section data-section><h3 class="nk-group">Featured work</h3>'
            + '\n'.join(featured(p) for p in FEATURED) +
            '</section><section data-section><h3 class="nk-group">More projects</h3><div class="nk-grid nk-proj-grid">'
            + '\n'.join(more(p) for p in MORE) +
            '</div></section>'
            '<p class="nk-note">All public code lives on <a href="https://github.com/Noraldim" target="_blank" rel="noopener noreferrer">github.com/Noraldim</a>. '
            'The research behind several of these projects is written up under <a href="/papers/">Papers</a>.</p>'
            '</div></div>')
    src = PAGE.read_text(encoding='utf-8')
    a = src.index('<div class="page archive nk-wide')
    b = src.index('\n            </main>')
    src = src[:a] + main + src[b:]
    src = re.sub(r'<script type="text/javascript">\n\(function \(\) \{\n  var buttons = document.querySelectorAll\(\'\.nk-filter button\'\);.*?</script>', '', src, flags=re.S)
    src = src.replace('</body>', SCRIPT + '</body>', 1)
    desc = ('Projects by Noraldim Kamis: Madaries multi-tenant school SaaS, Elsiraj currency-exchange marketplace, '
            'a government healthcare education platform, an AI urban planner from satellite imagery, and a TEKNOFEST-finalist fire-detection drone.')
    for pat in [r'(<meta name="Description" content=")[^"]*', r'(<meta property="og:description" content=")[^"]*',
                r'(<meta name="twitter:description" content=")[^"]*']:
        src = re.sub(pat, lambda m: m.group(1) + desc, src)
    PAGE.write_text(src, encoding='utf-8')
    print('wrote', PAGE.relative_to(ROOT))


if __name__ == '__main__':
    build()
