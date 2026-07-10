"""
Local OCR MCP Server — 基于本地 RapidOCR 引擎的图片文字识别
"""
import json, subprocess, sys, os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-ocr")
_BASEDIR = os.path.dirname(os.path.abspath(__file__))
OCR_SCRIPT = os.path.join(_BASEDIR, "scripts", "ocr.py")
PYTHON = sys.executable

def _run_ocr(args: list[str]) -> str:
    """执行 OCR，处理 Windows GBK 编码问题。"""
    result = subprocess.run(
        [PYTHON, OCR_SCRIPT] + args,
        capture_output=True, timeout=30
    )
    stdout = result.stdout.decode('utf-8', errors='replace')
    stderr = result.stderr.decode('utf-8', errors='replace')
    if result.returncode != 0:
        return json.dumps({"error": stderr.strip()})
    return stdout

@mcp.tool()
def ocr_image(image_path: str) -> str:
    """识别图片中的文字（中英文），返回 JSON。参数：图片路径。"""
    if not os.path.exists(image_path):
        return json.dumps({"error": f"文件不存在: {image_path}"})
    return _run_ocr([image_path])

@mcp.tool()
def ocr_clipboard() -> str:
    """识别剪贴板中的图片文字。"""
    return _run_ocr(["--clipboard"])

if __name__ == "__main__":
    mcp.run(transport="stdio")
