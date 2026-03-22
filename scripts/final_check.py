"""
Final check for MusicFun project.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("MusicFun Project - Final Check")
print("=" * 60)
print()

# List of tests
test_results = []

# Test 1: Configuration
print("1. Testing configuration...")
try:
    from config.settings import settings
    print(f"   OK - {settings.project_name} v{settings.version}")
    test_results.append(True)
except Exception as e:
    print(f"   FAIL - {e}")
    test_results.append(False)

print()

# Test 2: Data Models
print("2. Testing data models...")

# Song model
try:
    from src.models.song import Song, Platform
    song = Song(
        id="test_song",
        title="Test Song",
        artist="Test Artist",
        platform=Platform.NETEASE,
        platform_id="123"
    )
    print(f"   OK - Song: {song.title} - {song.artist}")
    test_results.append(True)
except Exception as e:
    print(f"   FAIL - Song model: {e}")
    test_results.append(False)

# Comment model
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
    print(f"   OK - Comment: {comment.content[:20]}...")
    test_results.append(True)
except Exception as e:
    print(f"   FAIL - Comment model: {e}")
    test_results.append(False)

# User model
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
    print(f"   OK - User: {user.username}")
    test_results.append(True)
except Exception as e:
    print(f"   FAIL - User model: {e}")
    test_results.append(False)

print()

# Test 3: Core Modules
print("3. Testing core modules...")

# Logger
try:
    from src.core.logger import get_logger
    logger = get_logger()
    logger.info("Test log message")
    print(f"   OK - Logger working")
    test_results.append(True)
except Exception as e:
    print(f"   FAIL - Logger: {e}")
    test_results.append(False)

# Exceptions
try:
    from src.core.exceptions import ConfigError
    error = ConfigError("Test error", config_key="test")
    print(f"   OK - Exception: {error.error_code}")
    test_results.append(True)
except Exception as e:
    print(f"   FAIL - Exceptions: {e}")
    test_results.append(False)

print()

# Test 4: Dependencies
print("4. Testing dependencies...")
try:
    import requests
    import pandas
    import pydantic
    import loguru
    import aiohttp
    print(f"   OK - All dependencies loaded")
    print(f"     requests: {requests.__version__}")
    print(f"     pandas: {pandas.__version__}")
    print(f"     pydantic: {pydantic.__version__}")
    test_results.append(True)
except Exception as e:
    print(f"   FAIL - Dependencies: {e}")
    test_results.append(False)

print()
print("=" * 60)

# Summary
passed = sum(test_results)
total = len(test_results)

print(f"SUMMARY: {passed}/{total} tests passed")
print()

if passed == total:
    print("SUCCESS: All tests passed!")
    print()
    print("MusicFun project is fully configured and ready for development.")
    print("Next steps:")
    print("1. Configure .env file (copy from .env.example)")
    print("2. Start implementing crawlers in src/platforms/")
    print("3. Create base crawler class in src/core/")
else:
    print(f"WARNING: {total - passed} test(s) failed.")
    print("Please check the error messages above.")

print()
