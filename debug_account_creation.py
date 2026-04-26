#!/usr/bin/env python
"""Debug database and account creation"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.models.db_config import get_db_connection, close_db_connection
from werkzeug.security import generate_password_hash
from mysql.connector import Error, IntegrityError

def test_db_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("🔍 DATABASE CONNECTION TEST")
    print("="*60)
    
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database!")
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if users table exists
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        print(f"✅ Connected to database!")
        print(f"   Current user count: {result['count']}")
        
        # List existing users
        cursor.execute("SELECT id, name, email FROM users LIMIT 5")
        users = cursor.fetchall()
        if users:
            print(f"\n   First {len(users)} users:")
            for user in users:
                print(f"      - {user['name']} ({user['email']})")
        
        cursor.close()
        return True
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            close_db_connection(conn)

def test_create_user():
    """Test creating a new user"""
    print("\n" + "="*60)
    print("🧪 USER CREATION TEST")
    print("="*60)
    
    import random
    unique_id = random.randint(100000, 999999)
    test_email = f"debug_test_{unique_id}@example.com"
    
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database!")
        return False
    
    try:
        cursor = conn.cursor()
        password_hash = generate_password_hash("testpass123")
        
        print(f"\nAttempting to create user:")
        print(f"   Email: {test_email}")
        print(f"   Name: Debug Test User")
        print(f"   Phone: 0987654321")
        
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            ("Debug Test User", test_email, "0987654321", password_hash)
        )
        conn.commit()
        
        print(f"\n✅ User created successfully!")
        
        # Verify the user was created
        cursor.execute("SELECT id, name, email FROM users WHERE email = %s", (test_email,))
        user = cursor.fetchone()
        if user:
            print(f"✅ Verified in database:")
            print(f"   ID: {user[0]}")
            print(f"   Name: {user[1]}")
            print(f"   Email: {user[2]}")
        
        cursor.close()
        return True
    except IntegrityError as e:
        print(f"❌ Integrity error: {e}")
        return False
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            close_db_connection(conn)

if __name__ == "__main__":
    print("\n🔧 DEBUGGING ACCOUNT CREATION SYSTEM")
    
    success = True
    success = test_db_connection() and success
    success = test_create_user() and success
    
    print("\n" + "="*60)
    if success:
        print("✅ DATABASE AND USER CREATION WORKING!")
    else:
        print("❌ PROBLEMS DETECTED - CHECK OUTPUT ABOVE")
    print("="*60 + "\n")
