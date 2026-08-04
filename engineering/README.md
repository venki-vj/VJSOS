---
title: Engineering README
date: 2026-08-05
version: 0.1.1
tags: [engineering, tools, automation, builders]
---

# VJSOS Engineering

> Tools, automation, and builders that power the production pipeline.

## Structure

```
engineering/
├── README.md              ← This file
├── ENGINES.md             ← Tools & engines documentation
├── automation/            ← CI/CD, pipeline automation
│   └── README.md
├── scripts/               ← Utility scripts, data processing
│   └── README.md
└── builders/             ← Scaffolding, code generators
    └── README.md
```

## Layers

| Layer | Purpose | Tools |
|-------|---------|-------|
| **Runtime** | Daily execution | Git, Bash, Python, Docker |
| **Production** | Asset pipelines | Blender, FFmpeg, Remotion |
| **Automation** | CI/CD, triggers | GitHub Actions, cron |
| **Builders** | Project generators | init scripts, templates |

## Philosophy

1. **Everything scriptable:** If you can't automate it, it doesn't exist in the system.
2. **Wrapped with care:** All tools get retries, logging, permissions, structured I/O.
3. **Phase-aware:** Not all tools are available in all phases — see [[docs/ARCHITECTURE_SPEC]].

## Quick Start

```bash
# Run a script
python engineering/scripts/parse-session-log.py --date 2026-08-05

# Generate a new project
python engineering/builders/init-android-project.py "android-basics-kotlin"

# See what automations exist
ls .github/workflows/
```

## Links

- [[engineering/ENGINES]] — full tools documentation
- [[governance/Standards]] — coding and file standards
- [[docs/ARCHITECTURE_SPEC]] — full architecture
- [[projects/Android]] — project-specific engineering
- [[projects/KidsStudio]] — animation pipeline