<div dir="rtl" align="right">

# 🔊 Google Text-to-Speech App — تطبيق تحويل النص إلى كلام

</div>

<div dir="rtl" align="right">

تطبيق متعدد المنصات لتحويل النص إلى كلام باستخدام Google Text-to-Speech.
**متاح بالكامل لقارئات الشاشة** (NVDA, JAWS, VoiceOver, TalkBack).

</div>

---

## ✨ Features / المميزات

<div dir="rtl" align="right">

- ♿ **دعم كامل لقارئات الشاشة** — كل عنصر يحمل وصفاً واضحاً
- ⌨️ **تنقل كامل بلوحة المفاتيح** — Tab / Enter / Esc / Ctrl+S / Ctrl+Q
- 🌍 **دعم أكثر من 10 لغات** — العربية، الإنجليزية، الفرنسية، وغيرها
- 💾 **حفظ تلقائي بصيغة MP3** مع اسم بالتاريخ والوقت
- 📦 **تثبيت تلقائي للمكتبات** عند أول تشغيل
- 🖥️ **يعمل على كل الأنظمة** — Windows, macOS, Linux, Android

</div>

- ♿ **Full screen reader support** — every widget has a clear label
- ⌨️ **Full keyboard navigation** — Tab / Enter / Esc / Ctrl+S / Ctrl+Q
- 🌍 **10+ languages supported** — Arabic, English, French, and more
- 💾 **Auto-save as MP3** with timestamp filename
- 📦 **Auto-installs dependencies** on first run
- 🖥️ **Cross-platform** — Windows, macOS, Linux, Android

---

## 📂 Project Structure / هيكل المشروع

```
Google-TTS-App/
├── app.py              # CLI version (terminal)
├── app_gui.py          # GUI version (tkinter — accessible)
├── main.py             # Android/Kivy version (accessible)
├── requirements.txt    # Python dependencies
├── run.bat             # Windows launcher (auto-installs Python)
├── run.sh              # Linux/macOS launcher (auto-installs Python)
├── build_windows.bat   # Build standalone .exe (PyInstaller)
├── build_mac.sh        # Build standalone macOS binary (PyInstaller)
├── build_linux.sh      # Build standalone Linux binary (PyInstaller)
├── build_android.sh    # Build Android APK (Buildozer)
├── buildozer.spec      # Android build configuration
├── README.md           # This file
└── output/             # Generated MP3 files (auto-created)
```

---

## 🚀 Quick Start / البدء السريع

### Option 1: Run directly (CLI)

```bash
# Linux / macOS
chmod +x run.sh
./run.sh

# Windows
run.bat
```

### Option 2: Run GUI (Accessible)

```bash
python3 app_gui.py
```

### Option 3: Run with Python manually

```bash
pip install gTTS pygame
python3 app.py        # CLI version
python3 app_gui.py    # GUI version
```

---

## ♿ Accessibility / إمكانية الوصول

<div dir="rtl" align="right">

### دعم قارئات الشاشة

هذا التطبيق مصمم خصيصاً ليكون متاحاً بالكامل للمكفوفين وضعاف البصر:

| الميزة | الوصف |
|--------|-------|
| تسميات واضحة | كل زر وحقل نص يحمل وصفاً مقروءاً |
| تنقل Tab | يمكن الوصول لكل العناصر بلوحة المفاتيح |
| اختصارات | Enter = تحويل، Esc = إيقاف، Ctrl+S = حفظ |
| شريط الحالة | يُقرأ تلقائياً عند تغير الحالة |
| بدون صور | واجهة نصية بالكامل — لا زخرفة بصرية |
| تباين عالي | ألوان واضحة (أسود على أبيض) |

</div>

### Screen Reader Support

This app is designed from the ground up for full accessibility:

| Feature | Description |
|---------|-------------|
| Clear labels | Every button and text field has a readable description |
| Tab navigation | All elements reachable via keyboard |
| Shortcuts | Enter = Convert, Esc = Stop, Ctrl+S = Save, Ctrl+Q = Quit |
| Status bar | Automatically announced on state changes |
| No images | Purely text-based UI — no decorative elements |
| High contrast | Clear colors (black on white) |

### Tested with:
- **Windows**: NVDA, JAWS
- **macOS**: VoiceOver
- **Linux**: Orca
- **Android**: TalkBack

---

## 🏗️ Building Standalone Executables / بناء ملفات تنفيذية مستقلة

<div dir="rtl" align="right">

### بناء لنظام Windows (ملف .exe)

</div>

```batch
:: On Windows — creates dist\GoogleTTS.exe
build_windows.bat
```

The `.exe` bundles Python + all libraries. No installation needed on target machine.

---

<div dir="rtl" align="right">

### بناء لنظام macOS (ملف تنفيذي)

</div>

```bash
# On macOS — creates dist/GoogleTTS
chmod +x build_mac.sh
./build_mac.sh
```

---

<div dir="rtl" align="right">

### بناء لنظام Linux (ملف تنفيذي مستقل)

</div>

```bash
# On Linux — creates dist/GoogleTTS
chmod +x build_linux.sh
./build_linux.sh
```

---

<div dir="rtl" align="right">

### بناء لنظام Android (ملف APK)

</div>

```bash
# On Linux (required for Buildozer) — creates bin/*.apk
chmod +x build_android.sh
./build_android.sh
```

**Android build requirements:**
- Linux host (Ubuntu recommended)
- Java JDK 17
- ~4 GB disk space (first build downloads Android SDK/NDK)

Install on device:
```bash
adb install bin/googtts-1.0.0-arm64-v8a-debug.apk
```

---

## ⌨️ Keyboard Shortcuts / اختصارات لوحة المفاتيح

| Shortcut | Action | الإجراء |
|----------|--------|--------|
| `Enter` | Convert text & play audio | تحويل النص وتشغيل الصوت |
| `Escape` | Stop audio playback | إيقاف تشغيل الصوت |
| `Ctrl+S` | Save last MP3 to custom location | حفظ آخر ملف MP3 |
| `Ctrl+Q` | Quit application | إغلاق التطبيق |
| `Tab` | Navigate between elements | التنقل بين العناصر |

---

## 🌍 Supported Languages / اللغات المدعومة

| Code | Language | اللغة |
|------|----------|------|
| `ar` | Arabic | العربية |
| `en` | English | الإنجليزية |
| `fr` | French | الفرنسية |
| `es` | Spanish | الإسبانية |
| `de` | German | الألمانية |
| `tr` | Turkish | التركية |
| `ja` | Japanese | اليابانية |
| `ko` | Korean | الكورية |
| `zh-CN` | Chinese | الصينية |
| `ru` | Russian | الروسية |

---

## 📋 Requirements / المتطلبات

- Python 3.8+ (auto-installed by launcher scripts)
- Internet connection (for Google TTS API)
- Audio output device (speakers or headphones)

### Python packages:
- `gTTS` — Google Text-to-Speech
- `pygame` — Audio playback
- `kivy` — Android/desktop GUI (optional)

---

## 📄 License / الرخصة

MIT License — Free to use, modify, and distribute.

رخصة MIT — مجاني للاستخدام والتعديل والتوزيع.
