#!/usr/bin/env bash
# ==============================================
#  Google Text-to-Speech Application Launcher
#  مشغّل تطبيق تحويل النص إلى كلام
# ==============================================

set -e

echo "============================================"
echo "  Google Text-to-Speech Application"
echo "  تطبيق تحويل النص إلى كلام"
echo "============================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_CMD=""

# --- Detect Python ---
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    echo "[✓] python3 found: $(python3 --version)"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
    echo "[✓] python found: $(python --version)"
else
    echo "[!] Python not found. Attempting to install Python 3.11..."
    echo "[!] لم يتم العثور على Python. جاري محاولة تثبيت Python 3.11..."
    echo ""

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Debian/Ubuntu
        if command -v apt-get &>/dev/null; then
            echo "Detected Debian/Ubuntu. Using apt..."
            sudo apt-get update -qq
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update -qq
            sudo apt-get install -y python3.11 python3.11-venv python3-pip
            PYTHON_CMD="python3.11"
        # Fedora/RHEL
        elif command -v dnf &>/dev/null; then
            echo "Detected Fedora/RHEL. Using dnf..."
            sudo dnf install -y python3.11 python3-pip
            PYTHON_CMD="python3.11"
        # Arch
        elif command -v pacman &>/dev/null; then
            echo "Detected Arch Linux. Using pacman..."
            sudo pacman -Sy --noconfirm python python-pip
            PYTHON_CMD="python3"
        else
            echo "[ERROR] Unsupported Linux distribution."
            echo "[خطأ] توزيعة Linux غير مدعومة."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &>/dev/null; then
            echo "Detected macOS with Homebrew. Installing Python 3.11..."
            brew install python@3.11
            PYTHON_CMD="python3.11"
        else
            echo "Homebrew not found. Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install python@3.11
            PYTHON_CMD="python3.11"
        fi
    else
        echo "[ERROR] Unsupported OS: $OSTYPE"
        echo "[خطأ] نظام تشغيل غير مدعوم: $OSTYPE"
        exit 1
    fi

    if ! command -v "$PYTHON_CMD" &>/dev/null; then
        echo "[ERROR] Python installation failed."
        echo "[خطأ] فشل تثبيت Python."
        exit 1
    fi

    echo "[✓] Python installed successfully: $($PYTHON_CMD --version)"
    echo "[✓] تم تثبيت Python بنجاح"
fi

echo ""
echo "Starting application... / جاري تشغيل التطبيق..."
echo ""
$PYTHON_CMD "$SCRIPT_DIR/app.py"
