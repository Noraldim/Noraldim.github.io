#!/usr/bin/env python3
"""Rebuild /index.json, the search index used by the header search box.

Run from the repository root after adding or editing a page:
    python3 tools/build-search-index.py
"""
import glob
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'papers/index.html', 'papers/*/index.html',
         'articles/index.html', 'posts/*/index.html', 'projects/index.html']
SKIP_BLOCKS = re.compile(r'<(script|style|nav|svg)\b.*?</\1>', re.S | re.I)


def text_of(fragment):
    fragment = SKIP_BLOCKS.sub(' ', fragment)
    fragment = re.sub(r'<[^>]+>', ' ', fragment)
    return re.sub(r'\s+', ' ', html.unescape(fragment)).strip()


def main():
    entries = []
    for pattern in PAGES:
        for path in sorted(glob.glob(str(ROOT / pattern))):
            src = Path(path).read_text(encoding='utf-8')
            rel = Path(path).relative_to(ROOT).as_posix()
            uri = '/' + rel[:-len('index.html')]
            title = re.search(r'<title>(.*?)</title>', src, re.S).group(1)
            title = html.unescape(re.sub(r'\s*-\s*noraldim$', '', title)).strip()
            if uri == '/':
                title = 'Noraldim Kamis'
            main_html = src[src.find('<main'):src.find('</main>')]
            date = re.search(r'<time datetime="([^"]+)"', main_html)
            desc = re.search(r'<meta name="Description" content="([^"]*)"', src)
            body = re.sub(r'<div class="nk-actions">.*?</div>', ' ', main_html, flags=re.S)
            body = re.sub(r'<a class="nk-back".*?</a>', ' ', body, flags=re.S)
            entries.append({
                'objectID': uri,
                'uri': uri,
                'title': title,
                'date': date.group(1) if date else '',
                'tags': [], 'categories': [],
                'content': (html.unescape(desc.group(1)) + ' ' if desc else '') + text_of(body),
            })
    out = ROOT / 'index.json'
    out.write_text(json.dumps(entries, ensure_ascii=False), encoding='utf-8')
    print(f'wrote {out.relative_to(ROOT)}: {len(entries)} pages')


if __name__ == '__main__':
    main()
