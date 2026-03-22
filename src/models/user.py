"""
User data models for MusicFun project.

Contains Pydantic models for user data with validation and serialization.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict


class UserGender(str, Enum):
    """User gender enumeration."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class UserStatus(str, Enum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    DELETED = "deleted"
    VERIFIED = "verified"


class UserType(str, Enum):
    """User type enumeration."""
    NORMAL = "normal"
    VIP = "vip"
    ARTIST = "artist"
    CELEBRITY = "celebrity"
    OFFICIAL = "official"
    BOT = "bot"


class User(BaseModel):
    """
    User information model.
    
    Contains basic user information, profile data, and statistics.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )
    
    # Basic information
    id: str = Field(..., description="User ID (platform unique identifier)")
    username: str = Field(..., description="Username")
    nickname: Optional[str] = Field(None, description="Nickname or display name")
    
    # Platform information
    platform: str = Field(..., description="Platform name")
    platform_id: str = Field(..., description="Original platform ID")
    
    # Profile information
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    cover_url: Optional[str] = Field(None, description="Cover image URL")
    bio: Optional[str] = Field(None, description="Biography or description")
    gender: UserGender = Field(UserGender.UNKNOWN, description="Gender")
    birthday: Optional[datetime] = Field(None, description="Birthday")
    location: Optional[str] = Field(None, description="Location")
    
    # Contact information
    email: Optional[str] = Field(None, description="Email address")
    website: Optional[str] = Field(None, description="Website URL")
    social_links: Dict[str, str] = Field(default_factory=dict, description="Social media links")
    
    # User type and status
    user_type: UserType = Field(UserType.NORMAL, description="User type")
    status: UserStatus = Field(UserStatus.ACTIVE, description="User status")
    is_verified: bool = Field(False, description="Is verified user")
    verification_reason: Optional[str] = Field(None, description="Verification reason")
    
    # Statistics
    follower_count: int = Field(0, description="Follower count")
    following_count: int = Field(0, description="Following count")
    song_count: int = Field(0, description="Song count")
    playlist_count: int = Field(0, description="Playlist count")
    album_count: int = Field(0, description="Album count")
    like_count: int = Field(0, description="Total likes received")
    comment_count: int = Field(0, description="Comment count")
    
    # Level and badges
    level: Optional[int] = Field(None, description="User level")
    experience: Optional[int] = Field(None, description="Experience points")
    badges: List[str] = Field(default_factory=list, description="Badges")
    
    # Timestamps
    created_at: datetime = Field(..., description="Account creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    last_login_at: Optional[datetime] = Field(None, description="Last login time")
    crawled_at: Optional[datetime] = Field(None, description="Crawl time")
    
    # Extended data
    tags: List[str] = Field(default_factory=list, description="Tags")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Raw data")
    
    @field_validator('follower_count', 'following_count', 'song_count', 'playlist_count', 
                     'album_count', 'like_count', 'comment_count')
    @classmethod
    def validate_counts(cls, v: int) -> int:
        """Validate count values."""
        if v < 0:
            raise ValueError('Count must be non-negative')
        return v
    
    @field_validator('level', 'experience')
    @classmethod
    def validate_level_experience(cls, v: Optional[int]) -> Optional[int]:
        """Validate level and experience."""
        if v is not None and v < 0:
            raise ValueError('Level/experience must be non-negative')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Basic email validation."""
        if v is not None and '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    def get_display_name(self) -> str:
        """Get display name (nickname or username)."""
        return self.nickname or self.username
    
    def get_gender_display(self) -> str:
        """Get gender display name."""
        gender_names = {
            UserGender.MALE: "Male",
            UserGender.FEMALE: "Female",
            UserGender.OTHER: "Other",
            UserGender.UNKNOWN: "Unknown"
        }
        return gender_names.get(self.gender, "Unknown")
    
    def get_user_type_display(self) -> str:
        """Get user type display name."""
        type_names = {
            UserType.NORMAL: "Normal User",
            UserType.VIP: "VIP User",
            UserType.ARTIST: "Artist",
            UserType.CELEBRITY: "Celebrity",
            UserType.OFFICIAL: "Official Account",
            UserType.BOT: "Bot"
        }
        return type_names.get(self.user_type, "Unknown")
    
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = False) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(exclude_none=exclude_none)
    
    def summary(self) -> str:
        """Get user summary."""
        display_name = self.get_display_name()
        verified = "✓ " if self.is_verified else ""
        return f"{verified}{display_name} ({self.follower_count} followers, {self.get_user_type_display()})"
    
    def calculate_engagement_rate(self) -> float:
        """Calculate engagement rate (likes per follower)."""
        if self.follower_count == 0:
            return 0.0
        return round(self.like_count / self.follower_count * 100, 2)
    
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


class UserProfile(BaseModel):
    """User profile with detailed information."""
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )
    
    user: User = Field(..., description="User information")
    
    # Detailed statistics
    total_listen_time: int = Field(0, description="Total listen time in seconds")
    favorite_genres: List[str] = Field(default_factory=list, description="Favorite genres")
    favorite_artists: List[str] = Field(default_factory=list, description="Favorite artists")
    recently_played: List[Dict[str, Any]] = Field(default_factory=list, description="Recently played songs")
    
    # Achievements
    achievements: List[Dict[str, Any]] = Field(default_factory=list, description="Achievements")
    
    # Privacy settings
    is_public: bool = Field(True, description="Is profile public")
    show_location: bool = Field(False, description="Show location")
    show_birthday: bool = Field(False, description="Show birthday")
    
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = False) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(exclude_none=exclude_none)
    
    def get_listen_time_formatted(self) -> str:
        """Get formatted listen time."""
        hours = self.total_listen_time // 3600
        minutes = (self.total_listen_time % 3600) // 60
        seconds = self.total_listen_time % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"


# Example usage
if __name__ == "__main__":
    # Create example user
    example_user = User(
        id="netease_user_123",
        username="music_fan",
        nickname="Music Fan",
        platform="netease",
        platform_id="123456",
        avatar_url="https://example.com/avatar.jpg",
        bio="Love music and exploring new artists!",
        gender=UserGender.MALE,
        location="Beijing, China",
        user_type=UserType.VIP,
        is_verified=True,
        verification_reason="Music influencer",
        follower_count=5000,
        following_count=200,
        song_count=150,
        playlist_count=25,
        like_count=10000,
        created_at=datetime.now()
    )
    
    print("User created successfully!")
    print(f"Display name: {example_user.get_display_name()}")
    print(f"Verified: {example_user.is_verified}")
    print(f"Followers: {example_user.follower_count}")
    print(f"Following: {example_user.following_count}")
    print(f"Engagement rate: {example_user.calculate_engagement_rate()}%")
    print(f"Summary: {example_user.summary()}")
    
    # Test JSON serialization
    json_data = example_user.to_json()
    print(f"\nJSON representation (first 200 chars):\n{json_data[:200]}...")
    
    # Test timestamp conversion
    timestamp = 946684800000  # 2000-01-01 00:00:00 in milliseconds
    dt = User.from_milliseconds_timestamp(timestamp, "birthday")
    print(f"\nTimestamp conversion: {timestamp} -> {dt}")
    
    # Test user profile
    user_profile = UserProfile(
        user=example_user,
        total_listen_time=3600 * 100 + 1800,  # 100.5 hours
        favorite_genres=["Pop", "Rock", "Jazz"],
        favorite_artists=["Artist1", "Artist2", "Artist3"],
        recently_played=[
            {"song_id": "song1", "title": "Song One", "play_count": 10},
            {"song_id": "song2", "title": "Song Two", "play_count": 5}
        ]
    )
    
    print(f"\nUser Profile:")
    print(f"Total listen time: {user_profile.get_listen_time_formatted()}")
    print(f"Favorite genres: {', '.join(user_profile.favorite_genres)}")
    
    # Test validation
    try:
        invalid_user = User(
            id="test",
            username="test",
            platform="test",
            platform_id="test",
            follower_count=-10  # Invalid count
        )
    except ValueError as e:
        print(f"\nValidation works: {e}")