# -*- coding: utf-8 -*-
"""トップの一覧を作る。🔴 並びは時系列（古い順）。数は手で書かず全部計算する。"""
import io, json, os, re, glob

# 表題・時期は _made.json（PDF由来）＋9月（source.md由来）
decks = json.load(open('_made.json', encoding='utf-8'))
decks.append({'slug': '2026-09-sleep', 'title': '睡眠の応用神経学', 'when': '2026年9月',
              'n': 122, 'mb': 11.8, 'fid': None, 'note': '用語集128語つき'})

# 🔴 実データで検算：フォルダと枚数が一致するか
for d in decks:
    real = len(glob.glob(d['slug'] + '/img/*.webp'))
    assert real == d['n'], f"🔴 {d['slug']}: 台帳{d['n']}枚 / 実際{real}枚"
    assert os.path.exists(d['slug'] + '/index.html'), f"🔴 {d['slug']}/index.html が無い"

decks.sort(key=lambda d: (d['when'], d['slug']))   # 時系列（古い順）

cards = []
for d in decks:
    extra = f" ・ {d['note']}" if d.get('note') else ""
    cards.append(f"""  <a class="card" href="{d['slug']}/">
    <span class="date">{d['when']}</span>
    <div class="ttl">{d['title']}</div>
    <div class="meta">{d['n']}枚{extra}</div>
  </a>""")

HTML = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>FNTニューロコミュニティ 月例WS 資料</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700&family=Noto+Sans+JP:wght@400;500&display=swap">
<style>
:root{--bg:#F4F2EC;--panel:#fff;--ink:#1C2333;--sub:#5F6678;--line:#E2DED4;
 --violet:#4A2A82;--cyan:#00B5E6;
 --disp:"Zen Kaku Gothic New","Hiragino Kaku Gothic ProN",sans-serif;
 --body:"Noto Sans JP","Hiragino Kaku Gothic ProN",sans-serif;}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --bg:#0E1320;--panel:#181F30;--ink:#E8EAF1;--sub:#98A1B7;--line:#28314A;
 --violet:#B49BE8;--cyan:#3FD2FF;}}
:root[data-theme="dark"]{--bg:#0E1320;--panel:#181F30;--ink:#E8EAF1;--sub:#98A1B7;
 --line:#28314A;--violet:#B49BE8;--cyan:#3FD2FF;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);
 padding:32px 20px 60px;line-height:1.8}
.wrap{max-width:720px;margin:0 auto}
h1{font-family:var(--disp);font-size:21px;color:var(--violet);margin:0 0 4px}
.sub{font-size:12.5px;color:var(--sub);margin:0 0 28px;letter-spacing:.04em}
a.card{display:block;background:var(--panel);border:1px solid var(--line);
 border-radius:14px;padding:18px 20px;text-decoration:none;color:inherit;
 margin:0 0 12px;transition:border-color .15s}
a.card:hover{border-color:var(--violet)}
.date{font-size:11.5px;color:var(--cyan);letter-spacing:.08em;font-weight:700}
.ttl{font-family:var(--disp);font-weight:700;font-size:17px;margin:3px 0 5px}
.meta{font-size:12.5px;color:var(--sub)}
.note{font-size:12px;color:var(--sub);margin-top:32px;padding-top:18px;
 border-top:1px solid var(--line)}
</style>
</head>
<body>
<div class="wrap">
  <h1>月例ワークショップ 資料</h1>
  <p class="sub">FNTニューロコミュニティ ／ 応用実践WS ／ 受講者用 ／ 全@@NDECK@@回・@@NPAGE@@枚</p>

@@CARDS@@

  <p class="note">
    スマホでも見られます。左右のキー、またはスワイプで送ります。<br>
    各回の「目次」から、見出しでページを探せます。
  </p>
</div>
</body>
</html>
"""
HTML = (HTML.replace('@@CARDS@@', '\n'.join(cards))
            .replace('@@NDECK@@', str(len(decks)))
            .replace('@@NPAGE@@', str(sum(d['n'] for d in decks))))
io.open('index.html', 'w', encoding='utf-8').write(HTML)
print(f"一覧: {len(decks)}回 / 合計{sum(d['n'] for d in decks)}枚 / 画像{sum(d['mb'] for d in decks):.1f}MB")
for d in decks: print(f"  {d['when']:10} {d['title']}（{d['n']}枚）")
