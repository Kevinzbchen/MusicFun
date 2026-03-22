"""
Netease Music crawler with mock support.
All output in English, ASCII only.
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from src.core.base_crawler import BaseCrawler
from src.models.song import Song
from src.models.comment import Comment
from src.models.user import User
from datetime import datetime


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
            user = User(
                user_id=10000 + i,
                nickname=nickname,
                avatar_url=None,
                signature="Music enthusiast"
            )
            comment = Comment(
                comment_id=str(100000 + i + song_id),
                content=content,
                user=user,
                song_id=str(song_id),
                platform="netease",
                likes=likes,
                time=datetime.now(),
                is_hot=True
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
                        "user": c.user.nickname,
                        "content": c.content,
                        "likes": c.likes,
                        "time": c.time.isoformat() if hasattr(c.time, 'isoformat') else str(c.time)
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