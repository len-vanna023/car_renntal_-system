"""
Test login for vanna@gmail.com with all 4 fields
"""
import mysql.connector
from werkzeug.security import check_password_hash

def normalize_phone(value):
    """Normalize phone numbers by stripping non-digit characters."""
    if not value:
        return ''
    return ''.join(ch for ch in value if ch.isdigit())

print("\n" + "="*70)
print("🧪 TESTING LOGIN FOR vanna@gmail.com")
print("="*70 + "\n")

# Test credentials (exactly as you entered in the form)
test_fullname = "len vanna"
test_email = "vanna@gmail.com"
test_phone = "090807814"
test_password = "0707200717"

print("Testing with these credentials:")
print(f"  Full Name: {test_fullname}")
print(f"  Email:     {test_email}")
print(f"  Phone:     {test_phone}")
print(f"  Password:  {test_password}")
print()

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='car_rental_db',
        use_pure=True
    )
    cursor = conn.cursor(dictionary=True)
    
    # Step 1: Fetch admin by email
    print("Step 1: Fetching admin from database...")
    cursor.execute("SELECT * FROM admin_accounts WHERE email = %s", (test_email.lower(),))
    admin = cursor.fetchone()
    
    if not admin:
        print("❌ FAILED: Admin not found in database")
        exit()
    
    print("✅ Admin found in database")
    print(f"   DB Full Name: {admin['fullname']}")
    print(f"   DB Email:     {admin['email']}")
    print(f"   DB Phone:     {admin['phone']}")
    print()
    
    # Step 2: Validate fullname
    print("Step 2: Validating fullname...")
    stored_fullname = (admin['fullname'] or '').strip()
    if stored_fullname.lower() == test_fullname.lower():
        print(f"✅ Fullname matches!")
        print(f"   Stored:  '{stored_fullname}' (lowercase: '{stored_fullname.lower()}')")
        print(f"   Input:   '{test_fullname}' (lowercase: '{test_fullname.lower()}')")
    else:
        print(f"❌ Fullname doesn't match!")
        print(f"   Stored:  '{stored_fullname}' (lowercase: '{stored_fullname.lower()}')")
        print(f"   Input:   '{test_fullname}' (lowercase: '{test_fullname.lower()}')")
        exit()
    print()
    
    # Step 3: Validate phone
    print("Step 3: Validating phone...")
    stored_phone = normalize_phone(admin.get('phone') or '')
    input_phone = normalize_phone(test_phone)
    if stored_phone == input_phone:
        print(f"✅ Phone matches!")
        print(f"   Stored (normalized):  '{stored_phone}'")
        print(f"   Input (normalized):   '{input_phone}'")
    else:
        print(f"❌ Phone doesn't match!")
        print(f"   Stored (normalized):  '{stored_phone}'")
        print(f"   Input (normalized):   '{input_phone}'")
        exit()
    print()
    
    # Step 4: Validate password
    print("Step 4: Validating password...")
    stored_password = admin['password']
    print(f"   Password in DB: {stored_password[:50]}...")
    
    password_matches = False
    try:
        password_matches = check_password_hash(stored_password, test_password)
        if password_matches:
            print(f"✅ Password matches (hashed verification)!")
        else:
            print(f"❌ Password doesn't match!")
            # Try plain text as fallback
            if stored_password == test_password:
                print(f"⚠️  But plain text matches (password needs hashing)")
                password_matches = True
    except Exception as e:
        print(f"⚠️  Hash check failed, trying plain text: {e}")
        if stored_password == test_password:
            print(f"✅ Plain text password matches")
            password_matches = True
    
    if not password_matches:
        print(f"❌ Password verification failed!")
        exit()
    
    print()
    print("="*70)
    print("🎉 ALL VALIDATION PASSED!")
    print("="*70)
    print("✅ Fullname: MATCH")
    print("✅ Email:    MATCH")
    print("✅ Phone:    MATCH")
    print("✅ Password: MATCH")
    print()
    print("🎯 LOGIN WILL BE SUCCESSFUL!")
    print("="*70)
    print()
    print("NOW GO LOGIN AT: http://localhost:5000/admin/login")
    print()
    print("Use EXACTLY these details:")
    print(f"  Full Name: {test_fullname}")
    print(f"  Email:     {test_email}")
    print(f"  Phone:     {test_phone}")
    print(f"  Password:  {test_password}")
    print("="*70 + "\n")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
