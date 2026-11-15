#!/usr/bin/env python3
"""
VJSOS Gemma4 Episode Generator
==============================
Drives the locally-installed Ollama gemma4:26b model with the text-based
creative brief (assets have no vision — we feed detailed text descriptions)
to produce a storyboard JSON that feeds the video orchestrator pipeline.

Usage:
    python generate_episode.py [--episode 1] [--shots 6] [--model gemma4:26b]
"""
import argparse
import json
import os
import sys
import urllib.request

OLLAMA_API = os.environ.get("OLLAMA_API", "http://localhost:11434")
BRIEF_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "output", "assets", "creative_brief.md")


def read_brief():
    with open(BRIEF_PATH, "r", encoding="utf-8") as f:
        return f.read()


def call_model(prompt, model, system=None, temperature=0.8, num_predict=2048):
    """Call the Ollama chat API. Returns the model's text response."""
    payload = {
        "model": model,
        "messages": [],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": num_predict},
    }
    if system:
        payload["messages"].append({"role": "system", "content": system})
    payload["messages"].append({"role": "user", "content": prompt})

    req = urllib.request.Request(
        f"{OLLAMA_API}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("message", {}).get("content", "")


def extract_json(text):
    """Pull the first JSON object out of a model response that may contain prose."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError("No JSON object found in model response")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", type=int, default=1, help="Episode number")
    parser.add_argument("--shots", type=int, default=6, help="Number of shots to request")
    parser.add_argument("--model", default="gemma4:26b", help="Ollama model name")
    parser.add_argument("--out", default=None, help="Output shot list JSON path")
    args = parser.parse_args()

    brief = read_brief()
    print(f":: Reading creative brief ({len(brief)} chars)")

    system_prompt = (
        "You are the showrunner of 'ALEX & JACK: THE CURIOUS PARK', a 3D animated "
        "children's series. You are an expert storyboard artist and shot-lister. "
        "You ALWAYS respond with valid JSON only — no prose, no markdown fences."
    )

    user_prompt = f"""Here is the creative brief for our animated series:

{brief}

Now create Episode {args.episode}. Write a self-contained, delightful {args.shots}-shot
micro-episode where Alex and Jack discover something curious in Sunnydale Park.

RULES:
- Keep it kid-safe, warm, and gently educational.
- Vary the shots: use different "type" values across the shot list (see below).
- Each shot needs a vivid, production-ready visual prompt.
- Each shot should reference the actual visual identity (orange hoodie, round
  glasses, brown-and-white pup, orange slide, green park).

Respond with EXACTLY this JSON structure (no other keys):

{{
  "meta": {{
    "title": "Episode title",
    "logline": "One sentence",
    "duration": <total seconds as int>,
    "fps": 30,
    "resolution": "3840x2160",
    "aspect_ratio": "16:9",
    "style": "3D stylized Pixar-inspired",
    "episode": {args.episode}
  }},
  "shots": [
    {{
      "id": "shot_01_<slug>",
      "type": "remotion | static | screen_capture",
      "prompt": "<production-ready visual description referencing Alex/Jack/park>",
      "duration": <int seconds 2-8>,
      "output": "shot_01_<slug>.mp4"
    }}
  ]
}}"""

    print(f":: Asking {args.model} to write Episode {args.episode}...")
    raw = call_model(user_prompt, args.model, system=system_prompt, temperature=0.85, num_predict=4096)
    print(f":: Model responded ({len(raw)} chars)")

    try:
        shot_list = extract_json(raw)
    except ValueError as exc:
        print(f"!! Could not parse JSON from model. Dumping raw response:\n{raw[:2000]}", file=sys.stderr)
        sys.exit(1)

    # Normalize / validate
    total = 0
    for shot in shot_list.get("shots", []):
        shot.setdefault("fps", 30)
        total += shot.get("duration", 0)
    shot_list["meta"]["duration"] = total

    if args.out is None:
        args.out = os.path.join(
            os.path.dirname(__file__), "..", "..", "output", f"episode_{args.episode:02d}_shotlist.json"
        )
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(shot_list, f, indent=2, ensure_ascii=False)

    print(f":: Wrote {len(shot_list.get('shots', []))} shots ({total}s) to {args.out}")
    print(json.dumps(shot_list, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
