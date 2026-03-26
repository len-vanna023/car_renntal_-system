"""
Restore/Add the main admin accounts
"""
import mysql.connector
from werkzeug.security import generate_password_hash

def restore_admins():
    """Restore the main admin accounts"""
    
    # Main admin accounts to ensure exist
    main_admins = [
        {
            'fullname': 'nana cute',
            'email': 'cute@gmail.com',
            'phone': '0987654321',
            'password': '123456789'
        }
    ]
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='car_rental_db',
            use_pure=True
        )
        cursor = conn.cursor()
        
        print("\n" + "="*70)
        print("🔄 RESTORING MAIN ADMIN ACCOUNTS")
        print("="*70 + "\n")
        
        for admin in main_admins:
            # Check if exists
            cursor.execute("SELECT email FROM admin_accounts WHERE email = %s", 
                         (admin['email'].lower(),))
            
            if cursor.fetchone():
                print(f"✅ Admin '{admin['email']}' already exists - skipping")
            else:
                # Hash password and insert
                hashed_password = generate_password_hash(admin['password'])
                
                cursor.execute("""
                    INSERT INTO admin_accounts (fullname, email, phone, password)
                    VALUES (%s, %s, %s, %s)
                """, (admin['fullname'], admin['email'].lower(), admin['phone'], hashed_password))
                
                conn.commit()
                
                print(f"✅ Added admin: {admin['email']}")
                print(f"   Full Name: {admin['fullname']}")
                print(f"   Phone:     {admin['phone']}")
                print(f"   Password:  {admin['password']}")
                print()
        
        # Show all current admins
        print("\n" + "="*70)
        print("📊 ALL ADMIN ACCOUNTS IN DATABASE")
        print("="*70 + "\n")
        
        cursor.execute("SELECT id, fullname, email, phone FROM admin_accounts ORDER BY id")
        admins = cursor.fetchall()
        
        for admin in admins:
            print(f"👤 ID: {admin[0]}")
            print(f"   Name:  {admin[1]}")
            print(f"   Email: {admin[2]}")
            print(f"   Phone: {admin[3]}")
            print()
        
        print("="*70)
        print(f"✅ Total admin accounts: {len(admins)}")
        print("="*70 + "\n")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database error: {e}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    restore_admins()
