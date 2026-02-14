---
name: feishu-bitable-sync
description: Sync processed content from content-curator to Feishu Bitable. Scans output directories and uploads metadata, cover images, and summaries to a configured Feishu table.
license: MIT
---

# Feishu Bitable Sync Skill

## 🎯 Mission

将 content-curator 已处理的内容同步到飞书多维表格,支持批量同步和增量更新。

---

## 🔇 Silent Execution Protocol

**CRITICAL: This skill executes silently without confirmation**

- Triggered by: `/feishu-bitable-sync` or semantic triggers
- Behavior: **Fully automatic**, scans and syncs immediately
- Example: `/feishu-bitable-sync --sync-all`

**Execution Philosophy:**
- ✅ Zero interruption, automatic processing
- ✅ Scans all output directories automatically
- ✅ Skips already synced items (based on Feishu record ID in state.yaml)
- ✅ Handles errors gracefully with clear messages

---

## 📋 System Architecture

```
feishu-bitable-sync/
├── sync_feishu.py          # Main sync script
└── SKILL.md               # This file
```

**Dependencies:**
- Requires `content-curator` to be configured
- Uses shared config from `content-curator/config/sources.yaml`
- Updates shared state in `content-curator/config/state.yaml`

---

## 🚀 Quick Start

### Prerequisites

1. **content-curator must be configured first:**
   ```bash
   /content-curator --init
   ```

2. **Edit Feishu credentials** in `content-curator/config/sources.yaml`:
   ```yaml
   api_keys:
     feishu:
       app_id: "cli_xxx"
       app_secret: "xxx"
       bitable_app_token: "bascnxxx"  # From Bitable URL
       table_id: "tblxxx"              # From Bitable URL
   ```

3. **Ensure you have processed content** in output directory:
   ```
   content-curator/output/
   ├── YYYY-MM-DD/
   │   └── platform_source_id/
   │       ├── metadata.md
   │       ├── rewritten.md
   │       └── cover.jpg
   ```

---

## 🎯 Usage

### Sync All Unsynced Content

```bash
# Scan all output directories and sync to Feishu
/feishu-bitable-sync

# Explicitly sync all (same as above)
/feishu-bitable-sync --sync-all
```

### What Gets Synced

For each content folder, the skill uploads:

1. **Metadata** (from `metadata.md`):
   - Platform (YouTube, Bilibili, Xiaoyuzhou)
   - URL (as hyperlink)
   - Published date (as Feishu date field, millisecond timestamp)
   - Tags

2. **Content** (from `rewritten.md`):
   - Chinese title (from first `# 标题` line, fallback to metadata title)
   - AI-rewritten summary (first 5000 chars → 摘要正文)
   - Extracted quotes (金句1-5, each max 200 chars)
   - Guest names with roles (from `嘉宾信息` section, format: `Name (角色)`, fallback to channel name)

3. **Media**:
   - Cover image (uploaded to Feishu and linked)

---

## 📊 Feishu Bitable Table Structure

**Recommended table schema:**

| 字段名 | 字段类型 | 说明 |
|--------|----------|------|
| 标题 | 文本 | AI 改写后的标题 |
| 平台来源 | 单选 | YOUTUBE / BILIBILI / XIAOYUZHOU |
| 原内容链接 | 网址 | 原始视频/播客链接 |
| 发布时间 | 日期 | 内容的真实发布时间（毫秒时间戳） |
| 封面图 | 附件 | 封面图片 |
| 嘉宾 | 文本 | 嘉宾姓名（从 rewritten.md 嘉宾信息提取，或回退到频道名） |
| 标签 | 多选 | 内容标签 |
| 金句1-5 | 文本 | AI 提取的关键引用（每条最多200字） |
| 摘要正文 | 多行文本 | AI 改写的摘要内容（最多5000字）|
| 本地路径 | 文本 | 输出文件夹路径 |
| 处理时间 | 日期 | 内容处理时间 |

---

## 🔄 Workflow

### Phase 1: Initialization

1. **Load configuration:**
   - Read Feishu credentials from `content-curator/config/sources.yaml`
   - Validate API keys (app_id, app_secret, bitable_app_token, table_id)

2. **Load state:**
   - Read processing state from `content-curator/config/state.yaml`
   - Identify already synced items (have `feishu_record_id`)

3. **Scan output directory:**
   - Default: `content-curator/output/` (or configured path)
   - Support both structures:
     - New: `YYYY-MM-DD/platform_source_id/`
     - Old: `YYYY-MM-DD-title/`

**Error Handling:**
- Config files missing → EXIT with error message
- Invalid YAML → Show syntax error, EXIT
- Feishu credentials missing → EXIT with error message

---

### Phase 2: Content Discovery

**Actions:**

1. **Recursively scan output directories:**
   ```python
   for date_dir in output_path.iterdir():
       if date_dir.is_dir():
           if re.match(r'\d{4}-\d{2}-\d{2}$', date_dir.name):
               # New structure: scan subdirectories
               for content_folder in date_dir.iterdir():
                   process_folder(content_folder)
           else:
               # Old structure: direct content folder
               process_folder(date_dir)
   ```

2. **Validate content folder:**
   - Must have `metadata.md`
   - Should have `rewritten.md` (optional but recommended)
   - Should have cover image (`cover.jpg|webp|png`)

3. **Check if already synced:**
   - Look for `feishu_record_id` in metadata YAML frontmatter
   - If exists and `synced_to_feishu: true`, skip

**Output:**
```
Found 15 content folders:
  - 2026-01-01/youtube_abc123 (not synced)
  - 2026-01-02/bilibili_BV1xx (already synced, skip)
  - 2026-01-03/xiaoyuzhou_xyz (not synced)
  ...

Ready to sync: 8 items
```

---

### Phase 3: Feishu Authentication

**Get tenant access token:**

```python
class FeishuClient:
    def get_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

        response = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })

        data = response.json()
        self.access_token = data['tenant_access_token']
        self.token_expires_at = time.time() + data['expire'] - 60

        return self.access_token
```

**Error Handling:**
- Authentication failed → EXIT with error message
- Token expired → Auto-refresh
- Invalid credentials → EXIT with helpful message

---

### Phase 4: Content Upload

**For each unsynced content folder:**

#### Step 4.1: Read Metadata

```python
# Read metadata.md
with open(metadata_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse YAML frontmatter
if content.startswith('---'):
    parts = content.split('---', 2)
    metadata = yaml.safe_load(parts[1])
```

#### Step 4.2: Read Rewritten Content

```python
# Read rewritten.md
with open(rewritten_file, 'r', encoding='utf-8') as f:
    rewritten = f.read()

# Extract quotes (from 金句 section)
quotes = extract_quotes(rewritten)

# Extract guest names (from 嘉宾信息 section, e.g. **Name** - Title)
guests = extract_guests(rewritten)
```

#### Step 4.3: Upload Cover Image

```python
def upload_cover_image(self, image_path):
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"

    with open(image_path, 'rb') as f:
        files = {
            'file': (image_path.name, f, 'image/jpeg'),
            'file_name': (None, image_path.name),
            'parent_type': (None, 'bitable_image'),
            'parent_node': (None, self.bitable_app_token),
            'size': (None, str(image_path.stat().st_size))
        }

        response = requests.post(url, files=files, headers={
            'Authorization': f'Bearer {self.get_access_token()}'
        })

    return response.json()['data']['file_token']
```

**Error Handling:**
- Image not found → Use empty cover field, continue
- Upload failed → Retry once, then use empty cover field
- Invalid image → Log warning, continue

---

#### Step 4.4: Create Bitable Record

```python
def add_record(self, bitable_app_token, table_id, fields):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{bitable_app_token}/tables/{table_id}/records"

    response = requests.post(url, json={
        "fields": fields
    }, headers={
        'Authorization': f'Bearer {self.get_access_token()}',
        'Content-Type': 'application/json'
    })

    return response.json()['data']['record']['record_id']
```

**Fields mapping:**
```python
fields = {
    "标题": metadata['title'],
    "平台来源": metadata['platform'].upper(),
    "原内容链接": {"link": metadata['url'], "text": metadata['title']},
    "发布时间": date_to_ms(metadata['published_at']),  # 毫秒时间戳
    "封面图": [{"file_token": cover_token, "name": cover_name}] if cover_token else [],
    "嘉宾": ", ".join(guests) if guests else metadata.get('channel', ''),
    "标签": metadata.get('tags', []),
    "金句1": quotes[0][:200],  # 金句1-5 分别存储
    "金句2": quotes[1][:200],
    "金句3": quotes[2][:200],
    "金句4": quotes[3][:200],
    "金句5": quotes[4][:200],
    "摘要正文": rewritten[:5000],
}
```

**Error Handling:**
- Record creation failed → Log error, mark as failed, continue with next
- Field type mismatch → Log warning, skip problematic field, continue
- API rate limit → Wait and retry (max 3 attempts)

---

### Phase 5: State Update

**Update `content-curator/config/state.yaml`:**

```python
# Update state
platform = metadata['platform']
item_id = metadata['id']

state['processed'][platform][item_id]['synced_to_feishu'] = True
state['processed'][platform][item_id]['feishu_record_id'] = record_id

# Save state
with open(STATE_FILE, 'w', encoding='utf-8') as f:
    yaml.dump(state, f, allow_unicode=True, default_flow_style=False)
```

**Also update metadata.md frontmatter:**
```yaml
synced_to_feishu: true
feishu_record_id: "recxxx"
```

---

### Phase 6: Execution Report

**Output summary:**

```
✅ Feishu Sync Complete!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
   • Total folders scanned: 15
   • Already synced (skipped): 7
   • Newly synced: 8
   • Failed: 0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📹 Synced Items:

1. [YouTube] AGI, Aliens, and Intelligence | Joscha Bach
   ├─ Folder: 2026-01-01/youtube_abc123
   ├─ Feishu Record: recxxx
   └─ Status: ✅ Synced

2. [Bilibili] 为什么人类至今没有发现外星人?
   ├─ Folder: 2026-01-03/bilibili_BV1xx
   ├─ Feishu Record: recyyy
   └─ Status: ✅ Synced

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Next Steps:
   • View Feishu Bitable: [Link]
   • Re-run anytime to sync new content

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔄 Error Decision Tree

```
ERROR ENCOUNTERED
│
├─ Configuration Phase
│   ├─ Config files missing → EXIT (content-curator not initialized)
│   ├─ Feishu credentials missing → EXIT (need setup first)
│   └─ Invalid credentials → EXIT (authentication failed)
│
├─ Discovery Phase
│   ├─ No output directory → EXIT (nothing to sync)
│   ├─ No content folders → EXIT (nothing to sync)
│   └─ All already synced → Output "All up to date" → EXIT
│
├─ Authentication Phase
│   ├─ Token request failed → EXIT (cannot proceed)
│   └─ Invalid app_id/secret → EXIT (fix credentials)
│
├─ Upload Phase (per item)
│   ├─ Metadata missing → SKIP item → CONTINUE
│   ├─ Cover upload failed → Use empty cover → CONTINUE
│   ├─ Record creation failed → Log error → SKIP item → CONTINUE
│   └─ API rate limit → Wait 60s → Retry (max 3) → If failed → SKIP item
│
└─ State Update Phase
    └─ File write failed → Log warning → CONTINUE (will retry next run)
```

**Philosophy:**
- Individual item failures should NOT stop batch sync
- Log all errors clearly
- Mark failed items for manual review
- Always produce a comprehensive report

---

## 🛠️ Command Reference

### Basic Usage

```bash
# Sync all unsynced content
/feishu-bitable-sync

# Explicitly sync all (same as above)
/feishu-bitable-sync --sync-all
```

### Semantic Triggers

The skill also responds to natural language:
- "同步到飞书"
- "sync to feishu"
- "更新飞书多维表格"
- "upload to bitable"

---

## 📝 Integration with content-curator

This skill is designed to work seamlessly with `content-curator`:

1. **Shared configuration:**
   - Both skills read from `content-curator/config/sources.yaml`
   - Both update `content-curator/config/state.yaml`

2. **Automatic sync option:**
   - In `sources.yaml`, set `auto_sync_feishu: true`
   - `content-curator` will call this skill automatically after processing

3. **Manual sync option:**
   - Run `/feishu-bitable-sync` anytime to sync previously processed content
   - Useful for:
     - Initial bulk sync of old content
     - Retry failed syncs
     - Update Feishu after changing rewrite prompts

---

## 🐛 Troubleshooting

### Issue: "Feishu credentials not configured"

**Solution:**
1. Run `/content-curator --init` if not done
2. Edit `content-curator/config/sources.yaml`
3. Add Feishu credentials under `api_keys.feishu`

### Issue: "Authentication failed"

**Solution:**
1. Verify `app_id` and `app_secret` in config
2. Check app permissions in Feishu admin console
3. Ensure app has access to the Bitable

### Issue: "Record creation failed: Field not found"

**Solution:**
1. Verify Bitable table schema matches expected fields
2. Check field names (must be exact match, case-sensitive)
3. Ensure field types match (text, number, date, etc.)

### Issue: "All items already synced"

**Solution:**
- This is normal if you've already synced before
- To force re-sync, manually edit `metadata.md` frontmatter:
  ```yaml
  synced_to_feishu: false
  feishu_record_id: null
  ```

---

## 🔐 Security & Privacy

### API Key Storage
- **NEVER commit config files with real credentials to Git**
- Add to `.gitignore`:
  ```gitignore
  .claude/skills/*/config/sources.yaml
  ```

### Feishu Permissions
- App needs:
  - `bitable:app` (read/write Bitable)
  - `drive:drive` (upload images)

---

## 📈 Performance Considerations

### Processing Time Estimates
- **Per item**: ~5-10 seconds
  - Read files: 1s
  - Upload cover: 2-3s
  - Create record: 2-3s
  - Update state: 1s

- **Batch sync (50 items)**: ~5-8 minutes

### Rate Limits
- Feishu API: ~100 requests/minute
- This skill makes 2-3 requests per item:
  1. Get access token (cached)
  2. Upload cover image
  3. Create record

### Optimization
- Access token is cached (valid for ~2 hours)
- Failed items are skipped quickly
- Already synced items are skipped instantly

---

## 📄 License

MIT License - Feel free to customize and extend this skill for your own use.

---

**Ready to sync?** Run `/feishu-bitable-sync` to get started! 🚀
