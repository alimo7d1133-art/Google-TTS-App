#!/usr/bin/env python3
"""
Google Text-to-Speech Application
تطبيق تحويل النص إلى كلام باستخدام Google Text-to-Speech

Auto-installs required packages on first run.
"""

import sys
import subprocess
import os
from datetime import datetime


def install_requirements():
    """Auto-install required packages if not present."""
    required = {'gtts': 'gTTS', 'pygame': 'pygame'}
    for import_name, pip_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"جاري تثبيت {pip_name} ... / Installing {pip_name}...")
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', pip_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"تم تثبيت {pip_name} بنجاح ✓ / {pip_name} installed successfully ✓")


install_requirements()

from gtts import gTTS
import pygame


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def init_audio():
    """Initialize the pygame mixer for audio playback."""
    pygame.mixer.init()


def text_to_speech(text: str, lang: str = "ar") -> str:
    """
    Convert text to speech, save as MP3 and return the file path.

    Args:
        text: The text to convert.
        lang: Language code (default 'ar' for Arabic).

    Returns:
        Absolute path to the saved MP3 file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tts_{timestamp}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)
    return filepath


def play_audio(filepath: str):
    """Play an MP3 file using pygame."""
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()


def get_language_choice() -> str:
    """Prompt user to choose a language and return the language code."""
    languages = {
        "1": ("ar", "العربية / Arabic"),
        "2": ("en", "الإنجليزية / English"),
        "3": ("fr", "الفرنسية / French"),
        "4": ("es", "الإسبانية / Spanish"),
        "5": ("de", "الألمانية / German"),
        "6": ("tr", "التركية / Turkish"),
    }

    print("\n╔══════════════════════════════════════╗")
    print("║       اختر اللغة / Choose Language       ║")
    print("╠══════════════════════════════════════╣")
    for key, (code, name) in languages.items():
        print(f"║  {key}. {name:<34} ║")
    print("╚══════════════════════════════════════╝")

    choice = input("\nأدخل رقم اللغة / Enter language number [1]: ").strip()
    if choice in languages:
        return languages[choice][0]
    return "ar"


def main():
    """Main application loop."""
    init_audio()

    print("=" * 50)
    print("  Google Text-to-Speech / تحويل النص إلى كلام")
    print("=" * 50)
    print("اكتب 'خروج' أو 'exit' أو 'q' للخروج من التطبيق")
    print("Type 'exit' or 'q' to quit the application\n")

    while True:
        lang = get_language_choice()

        text = input("\nأدخل النص / Enter text: ").strip()
        if not text:
            print("⚠  الرجاء إدخال نص / Please enter some text.")
            continue
        if text.lower() in ("exit", "q", "خروج"):
            print("\nمع السلامة! / Goodbye! 👋")
            break

        print(f"\n⏳ جاري التحويل... / Converting...")
        try:
            filepath = text_to_speech(text, lang)
            print(f"✅ تم الحفظ / Saved: {filepath}")
            print("🔊 جاري التشغيل... / Playing...")
            play_audio(filepath)
            print("✅ تم التشغيل بنجاح / Playback complete.")
        except Exception as e:
            print(f"❌ خطأ / Error: {e}")


if __name__ == "__main__":
    main()
