#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

QUERY="${1:-interesting AI tool automation side project}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "=== Bookmark-to-Shorts Pipeline ==="
echo "[1/5] Fetching bookmarks + generating script..."
uv run python scripts/fetch.py "$QUERY"

echo ""
echo "[2/5] Generating TTS audio..."
uv run python scripts/tts.py

echo ""
echo "[3/5] Copying audio to Remotion public dir..."
mkdir -p public
cp -f data/audio/scene-*.mp3 public/

echo ""
echo "[4/5] Rendering video..."
./node_modules/.bin/remotion render src/index.ts BkmkShort \
  --codec h264 \
  --output "data/out/short-${TIMESTAMP}.mp4"

echo ""
echo "[5/5] Generating blog draft..."
uv run python scripts/blog.py

OUTPUT="data/out/short-${TIMESTAMP}.mp4"
echo ""
echo "=== Done! ==="
echo "Video:  $OUTPUT"
echo "Duration: $(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT" 2>/dev/null)s"
echo "Blog:   data/blog-draft.md"
