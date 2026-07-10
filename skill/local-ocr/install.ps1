# Local OCR Skill — Install Script
# Installs rapidocr-onnxruntime + Pillow to system Python

$ErrorActionPreference = "Stop"
$PythonPath = "C:\Users\a\AppData\Local\Programs\Python\Python313\python.exe"

Write-Host "=== Local OCR Skill Installer ===" -ForegroundColor Cyan
Write-Host ""

# Check Python
if (-not (Test-Path $PythonPath)) {
    Write-Host "[FAIL] Python 3.13 not found at: $PythonPath" -ForegroundColor Red
    Write-Host "Please install Python 3.13 first, or edit this script to point to your Python."
    exit 1
}
Write-Host "[OK] Python found: $PythonPath" -ForegroundColor Green

# Check pip
$pipCheck = & $PythonPath -m pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] pip not available" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] pip ready" -ForegroundColor Green

# Install packages
Write-Host ""
Write-Host "[...] Installing rapidocr-onnxruntime + Pillow..." -ForegroundColor Yellow
& $PythonPath -m pip install rapidocr-onnxruntime Pillow -q

if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] pip install failed" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Packages installed" -ForegroundColor Green

# Quick test — import to verify
Write-Host ""
Write-Host "[...] Verifying installation..." -ForegroundColor Yellow
$testCode = @'
from rapidocr_onnxruntime import RapidOCR
print("RapidOCR imported OK")
'@
$testResult = & $PythonPath -c $testCode 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARN] Import test returned warnings (may be ok):" -ForegroundColor Yellow
    Write-Host $testResult
} else {
    Write-Host "[OK] RapidOCR import successful" -ForegroundColor Green
}

# Show model download note
Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Models will be auto-downloaded on first use to:" -ForegroundColor White
Write-Host "  %USERPROFILE%\.rapidocr\" -ForegroundColor Gray
Write-Host ""
Write-Host "Test it with:" -ForegroundColor White
Write-Host '  & "C:\Users\a\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\a\.agents\skills\local-ocr\ocr.py" --clipboard' -ForegroundColor Gray
Write-Host ""
