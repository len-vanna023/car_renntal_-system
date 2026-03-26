import os
import mysql.connector
from mysql.connector import pooling, Error
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../../config/.env')
load_dotenv(dotenv_path)

# Secure database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'car_rental_db'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'use_pure': True,
    'autocommit': False,
}

# Create connection pool for better resource management and security
connection_pool = None
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="car_rental_pool",
        pool_size=5,
        pool_reset_session=True,
        **db_config
    )
except Error as e:
    print(f"Error creating connection pool: {e}")


def get_db_connection():
    """Get a secure connection from the pool"""
    if not connection_pool:
        return None
    try:
        return connection_pool.get_connection()
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def close_db_connection(conn):
    """Properly close a database connection"""
    try:
        if conn:
            conn.close()
    except Error as e:
        print(f"Error closing connection: {e}")
    except Exception as e:
        print(f"Error closing connection: {e}")


def init_database():
    """Initialize database tables with proper structure"""
    conn = None
    try:
        # Connect without database first
        raw_conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=int(os.getenv('DB_PORT', 3306)),
            use_pure=True
        )
        cursor = raw_conn.cursor()

        # Create database if not exists
        db_name = os.getenv('DB_NAME', 'car_rental_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        raw_conn.close()

        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        
        # Create users table with security best practices
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                INDEX idx_email (email),
                INDEX idx_is_active (is_active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create admin_accounts table with proper indexing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE,
                phone VARCHAR(20),
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                INDEX idx_email (email),
                INDEX idx_is_active (is_active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create bookings table with foreign keys
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_email VARCHAR(120) NOT NULL,
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
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create cars table with comprehensive fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                brand VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                year INT NOT NULL,
                category VARCHAR(50) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                image TEXT,
                seats INT NOT NULL,
                transmission VARCHAR(20) NOT NULL,
                fuel_type VARCHAR(30) DEFAULT 'Gasoline',
                engine VARCHAR(50),
                horsepower INT,
                mileage INT DEFAULT 0,
                license_plate VARCHAR(20) UNIQUE,
                vin VARCHAR(50) UNIQUE,
                location VARCHAR(100) DEFAULT 'Main Branch',
                features TEXT,
                color VARCHAR(50),
                doors INT DEFAULT 4,
                luggage_capacity INT DEFAULT 2,
                air_conditioning BOOLEAN DEFAULT TRUE,
                gps BOOLEAN DEFAULT FALSE,
                bluetooth BOOLEAN DEFAULT TRUE,
                backup_camera BOOLEAN DEFAULT FALSE,
                status VARCHAR(20) DEFAULT 'available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_brand (brand),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        conn.commit()
        
        # Create default admin account if none exists
        cursor.execute("SELECT COUNT(*) FROM admin_accounts")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            YOUR_CUSTOM_PASSWORD = 'AdminLuxe2024!'  # Change in production
            default_password = generate_password_hash(YOUR_CUSTOM_PASSWORD)
            cursor.execute("""
                INSERT INTO admin_accounts (fullname, email, phone, password) 
                VALUES (%s, %s, %s, %s)
            """, ('LuxeDrive Admin', 'admin@luxedrive.com', '1234567890', default_password))
            conn.commit()
            print("\n" + "="*60)
            print("✅ DEFAULT ADMIN ACCOUNT CREATED SUCCESSFULLY!")
            print("="*60)
            print("   📧 Email: admin@luxedrive.com")
            print("   👤 Full Name: LuxeDrive Admin")
            print("   📱 Phone: 1234567890")
            print(f"   🔑 Password: {YOUR_CUSTOM_PASSWORD}")
            print("="*60)
            print("⚠️  SAVE THESE CREDENTIALS - You'll need them to login!")
            print("="*60 + "\n")
        
        cursor.close()
        close_db_connection(conn)
        
        print("✅ Database tables created successfully!")
        return True
        
    except Error as e:
        print(f"Database initialization error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            close_db_connection(conn)
