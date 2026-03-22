"""
Song data models for MusicFun project.

Contains Pydantic models for song data with validation and serialization.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict


class Platform(str, Enum):
    """Music platform enumeration."""
    NETEASE = "netease"
    QQ = "qq"
    KUGOU = "kugou"
    KUWO = "kuwo"
    SPOTIFY = "spotify"
    YOUTUBE = "youtube"
    OTHER = "other"


class SongStatus(str, Enum):
    """Song status enumeration."""
    ACTIVE = "active"
    DELETED = "deleted"
    UNAVAILABLE = "unavailable"
    COPYRIGHT = "copyright"


class Song(BaseModel):
    """
    Song information model.
    
    Contains basic song information, statistics, and metadata.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )
    
    # Basic information
    id: str = Field(..., description="Song ID (platform unique identifier)")
    title: str = Field(..., description="Song title")
    artist: str = Field(..., description="Artist/singer name")
    album: Optional[str] = Field(None, description="Album name")
    
    # Platform information
    platform: Platform = Field(..., description="Music platform")
    platform_id: str = Field(..., description="Original platform ID")
    url: Optional[str] = Field(None, description="Song URL")
    
    # Metadata
    duration: Optional[int] = Field(None, description="Duration in seconds")
    bitrate: Optional[int] = Field(None, description="Bitrate in kbps")
    format: Optional[str] = Field(None, description="Audio format")
    release_date: Optional[datetime] = Field(None, description="Release date")
    language: Optional[str] = Field(None, description="Language")
    genre: Optional[str] = Field(None, description="Genre")
    
    # Statistics
    play_count: Optional[int] = Field(0, description="Play count")
    like_count: Optional[int] = Field(0, description="Like count")
    comment_count: Optional[int] = Field(0, description="Comment count")
    share_count: Optional[int] = Field(0, description="Share count")
    download_count: Optional[int] = Field(0, description="Download count")
    
    # Ranking information
    rank: Optional[int] = Field(None, description="Rank position")
    rank_category: Optional[str] = Field(None, description="Rank category")
    rank_change: Optional[int] = Field(None, description="Rank change")
    
    # Lyric information
    has_lyric: bool = Field(False, description="Has lyrics")
    lyric_language: Optional[str] = Field(None, description="Lyric language")
    
    # Status information
    status: SongStatus = Field(SongStatus.ACTIVE, description="Song status")
    available: bool = Field(True, description="Is available")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Update time")
    crawled_at: Optional[datetime] = Field(None, description="Crawl time")
    
    # Extended data
    tags: List[str] = Field(default_factory=list, description="Tags")
    features: Dict[str, Any] = Field(default_factory=dict, description="Feature data")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Raw data")
    
    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v: Optional[int]) -> Optional[int]:
        """Validate duration."""
        if v is not None and v < 0:
            raise ValueError('Duration must be positive')
        return v
    
    @field_validator('play_count', 'like_count', 'comment_count', 'share_count', 'download_count')
    @classmethod
    def validate_counts(cls, v: Optional[int]) -> Optional[int]:
        """Validate count values."""
        if v is not None and v < 0:
            raise ValueError('Count must be non-negative')
        return v
    
    @field_validator('bitrate')
    @classmethod
    def validate_bitrate(cls, v: Optional[int]) -> Optional[int]:
        """Validate bitrate."""
        if v is not None and v <= 0:
            raise ValueError('Bitrate must be positive')
        return v
    
    def get_duration_formatted(self) -> Optional[str]:
        """Get formatted duration string."""
        if self.duration is None:
            return None
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
    
    def get_platform_name(self) -> str:
        """Get platform display name."""
        platform_names = {
            Platform.NETEASE: "Netease Music",
            Platform.QQ: "QQ Music",
            Platform.KUGOU: "Kugou Music",
            Platform.KUWO: "Kuwo Music",
            Platform.SPOTIFY: "Spotify",
            Platform.YOUTUBE: "YouTube Music",
            Platform.OTHER: "Other Platform"
        }
        return platform_names.get(self.platform, "Unknown Platform")
    
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = False) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(exclude_none=exclude_none)
    
    def summary(self) -> str:
        """Get song summary."""
        duration_str = self.get_duration_formatted() or "Unknown duration"
        return f"{self.title} - {self.artist} ({duration_str}, {self.get_platform_name()})"
    
    @classmethod
    def from_milliseconds_timestamp(cls, timestamp: Optional[int], field_name: str = "timestamp") -> Optional[datetime]:
        """Convert milliseconds timestamp to datetime."""
        if timestamp is None:
            return None
        try:
            # Convert milliseconds to seconds
            return datetime.fromtimestamp(timestamp / 1000)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid timestamp for {field_name}: {timestamp}") from e


class SongList(BaseModel):
    """Song list model."""
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )
    
    songs: List[Song] = Field(default_factory=list, description="List of songs")
    total: int = Field(0, description="Total count")
    page: Optional[int] = Field(None, description="Page number")
    page_size: Optional[int] = Field(None, description="Page size")
    has_more: bool = Field(False, description="Has more pages")
    
    def add_song(self, song: Song) -> None:
        """Add a song to the list."""
        self.songs.append(song)
        self.total = len(self.songs)
    
    def get_song_by_id(self, song_id: str) -> Optional[Song]:
        """Get song by ID."""
        for song in self.songs:
            if song.id == song_id:
                return song
        return None
    
    def filter_by_platform(self, platform: Platform) -> List[Song]:
        """Filter songs by platform."""
        return [song for song in self.songs if song.platform == platform]
    
    def filter_by_artist(self, artist: str) -> List[Song]:
        """Filter songs by artist."""
        return [song for song in self.songs if song.artist.lower() == artist.lower()]
    
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = False) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(exclude_none=exclude_none)


# Example usage
if __name__ == "__main__":
    # Create example song
    example_song = Song(
        id="netease_123456",
        title="Example Song",
        artist="Example Artist",
        album="Example Album",
        platform=Platform.NETEASE,
        platform_id="123456",
        duration=180,  # 3 minutes
        play_count=1000,
        like_count=500,
        comment_count=200
    )
    
    print("Song created successfully!")
    print(f"Title: {example_song.title}")
    print(f"Artist: {example_song.artist}")
    print(f"Platform: {example_song.get_platform_name()}")
    print(f"Duration: {example_song.get_duration_formatted()}")
    print(f"Summary: {example_song.summary()}")
    
    # Test JSON serialization
    json_data = example_song.to_json()
    print(f"\nJSON representation:\n{json_data[:200]}...")
    
    # Test timestamp conversion
    timestamp = 1672531200000  # 2023-01-01 00:00:00 in milliseconds
    dt = Song.from_milliseconds_timestamp(timestamp, "release_date")
    print(f"\nTimestamp conversion: {timestamp} -> {dt}")
    
    # Test validation
    try:
        invalid_song = Song(
            id="test",
            title="Test",
            artist="Test",
            platform=Platform.NETEASE,
            platform_id="test",
            duration=-10  # Invalid duration
        )
    except ValueError as e:
        print(f"\nValidation works: {e}")