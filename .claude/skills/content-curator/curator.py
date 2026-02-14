#!/usr/bin/env python3
"""
Content Curator - Main Program
Automated content curation workflow for YouTube, Bilibili, and Xiaoyuzhou
"""

import sys
import os
import argparse
import yaml
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
# Import will be done when needed to avoid errors if modules are not yet implemented

# Configuration
CONFIG_FILE = "config/sources.yaml"
STATE_FILE = "config/state.yaml"

class ContentCurator:
    def __init__(self):
        self.config = self.load_config()
        self.state = self.load_state()
        self.output_dir = Path(self.config.get('settings', {}).get('output_dir', './content-archive'))

    def load_config(self) -> dict:
        """Load configuration from sources.yaml"""
        if not os.path.exists(CONFIG_FILE):
            print(f"❌ Config file not found: {CONFIG_FILE}")
            print(f"💡 Run: curator.py --init to create configuration")
            sys.exit(1)

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_state(self) -> dict:
        """Load state from state.yaml"""
        if not os.path.exists(STATE_FILE):
            return {
                'processed': {
                    'youtube': {},
                    'bilibili': {},
                    'xiaoyuzhou': {}
                },
                'stats': {}
            }

        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f)
            if not state:
                return {
                    'processed': {
                        'youtube': {},
                        'bilibili': {},
                        'xiaoyuzhou': {}
                    },
                    'stats': {}
                }
            return state

    def save_state(self):
        """Save state to state.yaml"""
        self.state['last_updated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(self.state, f, allow_unicode=True, default_flow_style=False)

    def scan_youtube_channel(self, source: dict, limit: int = 10) -> List[dict]:
        """Scan a YouTube channel for new videos using yt-dlp"""
        print(f"   Scanning YouTube: {source['name']}...")

        channel_url = source.get('url', '')
        if not channel_url:
            print(f"      ⚠️ No URL found for {source['name']}, skipping")
            return []

        # Ensure URL ends with /videos for proper playlist extraction
        if not channel_url.endswith('/videos'):
            channel_url = channel_url.rstrip('/') + '/videos'

        try:
            # Use yt-dlp to get channel videos
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--playlist-end', str(limit),
                '--print', '%(id)s|||%(title)s|||%(duration)s|||%(upload_date)s|||%(view_count)s',
                channel_url
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, encoding='utf-8')

            if result.returncode != 0:
                print(f"      ⚠️ Failed to fetch: {result.stderr[:200]}")
                return []

            videos = []
            for line in result.stdout.strip().split('\n'):
                if not line or '|||' not in line:
                    continue

                parts = line.split('|||')
                if len(parts) < 3:
                    continue

                video_id = parts[0]
                title = parts[1]

                # Parse duration (handle float)
                try:
                    duration_sec = int(float(parts[2]))
                except (ValueError, IndexError):
                    duration_sec = 0

                # Parse upload date
                upload_date = parts[3] if len(parts) > 3 else ''
                if upload_date == 'NA' or not upload_date:
                    # If upload_date is NA, use today's date as placeholder
                    from datetime import date
                    upload_date = date.today().strftime('%Y%m%d')

                # Parse views
                try:
                    views = int(parts[4]) if len(parts) > 4 else 0
                except (ValueError, IndexError):
                    views = 0

                # Filter by duration
                min_duration_sec = source.get('min_duration', 30) * 60
                if duration_sec < min_duration_sec:
                    continue

                # Check if already processed
                if video_id in self.state['processed']['youtube']:
                    continue

                # Format duration as HH:MM:SS
                hours = duration_sec // 3600
                minutes = (duration_sec % 3600) // 60
                seconds = duration_sec % 60
                if hours > 0:
                    duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    duration_str = f"{minutes}:{seconds:02d}"

                # Format upload date
                if len(upload_date) == 8:  # YYYYMMDD
                    formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                else:
                    formatted_date = upload_date

                videos.append({
                    'id': video_id,
                    'title': title,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'duration': duration_str,
                    'duration_seconds': duration_sec,
                    'published_at': formatted_date,
                    'views': views,
                    'platform': 'youtube',
                    'source_name': source['name'],
                    'channel_id': source.get('channel_id', ''),
                    'tags': source.get('tags', [])
                })

            print(f"      ✅ Found {len(videos)} new videos")
            return videos

        except subprocess.TimeoutExpired:
            print(f"      ⚠️ Timeout while fetching channel")
            return []
        except Exception as e:
            print(f"      ⚠️ Error: {str(e)}")
            return []

    def scan_bilibili_user(self, source: dict, limit: int = 10) -> List[dict]:
        """Scan a Bilibili user for new videos using Bilibili API"""
        print(f"   Scanning Bilibili: {source['name']}...")

        # TODO: Implement Bilibili API scanning
        # For now, return empty list
        print(f"      ⚠️ Bilibili scanning not yet implemented")
        return []

    def scan_xiaoyuzhou_podcast(self, source: dict, limit: int = 10) -> List[dict]:
        """Scan a Xiaoyuzhou podcast for new episodes"""
        print(f"   Scanning Xiaoyuzhou: {source['name']}...")

        # TODO: Implement Xiaoyuzhou scanning
        # For now, return empty list
        print(f"      ⚠️ Xiaoyuzhou scanning not yet implemented")
        return []

    def scan_all_sources(self, platform: Optional[str] = None, limit: int = 10) -> List[dict]:
        """Scan all enabled sources for new content"""
        print("\n🔍 Scanning sources for new content...\n")

        all_items = []

        # Scan YouTube
        if not platform or platform == 'youtube':
            youtube_sources = self.config.get('sources', {}).get('youtube', [])
            for source in youtube_sources:
                if not source.get('enabled', True):
                    continue
                videos = self.scan_youtube_channel(source, limit)
                all_items.extend(videos)

        # Scan Bilibili
        if not platform or platform == 'bilibili':
            bilibili_sources = self.config.get('sources', {}).get('bilibili', [])
            for source in bilibili_sources:
                if not source.get('enabled', True):
                    continue
                videos = self.scan_bilibili_user(source, limit)
                all_items.extend(videos)

        # Scan Xiaoyuzhou
        if not platform or platform == 'xiaoyuzhou':
            xiaoyuzhou_sources = self.config.get('sources', {}).get('xiaoyuzhou', [])
            for source in xiaoyuzhou_sources:
                if not source.get('enabled', True):
                    continue
                episodes = self.scan_xiaoyuzhou_podcast(source, limit)
                all_items.extend(episodes)

        return all_items

    def display_selection_menu(self, items: List[dict]) -> List[dict]:
        """Display interactive selection menu and return selected items"""
        if not items:
            print("\n📭 No new content found across all sources.")
            return []

        print(f"\n🔍 Found {len(items)} new items across all sources:\n")
        print("=" * 80)

        # Group by platform
        youtube_items = [item for item in items if item['platform'] == 'youtube']
        bilibili_items = [item for item in items if item['platform'] == 'bilibili']
        xiaoyuzhou_items = [item for item in items if item['platform'] == 'xiaoyuzhou']

        # Display YouTube items
        if youtube_items:
            print(f"\n📺 YouTube ({len(youtube_items)} items):\n")
            for i, item in enumerate(youtube_items, 1):
                idx = i
                print(f"  {idx}. [{item['source_name']}] {item['title']}")
                print(f"      Duration: {item['duration']} | Published: {item['published_at']} | Views: {item.get('views', 0):,}")
                if item.get('tags'):
                    print(f"      Tags: {', '.join(item['tags'])}")
                print()

        # Display Bilibili items
        if bilibili_items:
            print(f"\n📺 Bilibili ({len(bilibili_items)} items):\n")
            start_idx = len(youtube_items) + 1
            for i, item in enumerate(bilibili_items, start_idx):
                print(f"  {i}. [{item['source_name']}] {item['title']}")
                print(f"      Duration: {item['duration']} | Published: {item['published_at']}")
                if item.get('tags'):
                    print(f"      Tags: {', '.join(item['tags'])}")
                print()

        # Display Xiaoyuzhou items
        if xiaoyuzhou_items:
            print(f"\n🎙️ Xiaoyuzhou ({len(xiaoyuzhou_items)} items):\n")
            start_idx = len(youtube_items) + len(bilibili_items) + 1
            for i, item in enumerate(xiaoyuzhou_items, start_idx):
                print(f"  {i}. [{item['source_name']}] {item['title']}")
                print(f"      Duration: {item['duration']} | Published: {item['published_at']}")
                if item.get('tags'):
                    print(f"      Tags: {', '.join(item['tags'])}")
                print()

        print("=" * 80)
        print("\n📝 Selection options:")
        print("  • Enter numbers (e.g., '1,2,5' or '1-3,5')")
        print("  • Enter 'all' to select all items")
        print("  • Enter 'youtube', 'bilibili', or 'xiaoyuzhou' to select platform")
        print("  • Enter 'q' to quit\n")

        # Get user selection
        while True:
            try:
                selection = input("Your selection: ").strip().lower()

                if selection == 'q':
                    print("\n👋 Cancelled by user")
                    return []

                if selection == 'all':
                    return items

                if selection == 'youtube':
                    return youtube_items

                if selection == 'bilibili':
                    return bilibili_items

                if selection == 'xiaoyuzhou':
                    return xiaoyuzhou_items

                # Parse number selection
                selected_indices = set()
                for part in selection.split(','):
                    part = part.strip()
                    if '-' in part:
                        # Range selection (e.g., "1-3")
                        start, end = part.split('-')
                        selected_indices.update(range(int(start), int(end) + 1))
                    elif part.isdigit():
                        selected_indices.add(int(part))

                # Get selected items
                selected_items = []
                for idx in sorted(selected_indices):
                    if 1 <= idx <= len(items):
                        selected_items.append(items[idx - 1])

                if not selected_items:
                    print("⚠️ No valid items selected. Please try again.\n")
                    continue

                # Confirm selection
                print(f"\n✅ Selected {len(selected_items)} items:")
                for i, item in enumerate(selected_items, 1):
                    print(f"  {i}. [{item['platform'].upper()}] {item['title']}")

                confirm = input("\nProceed with processing? [Y/n]: ").strip().lower()
                if confirm in ['', 'y', 'yes']:
                    return selected_items
                else:
                    print("\n🔄 Selection cancelled. Please select again.\n")
                    continue

            except (ValueError, IndexError) as e:
                print(f"⚠️ Invalid input: {e}. Please try again.\n")
                continue
            except KeyboardInterrupt:
                print("\n\n👋 Cancelled by user")
                return []

    def batch_mode(self, platform: Optional[str] = None, limit: int = 10):
        """Run in batch mode: scan sources and let user select items"""
        # Scan all sources
        items = self.scan_all_sources(platform, limit)

        # Display selection menu
        selected_items = self.display_selection_menu(items)

        if not selected_items:
            return

        # Process selected items
        print(f"\n🚀 Processing {len(selected_items)} items...\n")
        print("=" * 80)

        for i, item in enumerate(selected_items, 1):
            print(f"\n[{i}/{len(selected_items)}] Processing: {item['title']}")
            print(f"Platform: {item['platform'].upper()} | Duration: {item['duration']}")
            print("-" * 80)

            # TODO: Implement content processing
            # For now, just mark as processed
            platform_key = item['platform']
            if platform_key not in self.state['processed']:
                self.state['processed'][platform_key] = {}

            self.state['processed'][platform_key][item['id']] = {
                'title': item['title'],
                'source': item['source_name'],
                'processed_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                'published_at': item['published_at'],
                'duration': item['duration'],
                'url': item['url']
            }

            print(f"✅ Marked as processed (processing logic pending)\n")

        # Save state
        self.save_state()

        print("=" * 80)
        print(f"\n✅ Batch processing complete!")
        print(f"   • Processed: {len(selected_items)} items")
        print(f"   • State saved to: {STATE_FILE}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Content Curator - Automated content curation workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--batch',
        action='store_true',
        help='Run in batch mode: scan sources and select items interactively'
    )

    parser.add_argument(
        '--platform',
        choices=['youtube', 'bilibili', 'xiaoyuzhou'],
        help='Scan only specific platform (use with --batch)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum items to fetch per source (default: 10)'
    )

    parser.add_argument(
        'urls',
        nargs='*',
        help='URL(s) to process directly (URL mode)'
    )

    args = parser.parse_args()

    # Initialize curator
    curator = ContentCurator()

    # Determine mode
    if args.urls:
        print("🎯 URL Mode: Direct processing")
        print(f"   URLs: {', '.join(args.urls)}")
        print("\n⚠️ URL mode processing logic pending implementation\n")
    elif args.batch:
        # Batch mode
        curator.batch_mode(platform=args.platform, limit=args.limit)
    else:
        # Default: batch mode
        curator.batch_mode(platform=args.platform, limit=args.limit)


if __name__ == '__main__':
    main()
