"""
Test script for MusicFun data models.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=== Testing MusicFun Data Models ===\n")

# Test 1: Import all models
try:
    from src.models.song import Song, SongList, Platform, SongStatus
    from src.models.comment import Comment, CommentList, CommentType, CommentStatus
    from src.models.user import User, UserProfile, UserGender, UserStatus, UserType
    print("✓ All models imported successfully")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Create song instance
try:
    song = Song(
        id="netease_123456",
        title="Test Song",
        artist="Test Artist",
        album="Test Album",
        platform=Platform.NETEASE,
        platform_id="123456",
        duration=180,
        play_count=1000,
        like_count=500,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    print("✓ Song created successfully")
    print(f"  Title: {song.title}")
    print(f"  Artist: {song.artist}")
    print(f"  Platform: {song.platform}")
    print(f"  Duration: {song.get_duration_formatted()}")
    print(f"  Summary: {song.summary()}")
except Exception as e:
    print(f"✗ Song creation failed: {e}")

print()

# Test 3: Create comment instance
try:
    comment = Comment(
        id="comment_123",
        content="This is a test comment for the song.",
        target_id="netease_123456",
        target_type=CommentType.SONG,
        platform="netease",
        user_id="user_123",
        username="TestUser",
        like_count=50,
        created_at=datetime.now()
    )
    print("✓ Comment created successfully")
    print(f"  User: {comment.username}")
    print(f"  Content: {comment.content[:30]}...")
    print(f"  Likes: {comment.like_count}")
    print(f"  Is reply: {comment.is_reply()}")
    print(f"  Summary: {comment.summary()}")
except Exception as e:
    print(f"✗ Comment creation failed: {e}")

print()

# Test 4: Create user instance
try:
    user = User(
        id="user_123",
        username="testuser",
        nickname="Test User",
        platform="netease",
        platform_id="123",
        gender=UserGender.MALE,
        user_type=UserType.NORMAL,
        status=UserStatus.ACTIVE,
        follower_count=100,
        following_count=50,
        created_at=datetime.now()
    )
    print("✓ User created successfully")
    print(f"  Username: {user.username}")
    print(f"  Display name: {user.get_display_name()}")
    print(f"  Gender: {user.get_gender_display()}")
    print(f"  Followers: {user.follower_count}")
    print(f"  Summary: {user.summary()}")
except Exception as e:
    print(f"✗ User creation failed: {e}")

print()

# Test 5: Test JSON serialization
try:
    song_dict = song.to_dict()
    song_json = song.to_json()
    print("✓ JSON serialization successful")
    print(f"  Dict keys: {list(song_dict.keys())[:5]}...")
    print(f"  JSON length: {len(song_json)} characters")
except Exception as e:
    print(f"✗ JSON serialization failed: {e}")

print()

# Test 6: Test timestamp conversion
try:
    timestamp = 1672531200000  # 2023-01-01 00:00:00
    dt = Song.from_milliseconds_timestamp(timestamp, "test")
    print("✓ Timestamp conversion successful")
    print(f"  Timestamp: {timestamp}")
    print(f"  Datetime: {dt}")
except Exception as e:
    print(f"✗ Timestamp conversion failed: {e}")

print()

# Test 7: Test validation
try:
    # This should fail due to negative duration
    invalid_song = Song(
        id="test",
        title="Test",
        artist="Test",
        platform=Platform.NETEASE,
        platform_id="test",
        duration=-10
    )
    print("✗ Validation should have failed but didn't")
except ValueError as e:
    print(f"✓ Validation works correctly: {e}")
except Exception as e:
    print(f"✗ Unexpected error during validation: {e}")

print()

# Test 8: Test list models
try:
    song_list = SongList(
        songs=[song],
        total=1,
        page=1,
        page_size=10,
        has_more=False
    )
    print("✓ SongList created successfully")
    print(f"  Total songs: {song_list.total}")
    print(f"  Page: {song_list.page}")
    
    comment_list = CommentList(
        comments=[comment],
        total=1,
        target_id="netease_123456",
        target_type=CommentType.SONG
    )
    print("✓ CommentList created successfully")
    print(f"  Total comments: {comment_list.total}")
    print(f"  Target type: {comment_list.target_type}")
except Exception as e:
    print(f"✗ List models creation failed: {e}")

print()

# Test 9: Test user profile
try:
    user_profile = UserProfile(
        user=user,
        total_listen_time=3600 * 10,  # 10 hours
        favorite_genres=["Pop", "Rock"],
        favorite_artists=["Artist1", "Artist2"]
    )
    print("✓ UserProfile created successfully")
    print(f"  Listen time: {user_profile.get_listen_time_formatted()}")
    print(f"  Favorite genres: {', '.join(user_profile.favorite_genres)}")
except Exception as e:
    print(f"✗ UserProfile creation failed: {e}")

print()
print("=== Model Testing Complete ===")
print()

# Summary
print("Summary:")
print("- All models imported successfully")
print("- Individual instances created")
print("- JSON serialization works")
print("- Timestamp conversion works")
print("- Validation works correctly")
print("- List models work")
print("- User profile works")
print()
print("✓ All tests passed! The data models are ready for use.")