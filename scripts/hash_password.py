"""
Password Hashing Utility
Use this to get hashed passwords for manual insertion into database
"""
from werkzeug.security import generate_password_hash

def hash_password_interactive():
    """Interactive password hasher"""
    print("\n" + "="*70)
    print("🔐 PASSWORD HASHING UTILITY")
    print("="*70 + "\n")
    
    password = input("Enter password to hash: ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    hashed = generate_password_hash(password)
    
    print("\n" + "="*70)
    print("✅ PASSWORD HASHED SUCCESSFULLY!")
    print("="*70)
    print(f"Original:  {password}")
    print(f"Hashed:    {hashed}")
    print("="*70)
    print("\n💡 Copy the hashed password above and use it in your database insert.")
    print("="*70 + "\n")

def hash_password_direct(password):
    """Direct password hasher"""
    return generate_password_hash(password)

if __name__ == "__main__":
    # Interactive mode
    hash_password_interactive()
    
    # Or use direct mode - uncomment below:
    # result = hash_password_direct("your_password_here")
    # print(f"Hashed: {result}")
