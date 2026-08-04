# Project PlayStore — Android App Publishing

> Publishing Android Studio apps to the Play Store.

## Mission

Get VJSOS apps onto the Play Store — both public apps (creator tools, games) and internal tools for the studio itself.

## Pipeline

### 1. Pre-Launch
- App signing setup
- Store listing assets
- Screenshots and promotional images
- Privacy policy (GDPR / COPPA compliant)
- Content rating questionnaire

### 2. Release Build
- `engineers/scripts/build-apk.sh` — build script
- Signing config
- ProGuard / R8 for release
- App bundle (AAB) generation

### 3. Play Console Upload
- Store listing
- Content rating
- Pricing & distribution
- App content (targeting, ads, permissions)

### 4. Post-Launch
- Monitor crash reports (Firebase Crashlytics)
- Update with bug fixes
- Review metrics (installs, retention, ratings)

## Current Apps

| App | Status | Target |
|-----|--------|--------|
| VJSOS Studio Assistant | 🔄 Planning | v1.0 (Month 2) |
| Creator Tools | ⏸ Idea | MVP (Q4 2026) |

## Links

- [[projects/InternalTools]]
- [[projects/Android]]
- [[governance/RepositoryRules]]
- [[assets/thumbnails]]