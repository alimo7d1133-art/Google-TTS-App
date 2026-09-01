#!/usr/bin/env python3
"""
Google Text-to-Speech — Kivy (Android / Desktop)
تطبيق تحويل النص إلى كلام — واجهة Kivy للأندرويد

Accessibility: every widget carries a content description for TalkBack.
No decorative images — text, buttons, and input fields only.
"""

import os
import sys
import subprocess
from datetime import datetime

# Auto-install on desktop (on Android packages are bundled)
if sys.platform != "linux" or "ANDROID_ARGUMENT" not in os.environ:
    for pkg_import, pkg_pip in [("gtts", "gTTS"), ("kivy", "kivy")]:
        try:
            __import__(pkg_import)
        except ImportError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg_pip],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform

from gtts import gTTS

# High-contrast theme
Window.clearcolor = (1, 1, 1, 1)  # white background

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

LANGUAGES = {
    "العربية — Arabic": "ar",
    "الإنجليزية — English": "en",
    "الفرنسية — French": "fr",
    "الإسبانية — Spanish": "es",
    "الألمانية — German": "de",
    "التركية — Turkish": "tr",
}


class TTSRoot(BoxLayout):
    """Root layout with full accessibility content descriptions."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=16, spacing=12, **kwargs)
        self.sound = None

        # ---- Title ----
        title = Label(
            text="تحويل النص إلى كلام\nText to Speech",
            font_size="22sp",
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=70,
            halign="center",
            valign="middle",
        )
        title.bind(size=title.setter("text_size"))
        title.accessibility_description = "Application title: Text to Speech"
        self.add_widget(title)

        # ---- Language spinner ----
        lang_label = Label(
            text="اللغة / Language:",
            font_size="16sp",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=36,
            halign="left",
            valign="middle",
        )
        lang_label.bind(size=lang_label.setter("text_size"))
        lang_label.accessibility_description = "Language selector label"
        self.add_widget(lang_label)

        self.lang_spinner = Spinner(
            text="العربية — Arabic",
            values=list(LANGUAGES.keys()),
            size_hint_y=None,
            height=48,
            font_size="15sp",
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0, 0, 0, 1),
        )
        self.lang_spinner.accessibility_description = (
            "Choose language for text to speech conversion"
        )
        self.add_widget(self.lang_spinner)

        # ---- Text input ----
        input_label = Label(
            text="أدخل النص هنا / Enter text here:",
            font_size="16sp",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=36,
            halign="left",
            valign="middle",
        )
        input_label.bind(size=input_label.setter("text_size"))
        input_label.accessibility_description = "Text input field label"
        self.add_widget(input_label)

        self.text_input = TextInput(
            hint_text="اكتب النص المراد تحويله / Type the text to convert",
            font_size="16sp",
            multiline=True,
            size_hint_y=1,
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1),
        )
        self.text_input.accessibility_description = (
            "Text input. Type the text you want to convert to speech."
        )
        self.add_widget(self.text_input)

        # ---- Buttons ----
        btn_row = BoxLayout(size_hint_y=None, height=56, spacing=10)

        self.convert_btn = Button(
            text="تحويل وتشغيل / Convert & Play",
            font_size="15sp",
            bold=True,
            background_color=(0, 0.34, 0.7, 1),
            color=(1, 1, 1, 1),
        )
        self.convert_btn.accessibility_description = (
            "Convert text to speech and play audio"
        )
        self.convert_btn.bind(on_press=self.on_convert)
        btn_row.add_widget(self.convert_btn)

        self.stop_btn = Button(
            text="إيقاف / Stop",
            font_size="15sp",
            background_color=(0.75, 0.22, 0.17, 1),
            color=(1, 1, 1, 1),
            disabled=True,
        )
        self.stop_btn.accessibility_description = "Stop audio playback"
        self.stop_btn.bind(on_press=self.on_stop)
        btn_row.add_widget(self.stop_btn)

        self.add_widget(btn_row)

        # ---- Status ----
        self.status_label = Label(
            text="جاهز / Ready",
            font_size="14sp",
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=36,
            halign="left",
            valign="middle",
        )
        self.status_label.bind(size=self.status_label.setter("text_size"))
        self.status_label.accessibility_description = "Status: Ready"
        self.add_widget(self.status_label)

    # ---- Logic ----
    def set_status(self, msg):
        self.status_label.text = msg
        self.status_label.accessibility_description = f"Status: {msg}"

    def on_convert(self, *_args):
        text = self.text_input.text.strip()
        if not text:
            self.set_status("تنبيه: أدخل نصاً أولاً / Enter text first")
            return

        lang_name = self.lang_spinner.text
        lang_code = LANGUAGES.get(lang_name, "ar")

        self.convert_btn.disabled = True
        self.set_status("جاري التحويل... / Converting...")

        # Run conversion off-main thread via Clock
        Clock.schedule_once(lambda dt: self._do_convert(text, lang_code), 0.1)

    def _do_convert(self, text, lang):
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(OUTPUT_DIR, f"tts_{ts}.mp3")

            tts = gTTS(text=text, lang=lang)
            tts.save(filepath)

            self.sound = SoundLoader.load(filepath)
            if self.sound:
                self.sound.play()
                self.stop_btn.disabled = False
                self.set_status(f"جاري التشغيل / Playing: tts_{ts}.mp3")
                Clock.schedule_interval(self._check_playback, 0.5)
            else:
                self.set_status("خطأ: تعذر تحميل الصوت / Error loading audio")
        except Exception as exc:
            self.set_status(f"خطأ / Error: {exc}")
        finally:
            self.convert_btn.disabled = False

    def _check_playback(self, dt):
        if self.sound and self.sound.state == "play":
            return
        Clock.unschedule(self._check_playback)
        self.stop_btn.disabled = True
        self.set_status("تم التشغيل بنجاح / Playback finished")

    def on_stop(self, *_args):
        if self.sound:
            self.sound.stop()
        self.stop_btn.disabled = True
        self.set_status("تم الإيقاف / Stopped")


class GoogleTTSApp(App):
    title = "Google Text-to-Speech"

    def build(self):
        return TTSRoot()


if __name__ == "__main__":
    GoogleTTSApp().run()
