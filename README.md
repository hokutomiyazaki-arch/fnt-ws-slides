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

## パスコードは付けていない（2026-09-11 宮崎さん判断）

一度 `fnt0915` を付けたが**外した**。仕込みは `_gate.html` に残してあるので、
`python3 apply_gate.py` で入れられる（`--remove` で外せる。両方向を実測済み）。

外した理由は2つ。

1. 🔴 **静的ホストなので、パスコードは何も守らない。**
   画像のURL（`/2026-09-sleep/img/p.001.webp` など）を直接叩けば通らずに見られる
2. **開けない人が出るほうが損。** リンクを踏むのは大半がアプリ内ブラウザ（LINE・Instagram）で、
   そこは記憶が消えて毎回聞かれる。「コードなんだっけ」の問い合わせも増える

**本当の鍵は会員サイト側にある。** `bodydiscovery.jp` の会員限定エリアは SWPM で
本人確認していて、会員はそこにログインしている。**そのページからリンクするだけで、
実質的に会員しか辿れない。** ここに新しい鍵を足す必要はない。

検索には出さない（`robots.txt` と `noindex`）。

## 新しい月を足したあと

```
python3 pdf2site.py      # 過去回（PDF）を変換するとき
python3 gen_index.py      # 一覧を作り直す
```

公開後は **HEADのSHAでビルドを待ってから**、HTTPで全部叩いて確かめる
（`status` だけ見ると前回のビルドで抜ける。2026-09-11に踏んだ）。

```
~/dev/fnt-neuro-community/ws/scripts/wait_pages.sh hokutomiyazaki-arch/fnt-ws-slides
```
