[app]
# Google Text-to-Speech Android App
title = Google TTS
package.name = googtts
package.domain = org.googtts
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0

# Requirements — gTTS needs requests which needs urllib3, certifi, etc.
requirements = python3,kivy,gtts,requests,urllib3,charset-normalizer,idna,certifi,click

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Orientation
orientation = portrait

# Fullscreen off (better for accessibility)
fullscreen = 0

# Entry point
entrypoint = main.py

# Android API levels
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Architecture
android.archs = arm64-v8a,armeabi-v7a

# Accept SDK license
android.accept_sdk_license = True

# Use SDL2 bootstrap (supports audio)
p4a.bootstrap = sdl2

# Presplash and icon (none — accessibility first, no decorations)
# presplash.filename = %(source.dir)s/data/presplash.png
# icon.filename = %(source.dir)s/data/icon.png

# Android Accessibility — enable content descriptions
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
