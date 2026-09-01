#!/usr/bin/env bash
# ==============================================
#  Build Google TTS for macOS (.app bundle)
#  بناء التطبيق لنظام macOS
# ==============================================

set -e

echo "============================================"
echo "  Building Google TTS for macOS (.app)"
echo "  بناء التطبيق لنظام macOS"
echo "============================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Detect Python
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python is required. Run run.sh first to install it."
    echo "[خطأ] Python مطلوب. شغّل run.sh أولاً لتثبيته."
    exit 1
fi

echo "[✓] Using: $($PYTHON_CMD --version)"
echo ""

# Step 1: Install dependencies
echo "[1/3] Installing build dependencies..."
echo "[1/3] جاري تثبيت متطلبات البناء..."
$PYTHON_CMD -m pip install --upgrade pyinstaller gTTS pygame

# Step 2: Build .app bundle
echo ""
echo "[2/3] Building macOS .app bundle..."
echo "[2/3] جاري بناء حزمة .app لنظام macOS..."
$PYTHON_CMD -m PyInstaller \
    --onefile \
    --name "GoogleTTS" \
    --add-data "README.md:." \
    --hidden-import "gtts" \
    --hidden-import "pygame" \
    --hidden-import "gtts.tokenizer" \
    --hidden-import "gtts.tokenizer.pre_processors" \
    --hidden-import "gtts.tokenizer.tokenizer_cases" \
    --windowed \
    --console \
    --osx-bundle-identifier "com.googtts.app" \
    app.py

# Step 3: Verify
echo ""
if [ -f "dist/GoogleTTS" ]; then
    SIZE=$(du -h "dist/GoogleTTS" | cut -f1)
    echo "[3/3] ============================================"
    echo "  [✓] Build successful! / تم البناء بنجاح!"
    echo "  Output: dist/GoogleTTS"
    echo "  Size: $SIZE"
    echo "============================================"
    echo ""
    echo "[INFO] To create a proper .app bundle, run:"
    echo "  mkdir -p dist/GoogleTTS.app/Contents/MacOS"
    echo "  cp dist/GoogleTTS dist/GoogleTTS.app/Contents/MacOS/"
    echo ""
    echo "[INFO] You can distribute dist/GoogleTTS as a standalone executable."
    echo "[معلومة] يمكنك توزيع dist/GoogleTTS كتطبيق مستقل."
else
    echo "[ERROR] Build failed! Check the output above."
    echo "[خطأ] فشل البناء! تحقق من المخرجات أعلاه."
    exit 1
fi
