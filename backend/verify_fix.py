import sys
import os
sys.path.append(os.getcwd())

from app.core.security import get_password_hash, verify_password

def test_password_fix():
    print("Testing Password Fixes...")
    
    # Test 1: Normal password
    pw_normal = "StrongPass123!"
    hash_normal = get_password_hash(pw_normal)
    assert verify_password(pw_normal, hash_normal)
    print("✅ Normal password works")

    # Test 2: Long password > 72 chars
    pw_long = "A" * 100
    hash_long = get_password_hash(pw_long)
    assert verify_password(pw_long, hash_long)
    print("✅ Long password (100 chars) works (truncated internally)")

    # Test 3: Password with emojis (multibyte)
    pw_mixed = "🚀" * 50  # 200 bytes
    hash_mixed = get_password_hash(pw_mixed)
    assert verify_password(pw_mixed, hash_mixed)
    print("✅ Multibyte password works")

    print("\nALL CHECKS PASSED")

if __name__ == "__main__":
    test_password_fix()
