"""
Quick Add Admin - No confirmation needed
Add new admin accounts quickly
"""
import mysql.connector
from werkzeug.security import generate_password_hash

# ═══════════════════════════════════════════════════════════════
# EDIT THESE DETAILS TO ADD YOUR ADMIN ACCOUNT
# ═══════════════════════════════════════════════════════════════

NEW_ADMIN = {
    'fullname': 'Len Vanna',           # ← Change this
    'email': 'vanna@example.com',      # ← Change this
    'phone': '0987654321',             # ← Change this
    'password': 'Vanna@123'            # ← Change this
}

# ═══════════════════════════════════════════════════════════════

def quick_add_admin(fullname, email, phone, password):
    """Quick add admin to database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='car_rental_db',
            use_pure=True
        )
        cursor = conn.cursor()
        
        # Check if exists
        cursor.execute("SELECT email FROM admin_accounts WHERE email = %s", (email.lower(),))
        if cursor.fetchone():
            print(f"\n⚠️  Email '{email}' already exists in database!")
            print("   Please use a different email or login with existing credentials.\n")
            cursor.close()
            conn.close()
            return
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert
        cursor.execute("""
            INSERT INTO admin_accounts (fullname, email, phone, password)
            VALUES (%s, %s, %s, %s)
        """, (fullname, email.lower(), phone, hashed_password))
        
        conn.commit()
        
        print("\n" + "="*70)
        print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print("="*70)
        print(f"\n👤 Full Name: {fullname}")
        print(f"📧 Email:     {email}")
        print(f"📱 Phone:     {phone}")
        print(f"🔑 Password:  {password}")
        print(f"\n🔒 Password Status: Securely hashed in database")
        print("\n" + "="*70)
        print("✅ You can now login at: http://localhost:5000/admin/login")
        print("="*70 + "\n")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database error: {e}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("➕ QUICK ADD ADMIN TO MYSQL")
    print("="*70 + "\n")
    
    print("Adding admin account with details from NEW_ADMIN...")
    print(f"Full Name: {NEW_ADMIN['fullname']}")
    print(f"Email:     {NEW_ADMIN['email']}")
    print(f"Phone:     {NEW_ADMIN['phone']}")
    print()
    
    quick_add_admin(
        NEW_ADMIN['fullname'],
        NEW_ADMIN['email'],
        NEW_ADMIN['phone'],
        NEW_ADMIN['password']
    )
    
    print("💡 TIP: To add more admins:")
    print("   1. Edit the NEW_ADMIN dictionary at the top of this file")
    print("   2. Run this script again: python quick_add_admin.py\n")
