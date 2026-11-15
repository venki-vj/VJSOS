# VJSOS-AI Phase 2 Walkthrough — EDITOR QUICK REFERENCE
## One-Page Cheat Sheet for Post-Production

---

### ⏱️ TARGET TIMINGS (per screenplay)

| Section | Start | End | Duration | Key Visual |
|---------|-------|-----|----------|------------|
| Cold Open | 0:00 | 0:45 | 0:45 | Git log → 5-pane test → Title |
| Architecture | 0:45 | 1:45 | 1:00 | Animated diagram + tree |
| Skills | 1:45 | 3:30 | 1:45 | CLI demo, test run, prompt render |
| Plugins | 3:30 | 5:15 | 1:45 | Install → enable → vault → approve |
| Message Bus | 5:15 | 6:45 | 1:30 | Dual-pane pub/sub live |
| Analytics | 6:45 | 9:00 | 2:15 | All 5 components + dashboard JSON |
| Learning | 9:00 | 11:00 | 2:00 | Patterns → proposal lifecycle |
| Integration Test | 11:00 | 12:30 | 1:30 | **HERO: full test run uncut** |
| Closing | 12:30 | 13:30 | 1:00 | Summary → links → end card |

**Total Target: 13:30 ± 0:30**

---

### 🎬 FOOTAGE MAP (match filenames to segments)

| Segment | Expected Clips | Notes |
|---------|---------------|-------|
| Cold Open | `cold_open_01.mp4`, `cold_open_02.mp4` | 2 takes: git log, test panes |
| Architecture | `arch_tree.mp4`, `arch_diagram.mp4` | Diagram is GFX (V3), not screen cap |
| Skills | `skills_list.mp4`, `skills_register.mp4`, `skills_test.mp4`, `skills_prompt.mp4`, `skills_get.mp4` | 5 clips, speed typing 1.5x |
| Plugins | `plugins_list.mp4`, `plugins_install.mp4`, `plugins_enable.mp4`, `plugins_vault.mp4`, `plugins_review.mp4`, `plugins_get.mp4` | 6 clips |
| Message Bus | `bus_subscriber.mp4`, `bus_publisher.mp4` | **Sync these two** — publisher fires after subscriber ready |
| Analytics | `analytics_full.mp4` | One long take, scroll JSON slowly |
| Learning | `learning_full.mp4` | One long take |
| Integration | `integration_test_FULL.mp4` | **DO NOT CUT** — single 90-sec take |
| Post-Test | `post_skills.mp4`, `post_plugins.mp4`, `post_dashboard.mp4`, `post_proposals.mp4` | Quick cuts, 2 sec each |

---

### ✂️ EDIT DECISIONS (pre-made)

| Situation | Decision |
|-----------|----------|
| Typing commands | **Speed up 1.5×** — keep `Enter` → output real-time |
| JSON output > 20 lines | **Slow scroll** (keyframe position) or **cut to GFX callout** |
| Terminal clear between sections | **Keep the `clear` command** — adds rhythm |
| Talking head | **Only 4 moments**: Intro (0:40), Bridge 1 (3:25), Bridge 2 (9:55), Outro (12:15) |
| Music transitions | **Hard cut at section boundaries** — no crossfade |
| SFX on every keystroke? | **No** — only on `Enter` (soft *tick*) and output appear (*pop*) |
| Terminal chrome | **Crop to content area** — hide title bar, tabs, scrollbar |

---

### 🎵 AUDIO SYNC CHECKLIST

- [ ] VO recorded separately (48kHz, mono, -18dB RMS)
- [ ] VO aligned to screenplay timestamps ±0.5s
- [ ] Music bed **sidechained to VO** (duck -6dB when VO active)
- [ ] SFX at -12dB relative to VO
- [ ] Master at **-14 LUFS** (YouTube), **-16 LUFS** (LinkedIn), **-13 LUFS** (Twitter)
- [ ] True peak ≤ -1 dBTP
- [ ] Stems delivered: VO_Dry, VO_Proc, Music_Stems(5), SFX, FullMix

---

### 🎨 GFX INTEGRATION (V3 track)

| GFX Asset | Trigger | Duration | Notes |
|-----------|---------|----------|-------|
| Architecture Diagram | 0:45 (after cold open) | 1:00 | Full screen, nodes pulse on VO mention |
| Section Title: SKILLS | 1:45 | 2:00 | Essential Graphics template |
| Skill Manifest Callout | 1:52 | 0:06 | Overlay on terminal, pin to line |
| Test Output Highlight | 2:10 | 0:06 | Teal bg on `qa_status: verified` |
| Section Title: PLUGINS | 3:30 | 2:00 | Same template |
| Manifest.json Callout | 3:42 | 0:06 | Overlay |
| Vault Diagram | 3:57 | 0:06 | 3 backends |
| SDK Module Map | 4:09 | 0:07 | 6 modules |
| Section Title: MESSAGE BUS | 5:15 | 2:00 | |
| MessageType Enum | 5:24 | 0:06 | 12 types, animate in |
| Bus Internals | 5:46 | 0:06 | Routing table, DLQ |
| Section Title: ANALYTICS | 6:45 | 2:00 | |
| Data Flow Diagram | 6:54 | 0:06 | Collector → Agg → Alerts → Dash |
| Alert Rule Callout | 7:06 | 0:06 | |
| CostTracker Pricing | 7:12 | 0:06 | Table |
| Dashboard JSON | 7:35 | 0:07 | Pretty print, scroll |
| Section Title: LEARNING | 9:00 | 2:00 | |
| Pattern Types | 9:09 | 0:06 | 5 types |
| Pattern Object | 9:21 | 0:06 | |
| Proposal Lifecycle | 9:33 | 0:06 | 7 states |
| TrendAnalyzer | 9:45 | 0:05 | |
| Integration Flow | 11:38 | 0:17 | Particle animation |
| Summary Card | 12:30 | 0:08 | 5 checkmarks |
| End Card | 12:58 | 0:12 | Logo + CTA |

---

### 📦 EXPORT SETTINGS

| Platform | Codec | Bitrate | Audio | Resolution |
|----------|-------|---------|-------|------------|
| **Master** | ProRes 422 HQ | — | 48k/24-bit | 3840×2160 |
| **YouTube** | H.264 High | 20 Mbps CBR | AAC 320k | 3840×2160 |
| **Twitter/X** | H.264 High | 8 Mbps CBR | AAC 128k | 1920×1080 |
| **LinkedIn** | H.264 High | 10 Mbps CBR | AAC 256k | 1920×1080 |
| **Shorts/Reels** | H.264 High | 12 Mbps | AAC 128k | 1080×1920 (vertical crop) |

**Color Space**: Rec.709 (all). **Frame Rate**: 30 fps (all).

---

### 🔍 QC CHECKLIST (watch full before delivery)

- [ ] No dropped frames (check 30fps compliance)
- [ ] VO sync ±0.25s entire runtime
- [ ] All terminal text readable at 1080p (min 14pt equivalent)
- [ ] No PII in footage (tokens, paths, emails blurred)
- [ ] Music license cleared (stems or CC-BY)
- [ ] Chapters/timestamps match screenplay
- [ ] Subtitles (.srt) synced, no typos
- [ ] Thumbnails: 3 variants (1280×720), text safe zone
- [ ] Description template filled with links
- [ ] End screen elements (subscribe, related video) in YouTube upload

---

### 🚨 COMMON PITFALLS

| Pitfall | Fix |
|---------|-----|
| Terminal text too small | Zoom terminal 1.5× before recording; crop in post |
| Music too loud | Sidechain threshold -24dB, ratio 4:1, check on phone speaker |
| VO pops | De-ess at 6kHz, high-pass 80Hz, gentle comp 3:1 |
| Integration test too long | **Don't cut** — it's the hero shot. Speed up only if >2min |
| GFX doesn't match terminal | Use corner-pin on GFX, track terminal corners |
| Color shift on export | Master in Rec.709, apply LUT only to GFX, not terminal |

---

### 📁 FILE NAMING CONVENTION

```
vjsos-phase2-walkthrough_
  ├── master_prores.mov
  ├── youtube_4k.mp4
  ├── twitter_1080p.mp4
  ├── linkedin_1080p.mp4
  ├── shorts_vertical.mp4
  ├── chapters.txt
  ├── description.md
  ├── subtitles_en.srt
  ├── thumb_01.png
  ├── thumb_02.png
  └── thumb_03.png
```

---

**Editor:** _______________   **Date:** _______________   **Version:** _______________