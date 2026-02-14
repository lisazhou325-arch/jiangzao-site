#!/usr/bin/env python3
"""
BibiGPT API Client
Fetches transcripts from Bilibili and Xiaoyuzhou using BibiGPT API
"""

import requests
import time
from typing import Dict, Optional


class BibiGPTClient:
    """Client for BibiGPT API"""

    BASE_URL = "https://api.bibigpt.co/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize BibiGPT client

        Args:
            api_key: Your BibiGPT API key from https://bibigpt.co
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def get_transcript(self, url: str, include_detail: bool = True) -> Dict:
        """
        Get transcript and summary from video/podcast URL using BibiGPT API

        Args:
            url: Video/podcast URL (Bilibili or Xiaoyuzhou)
            include_detail: Whether to include detailed transcript (default: True)

        Returns:
            dict with keys: transcript, summary, title, duration, cover_url

        Raises:
            Exception: If API request fails
        """
        endpoint = f"{self.BASE_URL}/summarizeWithConfig"

        payload = {
            "url": url,
            "includeDetail": include_detail
        }

        try:
            response = self.session.post(endpoint, json=payload, timeout=300)
            response.raise_for_status()

            data = response.json()

            # BibiGPT API returns data directly or with a code field
            if isinstance(data, dict) and data.get("code") and data.get("code") != 0:
                raise Exception(f"BibiGPT API error: {data.get('message', 'Unknown error')}")

            # Extract result (API may return data directly or nested in 'data' field)
            result = data.get("data", data) if isinstance(data, dict) else data

            return {
                "transcript": result.get("transcript", "") or result.get("detail", ""),
                "summary": result.get("summary", ""),
                "title": result.get("title", ""),
                "duration": result.get("duration", 0),
                "duration_formatted": self._format_duration(result.get("duration", 0)),
                "cover_url": result.get("cover_url", "") or result.get("coverUrl", ""),
                "subtitle_language": "zh-Hans",  # BibiGPT mainly returns Chinese
                "subtitle_source": "bibigpt"
            }

        except requests.exceptions.Timeout:
            raise Exception("BibiGPT API timeout (video too long or server busy)")
        except requests.exceptions.RequestException as e:
            raise Exception(f"BibiGPT API request failed: {str(e)}")

    def get_bilibili_video_info(self, bvid: str) -> Dict:
        """
        Get Bilibili video metadata

        Args:
            bvid: Bilibili video ID (e.g., BV1xx411c7xx)

        Returns:
            dict with video metadata
        """
        # BibiGPT may provide this endpoint, or we use Bilibili public API
        bilibili_api = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

        try:
            response = requests.get(bilibili_api, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("code") != 0:
                raise Exception(f"Bilibili API error: {data.get('message')}")

            video_data = data.get("data", {})
            stats = video_data.get("stat", {})

            return {
                "bvid": bvid,
                "aid": video_data.get("aid"),
                "title": video_data.get("title", ""),
                "description": video_data.get("desc", ""),
                "cover_url": video_data.get("pic", ""),
                "uploader": video_data.get("owner", {}).get("name", ""),
                "uid": video_data.get("owner", {}).get("mid", ""),
                "published_at": self._timestamp_to_iso(video_data.get("pubdate", 0)),
                "duration": video_data.get("duration", 0),
                "duration_formatted": self._format_duration(video_data.get("duration", 0)),
                "views": stats.get("view", 0),
                "likes": stats.get("like", 0),
                "coins": stats.get("coin", 0),
                "favorites": stats.get("favorite", 0),
                "comments": stats.get("reply", 0),
                "shares": stats.get("share", 0),
                "tags": [tag["tag_name"] for tag in video_data.get("tags", [])] if video_data.get("tags") else []
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch Bilibili metadata: {str(e)}")

    def get_xiaoyuzhou_episode_info(self, episode_url: str) -> Dict:
        """
        Get Xiaoyuzhou episode metadata

        Note: Xiaoyuzhou doesn't have a public API, so we rely on BibiGPT
        or scraping (not recommended). For now, return basic info.

        Args:
            episode_url: Xiaoyuzhou episode URL

        Returns:
            dict with episode metadata
        """
        # This would require scraping or a dedicated API
        # For now, return placeholder
        return {
            "url": episode_url,
            "platform": "xiaoyuzhou",
            "note": "Full metadata extraction requires additional implementation"
        }

    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Format duration from seconds to HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    @staticmethod
    def _timestamp_to_iso(timestamp: int) -> str:
        """Convert Unix timestamp to ISO 8601 format"""
        from datetime import datetime
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

    def test_connection(self) -> bool:
        """
        Test if API key is valid

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try a simple request with a known working video
            test_url = "https://www.bilibili.com/video/BV1Sk4y1x7r2"
            result = self.get_transcript(test_url)
            return bool(result.get("summary") or result.get("transcript"))
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python fetch_bibigpt.py <api_key> <url>")
        sys.exit(1)

    api_key = sys.argv[1]
    url = sys.argv[2]

    client = BibiGPTClient(api_key)

    print(f"Fetching transcript from: {url}")
    result = client.get_transcript(url)

    print(f"\nTitle: {result['title']}")
    print(f"Duration: {result['duration_formatted']}")
    print(f"Transcript length: {len(result['transcript'])} characters")
    print(f"\nFirst 500 characters:")
    print(result['transcript'][:500])
