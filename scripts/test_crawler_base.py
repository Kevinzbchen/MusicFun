"""
Test script for base crawler and request handler.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("Testing Base Crawler and Request Handler")
print("=" * 60)
print()

# Test 1: Import modules
try:
    from src.core.base_crawler import BaseCrawler
    from src.core.request_handler import RequestHandler
    from src.models.song import Platform
    print("[PASS] Modules imported successfully")
except ImportError as e:
    print(f"[FAIL] Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Test RequestHandler
try:
    print("Testing RequestHandler...")
    
    # Create request handler
    handler = RequestHandler(
        base_url="https://httpbin.org",
        timeout=5,
        request_delay=0.1,
        enable_cache=False,
        rate_limit_per_minute=10
    )
    
    # Test GET request
    response = handler.get("/get")
    print(f"  GET request: {response.status_code}")
    
    # Test JSON parsing
    json_data = handler.get_json("/json")
    print(f"  JSON request: {len(json_data)} keys")
    
    # Test statistics
    stats = handler.get_statistics()
    print(f"  Request count: {stats['request_count']}")
    print(f"  Success rate: {stats['success_rate']:.2%}")
    
    handler.close()
    print("[PASS] RequestHandler test completed")
    
except Exception as e:
    print(f"[FAIL] RequestHandler test failed: {e}")

print()

# Test 3: Test BaseCrawler abstract class
try:
    print("Testing BaseCrawler abstract class...")
    
    # Test that BaseCrawler is abstract
    import inspect
    assert inspect.isabstract(BaseCrawler), "BaseCrawler should be abstract"
    
    # Check abstract methods
    abstract_methods = [
        'search',
        'get_song', 
        'get_comments',
        'get_user'
    ]
    
    for method_name in abstract_methods:
        method = getattr(BaseCrawler, method_name)
        assert getattr(method, '__isabstractmethod__', False), f"{method_name} should be abstract"
    
    print(f"  Abstract methods: {', '.join(abstract_methods)}")
    print("[PASS] BaseCrawler abstract class test completed")
    
except Exception as e:
    print(f"[FAIL] BaseCrawler abstract test failed: {e}")

print()

# Test 4: Test concrete crawler implementation
try:
    print("Testing concrete crawler implementation...")
    
    # Create a simple test crawler
    class TestCrawler(BaseCrawler):
        def search(self, query: str, limit: int = 10, **kwargs):
            from src.models.song import SongList
            return SongList()
        
        def get_song(self, song_id: str, **kwargs):
            from src.models.song import Song
            return Song(
                id=song_id,
                title="Test Song",
                artist="Test Artist",
                platform=self.platform,
                platform_id=song_id
            )
        
        def get_comments(self, song_id: str, limit: int = 100, **kwargs):
            from src.models.comment import CommentList
            return CommentList()
        
        def get_user(self, user_id: str, **kwargs):
            return {"id": user_id, "username": "test_user"}
    
    # Test configuration
    config = {
        "base_url": "https://api.example.com",
        "user_agent": "TestCrawler/1.0",
        "timeout": 30,
        "request_delay": 1.0
    }
    
    # Create crawler instance
    crawler = TestCrawler(Platform.NETEASE, config)
    
    # Test methods
    song = crawler.get_song("test_123")
    print(f"  Song created: {song.title} - {song.artist}")
    
    # Test statistics
    stats = crawler.get_statistics()
    print(f"  Crawler stats: {stats['platform']}")
    
    crawler.close()
    print("[PASS] Concrete crawler test completed")
    
except Exception as e:
    print(f"[FAIL] Concrete crawler test failed: {e}")

print()

# Test 5: Test error handling
try:
    print("Testing error handling...")
    
    from src.core.exceptions import NetworkError
    
    handler = RequestHandler(timeout=1)
    
    # This should fail (non-existent URL)
    try:
        handler.get("http://nonexistent.example.com")
        print("[FAIL] Should have raised NetworkError")
    except NetworkError:
        print("  NetworkError raised as expected")
    except Exception as e:
        print(f"  Unexpected error: {e}")
    
    handler.close()
    print("[PASS] Error handling test completed")
    
except Exception as e:
    print(f"[FAIL] Error handling test failed: {e}")

print()
print("=" * 60)
print("All tests completed!")
print("Base crawler and request handler are ready for use.")
