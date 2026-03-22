"""Display comments with proper encoding."""
import json
from pathlib import Path

def show_comments(json_file):
    """Display comments from JSON file with proper encoding."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("=" * 70)
    print(f"FILE: {json_file}")
    print("=" * 70)

    for song_name, song_data in data.items():
        print(f"\nSong: {song_name}")
        print(f"Artist: {song_data.get('artist', 'Unknown')}")
        print(f"Comments: {len(song_data.get('hot_comments', []))}")
        print("-" * 50)

        for i, comment in enumerate(song_data.get('hot_comments', [])[:10], 1):
            print(f"\n{i}. {comment.get('username', 'Unknown')}:")
            print(f"   {comment.get('content', '')}")
            print(f"   Likes: {comment.get('likes', 0)}")
        print()

if __name__ == "__main__":
    data_dir = Path("data/processed")
    json_files = list(data_dir.glob("netease_*.json"))

    if json_files:
        latest = max(json_files, key=lambda x: x.stat().st_mtime)
        show_comments(latest)
    else:
        print("No JSON files found")
        print("Run: python scripts/run_netease.py --keyword mihoyo --limit 2")