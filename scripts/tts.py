"""Generate TTS audio for each scene using edge-tts."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import edge_tts

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SCENES_FILE = DATA_DIR / "scenes.json"
AUDIO_DIR = DATA_DIR / "audio"

VOICE = "zh-TW-YunJheNeural"
RATE = "+5%"


async def generate_audio(scene: dict, out_path: Path) -> float:
    communicate = edge_tts.Communicate(scene["narration"], VOICE, rate=RATE)
    await communicate.save(str(out_path))
    # get duration via ffprobe
    proc = await asyncio.create_subprocess_exec(
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(out_path),
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return float(stdout.decode().strip())


async def main():
    script = json.loads(SCENES_FILE.read_text())
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    enriched_scenes = []
    total_duration = 0.0

    for scene in script["scenes"]:
        sid = scene["id"]
        audio_path = AUDIO_DIR / f"scene-{sid}.mp3"
        print(f"[tts] Scene {sid}: {scene['narration'][:30]}...")
        duration = await generate_audio(scene, audio_path)
        total_duration += duration
        enriched_scenes.append({
            **scene,
            "audio_file": str(audio_path),
            "audio_duration_sec": round(duration, 2),
        })
        print(f"[tts] Scene {sid}: {duration:.1f}s → {audio_path.name}")

    script["scenes"] = enriched_scenes
    script["total_duration_sec"] = round(total_duration, 2)

    SCENES_FILE.write_text(json.dumps(script, ensure_ascii=False, indent=2))
    print(f"[tts] 總長 {total_duration:.1f}s，已更新 {SCENES_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
