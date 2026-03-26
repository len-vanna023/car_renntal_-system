"""
Migrate cars table to add new comprehensive fields
"""
from db_config import get_db_connection
from mysql.connector import Error

def migrate_cars_table():
    """Add new fields to cars table"""
    
    print("\n" + "="*70)
    print("🔄 MIGRATING CARS TABLE - ADDING NEW FIELDS")
    print("="*70)
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor()
        
        # List of new columns to add
        new_columns = [
            ("brand", "VARCHAR(50) NOT NULL DEFAULT 'Unknown'"),
            ("model", "VARCHAR(50) NOT NULL DEFAULT 'Unknown'"),
            ("year", "INT NOT NULL DEFAULT 2024"),
            ("fuel_type", "VARCHAR(30) DEFAULT 'Gasoline'"),
            ("engine", "VARCHAR(50)"),
            ("horsepower", "INT"),
            ("mileage", "INT DEFAULT 0"),
            ("license_plate", "VARCHAR(20)"),
            ("vin", "VARCHAR(50)"),
            ("location", "VARCHAR(100) DEFAULT 'Main Branch'"),
            ("doors", "INT DEFAULT 4"),
            ("luggage_capacity", "INT DEFAULT 2"),
            ("air_conditioning", "BOOLEAN DEFAULT TRUE"),
            ("gps", "BOOLEAN DEFAULT FALSE"),
            ("bluetooth", "BOOLEAN DEFAULT TRUE"),
            ("backup_camera", "BOOLEAN DEFAULT FALSE"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]
        
        print("\n📝 Adding new columns to cars table:")
        print("-"*70)
        
        added_count = 0
        skipped_count = 0
        
        for column_name, column_definition in new_columns:
            try:
                # Try to add the column
                sql = f"ALTER TABLE cars ADD COLUMN {column_name} {column_definition}"
                cursor.execute(sql)
                print(f"✅ Added: {column_name}")
                added_count += 1
            except Error as e:
                if "Duplicate column" in str(e):
                    print(f"⚠️  {column_name} already exists - SKIPPED")
                    skipped_count += 1
                else:
                    print(f"❌ Error adding {column_name}: {e}")
        
        conn.commit()
        
        print("\n" + "="*70)
        print("✅ MIGRATION COMPLETE!")
        print("="*70)
        print(f"   Added: {added_count} new columns")
        print(f"   Skipped: {skipped_count} existing columns")
        
        # Show current table structure
        cursor.execute("DESCRIBE cars")
        columns = cursor.fetchall()
        
        print("\n📋 CURRENT CARS TABLE STRUCTURE:")
        print("-"*70)
        for col in columns:
            field_name = col[0]
            field_type = col[1]
            print(f"   {field_name:20s} {field_type}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*70)
        print("🎉 Your cars table is now ready for comprehensive data!")
        print("="*70)
        
    except Error as e:
        print(f"❌ Migration error: {e}")

def show_new_fields_info():
    """Show information about new fields"""
    
    print("\n" + "="*70)
    print("📚 NEW CAR FIELDS EXPLAINED")
    print("="*70)
    
    fields_info = {
        "brand": "Car manufacturer (e.g., Toyota, BMW, Mercedes)",
        "model": "Car model name (e.g., Camry, X5, E-Class)",
        "year": "Manufacturing year (e.g., 2024, 2023)",
        "fuel_type": "Fuel type (Gasoline, Diesel, Electric, Hybrid)",
        "engine": "Engine specifications (e.g., 2.0L Turbo, V6)",
        "horsepower": "Engine power in HP (e.g., 250, 300)",
        "mileage": "Current mileage in km (e.g., 15000)",
        "license_plate": "Vehicle license plate number",
        "vin": "Vehicle Identification Number (unique ID)",
        "location": "Current car location/branch",
        "doors": "Number of doors (2, 4, 5)",
        "luggage_capacity": "Luggage bags capacity (1-5)",
        "air_conditioning": "Has A/C (True/False)",
        "gps": "Has GPS navigation (True/False)",
        "bluetooth": "Has Bluetooth (True/False)",
        "backup_camera": "Has backup camera (True/False)",
        "updated_at": "Last update timestamp (auto-updated)"
    }
    
    print("\n🔍 Field Descriptions:")
    print("-"*70)
    for field, description in fields_info.items():
        print(f"\n   {field}:")
        print(f"      {description}")
    
    print("\n" + "="*70)
    print("💡 BENEFITS OF NEW FIELDS:")
    print("="*70)
    print("""
    ✅ More detailed car information
    ✅ Better filtering and search options
    ✅ API-ready structure
    ✅ Professional inventory management
    ✅ Track vehicle maintenance (mileage)
    ✅ Legal compliance (license plate, VIN)
    ✅ Better customer experience
    ✅ Modern features tracking (GPS, Bluetooth, etc.)
    """)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚗 CAR TABLE MIGRATION TOOL")
    print("="*70)
    print("""
This will add new comprehensive fields to your cars table.
Your existing car data will NOT be deleted!
New fields will have default values.
    """)
    
    migrate_cars_table()
    show_new_fields_info()
    
    print("\n✨ Migration complete! Restart your Flask app to use new fields.\n")
