---
name: local-ocr
description: Use when user asks to OCR/extract text from image/screenshot. 图片识别, 文字提取, 识字, 截图转文字. Local RapidOCR engine, Chinese+English, offline.
---

# local-ocr

Run OCR on an image. Returns JSON: text + 4-point box + {x,y,w,h} bbox + confidence score.

## Usage

```powershell
# From file (default: JSON to stdout)
python "C:\Users\a\.agents\skills\local-ocr\ocr.py" "<image_path>"

# From clipboard
python "C:\Users\a\.agents\skills\local-ocr\ocr.py" --clipboard

# HTML overlay (for human visual check)
python "C:\Users\a\.agents\skills\local-ocr\ocr.py" --format html "<path>" -o "out.html"
```

Python: `C:\Users\a\AppData\Local\Programs\Python\Python313\python.exe`

## Output

```json
{
  "blocks": [
    {"text": "...", "box": [[x1,y1],...], "bbox": {"x":0,"y":0,"w":0,"h":0}, "score": 0.99}
  ],
  "meta": {"total": N, "image": "path"}
}
```

## Install (once)

```powershell
& "C:\Users\a\.agents\skills\local-ocr\install.ps1"
```
