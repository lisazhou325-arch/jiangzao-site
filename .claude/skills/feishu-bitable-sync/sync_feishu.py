#!/usr/bin/env python3
"""
Content Curator - Process content and sync to Feishu Bitable
"""

import sys
import os
import re
import yaml
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

# Add daily-content-curator scripts to path
base_dir = os.path.dirname(__file__)
curator_dir = os.path.join(base_dir, '..', 'content-curator')
sys.path.insert(0, os.path.join(curator_dir, 'scripts'))
from feishu_sync import FeishuClient
from metadata_extractor import extract_quotes_from_rewritten

CONFIG_FILE = os.path.join(curator_dir, 'config', 'sources.yaml')
STATE_FILE = os.path.join(curator_dir, 'config', 'state.yaml')

def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_state():
    if not os.path.exists(STATE_FILE):
        return {'processed': {'bilibili': {}, 'youtube': {}}, 'stats': {}}
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {'processed': {'bilibili': {}, 'youtube': {}}, 'stats': {}}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(state, f, allow_unicode=True, default_flow_style=False)

def _extract_chinese_title(rewritten: str) -> str:
    """从 rewritten.md 提取第一个 ## 标题作为中文标题"""
    match = re.search(r'^## (.+)$', rewritten, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ''


def _extract_guests(rewritten: str) -> str:
    """从创作说明提取嘉宾名，优先用 嘉宾: 字段，回退到选题方向里的人名"""
    # 优先：嘉宾：字段
    match = re.search(r'嘉宾[：:]\s*(.+)', rewritten)
    if match:
        return match.group(1).strip()

    # 回退：从选题方向提取人名
    match = re.search(r'选题方向[：:]\s*(.+)', rewritten)
    if not match:
        return ''
    direction = match.group(1).strip()
    segments = [s.strip() for s in direction.split('+')]
    names = []
    for seg in segments:
        en_name = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', seg)
        zh_name = re.search(r'[\u4e00-\u9fff]{1,3}·[\u4e00-\u9fff]{1,4}', seg)
        if en_name:
            names.append(en_name.group(1))
        elif zh_name:
            names.append(zh_name.group(0))
    return '、'.join(names) if names else ''


def _extract_body(rewritten: str) -> str:
    """去掉开头金句列表和创作说明，返回正文部分，最多5000字"""
    # 跳过开头的金句（1. "..." 格式）和创作说明（📝 ... --- 之间的内容）
    # 找到第一个 ## 标题作为正文起点
    match = re.search(r'\n(## .+)', rewritten)
    if match:
        body = rewritten[match.start():].strip()
    else:
        # 没有 ## 标题，跳过 --- 分隔线之后的内容
        parts = rewritten.split('---', 1)
        body = parts[-1].strip() if len(parts) > 1 else rewritten.strip()
    return body[:5000]


def sync_to_feishu(metadata, rewritten_summary, cover_path=None):
    """Sync content to Feishu Bitable"""
    config = load_config()
    feishu_config = config.get('api_keys', {}).get('feishu', {})

    if not feishu_config.get('app_id') or not feishu_config.get('app_secret'):
        print('   [SKIP] Feishu credentials not configured')
        return None

    client = FeishuClient(feishu_config['app_id'], feishu_config['app_secret'])

    # Prepare metadata for sync
    sync_data = {
        'title': metadata.get('title', ''),
        'original_title': metadata.get('title', ''),
        'platform': metadata.get('platform', ''),
        'url': metadata.get('url', ''),
        'published_at': metadata.get('published_at', ''),
        'processed_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'duration': metadata.get('duration', ''),
        'channel': metadata.get('channel', '') or metadata.get('uploader', ''),
        'guests_str': _extract_guests(rewritten_summary) if rewritten_summary else (metadata.get('guests_str', '') or metadata.get('channel', '') or metadata.get('source', '')),
        'views': metadata.get('views', 0),
        'likes': metadata.get('likes', 0),
        'tags': metadata.get('tags', []),
        'output_dir': metadata.get('output_dir', ''),
        'rewritten_summary': _extract_body(rewritten_summary) if rewritten_summary else '',
        'chinese_title': _extract_chinese_title(rewritten_summary) if rewritten_summary else '',
        'quotes': metadata.get('quotes', [])
    }
    
    record_id = client.sync_content(
        feishu_config['bitable_app_token'],
        feishu_config['table_id'],
        sync_data,
        Path(cover_path) if cover_path else None
    )
    
    return record_id

def sync_existing_outputs():
    """Sync all existing outputs to Feishu (supports new date-based structure)"""
    config = load_config()
    state = load_state()

    output_dir = config.get('settings', {}).get('output_dir', './content-archive')
    # Make path relative to curator_dir
    if not os.path.isabs(output_dir):
        base_dir = os.path.dirname(__file__)
        curator_dir = os.path.join(base_dir, '..', 'content-curator')
        output_dir = os.path.join(curator_dir, output_dir)
    output_path = Path(output_dir)

    if not output_path.exists():
        print(f'No output directory found at: {output_path}')
        return

    synced = 0
    failed = 0

    # Scan date directories (new structure: content-archive/YYYY-MM-DD/platform_source_id/)
    # Also support old structure (content-archive/YYYY-MM-DD-title/)
    for item in output_path.iterdir():
        if item.is_dir():
            # Check if this is a date directory (YYYY-MM-DD format)
            if re.match(r'\d{4}-\d{2}-\d{2}$', item.name):
                # New structure: date directory, scan subdirectories
                for content_folder in item.iterdir():
                    if content_folder.is_dir():
                        synced, failed = process_content_folder(content_folder, synced, failed)
            else:
                # Old structure: direct content folder
                synced, failed = process_content_folder(item, synced, failed)

    print('')
    print(f'Summary: {synced} synced, {failed} failed')

def process_content_folder(folder, synced_count, failed_count):
    """Process a single content folder for syncing"""
    metadata_file = folder / 'metadata.md'
    rewritten_file = folder / 'rewritten.md'

    if not metadata_file.exists():
        return synced_count, failed_count

    print(f'Processing: {folder.name}')

    # Read metadata
    with open(metadata_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML frontmatter
    metadata = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1])
            except:
                pass

    # Read rewritten content
    rewritten = ''
    quotes = []
    if rewritten_file.exists():
        with open(rewritten_file, 'r', encoding='utf-8') as f:
            rewritten = f.read()
        # Extract quotes from rewritten content
        quotes = extract_quotes_from_rewritten(rewritten)

    # Add quotes to metadata
    metadata['quotes'] = quotes

    # Find cover image
    cover = None
    for ext in ['jpg', 'jpeg', 'png', 'webp']:
        cover_file = folder / f'cover.{ext}'
        if cover_file.exists():
            cover = str(cover_file)
            break

    metadata['output_dir'] = str(folder)

    try:
        record_id = sync_to_feishu(metadata, rewritten, cover)
        if record_id:
            print(f'   [OK] Synced: {record_id}')
            return synced_count + 1, failed_count
        else:
            print(f'   [SKIP] No record created')
            return synced_count, failed_count
    except Exception as e:
        print(f'   [ERROR] {e}')
        return synced_count, failed_count + 1

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--sync-all':
        sync_existing_outputs()
    else:
        print('Usage:')
        print('  python sync_feishu.py --sync-all   Sync all existing outputs to Feishu')
