"""
Car Rental System - Complete MySQL Database Setup Script
This script will create and initialize the entire database structure for your system
"""

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash
import json

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change this if your MySQL has a password
    'database': 'car_rental_db'
}

def create_database():
    """Create the database if it doesn't exist"""
    print("\n" + "="*60)
    print("STEP 1: Creating Database")
    print("="*60)
    
    try:
        # Connect without database selection
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Database '{DB_CONFIG['database']}' created successfully!")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables"""
    print("\n" + "="*60)
    print("STEP 2: Creating Tables")
    print("="*60)
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 1. Users Table
        print("\n📋 Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Users table created")
        
        # 2. Admin Accounts Table
        print("📋 Creating 'admin_accounts' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_admin_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Admin accounts table created")
        
        # 3. Cars Table
        print("📋 Creating 'cars' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                image TEXT,
                seats INT NOT NULL,
                transmission VARCHAR(20) NOT NULL,
                features TEXT,
                color VARCHAR(50),
                status VARCHAR(20) DEFAULT 'available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Cars table created")
        
        # 4. Bookings Table
        print("📋 Creating 'bookings' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_email VARCHAR(100) NOT NULL,
                user_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                car_id INT NOT NULL,
                car_name VARCHAR(100) NOT NULL,
                car_image TEXT,
                pickup_date DATE NOT NULL,
                return_date DATE NOT NULL,
                days INT NOT NULL,
                base_cost DECIMAL(10, 2) NOT NULL,
                discount_amount DECIMAL(10, 2) DEFAULT 0,
                total_cost DECIMAL(10, 2) NOT NULL,
                discounts_applied TEXT,
                status VARCHAR(20) DEFAULT 'confirmed',
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_user_email (user_email),
                INDEX idx_car_id (car_id),
                INDEX idx_status (status),
                INDEX idx_dates (pickup_date, return_date),
                FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE RESTRICT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Bookings table created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ All tables created successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_default_admin():
    """Insert default admin account"""
    print("\n" + "="*60)
    print("STEP 3: Creating Default Admin Account")
    print("="*60)
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT COUNT(*) FROM admin_accounts WHERE email = 'admin@luxedrive.com'")
        if cursor.fetchone()[0] > 0:
            print("ℹ️  Default admin already exists. Skipping...")
            cursor.close()
            conn.close()
            return True
        
        # Create default admin
        admin_data = {
            'fullname': 'System Administrator',
            'email': 'admin@luxedrive.com',
            'phone': '0891234567',
            'password': generate_password_hash('0707200717')
        }
        
        cursor.execute("""
            INSERT INTO admin_accounts (fullname, email, phone, password)
            VALUES (%s, %s, %s, %s)
        """, (admin_data['fullname'], admin_data['email'], admin_data['phone'], admin_data['password']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Default admin account created successfully!")
        print("\n📝 Admin Credentials:")
        print("   Email:    admin@luxedrive.com")
        print("   Password: 0707200717")
        print("   Name:     System Administrator")
        print("   Phone:    0891234567")
        
        return True
        
    except Error as e:
        print(f"❌ Error creating admin account: {e}")
        return False

def insert_sample_cars():
    """Insert sample cars into the database"""
    print("\n" + "="*60)
    print("STEP 4: Adding Sample Cars")
    print("="*60)
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if cars already exist
        cursor.execute("SELECT COUNT(*) FROM cars")
        car_count = cursor.fetchone()[0]
        
        if car_count > 0:
            print(f"ℹ️  Database already has {car_count} cars. Skipping sample data...")
            cursor.close()
            conn.close()
            return True
        
        # Sample cars data
        sample_cars = [
            {
                'name': 'Tesla Model S',
                'category': 'luxury',
                'price': 299.99,
                'image': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['Autopilot', 'Premium Sound', 'Panoramic Roof', 'Heated Seats']),
                'color': 'Pearl White',
                'status': 'available'
            },
            {
                'name': 'BMW 7 Series',
                'category': 'luxury',
                'price': 249.99,
                'image': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['Massage Seats', 'Executive Lounge', 'Premium Audio', 'Night Vision']),
                'color': 'Black Sapphire',
                'status': 'available'
            },
            {
                'name': 'Mercedes-Benz S-Class',
                'category': 'luxury',
                'price': 279.99,
                'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['MBUX System', 'Burmester Audio', 'Air Balance', 'Magic Body Control']),
                'color': 'Selenite Grey',
                'status': 'available'
            },
            {
                'name': 'Audi A8',
                'category': 'luxury',
                'price': 259.99,
                'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['Matrix LED', 'Virtual Cockpit', 'Bang & Olufsen', 'AI Traffic Assist']),
                'color': 'Navarra Blue',
                'status': 'available'
            },
            {
                'name': 'Toyota Camry',
                'category': 'sedan',
                'price': 89.99,
                'image': 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['Apple CarPlay', 'Lane Assist', 'Adaptive Cruise', 'Backup Camera']),
                'color': 'Silver',
                'status': 'available'
            },
            {
                'name': 'Honda Accord',
                'category': 'sedan',
                'price': 85.99,
                'image': 'https://images.unsplash.com/photo-1590362891991-f776e747a588?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['Honda Sensing', 'Wireless Charging', 'Sunroof', 'Premium Audio']),
                'color': 'Modern Steel',
                'status': 'available'
            },
            {
                'name': 'Porsche 911',
                'category': 'sports',
                'price': 399.99,
                'image': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800',
                'seats': 2,
                'transmission': 'automatic',
                'features': json.dumps(['Sport Chrono', 'PASM', 'Sport Exhaust', 'Carbon Brakes']),
                'color': 'Guards Red',
                'status': 'available'
            },
            {
                'name': 'Ford Mustang GT',
                'category': 'sports',
                'price': 179.99,
                'image': 'https://images.unsplash.com/photo-1584345604476-8ec5f49fdb28?w=800',
                'seats': 4,
                'transmission': 'manual',
                'features': json.dumps(['5.0L V8', 'Performance Pack', 'Recaro Seats', 'Active Exhaust']),
                'color': 'Race Red',
                'status': 'available'
            },
            {
                'name': 'Toyota RAV4',
                'category': 'suv',
                'price': 95.99,
                'image': 'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['AWD', 'Safety Sense', 'Power Liftgate', 'Blind Spot Monitor']),
                'color': 'Blueprint',
                'status': 'available'
            },
            {
                'name': 'Honda CR-V',
                'category': 'suv',
                'price': 92.99,
                'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800',
                'seats': 5,
                'transmission': 'automatic',
                'features': json.dumps(['Honda Sensing', 'Turbo Engine', 'Hands-Free Liftgate', 'Panoramic Sunroof']),
                'color': 'Sonic Gray Pearl',
                'status': 'available'
            },
            {
                'name': 'Lamborghini Huracán',
                'category': 'exotic',
                'price': 899.99,
                'image': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800',
                'seats': 2,
                'transmission': 'automatic',
                'features': json.dumps(['V10 Engine', 'Carbon Fiber', 'Track Mode', 'Launch Control']),
                'color': 'Arancio Borealis',
                'status': 'available'
            },
            {
                'name': 'Ferrari F8 Tributo',
                'category': 'exotic',
                'price': 999.99,
                'image': 'https://images.unsplash.com/photo-1592198084033-aade902d1aae?w=800',
                'seats': 2,
                'transmission': 'automatic',
                'features': json.dumps(['Twin-Turbo V8', 'Side Slip Control', 'F1-Trac', 'Carbon Fiber']),
                'color': 'Rosso Corsa',
                'status': 'available'
            }
        ]
        
        print(f"\n📦 Inserting {len(sample_cars)} sample cars...")
        
        for car in sample_cars:
            cursor.execute("""
                INSERT INTO cars (name, category, price, image, seats, transmission, features, color, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (car['name'], car['category'], car['price'], car['image'], car['seats'], 
                  car['transmission'], car['features'], car['color'], car['status']))
            print(f"  ✓ Added: {car['name']} ({car['category']}) - ${car['price']}/day")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✅ {len(sample_cars)} sample cars added successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error inserting sample cars: {e}")
        return False

def verify_setup():
    """Verify the database setup"""
    print("\n" + "="*60)
    print("STEP 5: Verifying Database Setup")
    print("="*60)
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check each table
        tables = ['users', 'admin_accounts', 'cars', 'bookings']
        
        print("\n📊 Database Statistics:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table.capitalize():20} {count:>5} records")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database verification completed!")
        return True
        
    except Error as e:
        print(f"❌ Error verifying database: {e}")
        return False

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🚗 CAR RENTAL SYSTEM - MYSQL DATABASE SETUP")
    print("="*60)
    print("\nThis script will set up your complete database structure")
    print("including tables, admin account, and sample data.\n")
    
    input("Press Enter to continue...")
    
    # Run setup steps
    steps = [
        ("Create Database", create_database),
        ("Create Tables", create_tables),
        ("Insert Admin Account", insert_default_admin),
        ("Insert Sample Cars", insert_sample_cars),
        ("Verify Setup", verify_setup)
    ]
    
    success = True
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Failed at step: {step_name}")
            success = False
            break
    
    if success:
        print("\n" + "="*60)
        print("✅ DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📝 Quick Start Guide:")
        print("   1. Start your Flask application: python app.py")
        print("   2. Admin Login: http://localhost:5000/admin/login")
        print("      Email: admin@luxedrive.com")
        print("      Password: 0707200717")
        print("   3. Create a customer account: http://localhost:5000/signup")
        print("   4. Browse cars: http://localhost:5000/cars")
        print("\n🎉 Your Car Rental System is ready to use!")
        print("="*60 + "\n")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        print("Make sure MySQL is running and credentials are correct.\n")

if __name__ == "__main__":
    main()
