"""
Test admin login functionality
"""
import mysql.connector
from werkzeug.security import check_password_hash

print("\n" + "="*70)
print("🧪 TESTING ADMIN LOGIN")
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
    
    # Test credentials
    test_email = "cute@gmail.com"
    test_password = "123456789"
    
    print(f"Testing login with:")
    print(f"  Email: {test_email}")
    print(f"  Password: {test_password}")
    print()
    
    # Fetch admin
    cursor.execute("SELECT * FROM admin_accounts WHERE email = %s", (test_email,))
    admin = cursor.fetchone()
    
    if not admin:
        print("❌ FAILED: Admin account not found")
    else:
        print("✅ Admin account found")
        print(f"   Full Name: {admin['fullname']}")
        print(f"   Email: {admin['email']}")
        print(f"   Phone: {admin['phone']}")
        print()
        
        # Test password
        stored_password = admin['password']
        try:
            password_matches = check_password_hash(stored_password, test_password)
            if password_matches:
                print("✅ Password verification successful!")
                print("   Password is correctly hashed and matches")
            else:
                print("❌ Password verification failed!")
                print("   The password does not match")
        except Exception as e:
            print(f"❌ Password verification error: {e}")
    
    print("\n" + "="*70)
    print("📝 LOGIN DETAILS:")
    print("="*70)
    print(f"URL: http://localhost:5000/admin/login")
    print(f"Email: {test_email}")
    print(f"Password: {test_password}")
    print("="*70 + "\n")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
