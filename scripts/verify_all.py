"""
Verify all MusicFun project components.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("MusicFun Project Verification")
print("=" * 50)
print()

tests = []

# Test 1: Configuration
try:
    from config.settings import settings
    tests.append(("Configuration", True, f"{settings.project_name} v{settings.version}"))
except Exception as e:
    tests.append(("Configuration", False, str(e)))

# Test 2: Data Models - Song
try:
    from src.models.song import Song, Platform
    song = Song(
        id="test_song",
        title="Test Song",
        artist="Test Artist",
        platform=Platform.NETEASE,
        platform_id="123"
    )
    tests.append(("Song Model", True, f"{song.title} - {song.artist}"))
except Exception as e:
    tests.append(("Song Model", False, str(e)))

# Test 3: Data Models - Comment
try:
    from src.models.comment import Comment, CommentType
    comment = Comment(
        id="test_comment",
        content="Test comment",
        target_id="test_song",
        target_type=CommentType.SONG,
        platform="netease",
        user_id="test_user",
        created_at=datetime.now()
    )
    tests.append(("Comment Model", True, f"{comment.content[:20]}..."))
except Exception as e:
    tests.append(("Comment Model", False, str(e)))

# Test 4: Data Models - User
try:
    from src.models.user import User, UserGender
    user = User(
        id="test_user",
        username="testuser",
        platform="netease",
        platform_id="456",
        gender=UserGender.MALE,
        created_at=datetime.now()
    )
    tests.append(("User Model", True, f"{user.username} ({user.get_gender_display()})"))
except Exception as e:
    tests.append(("User Model", False, str(e)))

# Test 5: Core - Logger
try:
    from src.core.logger import get_logger
    logger = get_logger()
    logger.info("Test log from verification")
    tests.append(("Logger", True, "Logging works"))
except Exception as e:
    tests.append(("Logger", False, str(e)))

# Test 6: Core - Exceptions
try:
    from src.core.exceptions import ConfigError
    error = ConfigError("Test error", config_key="test")
    tests.append(("Exceptions", True, f"{error.error_code}"))
except Exception as e:
    tests.append(("Exceptions", False, str(e)))

# Test 7: Dependencies
try:
    import requests
    import pandas
    import pydantic
    import loguru
    tests.append(("Dependencies", True, f"requests {requests.__version__}, pandas {pandas.__version__}"))
except Exception as e:
    tests.append(("Dependencies", False, str(e)))

# Print results
print("Test Results:")
print("-" * 50)

passed = 0
failed = 0

for name, success, message in tests:
    if success:
        print(f"[PASS] {name}: {message}")
        passed += 1
    else:
        print(f"[FAIL] {name}: {message}")
        failed += 1

print()
print("=" * 50)
print(f"Summary: {passed} passed, {failed} failed")
print()

if failed == 0:
    print("SUCCESS: All tests passed! MusicFun project is ready.")
else:
    print(f"WARNING: {failed} test(s) failed. Please check above.")

print()
print("Project structure verification complete.")
