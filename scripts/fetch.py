"""Fetch top bookmarks from mk-brain and generate narration script via Claude CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
BOOKMARKS_FILE = DATA_DIR / "bookmarks.json"
SCENES_FILE = DATA_DIR / "scenes.json"

SYSTEM_PROMPT = """\
你是一個知識型短影片腳本寫手。你會收到幾篇高分書籤摘要，
請從中挑出最有趣的 1 個主題，寫成 4 段旁白（每段 10-15 秒），
適合做成 45-60 秒的知識短影片。

要求：
- 繁體中文、口語化、有節奏感
- 第 1 段：hook（一句話抓注意力）
- 第 2 段：問題或現象
- 第 3 段：核心洞察 / 解法
- 第 4 段：觀點收尾 + CTA
- 每段 30-50 字
- 同時為每段寫一行「畫面提示」（給 Remotion 用的視覺描述）

輸出嚴格 JSON，格式：
{
  "title": "影片標題（10 字內）",
  "topic_url": "選中的書籤 URL",
  "scenes": [
    {
      "id": 1,
      "narration": "旁白文字",
      "visual_hint": "畫面提示",
      "duration_estimate_sec": 12
    }
  ]
}
只輸出 JSON，不要其他文字。"""


def generate_script(bookmarks: list[dict]) -> dict:
    material = "\n\n".join(
        f"[{i+1}] {b['title']}\nURL: {b['url']}\n摘要: {b.get('summary', '')}\n洞察: {b.get('core_insight', '')}\nSignal: {b.get('signal_score', 0)}"
        for i, b in enumerate(bookmarks)
    )

    prompt = f"{SYSTEM_PROMPT}\n\n以下是本週高分書籤：\n\n{material}"
    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "text"],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI failed: {result.stderr}")

    raw = result.stdout.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)


def main():
    if not BOOKMARKS_FILE.exists():
        print(f"[fetch] 找不到 {BOOKMARKS_FILE}")
        print("[fetch] 請先在 Claude session 中執行 mk-brain 搜尋並存入 data/bookmarks.json")
        sys.exit(1)

    bookmarks = json.loads(BOOKMARKS_FILE.read_text())
    print(f"[fetch] 讀取 {len(bookmarks)} 筆書籤")

    print("[fetch] 呼叫 Claude CLI 生成腳本...")
    script = generate_script(bookmarks)
    print(f"[fetch] 主題：{script['title']}")

    SCENES_FILE.write_text(json.dumps(script, ensure_ascii=False, indent=2))
    print(f"[fetch] 寫入 {SCENES_FILE}")


if __name__ == "__main__":
    main()
