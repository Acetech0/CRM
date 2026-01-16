from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test():
    pw = "StrongPass123!"
    
    print("--- Test 1: Plain String ---")
    try:
        h = pwd_context.hash(pw)
        print(f"Success: {h}")
    except Exception as e:
        print(f"Failed: {e}")

    print("\n--- Test 2: Truncated Bytes ---")
    pw_bytes = pw.encode("utf-8")[:72]
    try:
        h = pwd_context.hash(pw_bytes)
        print(f"Success: {h}")
    except Exception as e:
        print(f"Failed: {e}")

    print("\n--- Test 3: Truncated String (decode ignore) ---")
    pw_trunc_str = pw_bytes.decode("utf-8", errors="ignore")
    try:
        h = pwd_context.hash(pw_trunc_str)
        print(f"Success: {h}")
    except Exception as e:
        print(f"Failed: {e}")

    print("\n--- Test 4: Direct bcrypt usage ---")
    try:
        salt = bcrypt.gensalt()
        h = bcrypt.hashpw(pw_bytes, salt)
        print(f"Success: {h}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test()
