# VJSOS-AI Video Generation — Local Hybrid Pipeline

> **Goal:** Keep using the free `claude-code` model route (no paid tiers), but avoid the `400 No target in combo supports tool calling` error that happens when ~30 tools are attached.
>
> **Fix:** Drive video generation with **local tools** (ffmpeg / Remotion) orchestrated by a **skill** that does *only* JSON-prompt generation (no tool-calling). The skill stays under the free model's limits; the heavy rendering is 100% local.

---

## Prerequisites (already in your stack)

| Tool | Check |
|------|-------|
| Python 3.11+ | `python --version` |
| ffmpeg | `ffmpeg -version` |
| Node + npm | `node -v && npm -v` |
| Remotion (optional, for animated GFX) | `npx remotion --version` |
| `jq` (optional, for JSON piping) | `jq --version` |

---

## Step 0 — Verify the `video_production` skill is ready

```bash
# List the skill files you should already have created:
ls skills/video_production/binder/skill.md
ls skills/video_production/binder/prompt.md
ls skills/video_production/tests/test_shot_list_generation.yaml
```

```bash
# Verify the orchestrator exists:
ls scripts/video_orchestrator/run.py
```

---

## Step 1 — Register the video-production skill

```bash
# From repo root — note: pass the PACKAGE DIRECTORY, not the skill.md file.
# register_skill() looks for binder/skill.md inside the directory you give it.
python scripts/skills_cli.py register skills/video_production
```

Expected:
```
✓ Registered: video_production v1.0.0
```

Check status:
```bash
python scripts/skills_cli.py list --domain media
```

You should see `✓ video_production v1.0.0 (generation) - media`.

---

## Step 2 — Test the skill (validates shot-list generation)

```bash
python scripts/skills_cli.py test video_production
```

Expected: all assertions pass, `qa_status: verified`.

---

## Step 3 — Generate a shot list (LLM step — does **not** touch the tool route)

Variables are passed as `KEY=VALUE` positional arguments:

```bash
python scripts/skills_cli.py prompt video_production \
  script="Cold open: git log shows Phase2 commits." \
  style_guide="Dark terminal (One Dark Pro), teal accent #00D4AA, JetBrains Mono 14pt, 3840x2160." \
  duration_target="90s" \
  platform="youtube" \
  aspect_ratio="16:9" \
  > shot_list.json
```

Inspect the result:

```bash
cat shot_list.json | jq .metadata
cat shot_list.json | jq '.shots | length'
```

---

## Step 4 — Render locally with the orchestrator

### Option A — Render all shots + build master + delivery encodes:

```bash
python scripts/video_orchestrator/run.py shot_list.json \
  --out output/video \
  --remotion-cwd .  # omit if you have no Remotion project
```

Creates: `output/video/master.mp4`, `output/video/youtube.mp4`,
`output/video/linkedin.mp4`, `output/video/twitter.mp4`.

### Option B — Render shots only (faster iteration):

```bash
# Render each shot to a clip, stop before concat/encode:
python scripts/video_orchestrator/run.py shot_list.json \
  --out output/video \
  --render-only
```

Result: clips under `output/video/clips/`.

---

## Step 5 — (Optional) Add a generative-video plugin for future use

If you later want to call Veo / Runway / Kling / Sora, create a plugin:

```bash
# 1. Create the manifest file at: plugins/generative_video/manifest.json
{
  "plugin_id": "generative_video",
  "name": "Generative Video Provider",
  "version": "1.0.0",
  "capabilities": ["ai_video_generation"],
  "auth_method": "api_key",
  "rate_limits": { "calls_per_minute": 5, "calls_per_hour": 50 },
  "config_schema": {
    "provider": { "type": "string", "enum": ["veo", "runway", "kling", "sora"] }
  }
}
```

```bash
# 2. Install + enable it:
python scripts/plugins_cli.py install plugins/generative_video/manifest.json
python scripts/plugins_cli.py enable generative_video
```

```bash
# 3. Approve through Governor (required in prod):
python scripts/plugins_cli.py review generative_video --approve --reviewer governor@vjsos-ai
```

> Note: plugin calls **do** count against rate/usage. Keep them for long-form generative clips only; let local tools handle everything else.

---

## Full Quick-Start (copy-paste each line separately)

```bash
python scripts/skills_cli.py register skills/video_production
python scripts/skills_cli.py test video_production
python scripts/skills_cli.py prompt video_production script="Cold open: git log shows Phase2 commits." style_guide="Dark terminal, teal accent, 4K" duration_target="90s" platform="youtube" aspect_ratio="16:9" > shot_list.json
python scripts/video_orchestrator/run.py shot_list.json --out output/video --render-only
```

---

## Troubleshooting

### `400 No target in combo supports tool calling`

Happens when a request carries **tools** and the route (e.g. `claude-code`)
reports `"tool_calling": false` in `/v1/models`.

This pipeline avoids that by design: the skill does prompt-only generation
(no tools), and rendering is local.

```bash
# Confirm your route's flag:
curl -s http://localhost:20128/v1/models | grep -A3 claude-code
```

### Skill not found after register

- Make sure you ran from the **repo root** (where `skills/` lives).
- Re-run `python scripts/skills_cli.py register ...` and check stdout.

### ffmpeg not found

- Linux: `sudo apt install ffmpeg` or `brew install ffmpeg`
- Windows: `winget install ffmpeg`  or download from https://ffmpeg.org/download.html

### Remotion rendering fails

- Make sure `npx remotion` is available and your Remotion project entry exists
- Or switch those shots to `type: ffmpeg` with a `ffmpeg_filter` string.

---

## File Map (what this creates)

| Path | Purpose |
|------|---------|
| `skills/video_production/` | Skill package (manifest + prompt + tests) |
| `scripts/video_orchestrator/run.py` | Local renderer (Remotion + ffmpeg) |
| `scripts/_register_video_skill.py` | One-shot registration helper |
| `output/video/` | Generated clips, master, delivery encodes |
| `plugins/generative_video/` | (Optional) generative-video plugin template |

---

## Status: ✅ Ready for local video production

All steps are **local**:

- No cloud tokens needed for rendering.
- No dependency on a tool-capable remote model route.
- Free-tier `claude-code` can still be used for interactive Claude Code work, just not for tool-bearing API requests — this pipeline sidesteps that entirely.

Happy rendering! 🎬