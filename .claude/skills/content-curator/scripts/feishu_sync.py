#!/usr/bin/env python3
"""
Feishu Bitable Sync
Uploads content to Feishu (Lark) Bitable
"""

import requests
import time
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class FeishuClient:
    """Client for Feishu Open API"""

    BASE_URL = "https://open.feishu.cn/open-apis"

    def __init__(self, app_id: str, app_secret: str):
        """
        Initialize Feishu client

        Args:
            app_id: Feishu app ID
            app_secret: Feishu app secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = 0

    def get_access_token(self) -> str:
        """
        Get tenant access token (auto-refresh)

        Returns:
            Access token string
        """
        # Return cached token if still valid
        if time.time() < self.token_expires_at:
            return self.access_token

        # Request new token
        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"

        response = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }, timeout=10)

        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"Failed to get access token: {data.get('msg')}")

        self.access_token = data["tenant_access_token"]
        self.token_expires_at = time.time() + data["expire"] - 60  # Refresh 1min early

        return self.access_token

    def upload_image(self, image_path: Path, parent_type: str = "bitable_image",
                    parent_node: str = None) -> str:
        """
        Upload image to Feishu Drive

        Args:
            image_path: Path to image file
            parent_type: Parent type (default: bitable_image)
            parent_node: Parent node token (Bitable app token)

        Returns:
            File token of uploaded image
        """
        url = f"{self.BASE_URL}/drive/v1/medias/upload_all"

        with open(image_path, 'rb') as f:
            # Determine MIME type
            ext = image_path.suffix.lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.webp': 'image/webp',
                '.gif': 'image/gif'
            }
            mime_type = mime_types.get(ext, 'image/jpeg')

            files = {
                'file': (image_path.name, f, mime_type),
            }

            data = {
                'file_name': image_path.name,
                'parent_type': parent_type,
                'parent_node': parent_node or '',
                'size': str(image_path.stat().st_size)
            }

            response = requests.post(url, files=files, data=data, headers={
                'Authorization': f'Bearer {self.get_access_token()}'
            }, timeout=30)

        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"Failed to upload image: {result.get('msg')}")

        return result["data"]["file_token"]

    def add_bitable_record(self, app_token: str, table_id: str, fields: Dict) -> str:
        """
        Add a record to Bitable

        Args:
            app_token: Bitable app token
            table_id: Table ID
            fields: Field values dict

        Returns:
            Record ID of created record
        """
        url = f"{self.BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/records"

        response = requests.post(url, json={
            "fields": fields
        }, headers={
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }, timeout=30)

        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"Failed to add Bitable record: {result.get('msg')}")

        return result["data"]["record"]["record_id"]

    def sync_content(self, app_token: str, table_id: str, metadata: Dict,
                    cover_path: Optional[Path] = None) -> str:
        """
        Sync content item to Feishu Bitable

        Args:
            app_token: Bitable app token
            table_id: Table ID
            metadata: Content metadata dict
            cover_path: Path to cover image (optional)

        Returns:
            Record ID of created record
        """
        # Upload cover image if provided
        cover_field = []
        if cover_path and cover_path.exists():
            try:
                file_token = self.upload_image(cover_path, parent_node=app_token)
                cover_field = [{
                    "file_token": file_token,
                    "name": cover_path.name
                }]
            except Exception as e:
                print(f"Warning: Failed to upload cover image: {e}")

        # Prepare Bitable fields (matching actual table structure)
        # Prefer chinese_title from rewritten content if available
        title = metadata.get('chinese_title') or metadata.get('title', '')
        fields = {
            "标题": title,
            "平台来源": metadata.get('platform', '').upper(),
            "原内容链接": {
                "link": metadata.get('url', ''),
                "text": title
            },
            "封面图": cover_field,
            "标签": metadata.get('tags', []),
            "嘉宾": metadata.get('guests_str', '') or metadata.get('channel', ''),
        }

        # Add published_at as date field (millisecond timestamp)
        pub_date = metadata.get('published_at')
        if pub_date:
            from datetime import datetime, timezone
            dt = datetime.strptime(str(pub_date), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            fields["发布时间"] = int(dt.timestamp() * 1000)

        # Add quotes to individual fields (金句1-5)
        quotes = metadata.get('quotes', [])
        # Ensure we have exactly 5 quotes (pad with empty if needed)
        while len(quotes) < 5:
            quotes.append('')
        for i in range(5):
            field_name = f"金句{i+1}"
            fields[field_name] = quotes[i][:200] if quotes[i] else ''  # Limit to 200 chars per quote

        # Add rewritten summary to "摘要正文" field
        if metadata.get('rewritten_summary'):
            fields["摘要正文"] = metadata['rewritten_summary'][:5000]  # Limit to 5000 chars

        # Create record
        record_id = self.add_bitable_record(app_token, table_id, fields)

        return record_id

    def test_connection(self) -> bool:
        """
        Test if credentials are valid

        Returns:
            True if connection successful, False otherwise
        """
        try:
            token = self.get_access_token()
            return bool(token)
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python feishu_sync.py <app_id> <app_secret>")
        sys.exit(1)

    app_id = sys.argv[1]
    app_secret = sys.argv[2]

    client = FeishuClient(app_id, app_secret)

    print("Testing Feishu connection...")
    if client.test_connection():
        print("[OK] Connection successful!")
        print(f"Access token: {client.access_token[:20]}...")
    else:
        print("[FAIL] Connection failed")
        sys.exit(1)
