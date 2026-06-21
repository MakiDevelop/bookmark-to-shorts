"""Minimal multi-model router — 15 分鐘跑通版。

Usage:
    python router.py "幫我寫一個 Python decorator"
    python router.py "最近 AI agent 有什麼新趨勢"
    python router.py "這段 code 有沒有 bug" --context file.py
    echo "翻譯成英文：今天天氣很好" | python router.py -
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time

# ── 路由規則 ──────────────────────────────────────────────

RULES: list[tuple[str, list[str], str]] = [
    # (model_key, keywords, description)
    ("local",   ["翻譯", "摘要", "格式化", "列出", "整理", "簡單", "分類"],
                "日常瑣事 → 本地模型"),
    ("codex",   ["寫 code", "寫程式", "寫一個", "refactor", "重構", "debug", "修 bug",
                 "bug", "測試", "code review", "review", "code", "function",
                 "decorator", "api", "endpoint"],
                "寫 code / review → Codex"),
    ("gemini",  ["分析", "比較", "整個 repo", "大量", "讀完這份", "對比"],
                "分析比較 → Gemini"),
    ("scout",   ["最近", "趨勢", "新聞", "現在", "即時", "2026", "今天"],
                "時效性 → Scout"),
    ("opus",    ["架構", "不可逆", "戰略", "決策", "migrate", "遷移", "治理",
                 "governance"],
                "架構決策 → Opus"),
]

DEFAULT_ROUTE = "local"

# ── 模型指令 ──────────────────────────────────────────────

MODELS = {
    "local": {
        "cmd": ["ollama", "run", "qwen3.6"],
        "stdin": True,
        "label": "Qwen 3.6 (local)",
        "cost": "$0",
    },
    "codex": {
        "cmd": ["codex", "exec", "--sandbox", "workspace-write",
                "--skip-git-repo-check"],
        "stdin": False,  # prompt as positional arg
        "label": "Codex",
        "cost": "~$0.003",
    },
    "gemini": {
        "cmd": ["gemini", "-p"],
        "stdin": False,
        "label": "Gemini",
        "cost": "~$0.005",
    },
    "scout": {
        "cmd": ["gemini", "-p"],  # fallback; swap to perplexity if available
        "stdin": False,
        "label": "Scout (Gemini fallback)",
        "cost": "~$0.005",
    },
    "opus": {
        "cmd": ["claude", "-p", "--model", "claude-opus-4-6"],
        "stdin": False,
        "label": "Claude Opus",
        "cost": "~$0.05",
    },
}

FALLBACK_CHAIN = {
    "codex":  ["gemini", "opus"],
    "gemini": ["opus", "local"],
    "scout":  ["gemini", "local"],
    "opus":   ["gemini"],
    "local":  ["gemini"],
}

# ── 路由邏輯 ──────────────────────────────────────────────

def classify(task: str) -> tuple[str, str]:
    task_lower = task.lower()
    for model_key, keywords, desc in RULES:
        if any(kw in task_lower for kw in keywords):
            return model_key, desc
    return DEFAULT_ROUTE, "未匹配規則 → 預設本地模型"


def is_available(model_key: str) -> bool:
    cmd = MODELS[model_key]["cmd"][0]
    return shutil.which(cmd) is not None


def resolve(model_key: str) -> str:
    if is_available(model_key):
        return model_key
    for fallback in FALLBACK_CHAIN.get(model_key, []):
        if is_available(fallback):
            print(f"  ⚠ {MODELS[model_key]['label']} 不可用，fallback → {MODELS[fallback]['label']}",
                  file=sys.stderr)
            return fallback
    return DEFAULT_ROUTE


def call_model(model_key: str, prompt: str) -> tuple[str, float]:
    cfg = MODELS[model_key]
    if cfg["stdin"]:
        cmd = cfg["cmd"]
        input_text = prompt
    else:
        cmd = cfg["cmd"] + [prompt]
        input_text = None

    start = time.monotonic()
    result = subprocess.run(
        cmd, capture_output=True, text=True,
        timeout=120, input=input_text,
    )
    elapsed = time.monotonic() - start

    if result.returncode != 0:
        raise RuntimeError(f"{cfg['label']} failed: {result.stderr[:200]}")
    return result.stdout.strip(), elapsed

# ── Main ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Multi-model task router")
    parser.add_argument("task", help="Task description (use '-' to read from stdin)")
    parser.add_argument("--context", help="File to include as context")
    parser.add_argument("--dry-run", action="store_true", help="Show routing without executing")
    args = parser.parse_args()

    task = sys.stdin.read().strip() if args.task == "-" else args.task
    if args.context:
        with open(args.context) as f:
            task = f"{task}\n\n--- context ---\n{f.read()}"

    # Step 1: Classify
    model_key, reason = classify(task)
    print(f"[router] {reason}", file=sys.stderr)

    # Step 2: Resolve (check availability + fallback)
    resolved = resolve(model_key)
    cfg = MODELS[resolved]
    print(f"[router] → {cfg['label']} (est. {cfg['cost']}/req)", file=sys.stderr)

    if args.dry_run:
        print(f"[dry-run] Would call: {' '.join(cfg['cmd'][:3])}...", file=sys.stderr)
        return

    # Step 3: Call
    try:
        output, elapsed = call_model(resolved, task)
        print(output)
        print(f"\n[router] {elapsed:.1f}s | {cfg['label']} | {cfg['cost']}",
              file=sys.stderr)
    except Exception as e:
        print(f"[router] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
