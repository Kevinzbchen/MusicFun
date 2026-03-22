"""
Quick test for data models.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("Quick test for data models")
print("=" * 40)
print()

try:
    from src.models.comment import Comment, CommentType
    
    # Test 1: Create comment with all required fields
    comment = Comment(
        id="test_1",
        content="Test comment content",
        target_id="song_123",
        target_type=CommentType.SONG,
        platform="netease",
        user_id="user_123",
        created_at=datetime.now()
    )
    
    print("Test 1: Comment creation")
    print(f"  Status: PASS")
    print(f"  ID: {comment.id}")
    print(f"  Content: {comment.content}")
    print(f"  Target type: {comment.target_type}")
    print()
    
    # Test 2: Create comment with optional fields
    comment2 = Comment(
        id="test_2",
        content="Another test comment",
        target_id="song_456",
        target_type=CommentType.SONG,
        platform="netease",
        user_id="user_456",
        username="TestUser",
        like_count=10,
        created_at=datetime.now()
    )
    
    print("Test 2: Comment with optional fields")
    print(f"  Status: PASS")
    print(f"  Username: {comment2.username}")
    print(f"  Like count: {comment2.like_count}")
    print()
    
    # Test 3: Test JSON serialization
    json_data = comment.to_json()
    print("Test 3: JSON serialization")
    print(f"  Status: PASS")
    print(f"  JSON length: {len(json_data)} characters")
    print(f"  First 100 chars: {json_data[:100]}...")
    print()
    
    print("=" * 40)
    print("All tests passed!")
    
except Exception as e:
    print(f"Test failed: {e}")
    import traceback
    traceback.print_exc()
