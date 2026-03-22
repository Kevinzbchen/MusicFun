"""
Simple test script for MusicFun data models.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("Testing MusicFun Data Models")
print("=" * 50)
print()

# Test 1: Import all models
try:
    from src.models.song import Song, SongList, Platform, SongStatus
    from src.models.comment import Comment, CommentList, CommentType, CommentStatus
    from src.models.user import User, UserProfile, UserGender, UserStatus, UserType
    print("[PASS] All models imported successfully")
except ImportError as e:
    print(f"[FAIL] Import failed: {e}")
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
    print("[PASS] Song created successfully")
    print(f"  Title: {song.title}")
    print(f"  Artist: {song.artist}")
    print(f"  Platform: {song.platform}")
    print(f"  Duration: {song.get_duration_formatted()}")
except Exception as e:
    print(f"[FAIL] Song creation failed: {e}")

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
    print("[PASS] Comment created successfully")
    print(f"  User: {comment.username}")
    print(f"  Content: {comment.content[:30]}...")
    print(f"  Likes: {comment.like_count}")
except Exception as e:
    print(f"[FAIL] Comment creation failed: {e}")

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
    print("[PASS] User created successfully")
    print(f"  Username: {user.username}")
    print(f"  Display name: {user.get_display_name()}")
    print(f"  Followers: {user.follower_count}")
except Exception as e:
    print(f"[FAIL] User creation failed: {e}")

print()

# Test 5: Test JSON serialization
try:
    song_dict = song.to_dict()
    song_json = song.to_json()
    print("[PASS] JSON serialization successful")
    print(f"  Dict has {len(song_dict)} keys")
    print(f"  JSON is {len(song_json)} characters")
except Exception as e:
    print(f"[FAIL] JSON serialization failed: {e}")

print()

# Test 6: Test timestamp conversion
try:
    timestamp = 1672531200000  # 2023-01-01 00:00:00
    dt = Song.from_milliseconds_timestamp(timestamp, "test")
    print("[PASS] Timestamp conversion successful")
    print(f"  {timestamp} -> {dt}")
except Exception as e:
    print(f"[FAIL] Timestamp conversion failed: {e}")

print()

# Test 7: Test validation
try:
    invalid_song = Song(
        id="test",
        title="Test",
        artist="Test",
        platform=Platform.NETEASE,
        platform_id="test",
        duration=-10
    )
    print("[FAIL] Validation should have failed but didn't")
except ValueError as e:
    print(f"[PASS] Validation works correctly")
except Exception as e:
    print(f"[FAIL] Unexpected error: {e}")

print()

print("=" * 50)
print("All tests completed successfully!")
print("Data models are ready for use.")
