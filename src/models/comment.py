"""
Comment data models for MusicFun project.

Contains Pydantic models for comment data with validation and serialization.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CommentType(str, Enum):
    """Comment type enumeration."""
    SONG = "song"
    PLAYLIST = "playlist"
    ALBUM = "album"
    ARTIST = "artist"
    USER = "user"
    OTHER = "other"


class CommentStatus(str, Enum):
    """Comment status enumeration."""
    ACTIVE = "active"
    DELETED = "deleted"
    HIDDEN = "hidden"
    REPORTED = "reported"
    REVIEW = "review"


class Comment(BaseModel):
    """
    Comment information model.
    
    Contains comment data, user information, and engagement metrics.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )
    
    # Basic information
    id: str = Field(..., description="Comment ID (platform unique identifier)")
    content: str = Field(..., description="Comment content")
    
    # Target information
    target_id: str = Field(..., description="Target ID (song, playlist, etc.)")
    target_type: CommentType = Field(..., description="Target type")
    platform: str = Field(..., description="Platform name")
    
    # User information
    user_id: str = Field(..., description="User ID")
    username: Optional[str] = Field(None, description="Username")
    user_avatar: Optional[str] = Field(None, description="User avatar URL")
    user_level: Optional[int] = Field(None, description="User level")
    
    # Engagement metrics
    like_count: int = Field(0, description="Like count")
    reply_count: int = Field(0, description="Reply count")
    share_count: int = Field(0, description="Share count")
    
    # Parent comment (for replies)
    parent_id: Optional[str] = Field(None, description="Parent comment ID")
    root_id: Optional[str] = Field(None, description="Root comment ID")
    
    # Metadata
    is_hot: bool = Field(False, description="Is hot comment")
    is_top: bool = Field(False, description="Is top comment")
    is_owner: bool = Field(False, description="Is content owner")
    
    # Status
    status: CommentStatus = Field(CommentStatus.ACTIVE, description="Comment status")
    
    # Timestamps
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Update time")
    crawled_at: Optional[datetime] = Field(None, description="Crawl time")
    
    # Location information
    ip_location: Optional[str] = Field(None, description="IP location")
    device: Optional[str] = Field(None, description="Device information")
    
    # Extended data
    tags: List[str] = Field(default_factory=list, description="Tags")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Raw data")
    
    @field_validator('like_count', 'reply_count', 'share_count')
    @classmethod
    def validate_counts(cls, v: int) -> int:
        """Validate count values."""
        if v < 0:
            raise ValueError('Count must be non-negative')
        return v
    
    @field_validator('user_level')
    @classmethod
    def validate_user_level(cls, v: Optional[int]) -> Optional[int]:
        """Validate user level."""
        if v is not None and v < 0:
            raise ValueError('User level must be non-negative')
        return v
    
    def is_reply(self) -> bool:
        """Check if this is a reply comment."""
        return self.parent_id is not None
    
    def get_target_type_name(self) -> str:
        """Get target type display name."""
        type_names = {
            CommentType.SONG: "Song",
            CommentType.PLAYLIST: "Playlist",
            CommentType.ALBUM: "Album",
            CommentType.ARTIST: "Artist",
            CommentType.USER: "User",
            CommentType.OTHER: "Other"
        }
        return type_names.get(self.target_type, "Unknown")
    
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = False) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(exclude_none=exclude_none)
    
    def summary(self) -> str:
        """Get comment summary."""
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        username = self.username or f"User {self.user_id[:8]}"
        return f"{username}: {content_preview} ({self.like_count} likes)"
    
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


class CommentList(BaseModel):
    """Comment list model."""
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )
    
    comments: List[Comment] = Field(default_factory=list, description="List of comments")
    total: int = Field(0, description="Total count")
    page: Optional[int] = Field(None, description="Page number")
    page_size: Optional[int] = Field(None, description="Page size")
    has_more: bool = Field(False, description="Has more pages")
    target_id: Optional[str] = Field(None, description="Target ID")
    target_type: Optional[CommentType] = Field(None, description="Target type")
    
    def add_comment(self, comment: Comment) -> None:
        """Add a comment to the list."""
        self.comments.append(comment)
        self.total = len(self.comments)
    
    def get_comment_by_id(self, comment_id: str) -> Optional[Comment]:
        """Get comment by ID."""
        for comment in self.comments:
            if comment.id == comment_id:
                return comment
        return None
    
    def filter_by_user(self, user_id: str) -> List[Comment]:
        """Filter comments by user ID."""
        return [comment for comment in self.comments if comment.user_id == user_id]
    
    def filter_hot_comments(self) -> List[Comment]:
        """Filter hot comments."""
        return [comment for comment in self.comments if comment.is_hot]
    
    def filter_top_comments(self) -> List[Comment]:
        """Filter top comments."""
        return [comment for comment in self.comments if comment.is_top]
    
    def get_replies(self, comment_id: str) -> List[Comment]:
        """Get replies for a comment."""
        return [comment for comment in self.comments if comment.parent_id == comment_id]
    
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = False) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(exclude_none=exclude_none)
    
    def sort_by_likes(self, descending: bool = True) -> None:
        """Sort comments by like count."""
        self.comments.sort(key=lambda x: x.like_count, reverse=descending)
    
    def sort_by_time(self, descending: bool = True) -> None:
        """Sort comments by creation time."""
        self.comments.sort(key=lambda x: x.created_at, reverse=descending)


# Example usage
if __name__ == "__main__":
    # Create example comment
    example_comment = Comment(
        id="netease_comment_123",
        content="This is a great song! I really enjoy the melody and lyrics.",
        target_id="netease_song_456",
        target_type=CommentType.SONG,
        platform="netease",
        user_id="user_789",
        username="MusicLover",
        like_count=150,
        reply_count=12,
        created_at=datetime.now()
    )
    
    print("Comment created successfully!")
    print(f"User: {example_comment.username}")
    print(f"Content: {example_comment.content[:50]}...")
    print(f"Likes: {example_comment.like_count}")
    print(f"Summary: {example_comment.summary()}")
    
    # Test JSON serialization
    json_data = example_comment.to_json()
    print(f"\nJSON representation:\n{json_data[:200]}...")
    
    # Test timestamp conversion
    timestamp = 1672531200000  # 2023-01-01 00:00:00 in milliseconds
    dt = Comment.from_milliseconds_timestamp(timestamp, "created_at")
    print(f"\nTimestamp conversion: {timestamp} -> {dt}")
    
    # Test reply comment
    reply_comment = Comment(
        id="netease_comment_124",
        content="I agree with you!",
        target_id="netease_song_456",
        target_type=CommentType.SONG,
        platform="netease",
        user_id="user_999",
        username="AnotherFan",
        parent_id="netease_comment_123",
        like_count=25,
        created_at=datetime.now()
    )
    
    print(f"\nReply comment is reply: {reply_comment.is_reply()}")
    print(f"Parent ID: {reply_comment.parent_id}")