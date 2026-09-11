# -*- coding: utf-8 -*-
"""過去回のWS資料（Canva書き出しのPDF）を、9月と同じ形のビューアにする。

🔴 9月（gen_site.py）との違い
   - 正本が source.md ではなくPDFなので、用語集と章が作れない。目次と送りだけ
   - 各ページの見出しは PDF の1行目から取る（推測しない。文字が無い頁は空になる）
   - 比率は回ごとに違う（過去は16:9／9月は1280x1080）のでデータに持たせる

使い方: python3 pdf2site.py
"""
import fitz, io, os, json, re, shutil, sys
from PIL import Image

W, Q = 1600, 80   # 1600px幅・q80（実測：1頁あたり68〜117KB）

# (PDF, 出力フォルダ, 表題, 表示する時期, Driveのファイルid)
DECKS = [
    ('2026-01.pdf',  '2026-01-breathing-1', '神経科学と呼吸（パート1）',      '2026年1月', '1WJzsl9O_S8tPkZK20bdGSSQpeBkkQIig'),
    ('2026-01b.pdf', '2026-01-reflex-vvp',  'VVPの反射を活用したアセスメント', '2026年1月', '142xOe2tWACGrxe7v9G0DncTNFHQdUFaz'),
    ('2026-02.pdf',  '2026-02-vertigo',     'めまい患者に対する介入',          '2026年2月', '14wkqLILkByYuyrzaaZho9ND3vWUQG3hn'),
    ('2026-05.pdf',  '2026-05-breathing-2', '神経科学と呼吸（パート2）',       '2026年5月', '1PPAYMZJk9qabphslbbuhXOLaJn9OQElx'),
    ('2026-05b.pdf', '2026-05-bfr',         'BFRの応用事例',                  '2026年5月', '1EyWiYm3g9OFxxXlz4dGmy6iE3TN2CAhN'),
    # 🔴 2026-07.pdf（22頁）は 2026-08.pdf の前半22頁と完全一致だったので載せない
    ('2026-08.pdf',  '2026-08-ligament',    '靱帯の神経科学（前半＋後半）',    '2026年7・8月', '1_ociswrRTkttQUiCpr-YyM5kdha91ysd'),
]

def head(page):
    """そのページの見出し（テキストの最初の意味のある1行）。無ければ空。"""
    t = page.get_text().strip()
    for ln in t.split('\n'):
        ln = re.sub(r'\s+', ' ', ln).strip()
        # ページ番号・著作権表示・記号だけの行は見出しではない
        if len(ln) < 2: continue
        if re.fullmatch(r'[\d\s\./©-]+', ln): continue
        if ln.startswith('©') or 'All Rights Reserved' in ln: continue
        return ln[:60]
    return ''

tpl = io.open('tpl_pdf.html', encoding='utf-8').read()
made = []
for pdf, slug, title, when, fid in DECKS:
    src = os.path.join('入力', pdf)
    if not os.path.exists(src):
        print(f"🔴 {pdf} が無い"); sys.exit(1)
    d = fitz.open(src)
    shutil.rmtree(slug, ignore_errors=True)
    os.makedirs(slug + '/img')
    ratio = f"{d[0].rect.width:.0f}/{d[0].rect.height:.0f}"
    pages, tot = [], 0
    for n in range(len(d)):
        z = W / d[n].rect.width
        pm = d[n].get_pixmap(matrix=fitz.Matrix(z, z))
        im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
        p = '%s/img/p.%03d.webp' % (slug, n + 1)
        im.save(p, 'WEBP', quality=Q, method=6)
        tot += os.path.getsize(p)
        pages.append({'n': n + 1, 't': head(d[n]), 'img': 'img/p.%03d.webp' % (n + 1)})
    html = (tpl.replace('@@PAGES@@', json.dumps(pages, ensure_ascii=False))
               .replace('@@TITLE@@', title).replace('@@WHEN@@', when)
               .replace('@@RATIO@@', ratio).replace('@@SLUG@@', slug))
    io.open(slug + '/index.html', 'w', encoding='utf-8').write(html)
    io.open(slug + '/robots.txt', 'w', encoding='utf-8').write("User-agent: *\nDisallow: /\n")
    nt = sum(1 for x in pages if x['t'])
    print(f"  {slug:22} {len(pages):3}頁  {tot/1048576:5.1f}MB  見出しが取れた頁 {nt}/{len(pages)}")
    made.append({'slug': slug, 'title': title, 'when': when, 'n': len(pages),
                 'mb': round(tot / 1048576, 1), 'fid': fid})
io.open('_made.json', 'w', encoding='utf-8').write(json.dumps(made, ensure_ascii=False, indent=1))
print(f"\n{len(made)}回ぶん / 合計 {sum(x['mb'] for x in made):.1f}MB")
