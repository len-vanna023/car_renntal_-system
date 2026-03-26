"""
Add sample cars with all comprehensive fields
"""
from db_config import get_db_connection
from mysql.connector import Error
import json

def add_comprehensive_cars():
    """Add sample cars with complete information"""
    
    print("\n" + "="*70)
    print("🚗 ADDING COMPREHENSIVE CAR DATA")
    print("="*70)
    
    # Sample cars with ALL fields
    sample_cars = [
        {
            "name": "Mercedes-Benz S-Class 2024",
            "brand": "Mercedes-Benz",
            "model": "S-Class",
            "year": 2024,
            "category": "Luxury Sedan",
            "price": 250.00,
            "weekly_rate": 1500.00,
            "monthly_rate": 5000.00,
            "image": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8",
            "description": "Experience ultimate luxury with the Mercedes S-Class. Features cutting-edge technology, premium comfort, and exceptional performance.",
            "seats": 5,
            "doors": 4,
            "transmission": "Automatic",
            "fuel_type": "Gasoline",
            "engine": "3.0L V6 Turbo",
            "engine_size": "3.0L",
            "horsepower": 362,
            "mileage": "15,000 km",
            "luggage_capacity": 3,
            "features": json.dumps(["Leather Seats", "Panoramic Sunroof", "Heated Seats", "Massage Seats", "Premium Sound"]),
            "color": "Black Metallic",
            "air_conditioning": True,
            "gps": True,
            "bluetooth": True,
            "backup_camera": True,
            "license_plate": "LUX-S001",
            "vin": "WDDUG8CB1PA123456",
            "insurance_number": "INS-2024-MB-001",
            "location": "Main Branch",
            "status": "available"
        },
        {
            "name": "Tesla Model 3 2024",
            "brand": "Tesla",
            "model": "Model 3",
            "year": 2024,
            "category": "Electric Sedan",
            "price": 180.00,
            "weekly_rate": 1100.00,
            "monthly_rate": 4000.00,
            "image": "https://images.unsplash.com/photo-1560958089-b8a1929cea89",
            "description": "Experience the future of driving with Tesla Model 3. Full electric, autopilot capability, and zero emissions.",
            "seats": 5,
            "doors": 4,
            "transmission": "Automatic",
            "fuel_type": "Electric",
            "engine": "Dual Motor AWD",
            "engine_size": "N/A",
            "horsepower": 480,
            "mileage": "8,000 km",
            "luggage_capacity": 2,
            "features": json.dumps(["Autopilot", "Premium Interior", "Glass Roof", "Heated Seats", "15-inch Touchscreen"]),
            "color": "Pearl White",
            "air_conditioning": True,
            "gps": True,
            "bluetooth": True,
            "backup_camera": True,
            "license_plate": "EV-T001",
            "vin": "5YJ3E1EA1PF123456",
            "insurance_number": "INS-2024-TS-001",
            "location": "Airport Branch",
            "status": "available"
        },
        {
            "name": "Toyota Land Cruiser 2024",
            "brand": "Toyota",
            "model": "Land Cruiser",
            "year": 2024,
            "category": "Premium SUV",
            "price": 200.00,
            "weekly_rate": 1200.00,
            "monthly_rate": 4500.00,
            "image": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b",
            "description": "The legendary Toyota Land Cruiser - unmatched off-road capability with premium comfort. Perfect for adventures.",
            "seats": 7,
            "doors": 5,
            "transmission": "Automatic",
            "fuel_type": "Diesel",
            "engine": "3.3L V6 Twin-Turbo Diesel",
            "engine_size": "3.3L",
            "horsepower": 304,
            "mileage": "12,000 km",
            "luggage_capacity": 4,
            "features": json.dumps(["4WD", "Off-Road Package", "Leather", "Sunroof", "Multi-Terrain Select"]),
            "color": "White Pearl",
            "air_conditioning": True,
            "gps": True,
            "bluetooth": True,
            "backup_camera": True,
            "license_plate": "SUV-LC001",
            "vin": "JTMCY7AJ1P4123456",
            "insurance_number": "INS-2024-TY-001",
            "location": "Main Branch",
            "status": "available"
        },
        {
            "name": "BMW X7 2024",
            "brand": "BMW",
            "model": "X7",
            "year": 2024,
            "category": "Luxury SUV",
            "price": 220.00,
            "weekly_rate": 1300.00,
            "monthly_rate": 4800.00,
            "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e",
            "description": "BMW's flagship SUV offering exceptional luxury, space, and performance. Perfect for families and executives.",
            "seats": 7,
            "doors": 5,
            "transmission": "Automatic",
            "fuel_type": "Gasoline",
            "engine": "3.0L Inline-6 Turbo",
            "engine_size": "3.0L",
            "horsepower": 335,
            "mileage": "10,000 km",
            "luggage_capacity": 5,
            "features": json.dumps(["Panoramic Roof", "Ventilated Seats", "Premium Audio", "Adaptive Suspension", "Ambient Lighting"]),
            "color": "Carbon Black",
            "air_conditioning": True,
            "gps": True,
            "bluetooth": True,
            "backup_camera": True,
            "license_plate": "LUX-X7001",
            "vin": "5UXCW2C01P9123456",
            "insurance_number": "INS-2024-BMW-001",
            "location": "Main Branch",
            "status": "available"
        },
        {
            "name": "Porsche 911 Carrera 2024",
            "brand": "Porsche",
            "model": "911 Carrera",
            "year": 2024,
            "category": "Sports Car",
            "price": 350.00,
            "weekly_rate": 2100.00,
            "monthly_rate": 8000.00,
            "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70",
            "description": "The iconic Porsche 911 - a perfect blend of luxury and performance. Experience pure driving pleasure.",
            "seats": 4,
            "doors": 2,
            "transmission": "Automatic",
            "fuel_type": "Gasoline",
            "engine": "3.0L Twin-Turbo Flat-6",
            "engine_size": "3.0L",
            "horsepower": 379,
            "mileage": "5,000 km",
            "luggage_capacity": 1,
            "features": json.dumps(["Sport Chrono", "PASM", "Sport Exhaust", "Sport Seats Plus", "Porsche Communication Management"]),
            "color": "Racing Yellow",
            "air_conditioning": True,
            "gps": True,
            "bluetooth": True,
            "backup_camera": True,
            "license_plate": "SPT-911",
            "vin": "WP0AB2A99PS123456",
            "insurance_number": "INS-2024-POR-001",
            "location": "Premium Showroom",
            "status": "available"
        }
    ]
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor()
        
        print("\n📝 Adding comprehensive car data:")
        print("-"*70)
        
        added_count = 0
        
        for car in sample_cars:
            try:
                # Check if car already exists
                cursor.execute("SELECT id FROM cars WHERE vin = %s", (car['vin'],))
                existing = cursor.fetchone()
                
                if existing:
                    print(f"⚠️  {car['name']} (VIN: {car['vin']}) already exists - SKIPPED")
                    continue
                
                # Insert car with ALL fields
                sql = """
                    INSERT INTO cars (
                        name, brand, model, year, category, price, weekly_rate, monthly_rate,
                        image, description, seats, doors, transmission, fuel_type, engine,
                        engine_size, horsepower, mileage, luggage_capacity, features, color,
                        air_conditioning, gps, bluetooth, backup_camera, license_plate, vin,
                        insurance_number, location, status
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """
                
                values = (
                    car['name'], car['brand'], car['model'], car['year'], car['category'],
                    car['price'], car['weekly_rate'], car['monthly_rate'], car['image'],
                    car['description'], car['seats'], car['doors'], car['transmission'],
                    car['fuel_type'], car['engine'], car['engine_size'], car['horsepower'],
                    car['mileage'], car['luggage_capacity'], car['features'], car['color'],
                    car['air_conditioning'], car['gps'], car['bluetooth'], car['backup_camera'],
                    car['license_plate'], car['vin'], car['insurance_number'], car['location'],
                    car['status']
                )
                
                cursor.execute(sql, values)
                conn.commit()
                
                print(f"✅ Added: {car['name']}")
                print(f"   Brand: {car['brand']} | Model: {car['model']} | Year: {car['year']}")
                print(f"   Price: ${car['price']}/day | Features: {len(json.loads(car['features']))} items")
                print(f"   VIN: {car['vin']} | Location: {car['location']}")
                print()
                
                added_count += 1
                
            except Error as e:
                print(f"❌ Error adding {car['name']}: {e}")
        
        print("="*70)
        print(f"✅ Added {added_count} comprehensive cars to database!")
        print("="*70)
        
        # Show summary
        cursor.execute("""
            SELECT 
                brand, 
                COUNT(*) as count,
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price
            FROM cars 
            GROUP BY brand
            ORDER BY count DESC
        """)
        
        summary = cursor.fetchall()
        
        print("\n📊 CAR INVENTORY SUMMARY:")
        print("-"*70)
        print(f"{'Brand':<20} {'Count':<10} {'Avg Price':<15} {'Price Range':<20}")
        print("-"*70)
        
        for row in summary:
            brand, count, avg_price, min_price, max_price = row
            print(f"{brand:<20} {count:<10} ${avg_price:<14.2f} ${min_price:.2f} - ${max_price:.2f}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*70)
        print("🎉 COMPREHENSIVE CAR DATA LOADED!")
        print("="*70)
        print("""
Your database now has detailed car information including:
✅ Complete specifications (engine, horsepower, etc.)
✅ Modern features (GPS, Bluetooth, backup camera)
✅ Legal tracking (VIN, license plate, insurance)
✅ Maintenance info
✅ Multiple pricing options (daily, weekly, monthly)
✅ Rich descriptions and images
✅ Location tracking

Visit your website to see the enhanced car listings!
        """)
        
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚗 COMPREHENSIVE CAR DATA LOADER")
    print("="*70)
    print("""
This will add sample cars with ALL comprehensive fields:
- Basic info (brand, model, year)
- Technical specs (engine, HP, fuel type)
- Features (GPS, Bluetooth, A/C, camera)
- Legal info (VIN, license plate, insurance)
- Pricing (daily, weekly, monthly)
- Rich descriptions and images
    """)
    
    add_comprehensive_cars()
    
    print("\n✨ Your car rental system is now fully loaded with professional data!\n")
