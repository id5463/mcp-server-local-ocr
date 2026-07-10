#!/usr/bin/env python3
"""Local OCR. Outputs JSON (default) or HTML overlay. Chinese+English. Offline."""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def clipboard_image():
    ps = """
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$img=[System.Windows.Forms.Clipboard]::GetImage()
if(!$img){exit 1}
$img.Save($args[0],[System.Drawing.Imaging.ImageFormat]::Png)
"""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        path = f.name
    r = subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps, path],
                       capture_output=True, text=True)
    if r.returncode:
        os.unlink(path)
        print("ERROR: no image in clipboard", file=sys.stderr)
        sys.exit(1)
    return path


def b64_uri(path):
    with open(path, "rb") as f:
        d = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lower().lstrip(".")
    m = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
         "bmp": "image/bmp", "webp": "image/webp"}
    return f"data:{m.get(ext, 'image/png')};base64,{d}"


def to_bbox(box):
    xs, ys = [p[0] for p in box], [p[1] for p in box]
    return {"x": int(min(xs)), "y": int(min(ys)),
            "w": int(max(xs) - min(xs)), "h": int(max(ys) - min(ys))}


def out_json(results, elapse, img_path=None):
    blocks = []
    for box, text, score in results:
        blocks.append({
            "text": text.strip(),
            "box": [[int(p[0]), int(p[1])] for p in box],
            "bbox": to_bbox(box),
            "score": round(float(score), 4),
        })
    out = {"blocks": blocks, "meta": {"total": len(blocks)}}
    if img_path:
        out["meta"]["image"] = str(Path(img_path).resolve())
    print(json.dumps(out, ensure_ascii=False, indent=2))


def out_html(results, img_path):
    b64 = b64_uri(img_path)
    h = ""
    try:
        from PIL import Image
        with Image.open(img_path) as im:
            h = f"height:{im.size[1]}px;"
    except Exception:
        pass
    spans = []
    for box, text, score in results:
        b = to_bbox(box)
        spans.append(
            f'<span style="left:{b["x"]}px;top:{b["y"]}px;'
            f'width:{b["w"]}px;height:{b["h"]}px" '
            f'title="{float(score):.3f}">{text.strip()}</span>')
    print(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
body{{margin:0;background:#333}} .w{{position:relative;display:inline-block}}
.w img{{display:block;max-width:100%}}
.w span{{position:absolute;color:transparent;overflow:hidden}}
.w span:hover{{background:rgba(255,255,0,.35);color:red;font-size:12px}}
</style></head><body><div class="w" style="{h}">
<img src="{b64}">{"".join(spans)}</div></body></html>""")


def run(img_path, fmt="json"):
    from rapidocr_onnxruntime import RapidOCR
    engine = RapidOCR()
    result, _ = engine(img_path)
    if not result:
        if fmt == "json":
            print(json.dumps({"blocks": [], "meta": {"total": 0}}, ensure_ascii=False))
        return
    if fmt == "json":
        out_json(result, _, img_path)
    elif fmt == "html":
        out_html(result, img_path)
    else:
        print(f"ERROR: unknown format '{fmt}'", file=sys.stderr)
        sys.exit(1)


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser()
    p.add_argument("image", nargs="?", help="Image path")
    p.add_argument("--format", "-f", choices=["json", "html"], default="json")
    p.add_argument("--clipboard", "-c", action="store_true", help="OCR clipboard")
    p.add_argument("--output", "-o", help="Write to file")
    args = p.parse_args()

    if args.clipboard:
        path, tmp = clipboard_image(), True
    elif args.image:
        if not os.path.exists(args.image):
            print(f"ERROR: file not found: {args.image}", file=sys.stderr)
            sys.exit(1)
        path, tmp = args.image, False
    else:
        print("No image. Trying clipboard...", file=sys.stderr)
        path, tmp = clipboard_image(), True

    if args.output:
        sys.stdout = open(args.output, "w", encoding="utf-8")
    try:
        run(path, args.format)
    finally:
        if args.output:
            sys.stdout.close()
        if tmp:
            try:
                os.unlink(path)
            except OSError:
                pass


if __name__ == "__main__":
    main()
