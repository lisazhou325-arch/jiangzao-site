#!/usr/bin/env python3
"""
Subtitle Downloader - Unified subtitle extraction for all platforms
Priority: yt-dlp (free) → BibiGPT API (paid fallback)
"""

import os
import subprocess
import json
import re
from pathlib import Path
from typing import Optional, Dict, Tuple
import sys

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class SubtitleDownloader:
    """Unified subtitle downloader with fallback strategy"""

    def __init__(self, bibigpt_api_key: Optional[str] = None):
        self.bibigpt_api_key = bibigpt_api_key

    def download_subtitle_ytdlp(self, url: str, output_dir: Path, prefer_lang: str = 'zh') -> Optional[Dict]:
        """
        Download subtitle using yt-dlp (works for YouTube, Bilibili, and many other platforms)

        Args:
            url: Video URL (YouTube, Bilibili, etc.)
            output_dir: Directory to save subtitle file
            prefer_lang: Preferred language code (zh, en, etc.)

        Returns:
            Dict with transcript info or None if failed
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Clean up old subtitle files
        for old_file in output_dir.glob('subtitle*.srt'):
            old_file.unlink()

        # Try multiple subtitle strategies
        strategies = [
            # Strategy 1: Manual Chinese subtitle
            {'lang': 'zh', 'write_sub': True, 'write_auto': False, 'desc': 'Manual Chinese'},
            # Strategy 2: Manual English subtitle
            {'lang': 'en', 'write_sub': True, 'write_auto': False, 'desc': 'Manual English'},
            # Strategy 3: Auto Chinese subtitle
            {'lang': 'zh', 'write_sub': False, 'write_auto': True, 'desc': 'Auto Chinese'},
            # Strategy 4: Auto English subtitle
            {'lang': 'en', 'write_sub': False, 'write_auto': True, 'desc': 'Auto English'},
            # Strategy 5: Any available subtitle
            {'lang': 'en', 'write_sub': True, 'write_auto': True, 'desc': 'Any English'},
        ]

        for i, strategy in enumerate(strategies, 1):
            print(f"      Trying strategy {i}/{len(strategies)}: {strategy['desc']}")

            try:
                # Build yt-dlp command
                cmd = [
                    'yt-dlp',
                    '--skip-download',
                    '--sub-format', 'srt',
                    '--sub-langs', strategy['lang'],
                    '-o', str(output_dir / 'subtitle'),
                    url
                ]

                # Add subtitle download flags
                if strategy['write_sub']:
                    cmd.append('--write-sub')
                if strategy['write_auto']:
                    cmd.append('--write-auto-sub')

                # Run yt-dlp
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    encoding='utf-8'
                )

                # Check if subtitle file was created
                subtitle_files = list(output_dir.glob('subtitle*.srt'))

                if subtitle_files:
                    subtitle_file = subtitle_files[0]
                    print(f"      ✅ Downloaded: {subtitle_file.name}")

                    # Read and parse subtitle
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        subtitle_content = f.read()

                    # Convert SRT to plain text
                    transcript_text = self._srt_to_text(subtitle_content)

                    # Detect actual language
                    detected_lang = self._detect_language(subtitle_file.name)

                    # Determine if auto-generated
                    is_auto = strategy['write_auto'] and not strategy['write_sub']

                    return {
                        'transcript': transcript_text,
                        'raw_subtitle': subtitle_content,
                        'subtitle_file': str(subtitle_file),
                        'language': detected_lang,
                        'source': 'yt-dlp-auto' if is_auto else 'yt-dlp-manual',
                        'word_count': len(transcript_text.split())
                    }

            except subprocess.TimeoutExpired:
                print(f"      ⏱️ Timeout")
                continue
            except Exception as e:
                print(f"      ⚠️ Failed: {str(e)[:80]}")
                continue

        print(f"      ❌ All yt-dlp strategies failed")
        return None

    def download_subtitle_bibigpt(self, url: str, platform: str) -> Optional[Dict]:
        """
        Download subtitle using BibiGPT API (fallback for Bilibili/Xiaoyuzhou)

        Args:
            url: Video/podcast URL
            platform: Platform name (bilibili, xiaoyuzhou)

        Returns:
            Dict with transcript info or None if failed
        """
        if not self.bibigpt_api_key:
            print(f"      ⚠️ BibiGPT API key not configured, skipping")
            return None

        print(f"      📡 Calling BibiGPT API...")

        try:
            from fetch_bibigpt import BibiGPTClient

            client = BibiGPTClient(self.bibigpt_api_key)
            result = client.fetch_transcript(url)

            if result and result.get('transcript'):
                print(f"      ✅ BibiGPT API successful")
                return {
                    'transcript': result['transcript'],
                    'language': 'zh-Hans',
                    'source': 'bibigpt-api',
                    'word_count': len(result['transcript'].split()),
                    'summary': result.get('summary', '')
                }
            else:
                print(f"      ❌ BibiGPT API returned no transcript")
                return None

        except Exception as e:
            print(f"      ❌ BibiGPT API error: {str(e)[:100]}")
            return None

    def download(self, url: str, platform: str, output_dir: Path) -> Optional[Dict]:
        """
        Unified download with fallback strategy

        Priority:
        1. Try yt-dlp (free, works for most platforms)
        2. If yt-dlp fails and platform is Bilibili/Xiaoyuzhou, try BibiGPT API

        Args:
            url: Video URL
            platform: Platform name (youtube, bilibili, xiaoyuzhou)
            output_dir: Directory to save files

        Returns:
            Dict with transcript info or None if all methods failed
        """
        print(f"   📥 Downloading subtitle...")
        print(f"      URL: {url}")
        print(f"      Platform: {platform}")

        # Strategy 1: Try yt-dlp first (free!)
        print(f"\n   🎯 Trying yt-dlp (free)...")
        result = self.download_subtitle_ytdlp(url, output_dir)

        if result:
            return result

        # Strategy 2: Fallback to BibiGPT API for Bilibili/Xiaoyuzhou
        if platform in ['bilibili', 'xiaoyuzhou']:
            print(f"\n   🎯 Fallback to BibiGPT API (paid)...")
            result = self.download_subtitle_bibigpt(url, platform)

            if result:
                return result

        print(f"\n   ❌ All subtitle download strategies failed")
        return None

    def _srt_to_text(self, srt_content: str) -> str:
        """Convert SRT subtitle to plain text with timestamps"""
        lines = []
        current_timestamp = None

        for line in srt_content.split('\n'):
            line = line.strip()

            # Check if this is a timestamp line (e.g., "00:00:10,500 --> 00:00:13,000")
            if '-->' in line:
                # Extract start timestamp
                start_time = line.split('-->')[0].strip()
                # Convert to [HH:MM:SS] format
                if ',' in start_time:
                    start_time = start_time.split(',')[0]
                current_timestamp = f"[{start_time}]"
                continue

            # Skip empty lines and line numbers
            if not line or line.isdigit():
                continue

            # This is actual subtitle text
            if current_timestamp:
                lines.append(f"{current_timestamp} {line}")
                current_timestamp = None
            else:
                lines.append(line)

        return '\n'.join(lines)

    def _detect_language(self, filename: str) -> str:
        """Detect language from subtitle filename"""
        filename = filename.lower()

        if 'zh' in filename or 'chi' in filename:
            return 'zh-Hans'
        elif 'en' in filename:
            return 'en'
        else:
            return 'unknown'


def main():
    """Test the subtitle downloader"""
    import argparse

    parser = argparse.ArgumentParser(description="Test subtitle downloader")
    parser.add_argument('url', help='Video URL')
    parser.add_argument('--platform', default='youtube', choices=['youtube', 'bilibili', 'xiaoyuzhou'])
    parser.add_argument('--output', default='./test_output', help='Output directory')
    parser.add_argument('--bibigpt-key', help='BibiGPT API key for fallback')

    args = parser.parse_args()

    downloader = SubtitleDownloader(bibigpt_api_key=args.bibigpt_key)
    result = downloader.download(args.url, args.platform, Path(args.output))

    if result:
        print(f"\n✅ Success!")
        print(f"   Source: {result['source']}")
        print(f"   Language: {result['language']}")
        print(f"   Word count: {result['word_count']}")
        print(f"   Preview: {result['transcript'][:500]}...")
    else:
        print(f"\n❌ Failed to download subtitle")


if __name__ == '__main__':
    main()
