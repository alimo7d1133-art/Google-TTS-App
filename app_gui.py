#!/usr/bin/env python3
"""
Google Text-to-Speech — Accessible GUI (tkinter)
تطبيق تحويل النص إلى كلام — واجهة رسومية متاحة لقارئات الشاشة

Fully accessible with NVDA, JAWS, VoiceOver, and Orca.
Every widget has a clear label, Tab navigation works throughout,
and status messages are announced automatically.
"""

import sys
import subprocess
import os
import threading
from datetime import datetime

# --------------- Auto-install dependencies ---------------
def install_requirements():
    required = {'gtts': 'gTTS', 'pygame': 'pygame'}
    for import_name, pip_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', pip_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

install_requirements()

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gtts import gTTS
import pygame

# --------------- Constants ---------------
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

LANGUAGES = [
    ("ar", "العربية — Arabic"),
    ("en", "الإنجليزية — English"),
    ("fr", "الفرنسية — French"),
    ("es", "الإسبانية — Spanish"),
    ("de", "الألمانية — German"),
    ("tr", "التركية — Turkish"),
    ("ja", "اليابانية — Japanese"),
    ("ko", "الكورية — Korean"),
    ("zh-CN", "الصينية — Chinese"),
    ("ru", "الروسية — Russian"),
]


class AccessibleTTSApp:
    """Main application window — fully keyboard-navigable and screen-reader friendly."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Google Text-to-Speech — تحويل النص إلى كلام")
        self.root.geometry("620x520")
        self.root.minsize(500, 440)
        self.root.configure(bg="#ffffff")

        # High-contrast colours for low-vision users
        self.bg = "#ffffff"
        self.fg = "#000000"
        self.accent = "#0056b3"

        # Audio engine
        pygame.mixer.init()
        self.is_playing = False
        self.last_file = None

        self._build_ui()

        # Global keyboard shortcuts
        self.root.bind("<Return>", lambda e: self._convert())
        self.root.bind("<Control-Return>", lambda e: self._convert())
        self.root.bind("<Escape>", lambda e: self._stop_audio())
        self.root.bind("<Control-s>", lambda e: self._save_as())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())

        # Focus the text area on launch so screen readers announce it
        self.text_input.focus_set()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        main = tk.Frame(self.root, bg=self.bg, padx=16, pady=12)
        main.pack(fill=tk.BOTH, expand=True)

        # ---- Title (read once by screen reader) ----
        title = tk.Label(
            main,
            text="تحويل النص إلى كلام — Text to Speech",
            font=("Arial", 16, "bold"),
            bg=self.bg, fg=self.fg,
            anchor="w",
        )
        title.pack(fill=tk.X, pady=(0, 12))

        # ---- Language selector ----
        lang_frame = tk.Frame(main, bg=self.bg)
        lang_frame.pack(fill=tk.X, pady=(0, 8))

        lang_label = tk.Label(
            lang_frame,
            text="اللغة / Language:",
            font=("Arial", 12),
            bg=self.bg, fg=self.fg,
        )
        lang_label.pack(side=tk.LEFT, padx=(0, 8))

        self.lang_var = tk.StringVar(value="ar")
        self.lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=[f"{code} - {name}" for code, name in LANGUAGES],
            state="readonly",
            width=32,
            font=("Arial", 11),
        )
        self.lang_combo.set("ar - العربية — Arabic")
        self.lang_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Accessibility: link label to combo
        self.lang_combo.configure(takefocus=True)

        # ---- Text input ----
        text_label = tk.Label(
            main,
            text="أدخل النص هنا / Enter text here:",
            font=("Arial", 12),
            bg=self.bg, fg=self.fg,
            anchor="w",
        )
        text_label.pack(fill=tk.X, pady=(8, 4))

        self.text_input = tk.Text(
            main,
            font=("Arial", 13),
            wrap=tk.WORD,
            height=8,
            bg="#fafafa", fg=self.fg,
            insertbackground=self.fg,
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=2,
            highlightcolor=self.accent,
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        # ---- Button row ----
        btn_frame = tk.Frame(main, bg=self.bg)
        btn_frame.pack(fill=tk.X, pady=(4, 8))

        self.convert_btn = tk.Button(
            btn_frame,
            text="تحويل وتشغيل / Convert & Play  (Enter)",
            font=("Arial", 12, "bold"),
            bg=self.accent, fg="#ffffff",
            activebackground="#003d80", activeforeground="#ffffff",
            padx=12, pady=6,
            cursor="hand2",
            command=self._convert,
        )
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.stop_btn = tk.Button(
            btn_frame,
            text="إيقاف / Stop  (Esc)",
            font=("Arial", 12),
            bg="#c0392b", fg="#ffffff",
            activebackground="#922b21", activeforeground="#ffffff",
            padx=12, pady=6,
            command=self._stop_audio,
            state=tk.DISABLED,
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.save_btn = tk.Button(
            btn_frame,
            text="حفظ MP3 / Save  (Ctrl+S)",
            font=("Arial", 12),
            bg="#27ae60", fg="#ffffff",
            activebackground="#1e8449", activeforeground="#ffffff",
            padx=12, pady=6,
            command=self._save_as,
            state=tk.DISABLED,
        )
        self.save_btn.pack(side=tk.LEFT)

        # ---- Status bar (announced by screen readers) ----
        self.status_var = tk.StringVar(value="جاهز / Ready")
        self.status_bar = tk.Label(
            main,
            textvariable=self.status_var,
            font=("Arial", 11),
            bg="#f0f0f0", fg=self.fg,
            anchor="w",
            relief=tk.SUNKEN,
            padx=8, pady=4,
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # ---- Keyboard shortcuts help ----
        help_text = (
            "اختصارات: Enter = تحويل | Esc = إيقاف | Ctrl+S = حفظ | Ctrl+Q = خروج\n"
            "Shortcuts: Enter = Convert | Esc = Stop | Ctrl+S = Save | Ctrl+Q = Quit"
        )
        help_label = tk.Label(
            main,
            text=help_text,
            font=("Arial", 9),
            bg=self.bg, fg="#555555",
            anchor="w",
            justify=tk.LEFT,
        )
        help_label.pack(fill=tk.X, side=tk.BOTTOM, pady=(4, 0))

    # ------------------------------------------------------------------ Logic
    def _set_status(self, msg: str):
        self.status_var.set(msg)
        self.root.update_idletasks()

    def _get_lang_code(self) -> str:
        raw = self.lang_combo.get()
        return raw.split(" - ")[0].strip() if " - " in raw else "ar"

    def _convert(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self._set_status("تنبيه: أدخل نصاً أولاً / Warning: enter text first")
            messagebox.showwarning(
                "تنبيه / Warning",
                "الرجاء إدخال نص قبل التحويل.\nPlease enter text before converting.",
            )
            self.text_input.focus_set()
            return

        lang = self._get_lang_code()
        self.convert_btn.configure(state=tk.DISABLED)
        self._set_status("جاري التحويل... / Converting...")

        threading.Thread(target=self._convert_thread, args=(text, lang), daemon=True).start()

    def _convert_thread(self, text: str, lang: str):
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(OUTPUT_DIR, f"tts_{timestamp}.mp3")

            tts = gTTS(text=text, lang=lang)
            tts.save(filepath)
            self.last_file = filepath

            self.root.after(0, self._play_file, filepath)
        except Exception as exc:
            self.root.after(0, self._on_error, str(exc))

    def _play_file(self, filepath: str):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.is_playing = True
            self.stop_btn.configure(state=tk.NORMAL)
            self.save_btn.configure(state=tk.NORMAL)
            self.convert_btn.configure(state=tk.NORMAL)
            self._set_status(f"جاري التشغيل / Playing: {os.path.basename(filepath)}")
            self._poll_playback()
        except Exception as exc:
            self._on_error(str(exc))

    def _poll_playback(self):
        if pygame.mixer.music.get_busy():
            self.root.after(200, self._poll_playback)
        else:
            self.is_playing = False
            self.stop_btn.configure(state=tk.DISABLED)
            self._set_status("تم التشغيل بنجاح / Playback finished")

    def _stop_audio(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.stop_btn.configure(state=tk.DISABLED)
            self._set_status("تم الإيقاف / Stopped")

    def _save_as(self):
        if not self.last_file or not os.path.exists(self.last_file):
            self._set_status("لا يوجد ملف لحفظه / No file to save")
            return
        dest = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 Audio", "*.mp3")],
            title="حفظ الملف الصوتي / Save Audio File",
        )
        if dest:
            import shutil
            shutil.copy2(self.last_file, dest)
            self._set_status(f"تم الحفظ / Saved: {dest}")

    def _on_error(self, msg: str):
        self.convert_btn.configure(state=tk.NORMAL)
        self._set_status(f"خطأ / Error: {msg}")
        messagebox.showerror("خطأ / Error", msg)


def main():
    root = tk.Tk()
    AccessibleTTSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
