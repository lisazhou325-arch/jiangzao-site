#!/usr/bin/env python3
"""Patch Feishu records: Chinese titles + guest with role"""

import time
import yaml
import requests
from pathlib import Path
from datetime import datetime, timezone

FEISHU_BASE = "https://open.feishu.cn/open-apis"
access_token = None
token_expires_at = 0

config_path = Path(__file__).parent / ".claude" / "skills" / "content-curator" / "config" / "sources.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
feishu = config["api_keys"]["feishu"]
APP_ID = feishu["app_id"]
APP_SECRET = feishu["app_secret"]
APP_TOKEN = feishu["bitable_app_token"]
TABLE_ID = feishu["table_id"]


def get_token():
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
    return access_token


def update_record(record_id, fields):
    url = f"{FEISHU_BASE}/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    resp = requests.put(url, json={"fields": fields},
                        headers={"Authorization": f"Bearer {get_token()}",
                                 "Content-Type": "application/json"}, timeout=30)
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Update failed: {result.get('msg')}")
    print(f"  [OK] {record_id}")


get_token()

patches = [
    ("recvb7wuB7uK6R", {
        "标题": "Prime Intellect：让每家公司都成为AI研究实验室",
        "嘉宾": "Will Brown (Prime Intellect联合创始人), Johannes Hagemann (Prime Intellect联合创始人)",
    }),
    ("recvb7wvhJy9wb", {
        "标题": "拜耳CEO的激进实验：让168年老牌企业像快艇一样转向",
        "嘉宾": "Bill Anderson (拜耳CEO)",
    }),
    ("recvb7wvWQPdGW", {
        "标题": "AI重塑保险业：Pace如何用智能代理取代千亿美元BPO市场",
        "嘉宾": "Jamie Cuffe (Pace创始人兼CEO)",
    }),
]

for record_id, fields in patches:
    update_record(record_id, fields)
    print(f"     标题: {fields['标题']}")
    print(f"     嘉宾: {fields['嘉宾']}")

print("\nDone!")
