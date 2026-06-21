# Claude Design Brief — 「7 個 AI 模型協作」技術文章排版

## 設計目標

把一篇 2,500 字的技術乾貨文章，排成一個可以獨立分享的漂亮網頁。
目標不是 blog template，是讓讀者覺得「這篇值得存起來」的視覺品質。

## 風格參考

- **Linear changelog**（https://linear.app/changelog）— 深色背景、大量留白、段落之間呼吸感強
- **Vercel blog**（https://vercel.com/blog）— 工程師氣質、code block 有質感、表格不無聊
- **Stripe docs**（https://docs.stripe.com）— 資訊密度高但不壓迫，配色精準

不要像：Medium / Notion 預設排版 / 任何看起來像「AI 生成的 SaaS landing page」的東西

## 配色

- 背景：深藍黑（不是純黑，帶一點藍底，像 #0B1222）
- 主文字：柔白（#E6EDF3）
- Accent：琥珀 / 暖橘（#E8773D）— 用在重點數字、標題裝飾、hover
- 輔助色：柔綠（#7EE787）— 用在正面數據（省了多少錢、成功路徑）
- 錯誤/警告：柔紅（#F85149）— 用在踩坑故事的「坑」標記
- 邊線/分隔：深灰（#21262D）

不要用藍紫漸層。不要用典型的 AI 配色。

## 排版結構

### 頂部 Hero

```
┌────────────────────────────────────────────┐
│                                            │
│  我怎麼用 7 個 AI 模型協作                  │
│  成本砍 70%                                │
│  ─── 完整路由設定公開 ───                   │
│                                            │
│  Maki · blog.chibakuma.com · 2026.06       │
│  搭配影片「AI 不比模型比架構」               │
│                                            │
└────────────────────────────────────────────┘
```

- 標題用大字重磅字體，「70%」用 accent 色
- 副標小一號，低對比
- 作者行用 monospace

### Section 1：為什麼不是一個模型打天下

三個痛點並排卡片：

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ 成本失控  │  │ 延遲不均  │  │ 單點故障  │
│          │  │          │  │          │
│ 用賓士    │  │ 簡單任務  │  │ API 掛了  │
│ 載垃圾    │  │ 等 3-5 秒 │  │ 就全掛    │
└──────────┘  └──────────┘  └──────────┘
```

### Section 2：七位一體模型分工表

設計感表格（不是 HTML default table）：

```
角色            模型                 為什麼是它
─────────────────────────────────────────────────────
Architect       Claude Opus          推理天花板，不可逆決策
Engineer        Codex                sandbox 可跑測試驗證
Analyst         Gemini               100 萬 token context
Local Brain     Qwen 3.6 35B         零 API 費，批次/隱私
Writer          Gemma4 31B           中文寫作品質高
Scout-1         Perplexity Max       即時搜尋 + 自動引用
Scout-2         SuperGrok            X / 社群即時情報
```

- 角色欄用 accent 色
- 模型名用 monospace
- 每行之間有微妙的分隔線

### Section 3：路由決策樹

用 terminal / code block 風格呈現，有仿終端機的標題列（三個圓點）：

```
┌─ ● ● ● ── routing-decision-tree ─────────┐
│                                            │
│  收到任務                                   │
│  ├─ 單檔 ≤3 行？ → fast-path              │
│  ├─ 時效性？ → Scout-1 / Scout-2          │
│  ├─ 不認識的詞？ → 先查知識庫              │
│  ├─ 寫 code？ → Codex                     │
│  ├─ 分析比較？ → Gemini                   │
│  ├─ 簡單/隱私/批次？ → Qwen 本地           │
│  └─ 架構/不可逆？ → Claude Opus            │
│                                            │
└────────────────────────────────────────────┘
```

### Section 4：四個預設模式

小型橫排卡片，從左到右遞增複雜度：

```
fast-path → solo+review → council-lite → full-council
 Claude      Claude+Codex   +1 analyst     全員投票
```

用漸變色帶表示升級（從綠到橘到紅）

### Section 5：CLI 指令

5 個 code block，每個有模型名稱標籤，有 copy 按鈕感：

```bash
# Codex
codex exec --sandbox workspace-write < briefing.md > answer.md

# Gemini
gemini -p "Execute the briefing on stdin." < briefing.md > answer.md
```

### Section 6：成本結構

視覺化比較：

```
┌─────────────────────────────────────────┐
│  $12/週                    $40/週        │
│  ████████░░░░░░░░░░░░  vs  █████████████ │
│  七模型路由               全用 Opus      │
│  ↓ 70% ↓                               │
└─────────────────────────────────────────┘
```

下面附細項表（任務分佈 / 模型 / 週成本）

### Section 7：踩過的坑

四張卡片，每張有兩個區塊：

```
┌────────────────────────────────┐
│ ✕ 坑 1：Payload 不相容         │  ← 紅色標記
│                                │
│ Ollama 換版本後 max_tokens     │
│ 變成 max_completion_tokens，   │
│ scoring pipeline 靜默失敗兩天   │
│                                │
│ ────────────────────────────── │
│                                │
│ ✓ 教訓                        │  ← 綠色標記
│ 模型更換必須與 bug 修復分開做   │
└────────────────────────────────┘
```

### Section 8：從兩層開始就好

三步驟，簡潔的步驟指引：

```
Step 1 → 分出「需要推理」和「不需要推理」
Step 2 → 不需要推理的換便宜模型
Step 3 → 觀察哪些做不好 → 那就是第三層
```

結尾金句大字：「架構是長出來的，不是設計出來的。但前提是你要開始。」

### 底部 CTA

```
┌────────────────────────────────────────────┐
│                                            │
│  📺 影片：AI 不比模型比架構（37 秒版）       │
│  📦 GitHub：bookmark-to-shorts             │
│  ✍️ 更多文章：blog.chibakuma.com            │
│                                            │
└────────────────────────────────────────────┘
```

## 完整文章內容

以下是要排進去的全部文字（一字不改，只做排版）：

---

大多數人用 AI 的方式是：打開 ChatGPT，什麼都丟進去。進階一點的人會挑模型——「這個任務用 Claude 比較好」「那個用 Gemini」。但很少人認真想過：能不能建一套系統，讓任務自動流向最適合的模型？

我花了半年時間，從「全部丟 GPT」演化成 7 個模型協作的架構。這篇文章把完整設定攤開來，包括路由邏輯、成本結構、踩過的坑。可以直接抄。

### 為什麼不是一個模型打天下

**成本失控。** 簡單的格式轉換、摘要、制式回覆佔了八成請求，全丟旗艦模型等於用賓士載垃圾。

**延遲不均。** 旗艦模型推理慢，簡單任務等 3-5 秒是不必要的。本地模型 200ms 就能回。

**單點故障。** API 掛了就全掛。多模型意味著 fallback 路徑。

### 七位一體：每個模型為什麼在這裡

不是為了湊數。每個模型進來都是因為有一個具體缺口：

- Architect — Claude Opus — 推理天花板，不可逆決策
- Engineer — Codex — sandbox 可跑測試驗證，code review cost/quality 甜蜜點
- Analyst — Gemini — 100 萬 token context，整個 repo 丟進去分析
- Local Brain — Qwen 3.6 35B (A3B) — 自家 DGX Spark 跑，批次/隱私/投票，零 API 費
- Writer — Gemma4 31B — 本地跑，中文寫作品質高，文章生成/改寫
- Scout-1 — Perplexity Max — 即時搜尋 + 自動帶引用
- Scout-2 — SuperGrok — X / 社群即時情報

#### 為什麼 Scout 要兩個？

Perplexity 擅長結構化 research（學術、技術文件、帶引用），SuperGrok 擅長即時社群（X 趨勢、輿論風向）。兩者搜的東西不重疊，不是冗餘。

#### 為什麼本地模型要兩個？

Qwen 3.6 是 MoE 架構（35B 參數但只啟動 3B），推理極快、記憶體佔用低，適合大量批次和投票。Gemma4 31B 是 dense 架構，寫作品質更好但推理較慢，只在需要中文寫作時才叫它。不是同時跑。

### 路由決策樹：什麼任務派給誰

收到任務
├─ 單檔、≤3 行、明確可逆？ → fast-path：Claude 直接做，不路由
├─ 有時效性需求？ → Scout-1 或 Scout-2（學術/技術 → Perplexity，社群/X → Grok）
├─ 碰到不認識的專有名詞？ → 先查個人知識庫（4200+ 書籤語意搜尋）
├─ 寫 code / refactor？ → Codex（有 sandbox，能跑測試驗證）
├─ 程式碼分析 / 多方案比較？ → Gemini（大 context 窗口吃整包）
├─ 簡單任務 / 隱私資料 / 批次處理 / Council 投票？ → Qwen 本地跑
└─ 架構設計 / 不可逆決策 / 最終裁判？ → Claude Opus

### 四個預設模式

- fast-path：單檔 ≤3 行、明確、可逆 → Claude 自己做
- solo+review：一般實作 → Claude 做 + Codex review
- council-lite：跨系統、中風險 → Claude + Codex + 1 analyst
- full-council：不可逆、治理、戰略 → 全員投票

90% 的時間在 fast-path 和 solo+review。full-council 是 escalation，不是常態。

### CLI 指令

```bash
# Codex — sandbox 內執行，可寫檔但隔離
codex exec --sandbox workspace-write --skip-git-repo-check < briefing.md > answer.md

# Gemini — pipe 模式
gemini -p "Execute the briefing on stdin." < briefing.md > answer.md

# Grok — 關掉 web search 避免干擾
grok -p "$(cat briefing.md)" --disable-web-search 2>/dev/null > answer.md

# Qwen（本地 DGX Spark）
ollama run qwen3.6 < briefing.md > answer.md

# Gemma4（本地 MBP 或 DGX）
ollama run gemma4:31b < briefing.md > answer.md
```

Briefing 檔格式固定四段：TASK / CONTEXT（貼真 code）/ CONSTRAINTS / VERIFY。

### 成本結構

- 60% 日常/批次/投票 → Qwen 本地 → $0/週
- 15% Code review → Codex → ~$2/週
- 10% 分析/比較 → Gemini → ~$2/週
- 10% Scout research → Perplexity/Grok → ~$3/週
- 5% 架構/裁判 → Claude Opus → ~$5/週
- 合計 ~$12/週（vs 全用 Opus ~$40/週，差距 3 倍）

### 踩過的坑

**坑 1：模型切換後 payload 不相容。** Ollama 換模型版本後，max_tokens 變成 max_completion_tokens、response_format 格式變了。結果 scoring pipeline 靜默失敗，跑了兩天才發現分數全是 0。教訓：模型更換必須與 bug 修復分開做。

**坑 2：本地模型 context 太長吃光記憶體。** DGX Spark 128GB unified memory。Ollama 對 ≥48GB 設備自動拉 context 到 256K，結果 swap thrashing，第一次 LLM call 卡了 28 分鐘。教訓：一定要手動設 num_ctx=8192。

**坑 3：把 code review 也交給最強模型。** 一開始覺得 review 需要最強的推理。後來發現 Codex 有 sandbox 可以真的跑程式驗證，Claude 反而只能看。教訓：最強 ≠ 最適合。

**坑 4：三家共識不等於正確答案。** Council 投票時，Codex / Gemini / Grok 三方都說「方案 A 好」。後來 Perplexity 帶著 GitHub issues 和 benchmark 數據說「方案 A 在你的硬體上會失敗」，結果是對的。教訓：一個帶完整 evidence 的反對意見，可以推翻三方共識。

### 從兩層開始就好

第一步：把你現在的任務分成「需要推理」和「不需要推理」兩堆。
第二步：不需要推理的，換一個便宜模型。光這步就能砍一半成本。
第三步：觀察哪些任務便宜模型做不好。那些就是你第三層的候選。

架構是長出來的，不是第一天設計出來的。但前提是你要開始分流。

---

搭配影片「AI 不比模型比架構」。影片 37 秒講完核心概念，這篇補完整設定細節。

## 注意事項

- 文章內容一字不改，只做視覺排版
- 不要加 emoji
- 響應式設計，手機要能讀
- 如果內容太長一頁放不下，可以分 section 做成 scroll 體驗
- 匯出 HTML（之後會部署到 Ghost blog）
