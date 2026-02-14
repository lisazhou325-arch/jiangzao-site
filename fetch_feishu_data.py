#!/usr/bin/env python3
"""Fetch all records from Feishu Bitable to understand the data structure"""

import time
import yaml
import json
import requests
from pathlib import Path

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
    access_token = data["tenant_access_token"]
    token_expires_at = time.time() + data["expire"] - 60
    return access_token


def list_records():
    url = f"{FEISHU_BASE}/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    resp = requests.get(url, headers={"Authorization": f"Bearer {get_token()}"}, timeout=30)
    return resp.json()


def list_fields():
    url = f"{FEISHU_BASE}/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields"
    resp = requests.get(url, headers={"Authorization": f"Bearer {get_token()}"}, timeout=30)
    return resp.json()


get_token()

print("=== FIELDS ===")
fields_resp = list_fields()
print(json.dumps(fields_resp, ensure_ascii=False, indent=2))

print("\n=== RECORDS ===")
records_resp = list_records()
print(json.dumps(records_resp, ensure_ascii=False, indent=2))
