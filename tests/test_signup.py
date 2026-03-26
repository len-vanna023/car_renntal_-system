"""Test signup with password confirmation and database"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_signup_with_confirm():
    """Test customer signup with password confirmation"""
    
    print("\n" + "="*60)
    print("🧪 TESTING CUSTOMER SIGNUP WITH PASSWORD CONFIRMATION")
    print("="*60)
    
    # Test 1: Valid signup with matching passwords
    print("\n✅ Test 1: Valid signup (matching passwords)")
    data = {
        "fullname": "Test Password User",
        "email": "testpass@example.com",
        "phone": "0987654321",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {result}")
        
        if result.get('success'):
            print("   ✅ SUCCESS! Account created")
        else:
            print(f"   ❌ FAILED: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 2: Mismatched passwords
    print("\n❌ Test 2: Mismatched passwords (should fail)")
    data2 = {
        "fullname": "Another User",
        "email": "mismatch@example.com",
        "phone": "0123456789",
        "password": "password123",
        "confirm_password": "differentpass"  # Different!
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=data2,
            headers={"Content-Type": "application/json"}
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {result}")
        
        if not result.get('success') and 'match' in result.get('message', '').lower():
            print("   ✅ CORRECT! Properly rejected mismatched passwords")
        else:
            print(f"   ❌ UNEXPECTED: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 3: Missing confirm_password
    print("\n❌ Test 3: Missing confirm_password field (should fail)")
    data3 = {
        "fullname": "No Confirm User",
        "email": "noconfirm@example.com",
        "phone": "0123456789",
        "password": "password123"
        # Missing confirm_password!
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=data3,
            headers={"Content-Type": "application/json"}
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {result}")
        
        if not result.get('success'):
            print("   ✅ CORRECT! Properly rejected missing field")
        else:
            print(f"   ❌ UNEXPECTED SUCCESS")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print("\n" + "="*60)
    print("🏁 TESTING COMPLETE")
    print("="*60)

def check_database():
    """Check if new users are in database"""
    from db_config import get_db_connection
    
    print("\n" + "="*60)
    print("💾 CHECKING DATABASE")
    print("="*60)
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, phone, created_at FROM users ORDER BY id DESC LIMIT 5")
        users = cursor.fetchall()
        
        print(f"\n📋 Latest 5 Users in Database:")
        for idx, user in enumerate(users, 1):
            print(f"\n{idx}. {user['name']}")
            print(f"   Email: {user['email']}")
            print(f"   Phone: {user['phone']}")
            print(f"   Created: {user['created_at']}")
        
        cursor.close()
        conn.close()
        print("\n✅ Database connection working!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    # Make sure the server is running first!
    print("\n⚠️  Make sure Flask app is running on http://localhost:5000")
    print("="*60)
    
    test_signup_with_confirm()
    check_database()
    
    print("\n✨ All tests completed!\n")
