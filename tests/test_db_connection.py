"""
Test MySQL Database Connection
This script verifies that your MySQL connection is working properly
"""

import mysql.connector
from mysql.connector import Error
from db_config import get_db_config, get_db_connection
from werkzeug.security import check_password_hash

def test_connection():
    """Test basic MySQL connection"""
    print("\n" + "="*60)
    print("🔍 TESTING MYSQL DATABASE CONNECTION")
    print("="*60 + "\n")
    
    try:
        # Test raw connection to MySQL
        print("1️⃣ Testing connection to MySQL server...")
        raw_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            use_pure=True
        )
        
        if raw_conn.is_connected():
            print("   ✅ Successfully connected to MySQL server!")
            db_info = raw_conn.get_server_info()
            print(f"   📌 MySQL Server version: {db_info}")
            raw_conn.close()
        else:
            print("   ❌ Failed to connect to MySQL server")
            return False
            
    except Error as e:
        print(f"   ❌ Error connecting to MySQL: {e}")
        print("\n💡 TIP: Make sure MySQL service is running:")
        print("   Windows: net start MySQL80")
        return False
    
    # Test connection to car_rental_db database
    print("\n2️⃣ Testing connection to car_rental_db database...")
    conn = get_db_connection()
    
    if not conn:
        print("   ❌ Failed to connect to car_rental_db")
        print("\n💡 TIP: Run 'python app.py' first to create the database")
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"   ✅ Connected to database: {db_name}")
        
        # Check if tables exist
        print("\n3️⃣ Checking database tables...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"   ✅ Found {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"      - {table[0]}: {count} records")
        else:
            print("   ⚠️  No tables found. Run 'python app.py' to initialize database")
        
        # Check admin accounts
        print("\n4️⃣ Checking admin accounts...")
        cursor.execute("SELECT * FROM admin_accounts")
        admins = cursor.fetchall()
        
        if admins:
            print(f"   ✅ Found {len(admins)} admin account(s):")
            cursor.execute("SELECT id, fullname, email, phone FROM admin_accounts")
            admin_details = cursor.fetchall()
            for admin in admin_details:
                print(f"      👤 {admin[1]} ({admin[2]}) - Phone: {admin[3]}")
        else:
            print("   ⚠️  No admin accounts found")
            print("   💡 Admin account will be created on first app run")
        
        # Test password verification
        print("\n5️⃣ Testing admin password...")
        cursor.execute("SELECT email, password FROM admin_accounts WHERE email = %s", 
                      ('admin@luxedrive.com',))
        admin = cursor.fetchone()
        
        if admin:
            test_password = 'AdminLuxe2024!'
            stored_hash = admin[1]
            
            if check_password_hash(stored_hash, test_password):
                print(f"   ✅ Password verification successful!")
                print(f"   🔑 Confirmed password: {test_password}")
            else:
                print("   ⚠️  Password doesn't match expected value")
                print("   💡 Check db_config.py line 137 for current password")
        else:
            print("   ⚠️  Default admin account not found")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ DATABASE CONNECTION TEST COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 ADMIN LOGIN CREDENTIALS:")
        print("   🌐 URL: http://localhost:5000/admin/login")
        print("   📧 Email: admin@luxedrive.com")
        print("   🔑 Password: AdminLuxe2024!")
        print("="*60 + "\n")
        
        return True
        
    except Error as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    try:
        success = test_connection()
        if not success:
            print("\n❌ Database connection test failed!")
            print("💡 Check the tips above to resolve the issues\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
