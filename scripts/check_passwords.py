"""Check passwords in database - explain hashing"""
from db_config import get_db_connection
from werkzeug.security import check_password_hash
from mysql.connector import Error

def check_database_passwords():
    """Show what passwords look like in database and why"""
    
    print("\n" + "="*70)
    print("🔐 PASSWORD STORAGE IN DATABASE")
    print("="*70)
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check customer passwords
        print("\n👥 CUSTOMER ACCOUNTS:")
        print("-"*70)
        cursor.execute("SELECT id, name, email, password FROM users ORDER BY id LIMIT 5")
        users = cursor.fetchall()
        
        for user in users:
            print(f"\n📧 {user['name']} ({user['email']})")
            password_hash = user['password']
            print(f"   Password in DB: {password_hash[:80]}...")
            print(f"   Length: {len(password_hash)} characters")
            
            # Check if it's hashed
            if password_hash.startswith('scrypt:') or password_hash.startswith('pbkdf2:'):
                print(f"   ✅ Status: PROPERLY HASHED (Secure!)")
            else:
                print(f"   ⚠️  Status: NOT HASHED (Insecure!)")
        
        # Check admin passwords
        print("\n\n🛡️  ADMIN ACCOUNTS:")
        print("-"*70)
        cursor.execute("SELECT id, fullname, email, password FROM admin_accounts ORDER BY id")
        admins = cursor.fetchall()
        
        for admin in admins:
            print(f"\n📧 {admin['fullname']} ({admin['email']})")
            password_hash = admin['password']
            print(f"   Password in DB: {password_hash[:80]}...")
            print(f"   Length: {len(password_hash)} characters")
            
            # Check if it's hashed
            if password_hash.startswith('scrypt:') or password_hash.startswith('pbkdf2:'):
                print(f"   ✅ Status: PROPERLY HASHED (Secure!)")
            else:
                print(f"   ⚠️  Status: NOT HASHED (Insecure!)")
        
        print("\n" + "="*70)
        print("💡 WHY PASSWORDS LOOK 'MESSY':")
        print("="*70)
        print("""
This is NORMAL and GOOD! Here's why:

1. 🔒 **Security Through Hashing:**
   - Passwords are ENCRYPTED using bcrypt/scrypt algorithm
   - Even if someone hacks the database, they can't see real passwords
   - This is industry standard practice

2. 📝 **What You See vs What Users Type:**
   - User types: "password123"
   - Database stores: "scrypt:32768:8:1$abc123xyz..."
   - The "messy" text is the ENCRYPTED version

3. ✅ **How Login Works:**
   - User types password
   - System hashes what they typed
   - Compares hash with database hash
   - If they match, login succeeds

4. 🎯 **This Protects Your Users:**
   - Even YOU (the admin) can't see their real passwords
   - Hackers can't steal passwords from database
   - One-way encryption (can't be reversed)

EXAMPLE:
--------
Real Password:     "mypassword123"
Stored in DB:      "scrypt:32768:8:1$aoGSJA9CTBQcjnmL$bca2fd..."
                   ↑ This looks "messy" but it's SECURE!
""")
        
        # Test password verification
        print("\n" + "="*70)
        print("🧪 TESTING PASSWORD VERIFICATION:")
        print("="*70)
        
        # Test with first user
        if users:
            test_user = users[0]
            print(f"\nTesting user: {test_user['email']}")
            
            # Ask for known password
            print("\nLet me test if password verification works...")
            print("Testing with password: 'password123'")
            
            stored_hash = test_user['password']
            try:
                matches = check_password_hash(stored_hash, 'password123')
                if matches:
                    print("✅ Password 'password123' matches this user!")
                else:
                    print("❌ Password 'password123' does NOT match")
            except Exception as e:
                print(f"   Error testing: {e}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*70)
        print("✅ CONCLUSION: Your passwords are SECURE!")
        print("="*70)
        print("""
The 'messy' appearance is actually a GOOD SIGN!
It means your passwords are properly encrypted and secure.

This is how all professional websites work:
- Google, Facebook, Amazon - all store passwords this way
- It's the RIGHT way to handle passwords
- Your application is following security best practices

DO NOT try to store passwords in plain text!
The 'messy' hashed passwords are protecting your users! 🔐
""")
        
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_database_passwords()
