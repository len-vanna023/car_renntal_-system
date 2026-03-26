"""
Fix the password for vanna@gmail.com admin account
Hash the plain text password properly
"""
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

print("\n" + "="*70)
print("🔧 FIXING ADMIN PASSWORD FOR vanna@gmail.com")
print("="*70 + "\n")

try:
    # Connect to database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='car_rental_db',
        use_pure=True
    )
    cursor = conn.cursor(dictionary=True)
    
    # Get current admin details
    cursor.execute("SELECT * FROM admin_accounts WHERE email = %s", ('vanna@gmail.com',))
    admin = cursor.fetchone()
    
    if not admin:
        print("❌ Admin account vanna@gmail.com not found!")
    else:
        print("📊 Current Admin Details:")
        print(f"   ID:       {admin['id']}")
        print(f"   Name:     {admin['fullname']}")
        print(f"   Email:    {admin['email']}")
        print(f"   Phone:    {admin['phone']}")
        print(f"   Password: {admin['password'][:50]}...")
        print()
        
        # Check if password is already hashed
        current_password = admin['password']
        if current_password.startswith('scrypt:') or current_password.startswith('pbkdf2:'):
            print("✅ Password is already hashed")
            print(f"   Testing if '0707200717' works...")
            
            if check_password_hash(current_password, '0707200717'):
                print("   ✅ Password '0707200717' is correct!")
            else:
                print("   ❌ Password '0707200717' does NOT match the hash")
                print("   ⚠️  You need to use a different password")
        else:
            print("⚠️  Password is in PLAIN TEXT")
            print(f"   Current password: {current_password}")
            print()
            print("🔄 Hashing the password now...")
            
            # Hash the plain text password
            hashed = generate_password_hash(current_password)
            
            # Update in database
            cursor.execute(
                "UPDATE admin_accounts SET password = %s WHERE email = %s",
                (hashed, 'vanna@gmail.com')
            )
            conn.commit()
            
            print("✅ Password hashed successfully!")
            print()
            print("="*70)
            print("✅ LOGIN CREDENTIALS FOR vanna@gmail.com")
            print("="*70)
            print(f"Full Name: {admin['fullname']}")
            print(f"Email:     {admin['email']}")
            print(f"Phone:     {admin['phone']}")
            print(f"Password:  {current_password}")
            print()
            print("🔒 Password is now securely hashed in database")
            print("="*70)
            
            # Test the hash
            print("\n🧪 Testing hashed password...")
            if check_password_hash(hashed, current_password):
                print(f"✅ Hash verification successful!")
                print(f"   You can now login with password: {current_password}")
            else:
                print("❌ Hash verification failed!")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*70)
    print("🎯 NOW YOU CAN LOGIN!")
    print("="*70)
    print("Go to: http://localhost:5000/admin/login")
    print()
    print("Enter ALL 4 fields:")
    print(f"  Full Name: len vanna")
    print(f"  Email:     vanna@gmail.com")
    print(f"  Phone:     090807814")
    print(f"  Password:  0707200717")
    print("="*70 + "\n")
    
except mysql.connector.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
