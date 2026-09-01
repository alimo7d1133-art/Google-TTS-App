#!/usr/bin/env bash
# ==============================================
#  Build Google TTS for Linux (standalone binary)
#  بناء التطبيق لنظام Linux
# ==============================================

set -e

echo "============================================"
echo "  Building Google TTS for Linux"
echo "  بناء التطبيق لنظام Linux"
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

# Step 1: Install system deps for audio (if needed)
echo "[1/4] Checking system audio dependencies..."
echo "[1/4] جاري التحقق من متطلبات الصوت..."
if command -v apt-get &>/dev/null; then
    sudo apt-get install -y -qq libsdl2-mixer-2.0-0 libsdl2-2.0-0 2>/dev/null || true
elif command -v dnf &>/dev/null; then
    sudo dnf install -y SDL2 SDL2_mixer 2>/dev/null || true
fi

# Step 2: Install PyInstaller
echo ""
echo "[2/4] Installing build dependencies..."
echo "[2/4] جاري تثبيت متطلبات البناء..."
$PYTHON_CMD -m pip install --upgrade pyinstaller gTTS pygame

# Step 3: Build
echo ""
echo "[3/4] Building standalone Linux binary..."
echo "[3/4] جاري بناء الملف التنفيذي المستقل..."
$PYTHON_CMD -m PyInstaller \
    --onefile \
    --name "GoogleTTS" \
    --add-data "README.md:." \
    --hidden-import "gtts" \
    --hidden-import "pygame" \
    --hidden-import "gtts.tokenizer" \
    --hidden-import "gtts.tokenizer.pre_processors" \
    --hidden-import "gtts.tokenizer.tokenizer_cases" \
    --console \
    app.py

# Step 4: Verify and make AppImage-like structure
echo ""
if [ -f "dist/GoogleTTS" ]; then
    chmod +x dist/GoogleTTS
    SIZE=$(du -h "dist/GoogleTTS" | cut -f1)
    echo "[4/4] ============================================"
    echo "  [✓] Build successful! / تم البناء بنجاح!"
    echo "  Output: dist/GoogleTTS"
    echo "  Size: $SIZE"
    echo "============================================"
    echo ""
    echo "[INFO] The binary is self-contained and portable."
    echo "[INFO] Run it with: ./dist/GoogleTTS"
    echo "[معلومة] الملف التنفيذي مستقل وقابل للنقل."
    echo "[معلومة] شغّله بالأمر: ./dist/GoogleTTS"
    echo ""
    echo "[TIP] To create an AppImage, install appimagetool and run:"
    echo "  mkdir -p GoogleTTS.AppDir/usr/bin"
    echo "  cp dist/GoogleTTS GoogleTTS.AppDir/usr/bin/"
    echo "  # Add AppRun and .desktop file, then:"
    echo "  appimagetool GoogleTTS.AppDir GoogleTTS.AppImage"
else
    echo "[ERROR] Build failed! Check the output above."
    echo "[خطأ] فشل البناء! تحقق من المخرجات أعلاه."
    exit 1
fi
