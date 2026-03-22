"""
Netease Music crawler with mock support.
All output in English, ASCII only.
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from src.core.base_crawler import BaseCrawler
from src.models.song import Song
from src.models.comment import Comment, CommentType, CommentStatus
from src.models.user import User, UserType, UserGender, UserStatus
from datetime import datetime
import random


class NeteaseCrawler(BaseCrawler):
    """Netease Music crawler with mock support."""

    def __init__(self, use_mock: bool = False):
        """Initialize Netease crawler."""
        from config.settings import NETEASE_CONFIG, CRAWLER_CONFIG
        config = {**NETEASE_CONFIG, **CRAWLER_CONFIG}

        self.search_url = config.get("search_url", "https://music.163.com/api/search/get/")
        self.use_mock = use_mock

        super().__init__(config)
        logger.info(f"NeteaseCrawler initialized (mock mode: {use_mock})")

    def search(self, keyword: str, limit: int = 50, **kwargs) -> List[Song]:
        """Search for songs."""
        logger.info(f"Searching: {keyword}")

        params = {"s": keyword, "type": 1, "limit": limit, "offset": 0}
        response = self._make_request(self.search_url, method="POST", data=params)

        if not response:
            logger.warning(f"No response for search: {keyword}")
            return []

        try:
            data = response.json()
            songs_data = data.get("result", {}).get("songs", [])
            songs = []

            for song_data in songs_data:
                artists = [{"id": a["id"], "name": a["name"]} for a in song_data.get("artists", [])]
                songs.append(Song(
                    id=str(song_data["id"]),
                    title=song_data["name"],
                    artist=artists[0]["name"] if artists else "",
                    artists=artists,
                    platform="netease",
                    platform_id=str(song_data["id"]),
                    album=song_data.get("album", {}).get("name"),
                    duration=song_data.get("duration", 0) // 1000,
                    cover_url=song_data.get("album", {}).get("picUrl")
                ))

            logger.info(f"Found {len(songs)} songs")
            return songs
        except Exception as e:
            logger.error(f"Failed to parse search results: {e}")
            return []

    def _generate_mock_comments(self, song_id: int, limit: int) -> List[Comment]:
        """Generate realistic mock comments."""
        mock_comments = [
            ("music_lover", "This is absolutely beautiful! The melody is haunting.", 234),
            ("critic_123", "Excellent production quality. The arrangement is top tier.", 156),
            ("night_owl", "Perfect song for late night listening sessions.", 89),
            ("fan_2024", "Can't stop playing this. Another masterpiece!", 445),
            ("first_listener", "Just discovered this and I'm obsessed.", 67),
        ]

        comments = []
        for i, (nickname, content, likes) in enumerate(mock_comments[:limit]):
            # Create User with all required fields
            user = User(
                id=f"mock_user_{10000 + i}",
                username=nickname,
                nickname=nickname,
                platform="netease",
                platform_id=str(10000 + i),
                avatar_url=f"https://avatar.example.com/{nickname}.jpg",
                bio="Music enthusiast and frequent listener",
                gender=UserGender.UNKNOWN,
                location="Unknown",
                user_type=UserType.NORMAL,
                status=UserStatus.ACTIVE,
                is_verified=False,
                follower_count=random.randint(100, 10000),
                following_count=random.randint(50, 500),
                song_count=random.randint(10, 200),
                playlist_count=random.randint(1, 20),
                album_count=random.randint(0, 10),
                like_count=random.randint(500, 5000),
                comment_count=random.randint(50, 500),
                created_at=datetime.now(),
                crawled_at=datetime.now()
            )

            # Create Comment with all required fields
            comment = Comment(
                id=str(100000 + i + song_id),  # Unique comment ID
                content=content,
                target_id=str(song_id),  # The song ID
                target_type=CommentType.SONG,  # Type is song
                platform="netease",
                user_id=user.id,  # User ID
                username=user.username,  # Username
                user_avatar=user.avatar_url,  # User avatar
                user_level=random.randint(1, 10),  # Random user level
                like_count=likes,  # Like count
                reply_count=random.randint(0, 20),  # Random reply count
                share_count=random.randint(0, 10),  # Random share count
                parent_id=None,  # No parent for top-level comments
                root_id=None,  # No root for top-level comments
                is_hot=True,  # Mark as hot comment
                is_top=False,  # Not top comment
                is_owner=False,  # Not content owner
                status=CommentStatus.ACTIVE,  # Active status
                created_at=datetime.now(),  # Creation time
                updated_at=None,  # No updates
                crawled_at=datetime.now()  # Crawl time
            )
            comments.append(comment)

        logger.info(f"Generated {len(comments)} mock comments")
        return comments

    def get_comments(self, item_id: int, limit: int = 20, hot_only: bool = True, **kwargs) -> List[Comment]:
        """Get comments with fallback to mock."""
        logger.info(f"Getting comments for song: {item_id}")

        if self.use_mock:
            return self._generate_mock_comments(item_id, limit)

        # Real API attempts would go here
        logger.warning(f"No real API available, using mock for {item_id}")
        return self._generate_mock_comments(item_id, limit)

    def search_and_get_comments(self, keyword: str, max_songs: int = 30) -> Dict[str, Any]:
        """Complete workflow: search and get comments."""
        songs = self.search(keyword, limit=max_songs)

        if not songs:
            logger.warning(f"No songs found for keyword: {keyword}")
            return {}

        result = {}
        for idx, song in enumerate(songs, 1):
            logger.info(f"Processing {idx}/{len(songs)}: {song.title}")
            comments = self.get_comments(int(song.id), limit=self.config.get("max_comments_per_song", 10))

            result[song.title] = {
                "id": song.id,
                "artist": song.artist,
                "album": song.album,
                "duration": song.duration,
                "hot_comments": [
                    {
                        "user_id": c.user_id,
                        "username": c.username,
                        "content": c.content,
                        "likes": c.like_count,
                        "time": c.created_at.isoformat() if hasattr(c.created_at, 'isoformat') else str(c.created_at)
                    }
                    for c in comments
                ]
            }
            self._delay()

        logger.info(f"Completed. Processed {len(result)} songs")
        return result

    def get_song(self, song_id: int) -> Optional[Song]:
        """Required abstract method."""
        return None

    def get_user(self, user_id: int) -> Optional[User]:
        """Required abstract method."""
        return None