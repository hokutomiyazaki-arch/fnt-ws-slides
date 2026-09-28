#!/usr/bin/env python3
"""各回のページに出している画像から、ダウンロード用のPDFを作る。

    python3 make_pdf.py            # 全回
    python3 make_pdf.py 2026-09-sleep

出力：<回>/<回>.pdf と、その回のページ上部の「PDF」ボタン（無ければ足す。2回打っても1つ）

- 画像の並びは、その回の index.html に出てくる順（＝画面で見ている順）
- 台本・スピーカーノートは入らない（画像しか使わないため）
- 手元の元PDF（入力/）は使わない。最大93MBあり、スマホで落とすには重い
- PDFにするのは Chrome の print-to-pdf、圧縮は Ghostscript（どちらもこのMacに入っている）
"""
import os, re, subprocess, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def size_of(img):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(img)],
                         capture_output=True, text=True).stdout
    w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
    return w, h


def build(slug):
    d = ROOT / slug
    html = (d / "index.html").read_text(encoding="utf-8")
    srcs = []
    for s in re.findall(r'img/(p\.\d+\.\w+)', html):
        if s not in srcs:
            srcs.append(s)
    files = sorted(os.listdir(d / "img"))
    if sorted(srcs) != files:
        # ページ側の並びが取れないときは、ファイル名の順（p.001〜）で作る
        srcs = files
    w, h = size_of(d / "img" / srcs[0])
    pages = "\n".join(f'<div class="p"><img src="{(d / "img" / s).as_uri()}"></div>' for s in srcs)
    doc = f"""<!doctype html><meta charset="utf-8"><style>
@page{{size:{w}px {h}px;margin:0}}
html,body{{margin:0;padding:0;background:#fff}}
.p{{width:{w}px;height:{h}px;page-break-after:always;break-after:page;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.p:last-child{{page-break-after:auto;break-after:auto}}
.p img{{max-width:100%;max-height:100%;display:block}}
</style>{pages}"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(doc)
        tmp = f.name
    out = d / f"{slug}.pdf"
    raw = pathlib.Path(tmp).with_suffix(".raw.pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", f"--print-to-pdf={raw}", pathlib.Path(tmp).as_uri()],
                   check=True, capture_output=True)
    # Chrome は画像を無圧縮に近い形で埋めるので（睡眠の回で85MB）、JPEG で詰め直す（→約15MB）。
    # 解像度は落とさない（DownsampleColorImages=false）。JPEGQ=82 で文字がつぶれないことを目で確認済み
    subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.6", "-dDownsampleColorImages=false",
                    "-dAutoFilterColorImages=false", "-dColorImageFilter=/DCTEncode", "-dJPEGQ=82",
                    f"-sOutputFile={out}", str(raw)], check=True)
    os.unlink(tmp)
    os.unlink(raw)
    add_button(d, slug)
    return out, len(srcs)


BTN_MARK = 'id="btnPdf"'


def add_button(d, slug):
    """ページ上部のボタン列の最後に「PDF」を足す。download 属性でその場で保存される。"""
    p = d / "index.html"
    html = p.read_text(encoding="utf-8")
    if BTN_MARK in html:
        return
    i = html.index('<header class="top">')
    j = html.index("</header>", i)
    btn = f'  <a class="tbtn" {BTN_MARK} href="{slug}.pdf" download style="text-decoration:none">PDF</a>\n'
    html = html[:j] + btn + html[j:]
    p.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    slugs = sys.argv[1:] or sorted(p.name for p in ROOT.iterdir() if p.is_dir() and re.match(r"\d{4}-\d{2}-", p.name))
    for s in slugs:
        out, n = build(s)
        print(f"{s}: {n}枚 → {out.name} {out.stat().st_size/1e6:.1f}MB")
