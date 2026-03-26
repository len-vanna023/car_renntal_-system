"""Create a test customer account"""
from db_config import get_db_connection
from werkzeug.security import generate_password_hash
from mysql.connector import Error, IntegrityError

def create_test_customer():
    """Create a test customer account for easy testing"""
    
    # Test customer details
    fullname = "Test Customer"
    email = "test@customer.com"
    phone = "0123456789"
    password = "password123"
    
    print("\n🔧 CREATING TEST CUSTOMER ACCOUNT...")
    print("="*60)
    
    # Check if user already exists
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"⚠️  Customer already exists: {email}")
            print("\n📋 EXISTING CUSTOMER INFO:")
            print(f"   Name: {existing_user['name']}")
            print(f"   Email: {existing_user['email']}")
            print(f"   Phone: {existing_user['phone']}")
            print(f"   Password: password123 (for testing)")
        else:
            # Create new customer
            password_hash = generate_password_hash(password)
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                    (fullname, email, phone, password_hash)
                )
                conn.commit()
                print("✅ TEST CUSTOMER CREATED SUCCESSFULLY!")
                print("\n📋 CUSTOMER INFO:")
                print(f"   Name: {fullname}")
                print(f"   Email: {email}")
                print(f"   Phone: {phone}")
                print(f"   Password: {password}")
            except (Error, IntegrityError) as e:
                print(f"❌ Failed to create customer: {e}")
        
        # Show all customers
        cursor.execute("SELECT id, name, email, phone, created_at FROM users ORDER BY id")
        all_customers = cursor.fetchall()
        
        print("\n" + "="*60)
        print("👥 ALL CUSTOMERS IN DATABASE:")
        print("="*60)
        
        if not all_customers:
            print("⚠️  No customers found!")
        else:
            for idx, customer in enumerate(all_customers, 1):
                print(f"\n👤 Customer #{idx}:")
                print(f"   ID: {customer['id']}")
                print(f"   Name: {customer['name']}")
                print(f"   Email: {customer['email']}")
                print(f"   Phone: {customer['phone']}")
                print(f"   Created: {customer['created_at']}")
        
        print("\n" + "="*60)
        print("🎯 LOGIN INFO:")
        print("="*60)
        print("   URL: http://localhost:5000/login")
        print("   Email: test@customer.com")
        print("   Password: password123")
        print("="*60 + "\n")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    create_test_customer()
