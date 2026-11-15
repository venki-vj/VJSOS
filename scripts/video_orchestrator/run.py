#!/usr/bin/env python3
"""video_orchestrator — Execute a shot list JSON produced by the video_production skill.

Given a shot list (from the skill output), renders each shot locally using
Remotion (npx remotion render) or ffmpeg (filtergraph), concatenates the
segments, and encodes the final master + delivery files.

Usage:
  python scripts/video_orchestrator/run.py <shot_list.json> [--remotion-cwd DIR] [--out DIR]

Design follows VJSOS-AI:
- The LLM *directs* (outputs JSON shot instructions) — never renders bytes.
- Local tools *execute* (Remotion, ffmpeg) — deterministic, no API/proxy/combo risk.
- Every shot → one local render command; the orchestrator only shells out.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Unicode glyphs (🎬/⚠/✅) crash on Windows cp1252 consoles unless stdout is UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:  # Python < 3.7
    pass

# ─── Config ──────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUT = REPO_ROOT / "output" / "video"
CONCAT_LIST_FILE = DEFAULT_OUT / "concat.txt"
FINAL_RES = (3840, 2160)  # 4K master (per VIDEO_PRODUCTION_PACKAGE.md)


# ─── Shot dispatcher: each type → one local render command ───────────
def _clip_path(shot: Dict[str, Any], clips_dir: Path) -> Path:
    return clips_dir / f"{shot['id']}.mp4"


def _render_remotion(shot: Dict[str, Any], clips_dir: Path, remotion_cwd: Path) -> Path:
    """Render a Remotion composition to an mp4 clip."""
    out = _clip_path(shot, clips_dir)
    props_json = json.dumps(shot.get("props", {}))
    cmd = [
        "npx", "remotion", "render",
        shot.get("composition", "Main"),
        "--props", props_json,
        str(out),
    ]
    _run_shell(cmd, cwd=remotion_cwd, description=f"Remotion {shot['id']}")
    return out


def _render_ffmpeg(shot: Dict[str, Any], clips_dir: Path, remotion_cwd: Optional[Path]) -> Path:
    """Build an ffmpeg clip. Screen-capture shots use a testsrc lavfi source."""
    out = _clip_path(shot, clips_dir)
    cmd = ["ffmpeg", "-y"]
    if shot.get("source"):
        cmd += ["-i", str(Path(shot["source"]))]
    elif shot.get("type") == "screen_capture":
        res = shot.get("resolution", "1920x1080")
        cmd += ["-f", "lavfi", "-i", f"testsrc=size={res}:rate=30"]
    filt = shot.get("ffmpeg_filter", "")
    if filt:
        cmd += ["-vf", filt]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(out)]
    _run_shell(cmd, description=f"ffmpeg {shot['id']}")
    return out


def _render_static(shot: Dict[str, Any], clips_dir: Path, _: Optional[Path]) -> Path:
    """Static frames become a zoom/pan-free hold clip via ffmpeg."""
    return _render_ffmpeg({**shot, "source": None, "type": "ffmpeg"}, clips_dir, None)


RENDERERS = {
    "remotion": _render_remotion,
    "static": _render_static,
    "screen_capture": _render_ffmpeg,
    "talking_head": _render_ffmpeg,
    "ffmpeg": _render_ffmpeg,
}


# ─── Core orchestration ──────────────────────────────────────────────
def build_bundle(shot_list: Dict[str, Any]) -> None:
    """Validate the shot list against the skill output contract."""
    meta = shot_list.get("metadata", {})
    shots = shot_list.get("shots")
    if not shots:
        raise ValueError("shot_list.shots is empty")
    target = _parse_duration(meta.get("total_duration", "0"))
    total = sum(float(s.get("duration", 0)) for s in shots)
    if target and (total > target * 1.02 or total < target * 0.98):
        print(f"⚠  Total {total:.1f}s is off target ({meta.get('total_duration')}) — check shots.")


def render_shots(shot_list: Dict[str, Any], remotion_cwd: Optional[Path], out: Path) -> List[Path]:
    """Render every shot to a clip file. Returns ordered clip paths."""
    clips_dir = out / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    clips: List[Path] = []
    for shot in shot_list["shots"]:
        renderer = RENDERERS.get(shot.get("type", "ffmpeg"))
        if renderer is None:
            raise ValueError(f"Unknown shot type: {shot.get('type')}")
        clips.append(renderer(shot, clips_dir, remotion_cwd))
    return clips


def concat_clips(clips: List[Path], out_file: Path) -> Path:
    """Normalize each clip to the master profile, then concat deterministically."""
    tmp_dir = out_file.parent / "normalized"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    norm_clips: List[Path] = []
    for i, c in enumerate(clips):
        n = tmp_dir / f"{i:03d}_{c.stem}.mp4"
        vf = (f"scale={FINAL_RES[0]}:{FINAL_RES[1]}:force_original_aspect_ratio=decrease,"
              f"pad={FINAL_RES[0]}:{FINAL_RES[1]}:(ow-iw)/2:(oh-ih)/2,setsar=1")
        _run_shell(["ffmpeg", "-y", "-i", str(c), "-vf", vf, "-r", "30",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-an", str(n)],
                   description=f"Normalize {c.name}")
        norm_clips.append(n)

    with open(CONCAT_LIST_FILE, "w", encoding="utf-8") as f:
        for n in norm_clips:
            f.write(f"file '{n.resolve()}'\n")

    _run_shell(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(CONCAT_LIST_FILE),
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", str(out_file)],
               description="Concat segments")
    return out_file


def encode_delivery(master: Path, out: Path) -> None:
    """Produce platform delivery profiles (match EDITOR_QUICK_REFERENCE.md exports)."""
    profiles = {
        "youtube": ["-b:v", "20M", "-vf", "setsar=1"],
        "linkedin": ["-b:v", "10M", "-vf", "setsar=1"],
        "twitter": ["-b:v", "8M", "-vf", "scale=1280:720,setsar=1"],
    }
    for name, extra in profiles.items():
        dest = out / f"{name}.mp4"
        _run_shell(["ffmpeg", "-y", "-i", str(master), "-c:v", "libx264", "-preset", "medium",
                    *extra, "-c:a", "aac", "-b:a", "128k", "-ar", "48000", str(dest)],
                   description=f"Encode {name}")
        print(f"   {dest}")


# ─── Utilities ───────────────────────────────────────────────────────
def _parse_duration(s: str) -> float:
    """" Parse '90s', '2:30', '13:30' -> seconds. MM:SS or HH:MM:SS. """
    s = (s or "").strip()
    if not s:
        return 0.0
    if ":" in s:
        parts = [float(x) for x in s.split(":")]
        if len(parts) == 2:
            return parts[-1] + parts[-2] * 60
        return parts[-1] + parts[-2] * 60 + parts[-3] * 3600
    if s.lower().endswith("s"):
        return float(s[:-1])
    return float(s or 0)


def _run_shell(cmd: List[str], cwd: Optional[Path] = None, description: str = "") -> None:
    """Shell out to a local CLI tool (Remotion / ffmpeg). Deterministic & local."""
    if description:
        print(f"\n🎬 {description}\n$ {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"{description or 'command'} failed:\n{res.stderr or res.stdout}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("shot_list", help="Path to shot_list.json (from video_production skill)")
    ap.add_argument("--remotion-cwd", default=None, help="Dir containing the Remotion project")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="Output directory")
    ap.add_argument("--render-only", action="store_true", help="Stop after rendering clips")
    args = ap.parse_args()

    shot_list = json.loads(Path(args.shot_list).read_text(encoding="utf-8"))
    build_bundle(shot_list)
    out = Path(args.out)

    clips = render_shots(shot_list, Path(args.remotion_cwd) if args.remotion_cwd else None, out)
    print(f"\n✅ Rendered {len(clips)} shots:")
    for c in clips:
        print(f"   - {c}")

    if args.render_only:
        return 0

    master = out / "master.mp4"
    concat_clips(clips, master)
    print(f"\n✅ Master: {master}")
    encode_delivery(master, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())