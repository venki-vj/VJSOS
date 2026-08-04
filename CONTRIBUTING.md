# Contributing to VJSOS

Thank you for your interest in contributing to VJSOS! This project is the operating system for independent media studios — combining AI-augmented production with human creativity.

## How to Contribute

### 1. Report Issues
- Use the GitHub issue templates (bug report or feature request)
- Include clear reproduction steps and expected behavior
- Tag with the correct phase: `Phase 1`, `Phase 2`, `Phase 3`, or `Phase 4`

### 2. Propose Changes
- Fork the repository
- Create a feature branch: `feature/your-feature-name`
- Follow the [coding standards](governance/Standards.md)
- Update documentation for any changes
- Open a Pull Request

### 3. Pull Request Process
1. Ensure CI passes (lint, docs validation, JSON config)
2. Fill out the PR template completely
3. Link related issues with `Fixes #123` or `Refs #123`
4. Get 1 code review + 1 docs review
5. Squash and merge to `main`

### 4. Development Setup
This is a documentation + automation project — no build step required:
```bash
# Clone
git clone https://github.com/venki-vj/VJSOS.git

# No install needed — just run scripts directly
python engineering/scripts/parse-session-log.py --all
```

### 5. Documentation Standards
All markdown files must have:
```yaml
---
title: Descriptive Title
date: 2026-08-05
version: 0.1.1
tags: [tag1, tag2]
---
```
See [Markdown Style Guide](governance/MarkdownStyleGuide.md) and [Documentation Rules](governance/DocumentationRules.md).

### 6. Commit Message Format
```
type(scope): subject

[optional body]

[optional footer: issue refs]
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `build`, `perf`

### 7. Code of Conduct
Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Areas for Contribution

- **Content Production:** Android tutorials, Kids Studio scripts
- **Automation:** Engineering scripts, CI/CD improvements
- **Documentation:** Expand knowledge graph, improve guides
- **Tools:** New builders, render utilities, asset pipelines

## Questions?

Open a GitHub Discussion or check existing issues.