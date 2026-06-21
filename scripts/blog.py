"""Generate a blog draft from the same scenes.json used for the video."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SCENES_FILE = DATA_DIR / "scenes.json"
BOOKMARKS_FILE = DATA_DIR / "bookmarks.json"
BLOG_FILE = DATA_DIR / "blog-draft.md"

PROMPT_TEMPLATE = """\
你是 Maki，一個在 91APP 做 AI PoC 的工程師，同時經營技術部落格 blog.chibakuma.com。
你剛做了一支知識短影片，主題是「{title}」。

影片旁白：
{narrations}

素材來源書籤：
{bookmarks}

請根據以上內容，寫一篇搭配影片的部落格文章草稿（繁體中文 Markdown）。

要求：
- 標題要吸引人，但不要太誇張
- 開頭段：用影片同樣的 hook 帶入，但展開成更完整的論述
- 正文：比影片更深入，加入你自己的實務經驗觀點（可以假設合理的工程經驗）
- 引用書籤來源（附 URL）
- 結尾：呼應影片，加上「完整影片請看 YouTube」的 CTA
- 800-1200 字
- 語氣：工程師朋友聊天，不要太正式也不要太隨便
- 不要用 emoji

只輸出 Markdown 文章，不要其他說明。"""


def main():
    script = json.loads(SCENES_FILE.read_text())
    bookmarks = json.loads(BOOKMARKS_FILE.read_text())

    narrations = "\n".join(
        f"Scene {s['id']}: {s['narration']}" for s in script["scenes"]
    )
    bkmk_text = "\n".join(
        f"- [{b['title']}]({b['url']}): {b.get('core_insight', '')}"
        for b in bookmarks
    )

    prompt = PROMPT_TEMPLATE.format(
        title=script["title"],
        narrations=narrations,
        bookmarks=bkmk_text,
    )

    print("[blog] 呼叫 Claude CLI 生成部落格草稿...")
    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "text"],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI failed: {result.stderr}")

    BLOG_FILE.write_text(result.stdout.strip())
    print(f"[blog] 寫入 {BLOG_FILE}")
    print(f"[blog] 字數：{len(result.stdout.strip())} 字元")


if __name__ == "__main__":
    main()
