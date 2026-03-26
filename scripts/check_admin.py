"""Check admin accounts in database"""
from db_config import get_db_connection
from mysql.connector import Error

def check_admins():
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_accounts")
        admins = cursor.fetchall()
        
        print("\n" + "="*60)
        print("📋 ADMIN ACCOUNTS IN DATABASE")
        print("="*60)
        
        if not admins:
            print("⚠️  No admin accounts found in database!")
        else:
            for idx, admin in enumerate(admins, 1):
                print(f"\n👤 Admin #{idx}:")
                print(f"   ID: {admin['id']}")
                print(f"   Full Name: {admin['fullname']}")
                print(f"   Email: {admin['email']}")
                print(f"   Phone: {admin['phone']}")
                print(f"   Password Hash: {admin['password'][:50]}...")
                print(f"   Created: {admin['created_at']}")
        
        print("\n" + "="*60)
        print("🔑 LOGIN CREDENTIALS (Use ALL 4 fields):")
        print("="*60)
        if admins:
            admin = admins[0]
            print(f"   Full Name: {admin['fullname']}")
            print(f"   Email: {admin['email']}")
            print(f"   Phone: {admin['phone']}")
            # Show if password is hashed or plain text
            pwd = admin['password']
            is_hashed = pwd.startswith(('scrypt:', 'pbkdf2:'))
            if is_hashed:
                print(f"   Password: [HASHED - Contact admin for password]")
            else:
                print(f"   Password: {pwd}")
        print("="*60 + "\n")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_admins()
