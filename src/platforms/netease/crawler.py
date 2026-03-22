"""
Netease Music crawler with real API and mock support.
All output in English, ASCII only.
"""
from typing import List, Dict, Any, Optional
from src.core.logger import get_logger
logger = get_logger()
from src.core.base_crawler import BaseCrawler
from src.models.song import Song
from src.models.comment import Comment, CommentType, CommentStatus
from src.models.user import User, UserType, UserGender, UserStatus
from datetime import datetime
import random
import requests


class NeteaseCrawler(BaseCrawler):
    """Netease Music crawler with real API and mock support."""

    def __init__(self, use_mock: bool = False, api_url: str = "http://localhost:3000"):
        """Initialize Netease crawler."""
        from config.settings import NETEASE_CONFIG, CRAWLER_CONFIG
        config = {**NETEASE_CONFIG, **CRAWLER_CONFIG}

        self.search_url = config.get("search_url", "https://music.163.com/api/search/get/")
        self.use_mock = use_mock
        self.api_url = api_url

        super().__init__(config)
        logger.info(f"NeteaseCrawler initialized (mock mode: {use_mock}, api: {api_url})")

    def search(self, keyword: str, limit: int = 50, **kwargs) -> List[Song]:
        """Search for songs."""
        logger.info(f"Searching: {keyword}")

        # Try local API first
        if not self.use_mock:
            try:
                url = f"{self.api_url}/search?keywords={keyword}&limit={limit}"
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 200:
                        songs_data = data.get('result', {}).get('songs', [])
                        if songs_data:
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
                            logger.info(f"Found {len(songs)} songs from local API")
                            return songs
            except Exception as e:
                logger.warning(f"Local API search failed: {e}, falling back to direct search")

        # Fallback to direct search (original method)
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

            logger.info(f"Found {len(songs)} songs from direct search")
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
                id=f"mock_user_{10000 + i}",
                username=nickname,
                nickname=nickname,
                platform="netease",
                platform_id=str(10000 + i),
                avatar_url=f"https://avatar.example.com/{nickname}.jpg",
                bio="Music enthusiast",
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

            comment = Comment(
                id=str(100000 + i + song_id),
                content=content,
                target_id=str(song_id),
                target_type=CommentType.SONG,
                platform="netease",
                user_id=user.id,
                username=user.username,
                user_avatar=user.avatar_url,
                user_level=random.randint(1, 10),
                like_count=likes,
                reply_count=random.randint(0, 20),
                share_count=random.randint(0, 10),
                parent_id=None,
                root_id=None,
                is_hot=True,
                is_top=False,
                is_owner=False,
                status=CommentStatus.ACTIVE,
                created_at=datetime.now(),
                updated_at=None,
                crawled_at=datetime.now()
            )
            comments.append(comment)

        logger.info(f"Generated {len(comments)} mock comments")
        return comments

    def get_comments(self, item_id: int, limit: int = 20, hot_only: bool = True, **kwargs) -> List[Comment]:
        """Get comments from local Netease API or fallback to mock."""
        logger.info(f"Getting comments for song: {item_id}")

        # Try local API if not in mock mode
        if not self.use_mock:
            try:
                # Use the working /comment/music endpoint
                url = f"{self.api_url}/comment/music?id={item_id}&limit={limit}"
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    # Get comments based on hot_only flag
                    if hot_only:
                        comments_data = data.get('hotComments', [])
                    else:
                        comments_data = data.get('comments', [])

                    if comments_data:
                        comments = []
                        for cd in comments_data[:limit]:
                            # Parse user data
                            user_data = cd.get('user', {})

                            user = User(
                                id=str(user_data.get('userId', 0)),
                                username=user_data.get('nickname', 'Unknown'),
                                nickname=user_data.get('nickname'),
                                platform="netease",
                                platform_id=str(user_data.get('userId', 0)),
                                avatar_url=user_data.get('avatarUrl'),
                                bio=user_data.get('signature'),
                                gender=UserGender.UNKNOWN,
                                user_type=UserType.NORMAL,
                                status=UserStatus.ACTIVE,
                                follower_count=user_data.get('followeds', 0),
                                following_count=user_data.get('follows', 0),
                                created_at=datetime.now(),
                                crawled_at=datetime.now()
                            )

                            # Create comment
                            comment = Comment(
                                id=str(cd.get('commentId', 0)),
                                content=cd.get('content', ''),
                                target_id=str(item_id),
                                target_type=CommentType.SONG,
                                platform="netease",
                                user_id=user.id,
                                username=user.username,
                                user_avatar=user.avatar_url,
                                user_level=user_data.get('level', 1),
                                like_count=cd.get('likedCount', 0),
                                reply_count=cd.get('replyCount', 0),
                                share_count=cd.get('shareCount', 0),
                                parent_id=str(cd.get('parentCommentId')) if cd.get('parentCommentId') else None,
                                root_id=str(cd.get('rootCommentId')) if cd.get('rootCommentId') else None,
                                is_hot=hot_only,
                                is_top=cd.get('isTop', False),
                                is_owner=cd.get('isOwner', False),
                                status=CommentStatus.ACTIVE,
                                created_at=datetime.fromtimestamp(cd.get('time', 0) / 1000),
                                updated_at=None,
                                crawled_at=datetime.now()
                            )
                            comments.append(comment)

                        logger.info(f"Got {len(comments)} real comments from local API")
                        return comments
                    else:
                        logger.info(f"No comments found for song {item_id}")
                else:
                    logger.warning(f"API returned status {response.status_code} for song {item_id}")

            except requests.exceptions.ConnectionError:
                logger.warning(f"Cannot connect to local API at {self.api_url}")
            except Exception as e:
                logger.error(f"Failed to get comments from API: {e}")

        # Fallback to mock comments
        logger.info(f"Using mock comments for song {item_id}")
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