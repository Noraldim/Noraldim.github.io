#!/usr/bin/env python3
"""Stamp every page's custom.css link with a version taken from the file's contents.

Browsers cache /css/custom.css, so after a CSS change returning visitors can
see the old styles. Run this after editing css/custom.css:
    python3 tools/bump-css-version.py
"""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
version = hashlib.sha1((ROOT / 'css' / 'custom.css').read_bytes()).hexdigest()[:10]
pattern = re.compile(r'href="/css/custom\.css(\?v=[0-9a-f]+)?"')
changed = 0
for page in ROOT.rglob('*.html'):
    if '.git' in page.parts:
        continue
    src = page.read_text(encoding='utf-8')
    new = pattern.sub(f'href="/css/custom.css?v={version}"', src)
    if new != src:
        page.write_text(new, encoding='utf-8')
        changed += 1
print(f'custom.css version {version}: updated {changed} pages')
