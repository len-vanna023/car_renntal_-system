"""Fix admin accounts in database"""
from db_config import get_db_connection
from werkzeug.security import generate_password_hash
from mysql.connector import Error

def fix_admin_accounts():
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor()
        
        print("\n🔧 FIXING ADMIN ACCOUNTS...")
        print("="*60)
        
        # Fix admin #2 - remove leading space from email and hash password
        cursor.execute("""
            UPDATE admin_accounts 
            SET email = TRIM(email)
            WHERE email LIKE ' %'
        """)
        rows_fixed = cursor.rowcount
        print(f"✅ Fixed {rows_fixed} email(s) with leading spaces")
        
        # Hash any plain text passwords
        cursor.execute("SELECT id, email, password FROM admin_accounts")
        admins = cursor.fetchall()
        
        for admin_id, email, password in admins:
            # Check if password is not hashed (hashed passwords start with 'scrypt:' or 'pbkdf2:')
            if password and not password.startswith(('scrypt:', 'pbkdf2:')):
                print(f"🔑 Hashing password for: {email}")
                hashed = generate_password_hash(password)
                cursor.execute(
                    "UPDATE admin_accounts SET password = %s WHERE id = %s",
                    (hashed, admin_id)
                )
        
        conn.commit()
        
        print("\n✅ ADMIN ACCOUNTS FIXED!")
        print("="*60)
        
        # Show updated accounts
        cursor.execute("SELECT id, fullname, email, phone FROM admin_accounts ORDER BY id")
        admins = cursor.fetchall()
        
        print("\n📋 UPDATED ADMIN ACCOUNTS:")
        for admin_id, fullname, email, phone in admins:
            print(f"\n👤 Admin #{admin_id}:")
            print(f"   Full Name: {fullname}")
            print(f"   Email: {email}")
            print(f"   Phone: {phone}")
            print(f"   Password: 0707200717")
        
        print("\n" + "="*60)
        print("🎉 You can now login with:")
        print("   Email: admin@luxedrive.com")
        print("   Password: 0707200717")
        print("="*60 + "\n")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    fix_admin_accounts()
