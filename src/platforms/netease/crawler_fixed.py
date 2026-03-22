"""
Netease Music crawler implementation with mock mode.
All output in English, ASCII only.
"""
from typing import List, Dict, Any, Optional
import random
from datetime import datetime, timedelta
from loguru import logger
from src.core.base_crawler import BaseCrawler
from src.models.song import Song
from src.models.comment import Comment
from src.models.user import User


class NeteaseCrawlerFixed(BaseCrawler):
    """Netease Music crawler implementation with mock mode."""
    
    def __init__(self, use_mock: bool = False):
        """Initialize Netease crawler with configuration."""
        from config.settings import NETEASE_CONFIG, CRAWLER_CONFIG
        config = {**NETEASE_CONFIG, **CRAWLER_CONFIG}
        
        # Store URLs for use in methods
        self.search_url = config.get("search_url", "https://music.163.com/api/search/get/")
        self.use_mock = use_mock
        
        # Call parent with config
        super().__init__(config)
        logger.info(f"NeteaseCrawler initialized (mock mode: {use_mock})")
    
    def get_song(self, song_id: int) -> Optional[Song]:
        """Get detailed information about a song."""
        if self.use_mock:
            logger.info(f"[MOCK] Getting song detail: {song_id}")
            # Create mock song data
            mock_songs = [
                Song(
                    id=str(song_id),
                    title="Mock Song Title",
                    artist="Mock Artist",
                    artists=[{"id": 123, "name": "Mock Artist"}],
                    platform="netease",
                    platform_id=str(song_id),
                    album="Mock Album",
                    duration=180,
                    cover_url="https://example.com/mock-cover.jpg"
                ),
                Song(
                    id=str(song_id),
                    title="Another Mock Song",
                    artist="Another Artist",
                    artists=[{"id": 456, "name": "Another Artist"}],
                    platform="netease",
                    platform_id=str(song_id),
                    album="Another Album",
                    duration=240,
                    cover_url="https://example.com/another-cover.jpg"
                )
            ]
            return random.choice(mock_songs)
        
        logger.info(f"Getting song detail: {song_id}")
        
        url = f"https://music.163.com/api/song/detail/?ids=[{song_id}]"
        
        response = self._make_request(url, method="GET")
        if not response:
            return None
        
        try:
            data = response.json()
            songs_data = data.get("songs", [])
            if not songs_data:
                return None
            
            song_data = songs_data[0]
            
            # Parse artists
            artists = []
            for a in song_data.get("artists", []):
                artists.append({"id": a["id"], "name": a["name"]})
            
            # Create Song object with correct field names
            song = Song(
                id=str(song_data["id"]),
                title=song_data["name"],
                artist=artists[0]["name"] if artists else "",
                artists=artists,
                platform="netease",
                platform_id=str(song_data["id"]),
                album=song_data.get("album", {}).get("name"),
                duration=song_data.get("duration", 0) // 1000,
                cover_url=song_data.get("album", {}).get("picUrl")
            )
            return song
            
        except Exception as e:
            logger.error(f"Failed to parse song detail: {e}")
            return None
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user information."""
        if self.use_mock:
            logger.info(f"[MOCK] Getting user detail: {user_id}")
            # Create mock user data
            mock_users = [
                User(
                    user_id=user_id,
                    nickname="Mock User",
                    avatar_url="https://example.com/mock-avatar.jpg",
                    signature="This is a mock user signature"
                ),
                User(
                    user_id=user_id,
                    nickname="Test Fan",
                    avatar_url="https://example.com/test-avatar.jpg",
                    signature="Love this song!"
                ),
                User(
                    user_id=user_id,
                    nickname="Music Lover",
                    avatar_url="https://example.com/music-avatar.jpg",
                    signature="Always listening to good music"
                )
            ]
            return random.choice(mock_users)
        
        logger.info(f"Getting user detail: {user_id}")
        
        url = f"https://music.163.com/api/v1/user/detail/{user_id}"
        
        response = self._make_request(url, method="GET")
        if not response:
            return None
        
        try:
            data = response.json()
            profile = data.get("profile", {})
            
            user = User(
                user_id=profile.get("userId", user_id),
                nickname=profile.get("nickname", ""),
                avatar_url=profile.get("avatarUrl"),
                signature=profile.get("signature")
            )
            return user
            
        except Exception as e:
            logger.error(f"Failed to parse user detail: {e}")
            return None
    
    def search(self, keyword: str, limit: int = 50, **kwargs) -> List[Song]:
        """Search for songs by keyword."""
        if self.use_mock:
            logger.info(f"[MOCK] Searching for: {keyword}")
            # Generate mock songs based on keyword
            mock_songs = []
            for i in range(min(limit, 10)):  # Max 10 mock songs
                song = Song(
                    id=str(1000 + i),
                    title=f"{keyword} Song {i+1}",
                    artist=f"{keyword} Artist",
                    artists=[{"id": 1000 + i, "name": f"{keyword} Artist"}],
                    platform="netease",
                    platform_id=str(1000 + i),
                    album=f"{keyword} Album Vol.{i+1}",
                    duration=random.randint(120, 300),
                    cover_url=f"https://example.com/{keyword.lower()}-cover-{i+1}.jpg"
                )
                mock_songs.append(song)
            
            logger.info(f"[MOCK] Found {len(mock_songs)} mock songs")
            return mock_songs
        
        logger.info(f"Searching for: {keyword}")
        
        params = {
            "s": keyword,
            "type": 1,
            "limit": limit,
            "offset": 0
        }
        
        response = self._make_request(self.search_url, method="POST", data=params)
        if not response:
            logger.warning(f"No response for search: {keyword}")
            return []
        
        try:
            data = response.json()
            songs_data = data.get("result", {}).get("songs", [])
            songs = []
            
            for song_data in songs_data:
                # Parse artists
                artists = []
                for a in song_data.get("artists", []):
                    artists.append({"id": a["id"], "name": a["name"]})
                
                # Create Song object with correct field names
                song = Song(
                    id=str(song_data["id"]),
                    title=song_data["name"],
                    artist=artists[0]["name"] if artists else "",
                    artists=artists,
                    platform="netease",
                    platform_id=str(song_data["id"]),
                    album=song_data.get("album", {}).get("name"),
                    duration=song_data.get("duration", 0) // 1000,
                    cover_url=song_data.get("album", {}).get("picUrl")
                )
                songs.append(song)
            
            logger.info(f"Found {len(songs)} songs")
            return songs
            
        except Exception as e:
            logger.error(f"Failed to parse search results: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_comments(self, item_id: int, limit: int = 20, hot_only: bool = True, **kwargs) -> List[Comment]:
        """Get comments for a song."""
        if self.use_mock:
            logger.info(f"[MOCK] Getting comments for song ID: {item_id}")
            # Generate mock comments
            mock_comments = []
            comment_contents = [
                "This song is amazing!",
                "Love the melody and lyrics",
                "Best song I've heard this year",
                "The artist did a great job",
                "Can't stop listening to this",
                "Perfect for my playlist",
                "The beat is so catchy",
                "Emotional and powerful",
                "This brings back memories",
                "10/10 would recommend"
            ]
            
            for i in range(min(limit, len(comment_contents))):
                user = User(
                    user_id=1000 + i,
                    nickname=f"MockUser{i+1}",
                    avatar_url=f"https://example.com/avatar{i+1}.jpg",
                    signature=f"Music lover #{i+1}"
                )
                
                comment_time = datetime.now() - timedelta(days=random.randint(0, 30), 
                                                         hours=random.randint(0, 23))
                
                comment = Comment(
                    comment_id=str(2000 + i),
                    content=comment_contents[i],
                    user=user,
                    song_id=str(item_id),
                    platform="netease",
                    likes=random.randint(0, 1000),
                    time=comment_time,
                    is_hot=hot_only
                )
                mock_comments.append(comment)
            
            logger.info(f"[MOCK] Generated {len(mock_comments)} mock comments")
            return mock_comments
        
        logger.info(f"Getting comments for song ID: {item_id}")
        
        # Try multiple comment API endpoints
        endpoints = [
            f"https://music.163.com/api/v1/resource/comments/R_SO_4_{item_id}?limit={limit}",
            f"https://music.163.com/weapi/v1/resource/comments/R_SO_4_{item_id}?csrf_token=",
            f"https://netease-cloud-music-api-eight-ochre.vercel.app/comment/hot?id={item_id}",
            f"https://api.paugram.com/netease/comment/?id={item_id}&type=song"
        ]
        
        for url in endpoints:
            logger.debug(f"Trying endpoint: {url}")
            response = self._make_request(url, method="GET")
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Handle different response formats
                    comments_data = None
                    if "hotComments" in data:
                        comments_data = data.get("hotComments", [])
                    elif "comments" in data:
                        comments_data = data.get("comments", [])
                    elif "data" in data and "comments" in data["data"]:
                        comments_data = data["data"].get("comments", [])
                    
                    if comments_data:
                        comments = []
                        for comment_data in comments_data[:limit]:
                            from datetime import datetime
                            
                            # Handle different comment formats
                            if "user" in comment_data:
                                user_data = comment_data["user"]
                                user = User(
                                    user_id=user_data.get("userId", user_data.get("user_id", 0)),
                                    nickname=user_data.get("nickname", "Unknown"),
                                    avatar_url=user_data.get("avatarUrl"),
                                    signature=user_data.get("signature")
                                )
                                
                                comment_time = datetime.fromtimestamp(comment_data.get("time", 0) / 1000)
                                
                                comment = Comment(
                                    comment_id=str(comment_data.get("commentId", comment_data.get("comment_id", 0))),
                                    content=comment_data.get("content", ""),
                                    user=user,
                                    song_id=str(item_id),
                                    platform="netease",
                                    likes=comment_data.get("likedCount", comment_data.get("like_count", 0)),
                                    time=comment_time,
                                    is_hot=hot_only
                                )
                                comments.append(comment)
                        
                        logger.info(f"Got {len(comments)} comments from {url}")
                        return comments
                        
                except Exception as e:
                    logger.debug(f"Failed to parse response from {url}: {e}")
                    continue
        
        logger.warning(f"No comments found for song {item_id} from any endpoint")
        return []
    
    def search_and_get_comments(self, keyword: str, max_songs: int = 30) -> Dict[str, Any]:
        """Complete workflow: search and get comments for all songs."""
        songs = self.search(keyword, limit=max_songs)
        
        if not songs:
            logger.warning(f"No songs found for keyword: {keyword}")
            return {}
        
        result = {}
        for idx, song in enumerate(songs, 1):
            logger.info(f"Processing {idx}/{len(songs)}: {song.title}")
            
            comments = self.get_comments(int(song.id), limit=self.config.get("max_comments_per_song", 20))
            
            if comments:
                result[song.title] = {
                    "id": song.id,
                    "artist": song.artist,
                    "album": song.album,
                    "duration": song.duration,
                    "hot_comments": [
                        {
                            "user": c.user.nickname,
                            "content": c.content,
                            "likes": c.likes,
                            "time": c.time.isoformat() if hasattr(c.time, 'isoformat') else str(c.time)
                        }
                        for c in comments
                    ]
                }
                logger.info(f"  -> Got {len(comments)} comments for {song.title}")
            else:
                logger.info(f"  -> No comments found for {song.title}")
            
            # Only add delay in real mode (mock mode is instant)
            if not self.use_mock:
                self._delay()
        
        logger.info(f"Completed. Processed {len(result)} songs with comments")
        return result