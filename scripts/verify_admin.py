"""
Verify admin accounts in the database
"""
import mysql.connector

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
    
    # Get all admin accounts
    cursor.execute("SELECT id, fullname, email, phone, created_at FROM admin_accounts")
    admins = cursor.fetchall()
    
    print("\n" + "="*70)
    print("📋 ADMIN ACCOUNTS IN DATABASE")
    print("="*70)
    
    if not admins:
        print("❌ No admin accounts found!")
    else:
        for admin in admins:
            print(f"\n👤 Admin ID: {admin['id']}")
            print(f"   Full Name: {admin['fullname']}")
            print(f"   Email: {admin['email']}")
            print(f"   Phone: {admin['phone']}")
            print(f"   Created: {admin['created_at']}")
            print("-" * 70)
    
    print("\n" + "="*70)
    print("✅ Total admin accounts:", len(admins))
    print("="*70 + "\n")
    
    print("📝 TO LOGIN AS ADMIN, USE:")
    print("="*70)
    if admins:
        admin = admins[0]
        print(f"   Full Name: {admin['fullname']}")
        print(f"   Email: {admin['email']}")
        print(f"   Phone: {admin['phone']}")
        print(f"   Password: [Your original password before hashing]")
    print("="*70 + "\n")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
