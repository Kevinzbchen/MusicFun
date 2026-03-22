"""Generate HTML viewer for comments."""
import json
from pathlib import Path
from datetime import datetime

def generate_html(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MusicFun Comments</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .song {{ background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .song-title {{ font-size: 24px; font-weight: bold; color: #333; }}
        .artist {{ color: #666; margin-bottom: 15px; }}
        .comment {{ border-left: 3px solid #1DB954; padding: 10px 15px; margin: 10px 0; background: #f9f9f9; }}
        .username {{ font-weight: bold; color: #1DB954; }}
        .content {{ margin: 5px 0; line-height: 1.5; }}
        .likes {{ color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>MusicFun Comment Analysis</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
'''

    for song_name, song_data in data.items():
        html += f'''
    <div class="song">
        <div class="song-title">{song_name}</div>
        <div class="artist">{song_data.get('artist', 'Unknown')}</div>
        <div class="stats">Comments: {len(song_data.get('hot_comments', []))}</div>
'''
        for comment in song_data.get('hot_comments', [])[:20]:
            html += f'''
        <div class="comment">
            <div class="username">{comment.get('username', 'Unknown')}</div>
            <div class="content">{comment.get('content', '')}</div>
            <div class="likes">Likes: {comment.get('likes', 0)}</div>
        </div>
'''
        html += '    </div>\n'

    html += '</body></html>'

    output_file = Path('data/processed/comments_viewer.html')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML viewer saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    data_dir = Path('data/processed')
    json_files = list(data_dir.glob('netease_*.json'))
    if json_files:
        latest = max(json_files, key=lambda x: x.stat().st_mtime)
        generate_html(latest)
        print("\nOpen data/processed/comments_viewer.html in your browser")
    else:
        print("No JSON files found")