# -*- coding: utf-8 -*-
"""全ページにパスコードの札を入れる。

🔴 これは鍵ではない。GitHub Pages は静的なので、画像のURLを直接叩けば
   パスコードを通らずに見られる。のぞき見を止めるためのもの。
   本当に鍵をかけるならサーバー側で認証する（Vercelのミドルウェア等）。

一箇所（_gate.html）を直せば全ページに効く。何度実行しても増えない。
使い方: python3 apply_gate.py
"""
import io, glob, sys

MARK = 'fnt-ws-gate'
gate = io.open('_gate.html', encoding='utf-8').read().strip()

files = sorted(glob.glob('index.html') + glob.glob('*/index.html'))
if not files:
    print('🔴 index.html が見つからない'); sys.exit(1)

added = skipped = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    if MARK in s:
        print(f"  {f:34} すでに入っている"); skipped += 1; continue
    if '</title>' not in s:
        print(f"  🔴 {f}: </title> が無いので入れられない"); sys.exit(1)
    s = s.replace('</title>', '</title>\n' + gate, 1)
    io.open(f, 'w', encoding='utf-8').write(s)
    print(f"  {f:34} 入れた"); added += 1

# 🔴 検算：全ページに1回だけ入っていること
ng = []
for f in files:
    n = io.open(f, encoding='utf-8').read().count(MARK)
    if n != 1: ng.append((f, n))
if ng:
    print('🔴 回数がおかしい:', ng); sys.exit(1)
print(f"\n✅ {len(files)}ページすべてに1回だけ入っている（新規{added} / 既存{skipped}）")
