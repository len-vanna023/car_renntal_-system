"""
Create test accounts where you KNOW the passwords
This is for testing/development purposes only
"""
from db_config import get_db_connection
from werkzeug.security import generate_password_hash
from mysql.connector import Error, IntegrityError

def create_test_accounts_with_known_passwords():
    """Create test accounts with documented passwords"""
    
    print("\n" + "="*70)
    print("🧪 CREATING TEST ACCOUNTS WITH KNOWN PASSWORDS")
    print("="*70)
    print("\n⚠️  FOR TESTING PURPOSES ONLY!")
    print("These accounts have documented passwords so you can test login.\n")
    
    # List of test accounts with KNOWN passwords
    test_accounts = [
        {
            "name": "Test User 1",
            "email": "test1@test.com",
            "phone": "0111111111",
            "password": "password"  # Simple 8-char password
        },
        {
            "name": "Test User 2",
            "email": "test2@test.com",
            "phone": "0222222222",
            "password": "test1234"  # 8-char password
        },
        {
            "name": "Test User 3",
            "email": "test3@test.com",
            "phone": "0333333333",
            "password": "mypass123"  # 9-char password
        },
        {
            "name": "Demo Customer",
            "email": "demo@luxedrive.com",
            "phone": "0999999999",
            "password": "demo1234"  # Demo password
        }
    ]
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        print("📝 Creating test accounts:")
        print("-"*70)
        
        created_count = 0
        skipped_count = 0
        
        for account in test_accounts:
            # Check if email already exists
            cursor.execute("SELECT email FROM users WHERE email = %s", (account['email'],))
            existing = cursor.fetchone()
            
            if existing:
                print(f"⚠️  {account['email']} already exists - SKIPPED")
                skipped_count += 1
                continue
            
            # Create account
            password_hash = generate_password_hash(account['password'])
            
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                    (account['name'], account['email'], account['phone'], password_hash)
                )
                conn.commit()
                print(f"✅ Created: {account['email']}")
                created_count += 1
            except (Error, IntegrityError) as e:
                print(f"❌ Failed to create {account['email']}: {e}")
        
        print("\n" + "="*70)
        print("📋 TEST ACCOUNT CREDENTIALS")
        print("="*70)
        print("\n✅ These accounts are in your database with KNOWN passwords:\n")
        
        for account in test_accounts:
            cursor.execute("SELECT email FROM users WHERE email = %s", (account['email'],))
            if cursor.fetchone():
                print(f"📧 Email:    {account['email']}")
                print(f"   Password: {account['password']}  ← YOU KNOW THIS!")
                print(f"   Name:     {account['name']}")
                print(f"   Phone:    {account['phone']}")
                print()
        
        print("="*70)
        print(f"✅ Created {created_count} new test accounts")
        print(f"⚠️  Skipped {skipped_count} existing accounts")
        print("="*70)
        
        print("\n💡 HOW TO USE:")
        print("-"*70)
        print("""
1. Go to: http://localhost:5000/login

2. Login with any test account:
   Email:    test1@test.com
   Password: password

3. The password in database will still look "messy":
   Database: scrypt:32768:8:1$...
   
4. But YOU know the real password is: "password"

5. This way you can test login functionality!
""")
        
        print("\n🔒 SECURITY NOTE:")
        print("-"*70)
        print("""
Even though YOU know these test passwords:
- They are still ENCRYPTED in the database
- You still CANNOT see them in the database
- This is CORRECT security behavior
- For REAL customers, you should NEVER know their passwords!

These test accounts are ONLY for development/testing.
Real customer passwords should ALWAYS remain unknown to everyone!
""")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")

def show_current_test_accounts():
    """Show all test accounts that already exist"""
    
    print("\n" + "="*70)
    print("📋 EXISTING TEST ACCOUNTS IN DATABASE")
    print("="*70)
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get all users
        cursor.execute("""
            SELECT id, name, email, phone, password, created_at 
            FROM users 
            ORDER BY id
        """)
        users = cursor.fetchall()
        
        print(f"\n📊 Total Users: {len(users)}")
        print("-"*70)
        
        # Known test passwords (for reference)
        known_passwords = {
            "test@customer.com": "password123",
            "test1@test.com": "password",
            "test2@test.com": "test1234",
            "test3@test.com": "mypass123",
            "demo@luxedrive.com": "demo1234",
            "testpass@example.com": "testpass123"
        }
        
        for user in users:
            print(f"\n👤 ID {user['id']}: {user['name']}")
            print(f"   📧 Email: {user['email']}")
            print(f"   📱 Phone: {user['phone']}")
            print(f"   🔒 Password in DB: {user['password'][:50]}...")
            
            # Show known password if it's a test account
            if user['email'] in known_passwords:
                print(f"   🔑 Known Password: {known_passwords[user['email']]}  ← YOU KNOW THIS!")
            else:
                print(f"   ❓ Real Customer: Password unknown (CORRECT!)")
            
            print(f"   📅 Created: {user['created_at']}")
        
        print("\n" + "="*70)
        print("💡 LEGEND:")
        print("="*70)
        print("""
🔑 Known Password  = Test account, you know the password
❓ Password Unknown = Real customer, password is secret (GOOD!)
""")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎯 TEST ACCOUNT MANAGER")
    print("="*70)
    print("""
This script helps you create test accounts with KNOWN passwords.

IMPORTANT:
- Test accounts: You KNOW the password (for testing)
- Real customers: You DON'T know the password (for security)
- Both are encrypted in database (looks "messy")
- This is CORRECT and SECURE behavior!
""")
    
    # Show existing accounts first
    show_current_test_accounts()
    
    # Ask if user wants to create more test accounts
    print("\n" + "="*70)
    create_test_accounts_with_known_passwords()
    
    print("\n✨ Done! You now have test accounts with known passwords!")
    print("   Use these for testing, but remember: real customer passwords")
    print("   should ALWAYS remain encrypted and unknown! 🔒\n")
