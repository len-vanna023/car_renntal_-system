"""
DEMO: Add Sample Admin Accounts
This demonstrates how to add admin accounts to MySQL
"""
import mysql.connector
from werkzeug.security import generate_password_hash

def add_demo_admins():
    """Add sample admin accounts for testing"""
    
    # Sample admins to add
    sample_admins = [
        {
            'fullname': 'Len Vanna',
            'email': 'vanna@gmail.com',
            'phone': '0123456789',
            'password': 'Vanna@123'
        },
        {
            'fullname': 'Admin User',
            'email': 'admin@luxedrive.com',
            'phone': '0987654321',
            'password': 'Admin@123'
        },
        {
            'fullname': 'Manager',
            'email': 'manager@luxedrive.com',
            'phone': '0111222333',
            'password': 'Manager@123'
        }
    ]
    
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='car_rental_db',
            use_pure=True
        )
        cursor = conn.cursor()
        
        print("\n" + "="*70)
        print("➕ ADDING SAMPLE ADMIN ACCOUNTS")
        print("="*70 + "\n")
        
        added_count = 0
        skipped_count = 0
        
        for admin in sample_admins:
            # Check if email already exists
            cursor.execute("SELECT email FROM admin_accounts WHERE email = %s", 
                         (admin['email'].lower(),))
            
            if cursor.fetchone():
                print(f"⏭️  Skipped: {admin['email']} (already exists)")
                skipped_count += 1
                continue
            
            # Hash password
            hashed_password = generate_password_hash(admin['password'])
            
            # Insert admin
            cursor.execute("""
                INSERT INTO admin_accounts (fullname, email, phone, password)
                VALUES (%s, %s, %s, %s)
            """, (admin['fullname'], admin['email'].lower(), admin['phone'], hashed_password))
            
            conn.commit()
            
            print(f"✅ Added: {admin['fullname']} ({admin['email']})")
            added_count += 1
        
        print("\n" + "="*70)
        print(f"✅ Added: {added_count} admin(s)")
        print(f"⏭️  Skipped: {skipped_count} admin(s) (already exist)")
        print("="*70 + "\n")
        
        if added_count > 0:
            print("📝 LOGIN CREDENTIALS FOR NEW ADMINS:")
            print("="*70 + "\n")
            
            for admin in sample_admins:
                # Check if this was newly added
                cursor.execute("SELECT email FROM admin_accounts WHERE email = %s", 
                             (admin['email'].lower(),))
                if cursor.fetchone():
                    print(f"👤 {admin['fullname']}")
                    print(f"   Email:    {admin['email']}")
                    print(f"   Phone:    {admin['phone']}")
                    print(f"   Password: {admin['password']}")
                    print()
            
            print("="*70)
            print("🌐 Login URL: http://localhost:5000/admin/login")
            print("="*70 + "\n")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database error: {e}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    print("\n⚠️  This will add sample admin accounts to your database.")
    print("   Existing accounts will be skipped.\n")
    
    response = input("Continue? (yes/no): ").lower()
    
    if response == 'yes':
        add_demo_admins()
    else:
        print("\n❌ Operation cancelled.\n")
