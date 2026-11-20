#!/usr/bin/env python3
"""Regenerate /papers/ and one detail page per paper from the data below.

    python3 tools/build-papers.py
"""
import re, sys, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
F = ROOT / 'papers' / 'index.html'
src = open(F).read()

GH = 'https://github.com/Noraldim/'
papers = [
 dict(id='tubitak-plant-disease-platform',
  title='AI-Assisted Plant Disease Detection and Decision Support Platform',
  year='2025 &ndash; 2026', kind='T&Uuml;B&#304;TAK 2209-A research project', pages=4, lang='Turkish',
  cover='tubitak-plant-platform.jpg',
  alt='The T&Uuml;B&#304;TAK logo next to the platform pipeline: video source, YOLO leaf detection, CNN/ViT disease classifier, treatment advice',
  card='A T&Uuml;B&#304;TAK 2209-A project: a software platform that watches live drone or camera video, finds each leaf, names its disease and suggests what the farmer should do.',
  tags=['T&Uuml;B&#304;TAK 2209-A','YOLO','ByteTrack','FastAPI','Raspberry Pi','Edge AI'],
  lead='Plant diseases are usually noticed too late, and checking large fields by eye or in a lab is slow and expensive. This T&Uuml;B&#304;TAK 2209-A project, supervised by Dr. Ay&#351;enur T&uuml;rkmen at Bilecik &#350;eyh Edebali University, builds a fully software-based platform that works on <em>continuous video</em> instead of single photos. It finds each leaf, names the disease, records it once, and turns the result into treatment advice. It works with any drone, field camera or Raspberry Pi, and any trained model can be swapped in while it runs.',
  stats=[('2','stages: YOLO finds the leaf, a CNN / ViT names the disease'),('900&nbsp;&rarr;&nbsp;1','duplicate records per leaf, cut by track-based de-duplication'),('38','disease classes in the integrated PlantVillage classifier'),('0','location or personal data stored')],
  covers=[
   '<b>An API-first architecture</b> on Python, FastAPI, Ultralytics, PyTorch, OpenCV and SQLite. The web interface, a future mobile app and edge devices all share one REST interface, and inference never runs inside a request handler.',
   '<b>Source abstraction:</b> screen capture (for a drone app mirrored to a PC), video files, USB/CSI cameras and RTSP streams can be switched at runtime without stopping the pipeline.',
   '<b>Decoupled capture and inference</b> through a single latest-frame slot instead of a queue. Old frames are dropped, so latency never builds up and the system adapts itself to the hardware it runs on.',
   '<b>Two-stage detection:</b> YOLO (v8/11) locates each leaf and ByteTrack gives it an ID, then a MobileNetV2 or ViT classifier names the disease on the crop.',
   '<b>De-duplication:</b> one diseased leaf in view for 30&nbsp;s at 30&nbsp;FPS would create about 900 identical records. Persistent track IDs, a per-ID cool-down, a confidence threshold and a minimum box area cut that to one.',
   '<b>A decision-support engine</b> that maps each disease to its risk, symptoms, treatment and a natural remedy. A <b>model registry</b> hot-swaps any uploaded <code>.pt</code> model, with a staged path from ready-made models to fully custom ones.',
   '<b>Raspberry Pi edge node</b> in two modes: stream video to a GPU server, or run a lightweight YOLO11n on the Pi and send only detections, which saves bandwidth.',
   '<b>An honest baseline (Phase 0):</b> the untrained system identified the plant species correctly but forced out-of-scope plants into the nearest disease class with up to 0.91 confidence. High confidence is not correctness, and this finding justifies training on field data with an &ldquo;unknown&rdquo; class.',
  ],
  links=[('pdf','tubitak-plant-disease-platform.pdf')]),
 dict(id='urban-planner',
  title='Land Segmentation and Smart-City Planning from Satellite Imagery',
  year='2025', kind='Senior capstone', pages=9, lang='English',
  cover='urban-planner.jpg',
  alt='A Sentinel-2 satellite tile, its buildable-land mask, and the city plan generated on top of it',
  card='Finding land that is free to build on in Sentinel-2 imagery with seven deep segmentation models, then laying out a whole district on it automatically.',
  tags=['Semantic Segmentation','U-Net','DeepLabV3+','Sentinel-2','Urban Planning'],
  lead='Every new district starts with the same question: <em>where is there land that can be built on?</em> Today that is still answered by hand, from cadastral records and photo-interpretation. Urban-Planner answers it end-to-end. It segments open land in 10&nbsp;m Sentinel-2 imagery with deep encoder&ndash;decoder networks, then hands the mask to a rule-based planner that places a full district (houses, apartments, shops, schools, a hospital, a stadium) with no overlaps.',
  stats=[('0.942','overall score, DeepLabV3+ with ResNet-101'),('0.938','best Dice score (U-Net, ResNet-101)'),('0.725','Dice of a trivial &ldquo;all land&rdquo; baseline'),('84%','of tiles fit the full 236-building plan')],
  covers=[
   'Turning the 2,433 patches of the PASTIS benchmark into a binary <em>open land</em> vs. <em>background</em> target (60.1% positive pixels), and analysing the resulting dataset.',
   'Seven models compared under one metric suite: U-Net with ResNet-34, ResNet-101 and VGG-16 encoders, and DeepLabV3+ with ResNet-50, ResNet-101, Xception and EfficientNet-B5. Each one is described down to the layer its features are tapped from.',
   'The result: DeepLabV3+ beats U-Net and is more robust to configuration, and ResNet-101 is the best encoder in both families. The layer-level analysis shows that the Xception and EfficientNet-B5 taps sit one stride level higher than intended.',
   'An honest reading of the protocol. The reported scores are computed on images seen during training, so they are upper bounds, and the paper proposes a fold-based protocol to fix that.',
   'A formal, reproducible version of the smart-city planner. When a tile fails, it is because the land is too <em>fragmented</em>, not because there is too little of it.',
  ],
  links=[('pdf','urban-planner-land-segmentation.pdf'),('code',GH+'Urban-Planner')]),
 dict(id='astron',
  title='ASTRON: Real-Time UAV Detection and Trajectory Prediction with YOLOv8 and a Kalman Filter',
  year='2024', kind='Research article', pages=16, lang='English',
  cover='astron-kalman.jpg',
  alt='A drone flying a circle: the true path, noisy YOLO detections and the Kalman filter forecast',
  card='A custom YOLOv8 drone detector paired with a constant-velocity Kalman filter. The paper covers the theory, every implementation choice and what each one costs in pixels.',
  tags=['YOLOv8','Kalman Filter','Object Tracking','OpenCV','State Estimation'],
  lead='Detecting a drone in a video tells you where it <em>is</em>. Predicting where it <em>will be</em> is what lets a camera, a gimbal or an interceptor follow it. ASTRON is a compact real-time system that couples a YOLOv8 detector with a discrete-time Kalman filter built on OpenCV. The paper is a complete, self-contained account of it, from the network architecture to the filter maths to simulations that drive the <em>actual</em> OpenCV filter.',
  stats=[('0.956','mAP@0.5 of the custom <em>uav</em> detector'),('3.0&nbsp;M','detector parameters'),('5.7&nbsp;px','forecast error after tuning (down from 10.7)'),('45&times;','error reduction from a measurement gate')],
  covers=[
   'The YOLOv8 architecture, and a single-class <em>uav</em> detector trained for 100 epochs on the <em>IHA Nesne Tespit</em> dataset: precision 0.927, recall 0.905, mAP@0.5:0.95 of 0.582.',
   'The Kalman filter derived from first principles and specialised to ASTRON&rsquo;s four-state constant-velocity model.',
   'What every implementation choice really does: OpenCV&rsquo;s default covariances (Q&nbsp;=&nbsp;R&nbsp;=&nbsp;I, P<sub>0</sub>&nbsp;=&nbsp;0), the <em>correct-then-predict</em> call order that turns the output into a one-step-ahead forecast, and the coupling with a colour-threshold localiser.',
   'A proof that the filter settles into a steady-state &alpha;&ndash;&beta; tracker with &alpha;&nbsp;=&nbsp;0.822 and &beta;&nbsp;=&nbsp;0.422.',
   'Reproducible experiments on straight-line motion, a circular manoeuvre and missed detections. The default tuning <em>amplifies</em> detector noise, and a noise ratio r/q&nbsp;&asymp;&nbsp;100 fixes it. When the target is missed, the localiser reports the image origin, which can drag the prediction by more than 500&nbsp;px. A simple gate cuts that to 11&nbsp;px.',
   'A concrete roadmap from ASTRON to a full tracking-by-detection system.',
  ],
  links=[('pdf','astron-uav-kalman.pdf'),('code',GH+'ASTRON')]),
 dict(id='bcd-radix',
  title='From Decimal Digits to Binary Bits: Radix Conversion in C, IA-32 and x86-64',
  year='2024 &ndash; 2025', kind='Computer architecture', pages=6, lang='English',
  cover='bcd-radix.jpg',
  alt='The decimal number 532.13022 converted to binary, bit by bit, with the repeated-doubling steps',
  card='One conversion algorithm followed all the way down: the mathematics, the C code, the machine code GCC emits for two architectures, and a web front-end.',
  tags=['C','IA-32','x86-64','IEEE 754','Computer Architecture'],
  lead='Every number a person types is decimal, and every number a processor stores is binary. The boundary between the two is where bugs like <code>0.1&nbsp;+&nbsp;0.2&nbsp;!=&nbsp;0.3</code> come from. This paper takes the BM_Architecture course project, which converts BCD-style decimal inputs such as <code>532.13022</code> into binary, and follows it from the mathematics to the machine code to the browser.',
  stats=[('2<sup>&minus;10</sup>','worst-case error of the C program (exact for dyadic fractions)'),('25&ndash;55','fractional bits printed by the web converter'),('2','instruction sets compared side by side'),('6','robustness defects found and characterised')],
  covers=[
   'The two classical algorithms, repeated division for the integer part and repeated doubling for the fraction, formalised with proofs of correctness, termination and the truncation-error bound &epsilon;&nbsp;&lt;&nbsp;2<sup>&minus;n</sup>.',
   'A line-by-line walk through the C implementation.',
   'The machine code GCC&nbsp;12.2 produces for both targets: IA-32&rsquo;s stack-based x87 FPU and cdecl calling convention versus the SSE2 register file and System&nbsp;V AMD64 ABI of x86-64. Every compiler idiom is explained.',
   'The HTML/JavaScript front-end: a BCD number generator, and a 16-bit sign-magnitude binary calculator whose loop length depends on the unit in the last place of an IEEE-754 double.',
   'An experimental evaluation, six robustness defects (negative inputs, <code>int</code> overflow, malformed input and more), and an exact, integer-only conversion routine that removes all floating-point error.',
  ],
  links=[('pdf','bcd-radix-conversion.pdf'),('code',GH+'BM_Architecture'),('demo','https://www.binary.alpharesearch.me/')]),
 dict(id='plant-leaf-disease',
  title='Automated Diagnosis of Plant Leaf Diseases Using Machine Learning',
  year='2025', kind='Image processing', pages=15, lang='Turkish',
  cover='plant-leaf-disease.jpg',
  alt='A diseased leaf with dark lesions next to a grid of segmented grayscale leaf images',
  card='An image-processing pipeline for recognising leaf diseases, trained on phone photos from a home garden and on the PlantVillage dataset.',
  tags=['Image Processing','Neural Networks','OpenCV','NumPy','PlantVillage'],
  lead='Can a neural network tell a healthy leaf from a sick one? This project builds the whole pipeline from scratch on two very different sources. One is photos taken with a phone in the author&rsquo;s own garden, under changing light and on natural backgrounds. The other is the clean, labelled PlantVillage dataset from Kaggle. The report walks through every step, from the raw photo to the predicted class.',
  stats=[('2','datasets: home garden and PlantVillage'),('128&times;128','normalised grayscale input'),('4','hand-crafted features per region of interest'),('&asymp;60%','test accuracy')],
  covers=[
   'Image collection and preprocessing: resizing to a fixed 128&times;128, grayscale conversion and normalisation to [0,&nbsp;1].',
   'Labelling and one-hot encoding of disease classes, and how an image becomes a NumPy matrix the model can read.',
   'Region-of-interest selection and feature extraction: pixel mean and variance, Canny edge density, colour histogram and contour count.',
   'Training a multi-layer neural network and testing it on images it has never seen.',
   'An honest observation: the model does better on the standardised PlantVillage images than on the garden photos, because real-world lighting and image quality vary much more.',
  ],
  links=[('pdf','plant-leaf-disease-diagnosis.pdf'),('code',GH+'Training-CNN-Models')]),
]

def card(p):
    tags=''.join(f'<span>{t}</span>' for t in p['tags'])
    return f'''<a class="nk-card nk-paper" href="/papers/{p['id']}/">
  <div class="nk-cover"><img src="/papers/covers/{p['cover']}" alt="{p['alt']}" width="1200" height="675" loading="lazy"></div>
  <div class="nk-paper-body">
    <div class="nk-card-head"><h3>{p['title']}</h3><span class="nk-date">{p['year']}</span></div>
    <p class="nk-role">{p['kind']} &middot; {p['pages']} pages{' &middot; ' + p['lang'] if p['lang']!='English' else ''}</p>
    <p class="nk-desc">{p['card']}</p>
    <div class="nk-tags">{tags}</div>
    <span class="nk-more">Read more <i class="fas fa-arrow-right fa-fw" aria-hidden="true"></i></span>
  </div>
</a>'''

certs = '<h3 class="nk-group">Certifications</h3><div class="nk-facts"><div class="nk-fact"><b>Apr. 2025</b><span>Google IT Support Professional Certificate &mdash; Google</span></div><div class="nk-fact"><b>Nov. 2023</b><span>Containers, Kubernetes, and OpenShift V2 &mdash; IBM</span></div><div class="nk-fact"><b>June 2023</b><span>Data Analysis in Python (Pandas) &mdash; Udemy</span></div></div>'

import os
SITE = str(ROOT)

def actions(p):
    acts=[]
    for kind,url in p['links']:
        if kind=='pdf':
            acts.append(f'<a class="nk-btn nk-btn-primary" href="/papers/pdf/{url}" target="_blank" rel="noopener"><i class="fas fa-book-open fa-fw" aria-hidden="true"></i>Read the paper</a>')
            acts.append(f'<a class="nk-btn" href="/papers/pdf/{url}" download><i class="fas fa-download fa-fw" aria-hidden="true"></i>Download PDF</a>')
        elif kind=='code':
            acts.append(f'<a class="nk-btn" href="{url}" target="_blank" rel="noopener noreferrer"><i class="fab fa-github fa-fw" aria-hidden="true"></i>Source code</a>')
        elif kind=='demo':
            acts.append(f'<a class="nk-btn" href="{url}" target="_blank" rel="noopener noreferrer"><i class="fas fa-external-link-alt fa-fw" aria-hidden="true"></i>Live demo</a>')
    return '<div class="nk-actions">' + ''.join(acts) + '</div>'

def detail(i, p):
    stats=''.join(f'<div class="nk-stat"><b>{v}</b><span>{l}</span></div>' for v,l in p['stats'])
    items=''.join(f'<li>{c}</li>' for c in p['covers'])
    tags=''.join(f'<span>{t}</span>' for t in p['tags'])
    prev_p = papers[i-1] if i > 0 else None
    next_p = papers[i+1] if i+1 < len(papers) else None
    nav = '<nav class="nk-paper-nav" aria-label="More papers">'
    nav += (f'<a class="nk-paper-nav-prev" href="/papers/{prev_p["id"]}/"><small><i class="fas fa-arrow-left fa-fw" aria-hidden="true"></i> Previous</small><span>{prev_p["title"]}</span></a>' if prev_p else '<span></span>')
    nav += (f'<a class="nk-paper-nav-next" href="/papers/{next_p["id"]}/"><small>Next <i class="fas fa-arrow-right fa-fw" aria-hidden="true"></i></small><span>{next_p["title"]}</span></a>' if next_p else '<span></span>')
    nav += '</nav>'
    return f"""<div class="page single nk-paper-page">
<a class="nk-back" href="/papers/"><i class="fas fa-arrow-left fa-fw" aria-hidden="true"></i> All papers</a>
<article class="nk-paper-detail">
  <p class="nk-role">{p['kind']} &middot; {p['year']} &middot; {p['pages']} pages &middot; {p['lang']}</p>
  <h1 class="nk-paper-title">{p['title']}</h1>
  <img class="nk-detail-cover" src="/papers/covers/{p['cover']}" alt="{p['alt']}" width="1200" height="675">
  {actions(p)}
  <h2>What it is about</h2>
  <p class="nk-detail-lead">{p['lead']}</p>
  <div class="nk-stats">{stats}</div>
  <h2>What the paper covers</h2>
  <ul class="nk-covers">{items}</ul>
  <div class="nk-tags">{tags}</div>
  {actions(p)}
</article>
{nav}
</div></div>"""

MAIN_START = '<div class="page archive nk-wide">'
MAIN_END = '\n            </main>'
a = src.index(MAIN_START); b = src.index(MAIN_END)
# strip the old pop-up script if present
import re as _re
template = _re.sub(r'<script type="text/javascript">\n\(function \(\) \{\n  if \(typeof HTMLDialogElement.*?</script>', '', src, flags=_re.S)
a = template.index(MAIN_START); b = template.index(MAIN_END)

desc = 'Research papers by Noraldim Kamis: satellite land segmentation and city planning, YOLOv8 drone tracking with a Kalman filter, radix conversion across C, IA-32 and x86-64, and plant leaf disease diagnosis.'
def set_meta(page, title, d, url, img=None):
    page = page.replace('<title>Papers - noraldim</title>', f'<title>{title} - noraldim</title>')
    page = re.sub(r'(<meta name="Description" content=")[^"]*', lambda m: m.group(1)+d, page)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1)+d, page)
    page = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1)+d, page)
    page = page.replace('<meta property="og:title" content="Papers" />', f'<meta property="og:title" content="{title}" />')
    page = page.replace('<meta name="twitter:title" content="Papers"/>', f'<meta name="twitter:title" content="{title}"/>')
    page = page.replace('content="https://noraldim.net/papers/"', f'content="{url}"')
    page = page.replace('<link rel="canonical" href="https://noraldim.net/papers/" />', f'<link rel="canonical" href="{url}" />')
    page = re.sub(r'<meta property="og:image"[^>]*>', '', page)
    if img:
        page = page.replace('<meta name="twitter:card" content="summary"/>', f'<meta property="og:image" content="{img}" /><meta name="twitter:card" content="summary_large_image"/><meta name="twitter:image" content="{img}"/>')
    return page

index_main = ('<div class="page archive nk-wide"><h2 class="single-title animate__animated animate__pulse animate__faster">Papers</h2>'
 '<p class="nk-lead">Longer-form technical work: the research articles and reports behind the projects. Open a paper to see what it is about, then read the full PDF.</p>'
 '<div class="nk-grid nk-paper-grid">' + '\n'.join(card(p) for p in papers) + '</div>'
 + certs +
 '<p class="nk-note">Shorter pieces and tutorials live under <a href="/articles/">Articles</a>; the code sits in <a href="/projects/">Projects</a>.</p></div></div>')
index_page = template[:a] + index_main + template[b:]
open(F, 'w').write(set_meta(index_page, 'Papers', desc, 'https://noraldim.net/papers/'))

def plain(t): return html.unescape(re.sub(r'<[^>]+>', '', t)).replace('"', '&quot;')
for i, p in enumerate(papers):
    page = template[:a] + detail(i, p) + template[b:]
    page = set_meta(page, plain(p['title']), plain(p['card']), f"https://noraldim.net/papers/{p['id']}/",
                    f"https://noraldim.net/papers/covers/{p['cover']}")
    os.makedirs(f"{SITE}/papers/{p['id']}", exist_ok=True)
    open(f"{SITE}/papers/{p['id']}/index.html", 'w').write(page)

# sitemap
sm_path = SITE + '/sitemap.xml'; sm = open(sm_path).read()
for p in papers:
    loc = f"https://noraldim.net/papers/{p['id']}/"
    if loc not in sm:
        sm = sm.replace('</urlset>', f'<url>\n            <loc>{loc}</loc><lastmod>2026-11-20T00:00:00&#43;03:00</lastmod></url></urlset>')
open(sm_path, 'w').write(sm)
print('ok')
