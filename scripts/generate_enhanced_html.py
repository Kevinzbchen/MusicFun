"""
Enhanced HTML viewer for MusicFun comments.
"""
import json
from pathlib import Path
from datetime import datetime
import webbrowser


def generate_enhanced_html(json_file):
    """Generate a beautiful HTML viewer for comments."""

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Calculate statistics
    total_songs = len(data)
    total_comments = sum(len(song.get('hot_comments', [])) for song in data.values())
    total_likes = sum(
        sum(c.get('likes', 0) for c in song.get('hot_comments', []))
        for song in data.values()
    )

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MusicFun - 网易云音乐评论分析</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 36px;
            font-weight: bold;
        }}
        
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
            margin-top: 5px;
        }}
        
        .song-card {{
            background: white;
            border-radius: 16px;
            margin-bottom: 30px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .song-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }}
        
        .song-header {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
            padding: 20px 25px;
            border-bottom: 3px solid #667eea;
        }}
        
        .song-title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        
        .song-artist {{
            color: #666;
            margin-top: 5px;
        }}
        
        .song-meta {{
            display: flex;
            gap: 20px;
            margin-top: 10px;
            font-size: 14px;
            color: #888;
        }}
        
        .comments-section {{
            padding: 20px 25px;
        }}
        
        .comments-header {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .comment {{
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: background 0.2s;
        }}
        
        .comment:hover {{
            background: #e9ecef;
        }}
        
        .comment-user {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .user-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        .user-name {{
            font-weight: bold;
            color: #333;
        }}
        
        .comment-content {{
            line-height: 1.6;
            color: #555;
            margin-bottom: 10px;
        }}
        
        .comment-meta {{
            display: flex;
            gap: 15px;
            font-size: 12px;
            color: #999;
        }}
        
        .like-count {{
            color: #e74c3c;
        }}
        
        .load-more {{
            text-align: center;
            padding: 10px;
            color: #667eea;
            cursor: pointer;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            font-size: 14px;
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: 1fr;
            }}
            .song-title {{
                font-size: 18px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 MusicFun 评论分析报告</h1>
            <p>生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_songs}</div>
                    <div class="stat-label">歌曲数量</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_comments}</div>
                    <div class="stat-label">评论总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_likes:,}</div>
                    <div class="stat-label">总点赞数</div>
                </div>
            </div>
        </div>
'''

    for song_name, song_data in data.items():
        comments = song_data.get('hot_comments', [])
        total_comments_song = song_data.get('total_comments', len(comments))
        artist = song_data.get('artist', '未知艺术家')
        album = song_data.get('album', '未知专辑')
        duration = song_data.get('duration', 0)
        minutes = duration // 60
        seconds = duration % 60

        html += f'''
        <div class="song-card">
            <div class="song-header">
                <div class="song-title">{song_name}</div>
                <div class="song-artist">🎤 {artist}</div>
                <div class="song-meta">
                    <span>💿 {album}</span>
                    <span>⏱️ {minutes}:{seconds:02d}</span>
                    <span>💬 {total_comments_song} 条评论</span>
                </div>
            </div>
            <div class="comments-section">
                <div class="comments-header">热门评论 (前{len(comments)}条)</div>
'''

        for i, comment in enumerate(comments[:10], 1):
            username = comment.get('username', '未知用户')
            content = comment.get('content', '')
            likes = comment.get('likes', 0)
            time_str = comment.get('time', '')

            # Get first letter for avatar
            avatar_char = username[0] if username else '?'

            html += f'''
                <div class="comment">
                    <div class="comment-user">
                        <div class="user-avatar">{avatar_char}</div>
                        <div class="user-name">{username}</div>
                    </div>
                    <div class="comment-content">{content}</div>
                    <div class="comment-meta">
                        <span>❤️ <span class="like-count">{likes}</span> 赞</span>
                        <span>📅 {time_str[:10] if time_str else '未知时间'}</span>
                    </div>
                </div>
'''

        if len(comments) > 10:
            html += f'<div class="load-more">还有 {len(comments) - 10} 条评论...</div>'

        html += '''
            </div>
        </div>
'''

    html += '''
        <div class="footer">
            <p>Powered by MusicFun 🎵 | 数据来源于网易云音乐API</p>
        </div>
    </div>
</body>
</html>
'''

    output_file = Path('data/processed/comments_viewer.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_file


if __name__ == "__main__":
    data_dir = Path('data/processed')
    json_files = list(data_dir.glob('netease_*.json'))

    if json_files:
        latest = max(json_files, key=lambda x: x.stat().st_mtime)
        output = generate_enhanced_html(latest)
        print(f"HTML viewer saved to: {output}")

        # Auto-open in browser
        webbrowser.open(str(output))
    else:
        print("No JSON files found")
        print("Run: python scripts/run_netease.py --keyword 米哈游 --limit 5")