#!/usr/bin/env python3
"""Sync 2026-02-13 content to Feishu Bitable"""

import os
import re
import sys
import time
import yaml
import requests
from pathlib import Path
from datetime import datetime, timezone

FEISHU_BASE = "https://open.feishu.cn/open-apis"

# Config
APP_ID = None
APP_SECRET = None
BITABLE_APP_TOKEN = None
TABLE_ID = None

access_token = None
token_expires_at = 0


def load_config():
    global APP_ID, APP_SECRET, BITABLE_APP_TOKEN, TABLE_ID
    config_path = Path(__file__).parent / ".claude" / "skills" / "content-curator" / "config" / "sources.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    feishu = config["api_keys"]["feishu"]
    APP_ID = feishu["app_id"]
    APP_SECRET = feishu["app_secret"]
    BITABLE_APP_TOKEN = feishu["bitable_app_token"]
    TABLE_ID = feishu["table_id"]


def get_access_token():
    global access_token, token_expires_at
    if time.time() < token_expires_at:
        return access_token
    resp = requests.post(f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
                         json={"app_id": APP_ID, "app_secret": APP_SECRET}, timeout=10)
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Auth failed: {data.get('msg')}")
    access_token = data["tenant_access_token"]
    token_expires_at = time.time() + data["expire"] - 60
    print(f"  [OK] Got access token")
    return access_token


def upload_image(image_path):
    """Upload image to Feishu, return file_token"""
    url = f"{FEISHU_BASE}/drive/v1/medias/upload_all"
    ext = image_path.suffix.lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    mime = mime_map.get(ext, "image/jpeg")
    size = image_path.stat().st_size
    with open(image_path, "rb") as f:
        resp = requests.post(url, files={"file": (image_path.name, f, mime)},
                             data={"file_name": image_path.name, "parent_type": "bitable_image",
                                   "parent_node": BITABLE_APP_TOKEN, "size": str(size)},
                             headers={"Authorization": f"Bearer {get_access_token()}"}, timeout=30)
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Upload failed: {result.get('msg')}")
    return result["data"]["file_token"]


def add_record(fields):
    """Add a record to Bitable"""
    url = f"{FEISHU_BASE}/bitable/v1/apps/{BITABLE_APP_TOKEN}/tables/{TABLE_ID}/records"
    resp = requests.post(url, json={"fields": fields},
                         headers={"Authorization": f"Bearer {get_access_token()}",
                                  "Content-Type": "application/json"}, timeout=30)
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Add record failed: {result.get('msg')}")
    return result["data"]["record"]["record_id"]


def extract_quotes(text):
    """Extract quotes from rewritten.md (lines starting with number. under 金句 section)"""
    quotes = []
    in_quotes = False
    for line in text.split("\n"):
        if "金句" in line:
            in_quotes = True
            continue
        if in_quotes:
            m = re.match(r"^\d+\.\s*(.+)", line.strip())
            if m:
                quotes.append(m.group(1))
            elif line.strip().startswith("##") or line.strip().startswith("---"):
                in_quotes = False
    return quotes[:5]


def extract_guests(text):
    """Extract guest names with roles from rewritten.md (嘉宾信息 section)
    e.g. **Will Brown** - Prime Intellect联合创始人 -> Will Brown (Prime Intellect联合创始人)
    """
    guests = []
    in_guests = False
    for line in text.split("\n"):
        if "嘉宾信息" in line or ("嘉宾" in line and line.strip().startswith("##")):
            in_guests = True
            continue
        if in_guests:
            m = re.match(r"^\*\*(.+?)\*\*\s*[-–—]\s*(.+)", line.strip())
            if m:
                name = m.group(1).strip()
                role = m.group(2).strip().rstrip("。.")
                guests.append(f"{name} ({role})")
            elif line.strip().startswith("##") or line.strip().startswith("---"):
                in_guests = False
    return guests


def extract_chinese_title(text):
    """Extract Chinese title from first H1 in rewritten.md"""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            return line[2:].strip()
    return None


def date_to_ms(date_str):
    """Convert YYYY-MM-DD to millisecond timestamp for Feishu date field"""
    dt = datetime.strptime(str(date_str), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def parse_metadata(folder):
    """Parse metadata.md YAML frontmatter"""
    md_file = folder / "metadata.md"
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1])
    return {}


def find_cover(folder):
    """Find cover image in folder"""
    for ext in ["jpg", "jpeg", "png", "webp"]:
        p = folder / f"cover.{ext}"
        if p.exists():
            return p
    return None


def sync_folder(folder):
    """Sync a single content folder to Feishu"""
    print(f"\nProcessing: {folder.name}")

    metadata = parse_metadata(folder)
    if not metadata:
        print("  [SKIP] No metadata found")
        return None

    # Read rewritten content
    rewritten_file = folder / "rewritten.md"
    rewritten = ""
    quotes = []
    guests = []
    chinese_title = None
    if rewritten_file.exists():
        with open(rewritten_file, "r", encoding="utf-8") as f:
            rewritten = f.read()
        quotes = extract_quotes(rewritten)
        guests = extract_guests(rewritten)
        chinese_title = extract_chinese_title(rewritten)

    # Pad quotes to 5
    while len(quotes) < 5:
        quotes.append("")

    # Upload cover
    cover_field = []
    cover_path = find_cover(folder)
    if cover_path:
        try:
            token = upload_image(cover_path)
            cover_field = [{"file_token": token, "name": cover_path.name}]
            print(f"  [OK] Cover uploaded: {cover_path.name}")
        except Exception as e:
            print(f"  [WARN] Cover upload failed: {e}")

    # Build fields - prefer Chinese title from rewritten.md
    title = chinese_title or metadata.get("title", "")
    fields = {
        "标题": title,
        "平台来源": metadata.get("platform", "").upper(),
        "原内容链接": {"link": metadata.get("url", ""), "text": title},
        "封面图": cover_field,
        "标签": metadata.get("tags", []),
        "嘉宾": ", ".join(guests) if guests else metadata.get("channel", ""),
    }

    # Add published_at as date field
    pub_date = metadata.get("published_at")
    if pub_date:
        fields["发布时间"] = date_to_ms(pub_date)

    # Add quotes
    for i in range(5):
        fields[f"金句{i+1}"] = quotes[i][:200] if quotes[i] else ""

    # Add summary
    if rewritten:
        fields["摘要正文"] = rewritten[:5000]

    # Create record
    record_id = add_record(fields)
    print(f"  [OK] Record created: {record_id}")
    return record_id


def main():
    load_config()
    print("Feishu Bitable Sync - 2026-02-13")
    print("=" * 50)

    get_access_token()

    base = Path(__file__).parent / "content-archive" / "2026-02-13"
    if not base.exists():
        print(f"Directory not found: {base}")
        sys.exit(1)

    folders = sorted([f for f in base.iterdir() if f.is_dir()])
    print(f"Found {len(folders)} content folders")

    synced = 0
    failed = 0
    results = []

    for folder in folders:
        try:
            record_id = sync_folder(folder)
            if record_id:
                synced += 1
                results.append((folder.name, record_id, "OK"))
            else:
                results.append((folder.name, None, "SKIPPED"))
        except Exception as e:
            failed += 1
            results.append((folder.name, None, f"FAILED: {e}"))
            print(f"  [ERROR] {e}")

    print("\n" + "=" * 50)
    print(f"Done! Synced: {synced}, Failed: {failed}")
    for name, rid, status in results:
        print(f"  {name} -> {status}" + (f" ({rid})" if rid else ""))


if __name__ == "__main__":
    main()
