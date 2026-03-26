"""
Test admin login with all 4 fields validation
"""
import mysql.connector
from werkzeug.security import check_password_hash

def normalize_phone(value):
    """Normalize phone numbers by stripping non-digit characters."""
    if not value:
        return ''
    return ''.join(ch for ch in value if ch.isdigit())

print("\n" + "="*70)
print("🧪 TESTING ADMIN LOGIN - ALL 4 FIELDS VALIDATION")
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
    test_fullname = "nana cute"
    test_email = "cute@gmail.com"
    test_phone = "0987654321"
    test_password = "123456789"
    
    print("Testing login with ALL 4 fields:")
    print(f"  Full Name: {test_fullname}")
    print(f"  Email: {test_email}")
    print(f"  Phone: {test_phone}")
    print(f"  Password: {test_password}")
    print()
    
    # Fetch admin by email
    cursor.execute("SELECT * FROM admin_accounts WHERE email = %s", (test_email.lower(),))
    admin = cursor.fetchone()
    
    if not admin:
        print("❌ FAILED: Admin account not found in database")
    else:
        print("✅ Step 1: Admin account found in database")
        print()
        
        # Validate fullname
        stored_fullname = (admin['fullname'] or '').strip()
        if stored_fullname.lower() == test_fullname.lower():
            print(f"✅ Step 2: Full name matches")
            print(f"   Stored: '{stored_fullname}'")
            print(f"   Input:  '{test_fullname}'")
        else:
            print(f"❌ Step 2: Full name doesn't match")
            print(f"   Stored: '{stored_fullname}'")
            print(f"   Input:  '{test_fullname}'")
        print()
        
        # Validate phone
        stored_phone = normalize_phone(admin.get('phone') or '')
        input_phone = normalize_phone(test_phone)
        if stored_phone == input_phone:
            print(f"✅ Step 3: Phone number matches")
            print(f"   Stored (normalized): '{stored_phone}'")
            print(f"   Input (normalized):  '{input_phone}'")
        else:
            print(f"❌ Step 3: Phone number doesn't match")
            print(f"   Stored (normalized): '{stored_phone}'")
            print(f"   Input (normalized):  '{input_phone}'")
        print()
        
        # Validate password
        stored_password = admin['password']
        try:
            password_matches = check_password_hash(stored_password, test_password)
            if password_matches:
                print("✅ Step 4: Password verification successful!")
                print("   Password is correctly hashed and matches")
            else:
                print("❌ Step 4: Password verification failed!")
                print("   The password does not match")
        except Exception as e:
            print(f"❌ Step 4: Password verification error: {e}")
        print()
        
        # Final verdict
        all_valid = (
            stored_fullname.lower() == test_fullname.lower() and
            stored_phone == input_phone and
            password_matches
        )
        
        if all_valid:
            print("="*70)
            print("🎉 SUCCESS! ALL 4 FIELDS VALIDATED CORRECTLY!")
            print("="*70)
            print("✅ Admin login will work with these credentials")
        else:
            print("="*70)
            print("❌ FAILED! Some fields don't match")
            print("="*70)
    
    print("\n" + "="*70)
    print("📝 TO LOGIN AS ADMIN:")
    print("="*70)
    print(f"URL: http://localhost:5000/admin/login")
    print(f"Full Name: {test_fullname}")
    print(f"Email: {test_email}")
    print(f"Phone: {test_phone}")
    print(f"Password: {test_password}")
    print("="*70 + "\n")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
