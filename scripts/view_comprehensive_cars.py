"""View comprehensive car data from database"""
from db_config import get_db_connection
from mysql.connector import Error
import json

def view_cars():
    """Display all cars with comprehensive details"""
    
    print("\n" + "="*80)
    print("🚗 CAR INVENTORY - COMPREHENSIVE VIEW")
    print("="*80)
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database!")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get all cars
        cursor.execute("SELECT * FROM cars ORDER BY price DESC")
        cars = cursor.fetchall()
        
        print(f"\n📊 Total Cars: {len(cars)}")
        print("="*80)
        
        for idx, car in enumerate(cars, 1):
            print(f"\n{'='*80}")
            print(f"🚗 CAR #{idx}: {car.get('name', 'N/A')}")
            print(f"{'='*80}")
            
            # Basic Info
            print(f"\n📋 BASIC INFORMATION:")
            print(f"   Brand:        {car.get('brand', 'N/A')}")
            print(f"   Model:        {car.get('model', 'N/A')}")
            print(f"   Year:         {car.get('year', 'N/A')}")
            print(f"   Category:     {car.get('category', 'N/A')}")
            print(f"   Color:        {car.get('color', 'N/A')}")
            
            # Pricing
            print(f"\n💰 PRICING:")
            print(f"   Daily Rate:   ${car.get('price', 0):.2f}")
            if car.get('weekly_rate'):
                print(f"   Weekly Rate:  ${car.get('weekly_rate', 0):.2f}")
            if car.get('monthly_rate'):
                print(f"   Monthly Rate: ${car.get('monthly_rate', 0):.2f}")
            
            # Technical Specs
            print(f"\n⚙️  TECHNICAL SPECIFICATIONS:")
            print(f"   Seats:        {car.get('seats', 'N/A')}")
            print(f"   Doors:        {car.get('doors', 'N/A')}")
            print(f"   Transmission: {car.get('transmission', 'N/A')}")
            print(f"   Fuel Type:    {car.get('fuel_type', 'N/A')}")
            if car.get('engine'):
                print(f"   Engine:       {car.get('engine', 'N/A')}")
            if car.get('horsepower'):
                print(f"   Horsepower:   {car.get('horsepower', 'N/A')} HP")
            if car.get('mileage'):
                print(f"   Mileage:      {car.get('mileage', 'N/A')}")
            
            # Features
            print(f"\n🎯 MODERN FEATURES:")
            print(f"   Air Conditioning: {'✅ Yes' if car.get('air_conditioning') else '❌ No'}")
            print(f"   GPS Navigation:   {'✅ Yes' if car.get('gps') else '❌ No'}")
            print(f"   Bluetooth:        {'✅ Yes' if car.get('bluetooth') else '❌ No'}")
            print(f"   Backup Camera:    {'✅ Yes' if car.get('backup_camera') else '❌ No'}")
            
            # Additional Features
            if car.get('features'):
                try:
                    features_list = json.loads(car['features'])
                    if features_list:
                        print(f"\n✨ PREMIUM FEATURES:")
                        for feature in features_list:
                            print(f"   • {feature}")
                except:
                    pass
            
            # Legal Info
            print(f"\n📄 LEGAL & TRACKING:")
            if car.get('license_plate'):
                print(f"   License Plate: {car.get('license_plate', 'N/A')}")
            if car.get('vin'):
                print(f"   VIN:           {car.get('vin', 'N/A')}")
            if car.get('insurance_number'):
                print(f"   Insurance:     {car.get('insurance_number', 'N/A')}")
            
            # Location & Status
            print(f"\n📍 LOCATION & STATUS:")
            print(f"   Location:      {car.get('location', 'N/A')}")
            status = car.get('status', 'N/A')
            status_emoji = "✅" if status == "available" else "❌"
            print(f"   Status:        {status_emoji} {status.upper()}")
            
            # Description
            if car.get('description'):
                print(f"\n📝 DESCRIPTION:")
                print(f"   {car.get('description', 'N/A')}")
        
        # Summary Statistics
        print(f"\n{'='*80}")
        print("📊 INVENTORY STATISTICS")
        print(f"{'='*80}")
        
        # By Category
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM cars 
            GROUP BY category 
            ORDER BY count DESC
        """)
        categories = cursor.fetchall()
        
        print(f"\n📋 By Category:")
        for cat in categories:
            print(f"   {cat['category']:<20} {cat['count']} cars")
        
        # By Fuel Type
        cursor.execute("""
            SELECT fuel_type, COUNT(*) as count 
            FROM cars 
            GROUP BY fuel_type 
            ORDER BY count DESC
        """)
        fuel_types = cursor.fetchall()
        
        print(f"\n⛽ By Fuel Type:")
        for fuel in fuel_types:
            print(f"   {fuel['fuel_type']:<20} {fuel['count']} cars")
        
        # By Modern Features
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN gps = 1 THEN 1 ELSE 0 END) as with_gps,
                SUM(CASE WHEN bluetooth = 1 THEN 1 ELSE 0 END) as with_bluetooth,
                SUM(CASE WHEN backup_camera = 1 THEN 1 ELSE 0 END) as with_camera,
                SUM(CASE WHEN air_conditioning = 1 THEN 1 ELSE 0 END) as with_ac
            FROM cars
        """)
        features_stats = cursor.fetchone()
        
        print(f"\n🎯 Modern Features:")
        print(f"   GPS Navigation:    {features_stats['with_gps']} cars")
        print(f"   Bluetooth:         {features_stats['with_bluetooth']} cars")
        print(f"   Backup Camera:     {features_stats['with_camera']} cars")
        print(f"   Air Conditioning:  {features_stats['with_ac']} cars")
        
        # Price Range
        cursor.execute("""
            SELECT 
                MIN(price) as min_price,
                MAX(price) as max_price,
                AVG(price) as avg_price
            FROM cars
        """)
        price_stats = cursor.fetchone()
        
        print(f"\n💰 Price Range:")
        print(f"   Minimum: ${price_stats['min_price']:.2f}/day")
        print(f"   Maximum: ${price_stats['max_price']:.2f}/day")
        print(f"   Average: ${price_stats['avg_price']:.2f}/day")
        
        cursor.close()
        conn.close()
        
        print(f"\n{'='*80}")
        print("✅ Your comprehensive car database is ready!")
        print(f"{'='*80}\n")
        
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    view_cars()
