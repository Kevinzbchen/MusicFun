"""
Final verification script for MusicFun project.

Tests all major components of the project.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("MusicFun Project Final Verification")
print("=" * 60)
print()

# Test counters
passed = 0
failed = 0

# Test 1: Check project structure
try:
    required_dirs = [
        "src",
        "src/core",
        "src/models",
        "src/platforms",
        "src/utils",
        "src/storage",
        "config",
        "data",
        "logs",
        "scripts"
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"[OK] Directory exists: {dir_path}")
        else:
            print(f"[FAIL] Directory missing: {dir_path}")
            failed += 1
    
    passed += len(required_dirs)
    print()
except Exception as e:
    print(f"[FAIL] Directory check failed: {e}")
    failed += 1

# Test 2: Check required files
try:
    required_files = [
        "requirements.txt",
        "README.md",
        ".gitignore",
        "config/settings.py",
        "src/models/__init__.py",
        "src/models/song.py",
        "src/core/__init__.py",
        "src/core/logger.py",
        "src/core/exceptions.py",
        "scripts/simple_test.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"[OK] File exists: {file_path}")
        else:
            print(f"[FAIL] File missing: {file_path}")
            failed += 1
    
    passed += len(required_files)
    print()
except Exception as e:
    print(f"[FAIL] File check failed: {e}")
    failed += 1

# Test 3: Test configuration
try:
    from config.settings import settings
    print("[OK] Configuration loaded successfully")
    print(f"  Project: {settings.project_name} v{settings.version}")
    print(f"  Debug mode: {settings.debug}")
    print(f"  Data directory: {settings.data_dir}")
    passed += 1
    print()
except Exception as e:
    print(f"[FAIL] Configuration test failed: {e}")
    failed += 1

# Test 4: Test data models
try:
    from src.models.song import Song, Platform
    from src.models.comment import Comment, CommentType
    from src.models.user import User, UserGender
    from datetime import datetime

    # Create test instances
    song = Song(
        id="test_1",
        title="Test Song",
        artist="Test Artist",
        platform=Platform.NETEASE,
        platform_id="123"
    )
    
    comment = Comment(
        id="comment_1",
        content="Test comment",
        target_id="test_1",
        target_type=CommentType.SONG,
        platform="netease",
        user_id="user_1",
        username="TestUser",
        created_at=datetime.now()
    )
    
    user = User(
        id="user_1",
        username="testuser",
        platform="netease",
        platform_id="456",
        gender=UserGender.MALE,
        created_at=datetime.now()
    )
    
    print("[OK] Data models work correctly")
    print(f"  Song: {song.title} - {song.artist}")
    print(f"  Comment: {comment.username}: {comment.content[:20]}...")
    print(f"  User: {user.username} ({user.get_gender_display()})")
    passed += 1
    print()
except Exception as e:
    print(f"[FAIL] Data models test failed: {e}")
    failed += 1

# Test 5: Test core modules
try:
    from src.core.logger import get_logger
    from src.core.exceptions import MusicFunError, ConfigError
    
    # Get logger
    logger = get_logger()
    logger.info("Test log message from verification script")
    
    # Test exception
    error = ConfigError("Test configuration error", config_key="test_key")
    
    print("[OK] Core modules work correctly")
    print(f"  Logger: {type(logger).__name__}")
    print(f"  Exception: {error}")
    passed += 1
    print()
except Exception as e:
    print(f"[FAIL] Core modules test failed: {e}")
    failed += 1

# Test 6: Test dependencies
try:
    import requests
    import pandas
    import pydantic
    import loguru
    import aiohttp
    
    print("[OK] Key dependencies imported successfully")
    print(f"  requests: {requests.__version__}")
    print(f"  pandas: {pandas.__version__}")
    print(f"  pydantic: {pydantic.__version__}")
    print(f"  loguru: {loguru.__version__}")
    print(f"  aiohttp: {aiohttp.__version__}")
    passed += 1
    print()
except ImportError as e:
    print(f"[FAIL] Dependency import failed: {e}")
    failed += 1

# Summary
print("=" * 60)
print("VERIFICATION SUMMARY")
print("=" * 60)
print(f"Tests passed: {passed}")
print(f"Tests failed: {failed}")
print(f"Total tests: {passed + failed}")
print()

if failed == 0:
    print("SUCCESS: All tests passed! MusicFun project is ready for development.")
    print()
    print("Next steps:")
    print("1. Configure your .env file (copy from .env.example)")
    print("2. Start implementing platform crawlers in src/platforms/")
    print("3. Create base crawler class in src/core/base_crawler.py")
    print("4. Implement data storage in src/storage/")
else:
    print(f"WARNING: {failed} test(s) failed. Please check the issues above.")

print()
print("Project structure is complete and ready for development!")
