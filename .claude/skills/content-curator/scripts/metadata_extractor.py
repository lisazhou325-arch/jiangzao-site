#!/usr/bin/env python3
"""
Metadata Extraction Utilities
Common functions for extracting and processing metadata
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


def sanitize_filename(title: str, max_length: int = 100) -> str:
    """
    Sanitize title for use in filename

    Args:
        title: Original title
        max_length: Maximum filename length

    Returns:
        Sanitized filename
    """
    # Convert to lowercase
    title = title.lower()

    # Remove special characters
    title = re.sub(r'[^\w\s-]', '', title)

    # Replace spaces and multiple hyphens with single hyphen
    title = re.sub(r'[-\s]+', '-', title)

    # Remove leading/trailing hyphens
    title = title.strip('-')

    # Truncate to max length
    if len(title) > max_length:
        title = title[:max_length].rsplit('-', 1)[0]

    return title


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL

    Args:
        url: YouTube URL

    Returns:
        Video ID or None
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\?\/]+)',
        r'youtube\.com\/embed\/([^&\?\/]+)',
        r'youtube\.com\/v\/([^&\?\/]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def extract_bvid(url: str) -> Optional[str]:
    """
    Extract BVID from Bilibili URL

    Args:
        url: Bilibili URL

    Returns:
        BVID or None
    """
    pattern = r'bilibili\.com\/video\/(BV[A-Za-z0-9]+)'
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


def extract_xiaoyuzhou_episode_id(url: str) -> Optional[str]:
    """
    Extract episode ID from Xiaoyuzhou URL

    Args:
        url: Xiaoyuzhou URL

    Returns:
        Episode ID or None
    """
    pattern = r'xiaoyuzhou\.co\/episode\/([a-f0-9]+)'
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


def format_duration(seconds: int) -> str:
    """
    Format duration from seconds to HH:MM:SS or MM:SS

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def parse_duration(duration_str: str) -> int:
    """
    Parse duration string to seconds

    Args:
        duration_str: Duration string (HH:MM:SS or MM:SS)

    Returns:
        Duration in seconds
    """
    parts = duration_str.split(':')

    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    else:
        return int(parts[0])


def timestamp_to_iso(timestamp: int) -> str:
    """
    Convert Unix timestamp to ISO 8601 date

    Args:
        timestamp: Unix timestamp

    Returns:
        ISO date string (YYYY-MM-DD)
    """
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')


def iso_to_timestamp(iso_date: str) -> int:
    """
    Convert ISO 8601 date to Unix timestamp

    Args:
        iso_date: ISO date string (YYYY-MM-DD)

    Returns:
        Unix timestamp
    """
    dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
    return int(dt.timestamp())


def identify_platform(url: str) -> tuple:
    """
    Identify platform and extract ID from URL

    Args:
        url: Content URL

    Returns:
        Tuple of (platform, id) or raises ValueError
    """
    if 'youtube.com' in url or 'youtu.be' in url:
        video_id = extract_video_id(url)
        if video_id:
            return ('youtube', video_id)

    elif 'bilibili.com' in url:
        bvid = extract_bvid(url)
        if bvid:
            return ('bilibili', bvid)

    elif 'xiaoyuzhou.co' in url:
        episode_id = extract_xiaoyuzhou_episode_id(url)
        if episode_id:
            return ('xiaoyuzhou', episode_id)

    raise ValueError(f"Unsupported or invalid URL: {url}")


def create_output_directory(base_dir: str, published_date: str, title: str,
                           platform: str = None, source_type: str = None,
                           content_id: str = None) -> Path:
    """
    Create output directory for content item with date-based grouping

    New structure:
        content-archive/
          2025-12-18/
            youtube_ChannelName_VideoTitle/
            bilibili_SingleURL_BV1xxx/

    Args:
        base_dir: Base output directory (e.g., "content-archive")
        published_date: Published date (YYYY-MM-DD)
        title: Content title
        platform: Platform name (youtube, bilibili, xiaoyuzhou)
        source_type: Source type (ChannelName, SingleURL, etc.)
        content_id: Content ID (video ID, BVID, etc.)

    Returns:
        Path to created directory
    """
    # Create date-based parent directory
    date_dir = Path(base_dir) / published_date

    # Generate folder name
    if platform and source_type:
        # New format: platform_sourceType_identifier
        sanitized_title = sanitize_filename(title, max_length=50)
        if content_id:
            dir_name = f"{platform}_{source_type}_{content_id}"
        else:
            dir_name = f"{platform}_{source_type}_{sanitized_title}"
    else:
        # Fallback to old format for compatibility
        sanitized_title = sanitize_filename(title)
        dir_name = sanitized_title

    output_dir = date_dir / dir_name

    # Handle collisions
    counter = 1
    original_dir_name = dir_name
    while output_dir.exists():
        dir_name = f"{original_dir_name}_{counter}"
        output_dir = date_dir / dir_name
        counter += 1

    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir


def count_words(text: str) -> int:
    """
    Count words in text (works for both English and Chinese)

    Args:
        text: Input text

    Returns:
        Word count
    """
    # For Chinese, count characters (excluding punctuation/whitespace)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))

    # For English/other languages, count words
    words = len(re.findall(r'\b\w+\b', text))

    # Return whichever is higher (handles mixed content)
    return max(chinese_chars, words)


def extract_tags_from_text(text: str, max_tags: int = 10) -> List[str]:
    """
    Extract potential tags from text using simple keyword extraction

    Args:
        text: Input text
        max_tags: Maximum number of tags to return

    Returns:
        List of extracted tags
    """
    # This is a simple implementation
    # For production, consider using NLP libraries like jieba, NLTK, or spaCy

    # Common stopwords (expand as needed)
    stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
                'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but'}

    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())

    # Filter and count
    word_freq = {}
    for word in words:
        if len(word) > 2 and word not in stopwords:
            word_freq[word] = word_freq.get(word, 0) + 1

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Return top N
    return [word for word, freq in sorted_words[:max_tags]]


def extract_quotes_from_rewritten(rewritten_content: str) -> List[str]:
    """
    Extract quotes from rewritten content

    Args:
        rewritten_content: The rewritten markdown content

    Returns:
        List of 5 quotes (padded with empty strings if less than 5)
    """
    quotes = []

    # Format 1: opening numbered list with quoted strings e.g. 1. "..."
    quote_pattern_inline = r'\d+\.\s*[""「](.+?)[""」]'
    matches = re.findall(quote_pattern_inline, rewritten_content[:600])
    if matches:
        quotes.extend([q.strip() for q in matches])

    # Format 2: "# 金句精选" or "## 金句" section with numbered items (with or without quotes)
    if not quotes:
        section_match = re.search(r'#+ 金句[^\n]*\n((?:\d+\.\s*.+\n?)+)', rewritten_content, re.MULTILINE)
        if section_match:
            quote_pattern = r'\d+\.\s*[""「]?(.+?)[""」]?\s*$'
            matches = re.findall(quote_pattern, section_match.group(1), re.MULTILINE)
            quotes.extend([q.strip() for q in matches])

    # Format 3: opening numbered list without quotes e.g. 1. text...
    if not quotes:
        quote_pattern_noquote = r'^\d+\.\s*(.+)$'
        matches = re.findall(quote_pattern_noquote, rewritten_content[:600], re.MULTILINE)
        if matches:
            quotes.extend([q.strip() for q in matches])

    # Ensure exactly 5 quotes (pad with empty strings if needed)
    while len(quotes) < 5:
        quotes.append('')

    # Truncate to 5 if more
    return quotes[:5]


# Example usage
if __name__ == "__main__":
    # Test functions
    print("Testing URL parsing:")

    urls = [
        "https://youtube.com/watch?v=abc123",
        "https://bilibili.com/video/BV1xx411c7xx",
        "https://xiaoyuzhou.co/episode/123abc"
    ]

    for url in urls:
        try:
            platform, content_id = identify_platform(url)
            print(f"  {url} → {platform}: {content_id}")
        except ValueError as e:
            print(f"  {url} → Error: {e}")

    print("\nTesting filename sanitization:")
    titles = [
        "The Ultimate Guide to AI: Part 1 (2024)",
        "为什么人类至今没有发现外星人？🛸",
        "How to Build a $1M Company in 30 Days"
    ]

    for title in titles:
        sanitized = sanitize_filename(title)
        print(f"  {title} → {sanitized}")
