from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
import json
import os
import mysql.connector
from mysql.connector import Error, IntegrityError
from app.models.db_config import get_db_connection, init_database, close_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))

app = Flask(__name__)

# Load secure configuration
from app.config import get_config
config = get_config()
app.config.from_object(config)

# Set secure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = config.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = config.SESSION_COOKIE_SAMESITE
app.config['PERMANENT_SESSION_LIFETIME'] = config.PERMANENT_SESSION_LIFETIME

# Google OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID', ''),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', ''),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


def get_user_by_email(email):
    """Fetch a single user by email."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


def normalize_phone(value):
    """Normalize phone numbers by stripping non-digit characters."""
    if not value:
        return ''
    return ''.join(ch for ch in value if ch.isdigit())


def create_user(fullname, email, phone, password_hash):
    """Insert a new user account."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (fullname, email, phone, password_hash)
        )
        conn.commit()
        return True
    except IntegrityError as e:
        print(f"Integrity error creating user: {e}")
        return False
    except Error as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)

# Ensure required tables exist before handling requests
if not init_database():
    print("⚠️  Warning: Database initialization failed. Check MySQL service and credentials.")

# Database helper functions for cars
def get_all_cars():
    """Fetch all cars from database"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars ORDER BY id")
        cars = cursor.fetchall()
        # Convert features from TEXT to list
        for car in cars:
            if car.get('features') and isinstance(car['features'], str):
                try:
                    car['features'] = json.loads(car['features'])
                except:
                    car['features'] = car['features'].split(',')
            car['price'] = float(car['price'])
        return cars
    except Error as e:
        print(f"Error fetching cars: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


def get_car_by_id(car_id):
    """Fetch a single car by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        if car:
            car['price'] = float(car['price'])
            if car.get('features') and isinstance(car['features'], str):
                try:
                    car['features'] = json.loads(car['features'])
                except:
                    car['features'] = car['features'].split(',')
        return car
    except Error as e:
        print(f"Error fetching car: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


# Home page route
@app.route('/')
def home():
    cars = get_all_cars()
    return render_template('index.html', cars=cars)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/cars')
def cars():
    all_cars = get_all_cars()
    return render_template('cars.html', cars=all_cars)


@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = get_car_by_id(car_id)
    if not car:
        return "Car not found", 404
    return render_template('car_detail.html', car=car)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not fullname or not email or not password:
            return render_template('signup.html', error="All fields are required")

        if password != confirm_password:
            return render_template('signup.html', error="Passwords don't match")

        if len(password) < 6:
            return render_template('signup.html', error="Password must be at least 6 characters")

        phone = normalize_phone(phone)

        password_hash = generate_password_hash(password)

        if create_user(fullname, email, phone, password_hash):
            session['user_name'] = fullname
            session['user_email'] = email
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', error="Email already exists or error creating account")

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('login.html', error="Email and password are required")

        user = get_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/bookings')
def bookings():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if not conn:
        return render_template('bookings.html', bookings=[], error="Database connection failed")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM bookings WHERE user_email = %s ORDER BY booking_date DESC",
            (session['user_email'],)
        )
        user_bookings = cursor.fetchall()
        return render_template('bookings.html', bookings=user_bookings)
    except Error as e:
        print(f"Error fetching bookings: {e}")
        return render_template('bookings.html', bookings=[], error="Error fetching bookings")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


@app.route('/book-car/<int:car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    if 'user_email' not in session:
        return redirect(url_for('login'))

    car = get_car_by_id(car_id)
    if not car:
        return "Car not found", 404

    if request.method == 'POST':
        pickup_date = request.form.get('pickup_date')
        return_date = request.form.get('return_date')

        if not pickup_date or not return_date:
            return render_template('car_detail.html', car=car, error="Please select both dates")

        try:
            pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
            return_dt = datetime.strptime(return_date, '%Y-%m-%d')

            if return_dt <= pickup:
                return render_template('car_detail.html', car=car, error="Return date must be after pickup date")

            days = (return_dt - pickup).days
            base_cost = float(car['price']) * days
            discount_amount = 0
            discounts_applied = ""

            # Weekend discount (20%)
            if return_dt.weekday() >= 4 or pickup.weekday() >= 4:
                weekend_discount = base_cost * 0.20
                discount_amount += weekend_discount
                discounts_applied += "Weekend Discount (20%), "

            # Long-term discount (10% for 7+ days)
            if days >= 7:
                long_term_discount = base_cost * 0.10
                discount_amount += long_term_discount
                discounts_applied += "Long-term Discount (10%), "

            discounts_applied = discounts_applied.rstrip(', ')
            total_cost = base_cost - discount_amount

            conn = get_db_connection()
            if not conn:
                return render_template('car_detail.html', car=car, error="Database connection failed")

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings 
                (user_email, user_name, phone, car_id, car_name, car_image, pickup_date, return_date, 
                 days, base_cost, discount_amount, total_cost, discounts_applied, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'confirmed')
            """, (
                session['user_email'],
                session['user_name'],
                request.form.get('phone', ''),
                car_id,
                car['name'],
                car.get('image', ''),
                pickup_date,
                return_date,
                days,
                base_cost,
                discount_amount,
                total_cost,
                discounts_applied
            ))
            conn.commit()
            cursor.close()
            close_db_connection(conn)

            return redirect(url_for('bookings'))

        except ValueError:
            return render_template('car_detail.html', car=car, error="Invalid date format")

    return render_template('car_detail.html', car=car)


# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            return render_template('admin/login.html', error="Username and password required")

        conn = get_db_connection()
        if not conn:
            return render_template('admin/login.html', error="Database connection failed")

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM admin_accounts WHERE (username = %s OR email = %s) AND is_active = True",
                (username, username)
            )
            admin = cursor.fetchone()

            if admin and check_password_hash(admin['password'], password):
                session['admin_id'] = admin['id']
                session['admin_name'] = admin['fullname']
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin/login.html', error="Invalid credentials")
        except Error as e:
            print(f"Admin login error: {e}")
            return render_template('admin/login.html', error="Error during login")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                close_db_connection(conn)

    return render_template('admin/login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if not conn:
        return render_template('admin/dashboard.html', stats={}, error="Database connection failed")

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM cars")
        total_cars = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM bookings")
        total_bookings = cursor.fetchone()['total']

        cursor.execute("SELECT SUM(total_cost) as revenue FROM bookings WHERE status = 'confirmed'")
        revenue = cursor.fetchone()['revenue'] or 0

        stats = {
            'total_users': total_users,
            'total_cars': total_cars,
            'total_bookings': total_bookings,
            'revenue': float(revenue)
        }

        return render_template('admin/dashboard.html', stats=stats)
    except Error as e:
        print(f"Dashboard error: {e}")
        return render_template('admin/dashboard.html', stats={}, error="Error loading dashboard")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


@app.route('/admin/cars')
def admin_cars():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    cars = get_all_cars()
    return render_template('admin/cars.html', cars=cars)


@app.route('/admin/add-car', methods=['GET', 'POST'])
def admin_add_car():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            return render_template('admin/add_car.html', error="Database connection failed")

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cars 
                (name, brand, model, year, category, price, image, seats, transmission, 
                 fuel_type, engine, horsepower, color, doors, luggage_capacity, 
                 air_conditioning, gps, bluetooth, backup_camera, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form.get('name'),
                request.form.get('brand'),
                request.form.get('model'),
                int(request.form.get('year', 0)),
                request.form.get('category'),
                float(request.form.get('price', 0)),
                request.form.get('image'),
                int(request.form.get('seats', 4)),
                request.form.get('transmission'),
                request.form.get('fuel_type'),
                request.form.get('engine'),
                int(request.form.get('horsepower', 0)),
                request.form.get('color'),
                int(request.form.get('doors', 4)),
                int(request.form.get('luggage_capacity', 2)),
                request.form.get('air_conditioning') == 'on',
                request.form.get('gps') == 'on',
                request.form.get('bluetooth') == 'on',
                request.form.get('backup_camera') == 'on',
                'available'
            ))
            conn.commit()
            cursor.close()
            close_db_connection(conn)
            return redirect(url_for('admin_cars'))
        except Exception as e:
            print(f"Error adding car: {e}")
            return render_template('admin/add_car.html', error="Error adding car")

    return render_template('admin/add_car.html')


@app.route('/admin/edit-car/<int:car_id>', methods=['GET', 'POST'])
def admin_edit_car(car_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    car = get_car_by_id(car_id)
    if not car:
        return "Car not found", 404

    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            return render_template('admin/edit_car.html', car=car, error="Database connection failed")

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars SET
                name = %s, brand = %s, model = %s, year = %s, category = %s, price = %s,
                image = %s, seats = %s, transmission = %s, fuel_type = %s, engine = %s,
                horsepower = %s, color = %s, doors = %s, luggage_capacity = %s,
                air_conditioning = %s, gps = %s, bluetooth = %s, backup_camera = %s
                WHERE id = %s
            """, (
                request.form.get('name'),
                request.form.get('brand'),
                request.form.get('model'),
                int(request.form.get('year', 0)),
                request.form.get('category'),
                float(request.form.get('price', 0)),
                request.form.get('image'),
                int(request.form.get('seats', 4)),
                request.form.get('transmission'),
                request.form.get('fuel_type'),
                request.form.get('engine'),
                int(request.form.get('horsepower', 0)),
                request.form.get('color'),
                int(request.form.get('doors', 4)),
                int(request.form.get('luggage_capacity', 2)),
                request.form.get('air_conditioning') == 'on',
                request.form.get('gps') == 'on',
                request.form.get('bluetooth') == 'on',
                request.form.get('backup_camera') == 'on',
                car_id
            ))
            conn.commit()
            cursor.close()
            close_db_connection(conn)
            return redirect(url_for('admin_cars'))
        except Exception as e:
            print(f"Error updating car: {e}")
            return render_template('admin/edit_car.html', car=car, error="Error updating car")

    return render_template('admin/edit_car.html', car=car)


@app.route('/admin/delete-car/<int:car_id>', methods=['POST'])
def admin_delete_car(car_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if not conn:
        return redirect(url_for('admin_cars'))

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
        conn.commit()
        cursor.close()
        close_db_connection(conn)
    except Exception as e:
        print(f"Error deleting car: {e}")

    return redirect(url_for('admin_cars'))


@app.route('/admin/customers')
def admin_customers():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if not conn:
        return render_template('admin/customers.html', customers=[], error="Database connection failed")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        customers = cursor.fetchall()
        return render_template('admin/customers.html', customers=customers)
    except Error as e:
        print(f"Error fetching customers: {e}")
        return render_template('admin/customers.html', customers=[], error="Error fetching customers")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


@app.route('/admin/bookings')
def admin_bookings():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if not conn:
        return render_template('admin/bookings.html', bookings=[], error="Database connection failed")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings ORDER BY booking_date DESC")
        bookings = cursor.fetchall()
        return render_template('admin/bookings.html', bookings=bookings)
    except Error as e:
        print(f"Error fetching bookings: {e}")
        return render_template('admin/bookings.html', bookings=[], error="Error fetching bookings")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


@app.route('/admin/reports')
def admin_reports():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin/reports.html')


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    print("🚗 Car Rental System Starting...")
    print("=" * 50)
    print("✓ Database configured securely")
    print("✓ Session security enabled")
    print("✓ Input validation active")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
