---
name: content-curator
description: Unified content curation workflow that fetches videos/podcasts from YouTube, Bilibili, and Xiaoyuzhou, extracts transcripts via yt-dlp and BibiGPT API, rewrites content with AI, and archives structured outputs locally. Supports batch mode (user selection) and URL mode (automatic processing).
license: MIT
---

# Content Curator Skill

## Mission

自动化内容策展工作流，从多个平台（YouTube、Bilibili、小宇宙）抓取最新内容，获取转录文本，用 AI 改写成结构化中文深度摘要，归档到本地。

---

## Silent Execution Protocol

**CRITICAL: This skill follows different execution modes based on trigger type:**

### URL Mode (Silent - No Confirmation)
- Triggered by: Direct URL(s) provided
- Behavior: **Fully automatic**, process immediately without asking
- Example: `/content-curator https://youtube.com/watch?v=xxx`

### Batch Mode (Interactive - Requires Confirmation)
- Triggered by: No URL provided, or `--batch` flag
- Behavior: Scan all sources, list new content, **wait for user selection**
- Example: `/content-curator --batch`

**Execution Philosophy:**
- URL mode = Zero interruption, automatic processing
- Batch mode = Show list, wait for user to select items
- Always handle errors gracefully with clear messages
- Deduplicate automatically based on `state.yaml`

---

## System Architecture

```
content-curator/
├── config/
│   ├── sources.yaml           # Subscription sources + API keys
│   ├── sources.yaml.template  # Configuration template
│   ├── state.yaml             # Processing state tracker
│   ├── state.yaml.template    # State template
│   └── rewrite-prompt.md      # AI rewrite template
├── scripts/
│   ├── fetch_bibigpt.py       # BibiGPT API client
│   ├── metadata_extractor.py  # Metadata extraction utilities
│   └── subtitle_downloader.py # YouTube subtitle downloader
├── curator.py                 # Main orchestration script
├── templates/
│   └── output_structure.md    # Output file structure template
└── SKILL.md                   # This file
```

**Output Directory Structure:**
```
content-archive/
└── YYYY-MM-DD/
    └── {platform}_{source}_{id}/
        ├── metadata.md        # Metadata YAML frontmatter
        ├── transcript.md      # Original transcript with timestamps
        ├── rewritten.md       # AI-rewritten summary
        └── cover.{jpg|webp}   # Cover image
```

---

## Quick Start

### First Time Setup

1. **Initialize configuration files:**
   ```bash
   /content-curator --init
   ```
   This creates:
   - `config/sources.yaml` (with template)
   - `config/state.yaml` (empty tracker)
   - `config/rewrite-prompt.md` (default template)

2. **Edit `config/sources.yaml`** and add your API keys:
   ```yaml
   api_keys:
     bibigpt: "your_bibigpt_api_key_here"

   sources:
     youtube:
       - name: "Lex Fridman Podcast"
         url: "https://www.youtube.com/@lexfridman"
         min_duration: 30
     bilibili:
       - name: "回形针PaperClip"
         uid: "258150656"
     xiaoyuzhou:
       - name: "忽左忽右"
         podcast_id: "6021f949a789fca4eff51969"
   ```

3. **Customize rewrite prompt** (optional):
   Edit `config/rewrite-prompt.md` to match your style

---

## Trigger Conditions

### URL Mode (Automatic)
```bash
# Single URL
/content-curator https://youtube.com/watch?v=xxx

# Multiple URLs
/content-curator https://youtube.com/watch?v=xxx https://bilibili.com/video/BVxxx

# Bilibili / Xiaoyuzhou
/content-curator https://www.bilibili.com/video/BV1xxx
/content-curator https://www.xiaoyuzhou.com/episode/xxx
```

### Batch Mode (Interactive)
```bash
# Scan all sources and show selection menu
/content-curator --batch

# Scan specific platform only
/content-curator --batch --platform youtube
/content-curator --batch --platform bilibili

# Limit number of items per source
/content-curator --batch --limit 5
```

### Semantic Triggers
- "抓取我的订阅源最新内容"
- "处理这个YouTube视频：https://..."
- "获取这个B站视频的字幕并改写"

---

## Configuration Files

### 1. `config/sources.yaml`

Complete template with all options:

```yaml
# API Keys and Credentials
api_keys:
  # BibiGPT API key (required for Bilibili and Xiaoyuzhou)
  bibigpt: "your_bibigpt_api_key_here"

# Content Sources
sources:
  youtube:
    - name: "Channel Name"
      url: "https://www.youtube.com/@channel"
      min_duration: 30  # minutes, default 30
      enabled: true

  bilibili:
    - name: "UP主名称"
      uid: "12345678"
      enabled: true

  xiaoyuzhou:
    - name: "播客名称"
      podcast_id: "podcast_id_here"
      enabled: true

# Processing Settings
settings:
  output_dir: "content-archive"  # Relative to project root
  scan_days: 30                  # How far back to scan
  max_items_per_source: 10       # Max items per source in batch mode
```

### 2. `config/state.yaml`

Tracks processing state and deduplication:

```yaml
processed:
  youtube:
    "video_id":
      title: "Video Title"
      processed_at: "2026-01-01T12:00:00"
      output_dir: "content-archive/2026-01-01/youtube_channel_id/"
  bilibili:
    "BVxxx":
      title: "视频标题"
      processed_at: "2026-01-01T12:00:00"
  xiaoyuzhou:
    "episode_id":
      title: "播客标题"
      processed_at: "2026-01-01T12:00:00"
```

### 3. `config/rewrite-prompt.md`

AI rewrite template. Customize to match your preferred output style.

---

## Execution Workflow

### Phase 1: Initialization & Environment Check

**Actions:**

1. **Check required tools:**
   ```bash
   # yt-dlp (required for YouTube)
   python -m yt_dlp --version  # or yt-dlp --version

   # Deno (recommended JS runtime for yt-dlp)
   deno --version

   # ffmpeg (for subtitle format conversion)
   ffmpeg -version
   ```
   - yt-dlp missing → EXIT with install command: `pip install yt-dlp`
   - Deno missing → Recommend `winget install DenoLand.Deno` (Windows) or `curl -fsSL https://deno.land/install.sh | sh`
   - ffmpeg missing → Recommend `winget install Gyan.FFmpeg` (Windows)
   - If both Node.js and Deno missing → Use `--extractor-args "youtube:player_client=android"` as fallback

2. **Load configuration:**
   ```python
   with open('config/sources.yaml', 'r', encoding='utf-8') as f:
       config = yaml.safe_load(f)
   with open('config/state.yaml', 'r', encoding='utf-8') as f:
       state = yaml.safe_load(f) or {'processed': {}}
   ```

3. **Validate API keys:**
   - Check if `bibigpt` key exists (required for Bilibili/Xiaoyuzhou)
   - Warn if missing but continue

4. **Load rewrite prompt** from `config/rewrite-prompt.md`

5. **Create output directory** if missing

**Error Handling:**
- Config files missing → Run `--init` automatically
- Invalid YAML → Show syntax error, EXIT
- API keys missing → Warn, continue (will fail later if needed)

---

### Phase 2: Content Discovery

#### Mode A: URL Mode (Direct Processing)

**Input:** One or more URLs provided

**Actions:**
1. Parse each URL to identify platform:
   ```python
   def identify_platform(url):
       if 'youtube.com' in url or 'youtu.be' in url:
           return 'youtube', extract_video_id(url)
       elif 'bilibili.com' in url:
           return 'bilibili', extract_bvid(url)
       elif 'xiaoyuzhou.co' in url:
           return 'xiaoyuzhou', extract_episode_id(url)
       else:
           raise ValueError(f"Unsupported platform: {url}")
   ```

2. Check deduplication against `state.yaml`
3. Add to processing queue

**Proceed to Phase 3 automatically (no user confirmation needed)**

---

#### Mode B: Batch Mode (Interactive Selection)

**Input:** No URL provided, or `--batch` flag

**Actions:**

1. **Scan all enabled sources**, filter out already processed items via `state.yaml`

2. **Display interactive selection menu:**
   ```
   Found 23 new items across all sources:

   YouTube (12 items):
   ☐ 1. [Lex Fridman] AGI, Aliens, and Intelligence | Joscha Bach (1:42:35)
        Published: 2026-01-01 | Views: 245K | Tags: AI, Science
   ☐ 2. [The Diary Of A CEO] The Poo Doctor: Gut Health Secrets (2:11:36)
        Published: 2026-01-01 | Views: 405K | Tags: Health
   ...

   Bilibili (8 items):
   ☐ 13. [回形针] 为什么人类至今没有发现外星人？(15:23)
         Published: 2025-12-30 | Views: 1.2M | Tags: Science
   ...

   Xiaoyuzhou (3 items):
   ☐ 21. [忽左忽右] EP.123 科技乐观主义的终结？(52:14)
         Published: 2025-12-28 | Tags: Society, Tech
   ...

   Commands:
   - Enter numbers (e.g., "1,2,13") to select items
   - Enter "all" to select all
   - Enter "youtube" / "bilibili" / "xiaoyuzhou" to select platform
   - Enter "q" to quit

   Your selection:
   ```

3. **Wait for user input**, parse selection, add to processing queue

4. **Confirm before processing:**
   ```
   Selected 3 items:
     1. [YouTube] AGI, Aliens, and Intelligence | Joscha Bach
     2. [YouTube] The Poo Doctor: Gut Health Secrets
     3. [Bilibili] 为什么人类至今没有发现外星人？

   Proceed with processing? [Y/n]:
   ```

**Proceed to Phase 3 only after user confirms**

---

### Phase 3: Content Fetching

**For each item in processing queue:**

#### Step 3.1: Get Transcript

**Platform: YouTube — 4-Layer Subtitle Fallback Strategy**

Use yt-dlp to download subtitles with the following priority:

```bash
# Strategy 1: Manual Chinese subtitles
python -m yt_dlp --write-sub --sub-lang zh-Hans,zh-Hant,zh --skip-download -o "temp_%(id)s" <video_url> \
  --extractor-args "youtube:player_client=android" --remote-components ejs:github

# Strategy 2: Manual English subtitles
python -m yt_dlp --write-sub --sub-lang en --skip-download -o "temp_%(id)s" <video_url> \
  --extractor-args "youtube:player_client=android" --remote-components ejs:github

# Strategy 3: Auto-generated Chinese
python -m yt_dlp --write-auto-sub --sub-lang zh-Hans,zh-Hant --skip-download -o "temp_%(id)s" <video_url> \
  --extractor-args "youtube:player_client=android" --remote-components ejs:github

# Strategy 4: Auto-generated English (last resort)
python -m yt_dlp --write-auto-sub --sub-lang en --skip-download -o "temp_%(id)s" <video_url> \
  --extractor-args "youtube:player_client=android" --remote-components ejs:github
```

**YouTube API Limitations Handling:**
- Use `player_client=android` to bypass some restrictions
- Use `--remote-components ejs:github` to enable JavaScript challenge solving
- HTTP 429 (Too Many Requests) → Wait and retry with exponential backoff (60s, 120s, 240s), max 3 attempts

**VTT Subtitle → Plain Text Conversion:**
```python
# 1. Remove VTT headers (WEBVTT, Kind, Language lines)
# 2. Remove timestamp lines (00:00:00.000 --> 00:00:05.000)
# 3. Remove HTML tags (<c>, </c>, etc.)
# 4. Deduplicate repeated lines (VTT format often duplicates across cues)
# 5. Strip empty lines and normalize whitespace
```

**Platform: Bilibili & Xiaoyuzhou — BibiGPT API**

```python
def fetch_bibigpt_transcript(url, api_key):
    response = requests.post("https://bibigpt.co/api/v1/transcript", json={
        "url": url,
        "language": "zh-Hans"
    }, headers={"Authorization": f"Bearer {api_key}"})
    return response.json()
```

#### Step 3.2: Extract Metadata

Use `scripts/metadata_extractor.py` to extract:
- Title, original title
- Platform, URL
- Published date
- Duration
- Channel/Uploader name
- View count, like count
- Tags
- Cover image URL

#### Step 3.3: Download Cover Image

```python
# Download cover/thumbnail
cover_url = metadata.get('thumbnail') or metadata.get('cover_url')
if cover_url:
    response = requests.get(cover_url)
    ext = 'jpg' if 'youtube' in platform else 'webp'
    with open(output_dir / f'cover.{ext}', 'wb') as f:
        f.write(response.content)
```

**Error Handling:**
- Transcript fetch failed → Log error, skip item, continue
- Metadata extraction failed → Use partial data, continue
- Cover download failed → Skip cover, continue

---

### Phase 4: AI Rewrite

**Actions:**
1. Load rewrite prompt from `config/rewrite-prompt.md`
2. Combine prompt + transcript text
3. Send to AI for rewriting

**Long Content Segmentation Strategy (from youtube-digest):**
- If transcript word count > 15,000 characters → Split into segments by ~10 minute intervals
- Process each segment independently with the rewrite prompt
- Merge all segments into final output
- Each segment includes context: "This is segment N/M of the full content"

**Rewrite Output Requirements:**
- Structured Chinese summary
- Key points extraction
- Guest information (if applicable)
- Notable quotes
- Conclusion and insights

**Error Handling:**
- AI API error → Retry once, then save raw transcript as fallback
- Token limit exceeded → Auto-segment and retry

---

### Phase 5: File Generation

**For each processed item, create output directory and files:**

```
content-archive/YYYY-MM-DD/{platform}_{source}_{id}/
├── metadata.md        # YAML frontmatter with all metadata
├── transcript.md      # Original transcript (cleaned)
├── rewritten.md       # AI-rewritten summary
└── cover.{jpg|webp}   # Cover image
```

**metadata.md format:**
```yaml
---
title: "AI 改写后的标题"
original_title: "Original Title"
platform: youtube
url: "https://..."
published_at: "2026-01-01"
duration: "1:42:35"
channel: "Channel Name"
views: 245678
likes: 12345
tags: [AI, Science]
guests:
  - name: "Guest Name"
    title: "Guest Title"
quotes:
  - "Notable quote 1"
  - "Notable quote 2"
processed_at: "2026-01-01T12:00:00"
---
```

---

### Phase 6: State Management

**After each item is processed:**

```python
# Update state.yaml
state['processed'].setdefault(platform, {})[item_id] = {
    'title': metadata['title'],
    'processed_at': datetime.utcnow().isoformat(),
    'output_dir': str(output_dir)
}

with open('config/state.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(state, f, allow_unicode=True, default_flow_style=False)
```

This ensures:
- Deduplication across runs
- Crash recovery (partially processed batches can resume)
- Audit trail of all processed content

---

### Phase 7: Execution Report

**Output summary after all items processed:**

```
Processing Complete!

Summary:
  - Processed: 3 items
  - Succeeded: 3
  - Failed: 0

Items Processed:

1. [YouTube] AGI, Aliens, and Intelligence | Joscha Bach
   ├─ Channel: Lex Fridman
   ├─ Duration: 1:42:35 | Views: 245K
   ├─ Transcript: English (auto-generated, 18,234 words)
   └─ Output: content-archive/2026-01-01/youtube_lexfridman_abc123/

2. [Bilibili] 为什么人类至今没有发现外星人？
   ├─ Uploader: 回形针PaperClip
   ├─ Duration: 15:23 | Views: 1.2M
   ├─ Transcript: Chinese (BibiGPT, 3,842 words)
   └─ Output: content-archive/2025-12-30/bilibili_paperclip_BVxxx/

Next Steps:
  - View outputs: ls content-archive/
  - Edit rewrite prompt: vim config/rewrite-prompt.md
  - Sync to Feishu: /feishu-bitable-sync
```

---

## Error Decision Tree

```
Error occurred
├── Config file missing?
│   └── Run --init → Retry
├── API key invalid?
│   └── Show error with config path → EXIT
├── Network error?
│   └── Retry 3x with backoff → Skip item → Continue
├── yt-dlp not installed?
│   └── Show install command → EXIT
├── Subtitle not available?
│   └── Try all 4 fallback strategies → Skip if all fail → Continue
├── BibiGPT API error?
│   └── Retry once → Skip item → Continue
├── AI rewrite failed?
│   └── Retry once → Save raw transcript → Continue
├── File write error?
│   └── Check permissions → Skip item → Continue
└── Unknown error?
    └── Log full traceback → Skip item → Continue
```

---

## Command Reference

```bash
# URL Mode - process specific URLs
/content-curator <url1> [url2] [url3]

# Batch Mode - scan sources and select
/content-curator --batch
/content-curator --batch --platform youtube
/content-curator --batch --platform bilibili
/content-curator --batch --limit 5

# Initialize config files
/content-curator --init

# Clear processing state
/content-curator --clear-state
/content-curator --clear-state --platform youtube

# Re-process a specific item (ignore dedup)
/content-curator --force <url>
```

---

## Troubleshooting

### Issue: "yt-dlp not installed"
**Solution**: `pip install yt-dlp`

### Issue: "BibiGPT API key invalid"
**Solution**:
1. Check API key in `config/sources.yaml`
2. Test at https://bibigpt.co/api
3. Ensure key has sufficient credits

### Issue: "No subtitles available" (YouTube)
**Solution**: All 4 fallback strategies failed. The video genuinely has no subtitles. Consider:
1. Using BibiGPT API as alternative for YouTube too
2. Skipping the video

### Issue: "Batch mode shows no new items"
**Solution**:
1. Check if sources are enabled in `sources.yaml`
2. Verify published dates are within scan range
3. Clear state if items were wrongly marked as processed:
   ```bash
   /content-curator --clear-state --platform youtube
   ```

### Issue: "Duplicate titles in output directory"
**Solution**: Titles are truncated to 100 chars and sanitized. If collision occurs, video ID suffix is added automatically.

---

## License

MIT License - Feel free to customize and extend this skill for your own use.
