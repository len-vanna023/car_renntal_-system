"""
Add New Admin Account to MySQL Database
Run this script to create new admin accounts
"""
import mysql.connector
from werkzeug.security import generate_password_hash

def add_admin_account(fullname, email, phone, password):
    """Add a new admin account to the database"""
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
        
        # Check if email already exists
        cursor.execute("SELECT email FROM admin_accounts WHERE email = %s", (email.lower(),))
        if cursor.fetchone():
            print(f"\n❌ Error: Email '{email}' already exists!")
            print("   Please use a different email address.\n")
            cursor.close()
            conn.close()
            return False
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Insert new admin
        cursor.execute("""
            INSERT INTO admin_accounts (fullname, email, phone, password)
            VALUES (%s, %s, %s, %s)
        """, (fullname, email.lower(), phone, hashed_password))
        
        conn.commit()
        
        print("\n" + "="*70)
        print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print("="*70)
        print(f"👤 Full Name: {fullname}")
        print(f"📧 Email:     {email}")
        print(f"📱 Phone:     {phone}")
        print(f"🔑 Password:  {password}")
        print("="*70)
        print("✅ You can now login with these credentials!")
        print("🌐 URL: http://localhost:5000/admin/login")
        print("="*70 + "\n")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database error: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return False

def interactive_add_admin():
    """Interactive mode to add admin"""
    print("\n" + "="*70)
    print("➕ ADD NEW ADMIN ACCOUNT TO MYSQL")
    print("="*70 + "\n")
    
    print("Please enter the admin details:\n")
    
    fullname = input("👤 Full Name: ").strip()
    if not fullname:
        print("❌ Full name is required!")
        return
    
    email = input("📧 Email:     ").strip()
    if not email:
        print("❌ Email is required!")
        return
    
    phone = input("📱 Phone:     ").strip()
    if not phone:
        print("❌ Phone is required!")
        return
    
    password = input("🔑 Password:  ").strip()
    if not password:
        print("❌ Password is required!")
        return
    
    # Confirm
    print("\n" + "-"*70)
    print("Please confirm the details:")
    print("-"*70)
    print(f"👤 Full Name: {fullname}")
    print(f"📧 Email:     {email}")
    print(f"📱 Phone:     {phone}")
    print(f"🔑 Password:  {password}")
    print("-"*70)
    
    confirm = input("\nCreate this admin account? (yes/no): ").lower()
    
    if confirm == 'yes':
        add_admin_account(fullname, email, phone, password)
    else:
        print("\n❌ Operation cancelled.\n")

def quick_add_examples():
    """Show quick examples of adding admins"""
    print("\n" + "="*70)
    print("📝 QUICK EXAMPLES - Uncomment to use")
    print("="*70 + "\n")
    
    print("Example 1: Add yourself as admin")
    print('add_admin_account("Your Name", "your@email.com", "1234567890", "your_password")')
    print()
    
    print("Example 2: Add another admin")
    print('add_admin_account("John Doe", "john@example.com", "0987654321", "john123")')
    print()
    
    print("Example 3: Add manager")
    print('add_admin_account("Manager", "manager@company.com", "5551234567", "manager2024")')
    print()

if __name__ == "__main__":
    # Choose mode:
    
    # MODE 1: Interactive - asks for input
    interactive_add_admin()
    
    # MODE 2: Direct - uncomment and modify the line below
    # add_admin_account("Your Name", "your@email.com", "1234567890", "your_password")
    
    # MODE 3: Multiple admins - uncomment to add multiple at once
    # add_admin_account("Admin One", "admin1@example.com", "1111111111", "admin123")
    # add_admin_account("Admin Two", "admin2@example.com", "2222222222", "admin456")
