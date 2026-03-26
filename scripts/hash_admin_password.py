"""
Utility script to hash the admin password in the database
Run this once to update the plain text password to a hashed password
"""
import mysql.connector
from werkzeug.security import generate_password_hash

def hash_admin_passwords():
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
        cursor.execute("SELECT id, email, password FROM admin_accounts")
        admins = cursor.fetchall()
        
        print("\n" + "="*60)
        print("🔐 HASHING ADMIN PASSWORDS")
        print("="*60)
        
        for admin in admins:
            admin_id = admin['id']
            email = admin['email']
            current_password = admin['password']
            
            # Check if password is already hashed (hashed passwords start with specific prefixes)
            if current_password.startswith(('pbkdf2:', 'scrypt:', 'bcrypt:', '$')):
                print(f"✅ {email}: Password already hashed")
                continue
            
            # Hash the plain text password
            hashed_password = generate_password_hash(current_password)
            
            # Update the password in database
            cursor.execute(
                "UPDATE admin_accounts SET password = %s WHERE id = %s",
                (hashed_password, admin_id)
            )
            conn.commit()
            
            print(f"✅ {email}: Password hashed successfully")
            print(f"   Original: {current_password}")
            print(f"   Hashed: {hashed_password[:50]}...")
        
        print("="*60)
        print("✅ All admin passwords have been processed!")
        print("="*60 + "\n")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    hash_admin_passwords()
