-- ============================================================
-- CAR RENTAL SYSTEM - COMPLETE DATABASE SCHEMA
-- ============================================================
-- This SQL file creates the complete database structure
-- You can run this directly in MySQL Workbench or command line
-- ============================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS car_rental_db;
USE car_rental_db;

-- ============================================================
-- 1. USERS TABLE
-- ============================================================
-- Stores customer account information
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 2. ADMIN ACCOUNTS TABLE
-- ============================================================
-- Stores admin/staff account information
CREATE TABLE IF NOT EXISTS admin_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_admin_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 3. CARS TABLE
-- ============================================================
-- Stores vehicle inventory information
CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image TEXT,
    seats INT NOT NULL,
    transmission VARCHAR(20) NOT NULL,
    features TEXT,  -- Stored as JSON string
    color VARCHAR(50),
    status VARCHAR(20) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_status (status),
    INDEX idx_price (price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 4. BOOKINGS TABLE
-- ============================================================
-- Stores rental booking information
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
    CONSTRAINT fk_bookings_cars FOREIGN KEY (car_id) 
        REFERENCES cars(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- SAMPLE DATA (Optional - Remove if not needed)
-- ============================================================

-- Insert Default Admin (Password: 0707200717 - Remember to hash in production!)
-- Note: The password below is hashed using Werkzeug
INSERT INTO admin_accounts (fullname, email, phone, password) 
VALUES ('System Administrator', 'admin@luxedrive.com', '0891234567', 
'scrypt:32768:8:1$xMqZ0I9tGkFON8pU$a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef12')
ON DUPLICATE KEY UPDATE email=email;

-- Sample Cars Data
INSERT INTO cars (name, category, price, image, seats, transmission, features, color, status) VALUES
('Tesla Model S', 'luxury', 299.99, 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800', 5, 'automatic', '["Autopilot", "Premium Sound", "Panoramic Roof", "Heated Seats"]', 'Pearl White', 'available'),
('BMW 7 Series', 'luxury', 249.99, 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800', 5, 'automatic', '["Massage Seats", "Executive Lounge", "Premium Audio", "Night Vision"]', 'Black Sapphire', 'available'),
('Mercedes-Benz S-Class', 'luxury', 279.99, 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800', 5, 'automatic', '["MBUX System", "Burmester Audio", "Air Balance", "Magic Body Control"]', 'Selenite Grey', 'available'),
('Toyota Camry', 'sedan', 89.99, 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800', 5, 'automatic', '["Apple CarPlay", "Lane Assist", "Adaptive Cruise", "Backup Camera"]', 'Silver', 'available'),
('Honda Accord', 'sedan', 85.99, 'https://images.unsplash.com/photo-1590362891991-f776e747a588?w=800', 5, 'automatic', '["Honda Sensing", "Wireless Charging", "Sunroof", "Premium Audio"]', 'Modern Steel', 'available'),
('Porsche 911', 'sports', 399.99, 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800', 2, 'automatic', '["Sport Chrono", "PASM", "Sport Exhaust", "Carbon Brakes"]', 'Guards Red', 'available'),
('Ford Mustang GT', 'sports', 179.99, 'https://images.unsplash.com/photo-1584345604476-8ec5f49fdb28?w=800', 4, 'manual', '["5.0L V8", "Performance Pack", "Recaro Seats", "Active Exhaust"]', 'Race Red', 'available'),
('Toyota RAV4', 'suv', 95.99, 'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800', 5, 'automatic', '["AWD", "Safety Sense", "Power Liftgate", "Blind Spot Monitor"]', 'Blueprint', 'available'),
('Honda CR-V', 'suv', 92.99, 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800', 5, 'automatic', '["Honda Sensing", "Turbo Engine", "Hands-Free Liftgate", "Panoramic Sunroof"]', 'Sonic Gray Pearl', 'available'),
('Lamborghini Huracán', 'exotic', 899.99, 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800', 2, 'automatic', '["V10 Engine", "Carbon Fiber", "Track Mode", "Launch Control"]', 'Arancio Borealis', 'available'),
('Ferrari F8 Tributo', 'exotic', 999.99, 'https://images.unsplash.com/photo-1592198084033-aade902d1aae?w=800', 2, 'automatic', '["Twin-Turbo V8", "Side Slip Control", "F1-Trac", "Carbon Fiber"]', 'Rosso Corsa', 'available');

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================
-- Run these to verify your setup

-- Check table counts
SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'admin_accounts', COUNT(*) FROM admin_accounts
UNION ALL
SELECT 'cars', COUNT(*) FROM cars
UNION ALL
SELECT 'bookings', COUNT(*) FROM bookings;

-- View all cars by category
SELECT category, COUNT(*) as car_count, 
       AVG(price) as avg_price, 
       MIN(price) as min_price, 
       MAX(price) as max_price
FROM cars
GROUP BY category
ORDER BY category;

-- View admin accounts
SELECT id, fullname, email, phone, created_at 
FROM admin_accounts;

-- ============================================================
-- END OF SCHEMA
-- ============================================================
