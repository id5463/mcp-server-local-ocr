# MCP Server — Local OCR

基于本地 RapidOCR 引擎的图片文字识别 MCP 服务器。中英文支持，离线运行，无需网络。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

在 `opencode.jsonc` 中添加：

```jsonc
{
  "mcpServers": {
    "local-ocr": {
      "type": "stdio",
      "command": "python",
      "args": ["path/to/local_ocr_mcp.py"]
    }
  }
}
```

## 工具

| 工具 | 说明 |
|------|------|
| `ocr_image(image_path)` | 识别指定图片文件中的文字 |
| `ocr_clipboard()` | 识别剪贴板中的图片文字 |

## 注意

- 首次运行 RapidOCR 会自动下载模型文件（约 20MB）
- Windows 支持，Linux/macOS 需确认 `ocr.py` 中的剪贴板命令
