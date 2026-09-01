#!/usr/bin/env bash
# ==============================================
#  Build Google TTS for Android (APK)
#  بناء التطبيق لنظام Android
# ==============================================

set -e

echo "============================================"
echo "  Building Google TTS for Android (APK)"
echo "  بناء التطبيق لنظام Android"
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

# Step 1: Install Buildozer and dependencies
echo "[1/4] Installing Buildozer and system dependencies..."
echo "[1/4] جاري تثبيت Buildozer ومتطلبات النظام..."

$PYTHON_CMD -m pip install --upgrade buildozer cython

# Install system dependencies (Ubuntu/Debian)
if command -v apt-get &>/dev/null; then
    echo "Installing system packages for Android build..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq \
        build-essential \
        git \
        zip \
        unzip \
        openjdk-17-jdk \
        autoconf \
        libtool \
        pkg-config \
        zlib1g-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libtinfo5 \
        cmake \
        libffi-dev \
        libssl-dev \
        automake \
        2>/dev/null || true
fi

# Step 2: Clean previous build
echo ""
echo "[2/4] Cleaning previous build artifacts..."
echo "[2/4] جاري تنظيف مخرجات البناء السابقة..."
buildozer android clean 2>/dev/null || true

# Step 3: Build debug APK
echo ""
echo "[3/4] Building debug APK (this may take 15-30 minutes on first run)..."
echo "[3/4] جاري بناء APK (قد يستغرق 15-30 دقيقة في المرة الأولى)..."
echo ""
buildozer -v android debug

# Step 4: Check output
echo ""
APK_PATH=$(find bin -name "*.apk" 2>/dev/null | head -1)
if [ -n "$APK_PATH" ]; then
    SIZE=$(du -h "$APK_PATH" | cut -f1)
    echo "[4/4] ============================================"
    echo "  [✓] Build successful! / تم البناء بنجاح!"
    echo "  APK: $APK_PATH"
    echo "  Size: $SIZE"
    echo "============================================"
    echo ""
    echo "[INFO] Install on device:"
    echo "  adb install $APK_PATH"
    echo ""
    echo "[INFO] Or transfer the APK file to your phone."
    echo "[معلومة] أو انقل ملف APK إلى هاتفك."
else
    echo "[ERROR] Build failed! Check the output above."
    echo "[خطأ] فشل البناء! تحقق من المخرجات أعلاه."
    exit 1
fi
