"""
Simplified configuration for MusicFun.
All output in English, ASCII only.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOG_DIR = DATA_DIR / "logs"

# Create directories
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Netease Music configuration
NETEASE_CONFIG = {
    "base_url": "https://music.163.com/api/",
    "search_url": "https://music.163.com/api/search/get/",
    "comment_url": "https://music.163.com/api/v1/resource/comments/R_SO_4_{}",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://music.163.com/",
        "Cookie": os.getenv("NETEASE_COOKIE", "")
    }
}

# Crawler configuration
CRAWLER_CONFIG = {
    "timeout": 10,
    "retry_times": 3,
    "retry_delay": 2,
    "request_delay": 1,
    "max_comments_per_song": 20
}

# Export all variables for easy import
__all__ = [
    "BASE_DIR",
    "DATA_DIR", 
    "RAW_DATA_DIR",
    "PROCESSED_DATA_DIR",
    "LOG_DIR",
    "NETEASE_CONFIG",
    "CRAWLER_CONFIG"
]
