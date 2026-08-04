# Engineering — Tools & Engines

> The tool runtime layer — every tool wrapped with retries, logging, permissions, and structured outputs.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                Tool Runtime                         │
├─────────────────────────────────────────────────────┤
│  Permissions · Logging · Retries · Structured I/O   │
└─────────────────────────────────────────────────────┘
         │       │       │      │       │
    Git  │   Bash  │   Docker │  Python │  Android SDK
         │   │       │      │       │
         ▼   ▼       ▼      ▼       ▼
       Engine   Engine  Engine Engine Engine
         │       │       │      │       │
      Git CLI  Shell    Docker  Python  ADB/Gradle
      CLI      CLI      CLI     CLI     CLI
```

## Engine Registry

| Engine | Binary | VJSOS Wrapper | Use Case | Phase |
|--------|--------|---------------|----------|-------|
| **Git** | `git` | `engineering/scripts/git-log.py` | Version control, commits | 1 |
| **Bash** | `bash` | Direct (via CI) | Scripting, automation | 1-2 |
| **Docker** | `docker` | Direct (in workflow) | Reproducible environments | 1-2 |
| **Python** | `python3` | Direct | Tool scripting, parsing | 1-2 |
| **Node** | `node` | Direct (npm) | React apps, build tools | 1-2 |
| **Remotion** | `npx remotion` | `remotion.config.ts` | Video generation | 3 |
| **Blender** | `blender` | `render-queue.py` | 3D animation, rendering | 3 |
| **FFmpeg** | `ffmpeg` | `video-process.sh` | Video/audio processing | 2-3 |
| **Android SDK** | `adb`, `gradle` | `build-apk.sh` | Android development | 2 |
| **Browser** | Headless Chrome | `screenshot.sh` | Automation, testing | 2 |
| **REST APIs** | `curl`/`requests` | `api-client.py` | Web service integration | 1 |
| **MCP Servers** | Via Claude Code | Direct | Model context protocol | 1 |
| **Database** | SQLite | Direct | Structured data storage | 1-2 |

## Phase-Aware Execution

| Phase | Tools Available | Tools Deferred |
|-------|----------------|----------------|
| **Phase 1 — Brain** | Git, Bash, Python, Node, REST APIs, MCP, Browser | Docker (heavy), Blender, FFmpeg, Android SDK |
| **Phase 2 — Factory (light)** | + Docker, Python (ML libs), Node (Remotion), FFmpeg (short clips), Android SDK (emulator) | Blender (complex scenes) |
| **Phase 3 — Factory (heavy)** | + Blender (full), FFmpeg (4K), Remotion (full) | — |
| **Phase 4 — Data Center** | All tools on dedicated hardware | — |

## Tool Configuration

### Git
```bash
# Global config
git config --global user.name "VJSOS"
git config --global user.email "team@vjsos.studio"
git config --global init.defaultBranch main

# Repository config
core.autocrlf: input
core.editor: code --wait
pull.rebase: true
```

### Python
```bash
# Version: Python 3.11+
# Virtual environment: venv or conda
# Package management: pip (requirements.txt, version-pinned)
```

### Node
```bash
# Version: Node 20 LTS
# Package manager: npm 10+ or yarn 4
# Project: package.json + package-lock.json
```

### Docker
```bash
# Docker Desktop (Windows)
# Use for: reproducible builds, isolated environments
# Never commit secrets or credentials
```

## Permission Model

| Tool | Read | Write | Execute | Network |
|------|------|-------|---------|---------|
| Git | ✅ | ✅ | ✅ | ✅ |
| Bash | ✅ | ✅ | ✅ | ✅ |
| Docker | ✅ | ✅ | ✅ | ✅ |
| Python | ✅ | ✅ | ✅ | ✅ |
| Blender | ✅ | ✅ | ✅ | ❌ (local files) |
| Android SDK | ✅ | ✅ | ✅ | ✅ |
| REST API | ✅ | ⚠️ | ✅ | ✅ |

## Links

- [[engineering/automation/README]] — CI/CD pipelines
- [[engineering/scripts/README]] — utility scripts
- [[engineering/builders/README]] — project generators
- [[governance/Standards]] — coding standards
- [[docs/ARCHITECTURE_SPEC]] — full architecture specification