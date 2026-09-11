# fnt-ws-slides

FNTニューロコミュニティ 月例ワークショップ（応用実践WS）の**受講者用スライド**を配信する。

公開URL: https://hokutomiyazaki-arch.github.io/fnt-ws-slides/

## これは何か

月例WSの資料を、受講者がスマホでも見られる形（スライドアプリ）で配る場所。
章送り・目次・用語集の全文検索・枚ごとの用語表示・スワイプ送り・続きから再開が入っている。

## 🔴 このリポジトリは public

- **秘密・顧客情報・台本（スピーカーノート）は絶対に置かない**
- 置くのは、受講者に渡してよい資料だけ
- 検索エンジンには拾わせない（`robots.txt` と `noindex`）

## 正本はここではない

| | 場所 |
|---|---|
| **正本**（Markdown・台本つき・文献） | `fnt-neuro-community/ws/<年月>-<テーマ>/source.md` |
| 生成器 | `fnt-neuro-community/ws/<年月>-<テーマ>/view/gen_site.py` |
| **ここ** | 生成物の配信コピー |

## 新しい月を足す

```
cd ~/dev/fnt-neuro-community/ws/<年月>-<テーマ>/view
python3 gen_site.py site webpfull          # 原寸で静的サイトを書き出す
cp -R site/. ~/dev/fnt-ws-slides/<年月>-<テーマ>/
# トップの index.html にカードを1枚足す
```

画像は `img/` に外部ファイルとして置く（HTMLに埋め込まない）。
アーティファクトの16MB上限が無いので、**原寸のまま出せる**。

## パスコード

全ページに `fnt0915` の入力を置いている。仕込みは **`_gate.html` の1箇所だけ**で、
`python3 apply_gate.py` で全ページへ入る（何度実行しても増えない）。

🔴 **これは鍵ではない。** GitHub Pages は静的なので、画像のURL
（`/2026-09-sleep/img/p.001.webp` など）を直接叩けばパスコードを通らずに見られる。
「のぞき見を止める札」として置いている。本当に鍵をかけるなら、
置き場をVercel等に移してサーバー側で認証する。

パスコードそのものはページに書かず、SHA-256 だけを埋めている。
変えるときは `_gate.html` の `HASH` を差し替えて `apply_gate.py` を流す。

## 新しい月を足したあと

```
python3 pdf2site.py      # 過去回（PDF）を変換するとき
python3 gen_index.py      # 一覧を作り直す
python3 apply_gate.py     # 🔴 新しいページに札を入れる（忘れると素通しになる）
```
