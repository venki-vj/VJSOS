---
title: Android Studio Setup on Windows (2026 Beginner Guide)
episode: 13
series: Tutorials
length: "10:00"
target: "Beginners"
tags: [android, studio, setup, beginner, windows]
status: draft
---

# Android Studio Setup on Windows (2026 Beginner Guide)

## Hook (0:00–0:08)
"Struggling to install Android Studio on Windows? In the next 10 minutes, you'll have a working dev environment — no errors, no guesswork."

## What You'll Learn
- Download & install Android Studio (latest 2026 version)
- Configure SDK and emulator
- Create your first Kotlin + Jetpack Compose project
- Fix common Windows-specific issues

---

## Step 1: Download Android Studio (0:08–1:00)

### Action
1. Go to `developer.android.com/studio`
2. Click **"Download Android Studio"**
3. Choose **Windows (64-bit)** — .exe installer

### Visual
- Screen recording of download page
- Highlight "Windows" button

### Tips
- Use the **Canary/Preview** build only if you want latest features
- **Stable** is recommended for beginners

---

## Step 2: Run Installer (1:00–2:30)

### Action
1. Run `android-studio-2026.x.x.exe`
2. Click **Next** through welcome screen
3. **Important:** Choose components:
   - ✅ Android Studio
   - ✅ Android Virtual Device
   - ❌ Performance (optional)

### Visual
- Screen recording of each installer screen
- Pause at component selection

### Common Issue: "Installation failed"
- **Cause:** Antivirus blocking
- **Fix:** Disable real-time protection temporarily or add exception

---

## Step 3: First Launch & Setup Wizard (2:30–4:00)

### Action
1. Launch Android Studio
2. **Do not import settings** (choose "Do not import settings")
3. **UI Theme:** Choose Darcula (dark) or Light
4. **SDK Components:** Keep defaults
   - Android SDK
   - Android SDK Platform
   - Android Emulator (Intel x86)

### Visual
- First-launch wizard screens
- Show theme selection

### Windows-Specific: Emulator Acceleration
- **Intel CPU:** HAXM installer (auto)
- **AMD CPU:** Windows Hypervisor Platform (enable in Windows Features)
- **Apple Silicon:** Not applicable on Windows

---

## Step 4: SDK Manager — Verify Installation (4:00–5:00)

### Action
1. **Tools** → **SDK Manager**
2. **SDK Platforms** tab:
   - ✅ Android 14 (API 34) — **Latest stable**
   - ✅ Android 13 (API 33) — **Backward compatibility**
3. **SDK Tools** tab:
   - ✅ Android SDK Build-Tools 34.x
   - ✅ Android Emulator
   - ✅ Android SDK Platform-Tools
   - ✅ Intel x86 Emulator Accelerator (HAXM)

### Visual
- SDK Manager screenshots

---

## Step 5: Create Virtual Device (5:00–6:30)

### Action
1. **Tools** → **Device Manager**
2. **Create Device** → **Phone** → **Pixel 8** (or latest)
3. **System Image:** Download **Android 14 (API 34)** — Google APIs
4. **Advanced Settings:**
   - Camera: **Webcam0** (for camera testing)
   - RAM: 2048 MB (adjust if low RAM)
4. **Finish** → **Play** button to start emulator

### Visual
- Device Manager walkthrough
- Emulator booting

### Troubleshooting: Emulator Won't Start
| Error | Fix |
|-------|-----|
| "HAXM not installed" | SDK Manager → SDK Tools → Intel HAXM |
| "VT-x disabled" | BIOS → Enable Virtualization |
| "Emulator crashes" | Wipe Data in Device Manager |

---

## Step 6: Create First Project (6:30–8:00)

### Action
1. **New Project** → **Empty Activity** (Jetpack Compose)
2. **Name:** `MyFirstApp`
3. **Package:** `com.example.myfirstapp`
3. **Language:** Kotlin
4. **Minimum SDK:** API 24 (Android 7.0) — covers 95% devices
5. **Build Configuration:** **Kotlin DSL (build.gradle.kts)**

### Visual
- New Project wizard
- Show "Empty Activity" with Compose icon

---

## Step 7: Run on Emulator (8:00–9:00)

### Action
1. Wait for **Gradle sync** (bottom right)
2. Click **Green Play Button** (or Shift+F10)
3. Select **Pixel 8** emulator
4. App launches — "Hello Android!"

### Visual
- Gradle sync progress
- Emulator with running app

---

## Step 8: Quick Code Tour (9:00–9:45)

### Files to Highlight
| File | Purpose |
|------|---------|
| `MainActivity.kt` | UI entry point (Compose) |
| `build.gradle.kts` | Dependencies, plugins |
| `AndroidManifest.xml` | Permissions, app config |
| `res/values/strings.xml` | Text resources |

### Quick Edit Demo
- Change `Text("Hello Android!")` → `Text("Hello from VJSOS!")`
- Hot reload (Ctrl+S) shows instant update

---

## Before → After (9:45–9:55)
| Before | After |
|--------|-------|
| No Android Studio | ✅ Fully configured IDE |
| No emulator | ✅ Pixel 8 running |
| No project | ✅ Kotlin + Compose app |

---

## What to Learn Next (9:55–10:00)

**Video #14: "First App in Kotlin & Jetpack Compose"**
- Build a real counter app
- Learn Compose basics: Column, Row, Text, Button
- State management with `remember`

**Subscribe** for the complete Android development series!

---

## Production Notes

### Recording Checklist
- [ ] 1080p @ 30fps (OBS Studio)
- [ ] Clear audio (USB mic, -12dB peak)
- [ ] Cursor highlight enabled
- [ ] Windows notifications OFF

### Editing Notes
- Speed up Gradle sync (time-lapse)
- Add chapter markers (YouTube chapters)
- End screen: Video #14 + Subscribe button

### SEO
- **Title:** Android Studio Setup on Windows (2026 Beginner Guide)
- **Description:** Step-by-step Android Studio installation for Windows. Covers SDK, emulator, first Kotlin Compose project. Fixes common errors.
- **Tags:** android studio, windows, tutorial, beginner, kotlin, jetpack compose, 2026
- **Hashtags:** #AndroidDevelopment #Kotlin #JetpackCompose #VJSOS