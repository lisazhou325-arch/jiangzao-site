# Content Curator - Output Structure

Each processed content item creates a directory with the following structure:

```
YYYY-MM-DD-{sanitized-title}/
├── metadata.md        # Metadata with YAML frontmatter
├── transcript.md      # Original transcript with timestamps
├── rewritten.md       # AI-rewritten summary
└── cover.{jpg|webp}  # Cover image
```

---

## metadata.md Template

```markdown
---
id: "abc123"
title: "改写后的标题"
original_title: "Original Title"
platform: "youtube|bilibili|xiaoyuzhou"
url: "https://..."
published_at: "2026-01-01"
processed_at: "2026-01-03T10:30:00Z"
duration: "1:23:45"
duration_seconds: 5025

# Platform-specific
channel: "Channel Name"           # YouTube
uploader: "UP主名称"               # Bilibili
podcast: "播客名称"                # Xiaoyuzhou
channel_id: "UCxxx"               # YouTube
uid: "12345678"                   # Bilibili
podcast_id: "xxx"                 # Xiaoyuzhou

# Engagement
views: 123456
likes: 5678
coins: 234                        # Bilibili only
favorites: 567                    # Bilibili only
comments: 234
shares: 89                        # Bilibili only

# Content
description: "Video/podcast description..."
tags:
  - Tag1
  - Tag2
  - Tag3

# Transcript info
transcript_language: "zh-Hans|en"
transcript_source: "manual|auto-generated|bibigpt"

# AI-extracted info
guests:
  - name: "Guest Name"
    title: "Guest Title"
    affiliation: "Organization"
    social:
      twitter: "@handle"
      website: "https://..."

quotes:
  - "Key quote 1..."
  - "Key quote 2..."
  - "Key quote 3..."

# Feishu sync
synced_to_feishu: true|false
feishu_record_id: "recxxx"
---

# 改写后的标题

[Preview of rewritten content...]
```

---

## transcript.md Template

```markdown
# 原始转录文本

**标题**: Original Title
**来源**: Platform - Creator Name
**发布时间**: 2026-01-01
**时长**: 1:23:45
**转录语言**: Chinese (auto-generated)
**转录来源**: yt-dlp / BibiGPT

---

## 完整转录

[00:00:00] Opening remarks...

[00:05:30] First main point...

[00:15:23] Second main point...

...

[01:23:30] Closing remarks...

---

**词数统计**: 22,913 words
**字符数**: 126,777 characters
```

---

## rewritten.md Template

```markdown
# 改写后的标题

> **原标题**: Original Title
> **来源**: Platform - Creator Name
> **发布时间**: 2026-01-01
> **时长**: 1:23:45
> **嘉宾**: Guest Name (Title, Organization)

---

## 核心观点总结

1. **观点一**: 简洁概括第一个核心观点...
2. **观点二**: 简洁概括第二个核心观点...
3. **观点三**: 简洁概括第三个核心观点...
4. **观点四**: 简洁概括第四个核心观点...

## 关键洞察展开

### 第一个主题

详细阐述第一个主题的内容，包括：
- 具体的例子
- 引用的数据或研究
- 嘉宾的独特见解

### 第二个主题

详细阐述第二个主题的内容...

### 第三个主题

详细阐述第三个主题的内容...

## 金句摘录

> "第一条金句..."

> "第二条金句..."

> "第三条金句..."

## 结论与启发

总结核心价值，提供可行的思考方向或行动建议...

---

**字数统计**: 2,543 words
**改写时间**: 2026-01-03 10:30:00
**改写模型**: Claude Sonnet 4.5
```

---

## Directory Naming Convention

**Format**: `YYYY-MM-DD-{sanitized-title}`

**Sanitization Rules**:
1. Convert to lowercase
2. Remove special characters (keep only letters, numbers, hyphens)
3. Replace spaces with hyphens
4. Truncate to 100 characters
5. If collision occurs, append `-1`, `-2`, etc.

**Examples**:
- `2026-01-01-agi-aliens-and-intelligence-joscha-bach`
- `2025-12-30-bilibili-alien-civilization`
- `2025-12-28-xiaoyuzhou-tech-optimism-debate`
