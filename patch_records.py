#!/usr/bin/env python3
"""Patch existing Feishu records: add guests and published_at"""

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
    print(f"  [OK] Updated {record_id}")


def date_to_ms(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


# Patch data: record_id -> (guests, published_at)
patches = [
    ("recvb7wuB7uK6R", "Will Brown, Johannes Hagemann", "2026-02-10"),
    ("recvb7wvhJy9wb", "Bill Anderson", "2026-02-12"),
    ("recvb7wvWQPdGW", "Jamie Cuffe", "2026-02-03"),
]

get_token()
for record_id, guests, pub_date in patches:
    update_record(record_id, {
        "嘉宾": guests,
        "发布时间": date_to_ms(pub_date),
    })
    print(f"  -> {guests} | {pub_date}")

print("\nDone!")
