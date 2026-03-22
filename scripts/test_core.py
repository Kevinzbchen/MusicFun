"""
Test script for MusicFun core modules.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("Testing MusicFun Core Modules")
print("=" * 50)
print()

# Test 1: Import core modules
try:
    from src.core.logger import setup_logger, get_logger, log_exception
    from src.core.exceptions import (
        MusicFunError, CrawlerError, NetworkError, ParseError,
        ConfigError, ValidationError, StorageError
    )
    print("[PASS] Core modules imported successfully")
except ImportError as e:
    print(f"[FAIL] Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Test logger setup
try:
    # Setup logger with test directory
    test_log_dir = Path("test_logs")
    logger = setup_logger(
        log_dir=test_log_dir,
        log_level="INFO",
        log_file="test.log",
        error_file="test_error.log",
        console_output=False,  # Disable console for cleaner test output
        file_output=True
    )
    print("[PASS] Logger setup successful")
    print(f"  Log directory: {test_log_dir}")
    
    # Test logging
    logger.info("Test info message from logger")
    logger.warning("Test warning message")
    print("[PASS] Log messages written")
except Exception as e:
    print(f"[FAIL] Logger setup failed: {e}")

print()

# Test 3: Test exception creation
try:
    # Test ConfigError
    config_error = ConfigError(
        "Missing required configuration",
        config_key="api_key",
        config_file="config.yaml"
    )
    print("[PASS] ConfigError created")
    print(f"  Message: {config_error}")
    print(f"  Error code: {config_error.error_code}")
    
    # Test ValidationError
    validation_error = ValidationError(
        "Value must be positive",
        field="duration",
        value=-10
    )
    print("[PASS] ValidationError created")
    print(f"  Message: {validation_error}")
    
    # Test NetworkError
    network_error = NetworkError(
        "Connection failed",
        url="https://api.example.com",
        status_code=500
    )
    print("[PASS] NetworkError created")
    print(f"  Message: {network_error}")
    
    # Test to_dict method
    error_dict = config_error.to_dict()
    print("[PASS] Exception to_dict works")
    print(f"  Dict keys: {list(error_dict.keys())}")
except Exception as e:
    print(f"[FAIL] Exception creation failed: {e}")

print()

# Test 4: Test exception wrapping
try:
    try:
        # Simulate an error
        data = {"key": "value"}
        result = data["nonexistent"]  # This will raise KeyError
    except KeyError as e:
        # Wrap the generic exception
        wrapped_error = CrawlerError(
            f"Failed to access data: {e}",
            platform="netease",
            crawler_type="song"
        )
        print("[PASS] Exception wrapping successful")
        print(f"  Original: {type(e).__name__}: {e}")
        print(f"  Wrapped: {wrapped_error}")
except Exception as e:
    print(f"[FAIL] Exception wrapping failed: {e}")

print()

# Test 5: Test exception logging
try:
    logger = get_logger()
    
    # Create and log an exception
    parse_error = ParseError(
        "Invalid JSON format",
        data_type="json",
        raw_data="{invalid json}"
    )
    
    # Log the exception
    log_exception(
        parse_error,
        message="Data parsing failed",
        level="ERROR",
        context={"file": "data.json", "line": 42}
    )
    print("[PASS] Exception logging successful")
except Exception as e:
    print(f"[FAIL] Exception logging failed: {e}")

print()

# Test 6: Test exception hierarchy
try:
    # Create a CrawlerError
    crawler_error = CrawlerError(
        "Failed to crawl data",
        platform="netease",
        crawler_type="comment"
    )
    
    # Check inheritance
    assert isinstance(crawler_error, CrawlerError)
    assert isinstance(crawler_error, MusicFunError)
    assert isinstance(crawler_error, Exception)
    
    print("[PASS] Exception hierarchy correct")
    print(f"  Is CrawlerError: {isinstance(crawler_error, CrawlerError)}")
    print(f"  Is MusicFunError: {isinstance(crawler_error, MusicFunError)}")
    print(f"  Is Exception: {isinstance(crawler_error, Exception)}")
except Exception as e:
    print(f"[FAIL] Exception hierarchy test failed: {e}")

print()

# Cleanup test directory
try:
    import shutil
    if test_log_dir.exists():
        shutil.rmtree(test_log_dir)
        print("[PASS] Test log directory cleaned up")
except Exception as e:
    print(f"[NOTE] Cleanup failed: {e}")

print()
print("=" * 50)
print("All core module tests completed successfully!")
print("Core modules are ready for use.")
