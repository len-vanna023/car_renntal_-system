from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
import json
import os
import mysql.connector
from mysql.connector import Error, IntegrityError
from app.models.db_config import get_db_connection, init_database, close_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import secrets
from uuid import uuid4

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


def allowed_image_file(filename):
    """Allow common image file types for car uploads."""
    if not filename or '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def save_car_image(file_storage):
    """Save an uploaded car image and return its static path."""
    filename = secure_filename(file_storage.filename or '')
    if not allowed_image_file(filename):
        raise ValueError('Please upload a PNG, JPG, JPEG, WEBP, or GIF image.')

    extension = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid4().hex}.{extension}"
    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'cars')
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, unique_name)
    file_storage.save(file_path)
    return f"/static/uploads/cars/{unique_name}"


def delete_uploaded_car_image(image_path):
    """Delete a locally uploaded car image if it exists."""
    if not image_path or not image_path.startswith('/static/uploads/cars/'):
        return

    relative_path = image_path.replace('/static/', '').replace('/', os.sep)
    file_path = os.path.join(app.root_path, 'static', relative_path)
    if os.path.exists(file_path):
        os.remove(file_path)


def split_car_name(name):
    """Derive brand and model from the car name when separate fields are unavailable."""
    cleaned_name = (name or '').strip()
    if not cleaned_name:
        return '', ''

    name_parts = cleaned_name.split(None, 1)
    brand = name_parts[0]
    model = name_parts[1] if len(name_parts) > 1 else name_parts[0]
    return brand, model


def generate_license_plate():
    """Generate a simple unique plate for legacy car schemas."""
    return f"ADM{uuid4().hex[:8].upper()}"


def get_cars_table_columns(cursor):
    """Return the live cars table column names."""
    cursor.execute("SHOW COLUMNS FROM cars")
    return {row[0] for row in cursor.fetchall()}


def update_car_record(cursor, car_id, payload):
    """Update a car record for either supported cars table schema."""
    car_columns = get_cars_table_columns(cursor)

    name = (payload.get('name') or '').strip()
    category = (payload.get('category') or '').strip()
    transmission = (payload.get('transmission') or '').strip()
    image = (payload.get('image') or '').strip()
    color = (payload.get('color') or '').strip() or None
    features = payload.get('features') or []

    if isinstance(features, str):
        features = [feature.strip() for feature in features.split(',') if feature.strip()]

    seats = int(payload.get('seats', 0))
    price = float(payload.get('price', 0))

    if not name or not category or not transmission or not image:
        raise ValueError('Please fill in all required fields.')
    if seats < 1 or price <= 0:
        raise ValueError('Price and seats must be valid numbers.')

    brand, model = split_car_name(name)

    if 'image_url' in car_columns:
        cursor.execute("""
            UPDATE cars SET
            brand = %s,
            model = %s,
            car_type = %s,
            seats = %s,
            transmission = %s,
            daily_rate = %s,
            image_url = %s
            WHERE id = %s
        """, (
            brand,
            model,
            category,
            seats,
            transmission,
            price,
            image,
            car_id
        ))
    else:
        cursor.execute("""
            UPDATE cars SET
            name = %s,
            brand = %s,
            model = %s,
            category = %s,
            price = %s,
            image = %s,
            seats = %s,
            transmission = %s,
            color = %s,
            features = %s
            WHERE id = %s
        """, (
            name,
            brand,
            model,
            category,
            price,
            image,
            seats,
            transmission,
            color,
            json.dumps(features),
            car_id
        ))


def set_car_availability(cursor, car_id, available):
    """Update availability for either supported cars table schema."""
    car_columns = get_cars_table_columns(cursor)
    if 'is_available' in car_columns:
        cursor.execute("UPDATE cars SET is_available = %s WHERE id = %s", (bool(available), car_id))
    else:
        status = 'available' if available else 'unavailable'
        cursor.execute("UPDATE cars SET status = %s WHERE id = %s", (status, car_id))


def clear_user_session():
    """Remove only customer session keys."""
    for key in ('user_id', 'user_name', 'user_email'):
        session.pop(key, None)


def clear_admin_session():
    """Remove only admin session keys."""
    for key in ('admin_id', 'admin_name', 'admin_email'):
        session.pop(key, None)


def generate_booking_reference():
    """Create a simple unique booking reference."""
    return f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}{secrets.randbelow(1000):03d}"


def is_password_hash(value):
    """Detect Werkzeug password hashes stored in the database."""
    if not value:
        return False
    return value.startswith('scrypt:') or value.startswith('pbkdf2:')


def verify_admin_password(stored_password, provided_password):
    """Support both hashed and legacy plain-text admin passwords."""
    if not stored_password or provided_password is None:
        return False

    if is_password_hash(stored_password):
        try:
            return check_password_hash(stored_password, provided_password)
        except ValueError:
            return False

    return secrets.compare_digest(stored_password, provided_password)


def create_user(fullname, email, phone, password_hash):
    """Insert a new user account and return user ID."""
    conn = get_db_connection()
    if not conn:
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        # Split fullname into first_name and last_name
        name_parts = fullname.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Use the actual database columns
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, first_name, last_name, phone) VALUES (%s, %s, %s, %s, %s, %s)",
            (email.split('@')[0], email, password_hash, first_name, last_name, phone)
        )
        conn.commit()
        
        # Get the user ID that was just created
        user_id = cursor.lastrowid
        return user_id
    except IntegrityError as e:
        print(f"Integrity error creating user: {e}")
        return None
    except Error as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass

        try:
            if conn:
                close_db_connection(conn)
        except Exception:
            pass

# Ensure required tables exist before handling requests
if not init_database():
    print("⚠️  Warning: Database initialization failed. Check MySQL service and credentials.")

# Database helper functions for cars
def normalize_car_record(car):
    """Normalize car records across different DB schemas."""
    if not car:
        return car

    # Derive name if missing
    if not car.get('name'):
        brand = car.get('brand') or ''
        model = car.get('model') or ''
        derived_name = f"{brand} {model}".strip()
        if derived_name:
            car['name'] = derived_name

    # Normalize category
    if not car.get('category') and car.get('car_type'):
        car['category'] = car.get('car_type')

    # Normalize price (support older schema with daily_rate)
    price_value = car.get('price')
    if price_value is None and car.get('daily_rate') is not None:
        price_value = car.get('daily_rate')
    if price_value is not None:
        try:
            price_float = float(price_value)
        except (TypeError, ValueError):
            price_float = 0.0
        car['price'] = price_float
        car.setdefault('price_per_day', price_float)

    # Normalize image fields
    if not car.get('image') and car.get('image_url'):
        car['image'] = car.get('image_url')
    if not car.get('image_url') and car.get('image'):
        car['image_url'] = car.get('image')

    # Normalize status/availability
    if 'status' not in car and 'is_available' in car:
        car['status'] = 'available' if car.get('is_available') else 'unavailable'
    if 'available' not in car:
        if 'is_available' in car:
            car['available'] = bool(car.get('is_available'))
        elif 'status' in car:
            car['available'] = car.get('status') == 'available'

    # Convert features from TEXT to list
    if car.get('features') and isinstance(car['features'], str):
        try:
            car['features'] = json.loads(car['features'])
        except Exception:
            car['features'] = [f.strip() for f in car['features'].split(',') if f.strip()]
    elif car.get('features') is None:
        car['features'] = []

    return car


def get_all_cars():
    """Fetch all cars from database"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars ORDER BY id")
        cars = cursor.fetchall()
        return [normalize_car_record(car) for car in cars]
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
        return normalize_car_record(car)
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
        # Handle both JSON and form data
        is_json = request.is_json or request.content_type == 'application/json'
        
        if is_json:
            data = request.get_json() or {}
            fullname = data.get('fullname', '').strip()
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            password = data.get('password', '')
            confirm_password = data.get('confirm_password', '')
        else:
            fullname = request.form.get('fullname', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not fullname or not email or not password:
            if is_json:
                return jsonify({'success': False, 'message': 'All fields are required'}), 400
            return render_template('signup.html', error="All fields are required")

        if password != confirm_password:
            if is_json:
                return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
            return render_template('signup.html', error="Passwords don't match")

        if len(password) < 6:
            if is_json:
                return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
            return render_template('signup.html', error="Password must be at least 6 characters")

        # Normalize phone number
        phone = normalize_phone(phone)

        # Hash password
        password_hash = generate_password_hash(password)

        # Create user
        user_id = create_user(fullname, email, phone, password_hash)
        if user_id:
            # Set session for successful signup
            clear_admin_session()
            session['user_id'] = user_id
            session['user_name'] = fullname
            session['user_email'] = email
            
            if is_json:
                return jsonify({'success': True, 'message': 'Account created successfully', 'redirect': '/'}), 201
            return redirect(url_for('home'))
        else:
            if is_json:
                return jsonify({'success': False, 'message': 'Email already exists or error creating account'}), 400
            return render_template('signup.html', error="Email already exists or error creating account")

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle both JSON and form data
        is_json = request.is_json or request.content_type == 'application/json'
        
        if is_json:
            data = request.get_json() or {}
            email = data.get('email', '').strip()
            password = data.get('password', '')
        else:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

        # Validation
        if not email or not password:
            if is_json:
                return jsonify({'success': False, 'message': 'Email and password are required'}), 400
            return render_template('login.html', error="Email and password are required")

        # Get user from database
        user = get_user_by_email(email)

        # Verify password
        if user and check_password_hash(user['password_hash'], password):
            # Build full name from first and last name
            full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
            clear_admin_session()
            session['user_id'] = user['id']
            session['user_name'] = full_name
            session['user_email'] = user['email']
            
            if is_json:
                return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/'}), 200
            return redirect(url_for('home'))
        else:
            if is_json:
                return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')


@app.route('/logout')
def logout():
    clear_user_session()
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
            """
            SELECT
                b.id,
                b.booking_reference,
                b.status,
                b.total_cost,
                b.created_at AS booking_date,
                b.start_date AS pickup_date,
                b.end_date AS return_date,
                DATEDIFF(b.end_date, b.start_date) AS days,
                b.total_cost AS base_cost,
                0 AS discount_amount,
                '' AS discounts_applied,
                CONCAT(c.brand, ' ', c.model) AS car_name,
                c.image_url AS car_image
            FROM bookings b
            JOIN users u ON u.id = b.user_id
            JOIN cars c ON c.id = b.car_id
            WHERE u.email = %s
            ORDER BY b.created_at DESC
            """,
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
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        return redirect(url_for('login'))

    car = get_car_by_id(car_id)
    if not car:
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        return "Car not found", 404

    if request.method == 'POST':
        is_json = request.is_json or request.content_type == 'application/json'
        if is_json:
            data = request.get_json() or {}
            pickup_date = data.get('pickup_date')
            return_date = data.get('return_date')
            phone = data.get('phone', '')
        else:
            pickup_date = request.form.get('pickup_date')
            return_date = request.form.get('return_date')
            phone = request.form.get('phone', '')

        if not pickup_date or not return_date:
            if is_json:
                return jsonify({'success': False, 'message': 'Please select both dates'}), 400
            return render_template('car_detail.html', car=car, error="Please select both dates")

        try:
            pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
            return_dt = datetime.strptime(return_date, '%Y-%m-%d')

            if return_dt <= pickup:
                if is_json:
                    return jsonify({'success': False, 'message': 'Return date must be after pickup date'}), 400
                return render_template('car_detail.html', car=car, error="Return date must be after pickup date")

            if not car.get('available', False):
                if is_json:
                    return jsonify({'success': False, 'message': 'This car is currently unavailable'}), 400
                return render_template('car_detail.html', car=car, error="This car is currently unavailable")

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
                if is_json:
                    return jsonify({'success': False, 'message': 'Database connection failed'}), 500
                return render_template('car_detail.html', car=car, error="Database connection failed")

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings
                (booking_reference, user_id, car_id, start_date, end_date, pickup_location,
                 dropoff_location, status, total_cost, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                generate_booking_reference(),
                session['user_id'],
                car_id,
                pickup_date,
                return_date,
                'Main Branch',
                'Main Branch',
                'confirmed',
                total_cost,
                'pending'
            ))
            conn.commit()
            booking_id = cursor.lastrowid
            cursor.close()
            close_db_connection(conn)

            if is_json:
                discount_list = [item.strip() for item in discounts_applied.split(',') if item.strip()] if discounts_applied else []
                return jsonify({
                    'success': True,
                    'message': 'Booking confirmed!',
                    'booking_id': booking_id,
                    'discount_amount': discount_amount,
                    'discounts_applied': discount_list
                }), 200
            return redirect(url_for('bookings'))

        except ValueError:
            if is_json:
                return jsonify({'success': False, 'message': 'Invalid date format'}), 400
            return render_template('car_detail.html', car=car, error="Invalid date format")

    return render_template('car_detail.html', car=car)


# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        is_json = request.is_json or request.content_type == 'application/json'

        if is_json:
            data = request.get_json() or {}
            fullname = data.get('fullname', '').strip()
            email = data.get('email', '').strip().lower()
            phone = data.get('phone', '').strip()
            password = data.get('password', '')
        else:
            fullname = request.form.get('fullname', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            password = request.form.get('password', '')

        if not fullname or not email or not phone or not password:
            message = "Full name, email, phone, and password are required"
            if is_json:
                return jsonify({'success': False, 'message': message}), 400
            return render_template('admin/login.html', error=message)

        conn = get_db_connection()
        if not conn:
            message = "Database connection failed"
            if is_json:
                return jsonify({'success': False, 'message': message}), 500
            return render_template('admin/login.html', error=message)

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM admin_accounts WHERE email = %s AND is_active = TRUE",
                (email,)
            )
            admin = cursor.fetchone()

            fullname_matches = False
            phone_matches = False
            password_matches = False

            if admin:
                fullname_matches = (admin.get('fullname') or '').strip().lower() == fullname.lower()
                phone_matches = normalize_phone(admin.get('phone') or '') == normalize_phone(phone)
                password_matches = verify_admin_password(admin.get('password', ''), password)

            if admin and fullname_matches and phone_matches and password_matches:
                if not is_password_hash(admin.get('password', '')):
                    hashed_password = generate_password_hash(password)
                    cursor.execute(
                        "UPDATE admin_accounts SET password = %s WHERE id = %s",
                        (hashed_password, admin['id'])
                    )
                    conn.commit()

                clear_user_session()
                session['admin_id'] = admin['id']
                session['admin_name'] = admin['fullname']
                session['admin_email'] = admin.get('email', '')
                if is_json:
                    return jsonify({
                        'success': True,
                        'message': 'Admin login successful',
                        'redirect': '/admin/dashboard'
                    }), 200
                return redirect(url_for('admin_dashboard'))
            else:
                message = "Invalid admin credentials"
                if is_json:
                    return jsonify({'success': False, 'message': message}), 401
                return render_template('admin/login.html', error=message)
        except Error as e:
            print(f"Admin login error: {e}")
            message = "Error during login"
            if is_json:
                return jsonify({'success': False, 'message': message}), 500
            return render_template('admin/login.html', error=message)
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

        cars = get_all_cars()
        return render_template(
            'admin/dashboard.html',
            stats=stats,
            total_users=total_users,
            total_cars=total_cars,
            total_bookings=total_bookings,
            revenue=float(revenue),
            cars=cars
        )
    except Error as e:
        print(f"Dashboard error: {e}")
        return render_template(
            'admin/dashboard.html',
            stats={},
            total_users=0,
            total_cars=0,
            total_bookings=0,
            revenue=0,
            cars=[],
            error="Error loading dashboard"
        )
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
        image_path = None
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500

        try:
            name = request.form.get('name', '').strip()
            category = request.form.get('category', '').strip()
            transmission = request.form.get('transmission', '').strip()
            color = request.form.get('color', '').strip() or None
            features_input = request.form.get('features', '')
            features = [feature.strip() for feature in features_input.split(',') if feature.strip()]
            seats = int(request.form.get('seats', 0))
            price = float(request.form.get('price', 0))
            image_file = request.files.get('image')

            if not name or not category or not transmission or not features:
                return jsonify({'success': False, 'message': 'Please fill in all required fields.'}), 400
            if seats < 1 or price <= 0:
                return jsonify({'success': False, 'message': 'Price and seats must be valid numbers.'}), 400
            if not image_file or not image_file.filename:
                return jsonify({'success': False, 'message': 'Please choose an image to upload.'}), 400

            image_path = save_car_image(image_file)
            brand, model = split_car_name(name)

            cursor = conn.cursor()
            car_columns = get_cars_table_columns(cursor)

            if 'image_url' in car_columns:
                cursor.execute("""
                    INSERT INTO cars
                    (license_plate, brand, model, car_type, year, seats, transmission,
                     fuel_type, daily_rate, image_url, is_available)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    generate_license_plate(),
                    brand,
                    model,
                    category,
                    datetime.now().year,
                    seats,
                    transmission,
                    'Gasoline',
                    price,
                    image_path,
                    True
                ))
            else:
                cursor.execute("""
                    INSERT INTO cars
                    (name, brand, model, year, category, price, image, seats, transmission,
                     fuel_type, engine, horsepower, features, color, doors, luggage_capacity,
                     air_conditioning, gps, bluetooth, backup_camera, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    name,
                    brand,
                    model,
                    datetime.now().year,
                    category,
                    price,
                    image_path,
                    seats,
                    transmission,
                    'Gasoline',
                    '',
                    0,
                    json.dumps(features),
                    color,
                    4,
                    2,
                    True,
                    False,
                    True,
                    False,
                    'available'
                ))

            conn.commit()
            cursor.close()
            close_db_connection(conn)
            return jsonify({'success': True, 'message': 'Car added successfully!', 'redirect': '/admin/cars'}), 200
        except ValueError as e:
            if image_path:
                saved_file = os.path.join(app.root_path, image_path.lstrip('/').replace('/', os.sep))
                if os.path.exists(saved_file):
                    os.remove(saved_file)
            return jsonify({'success': False, 'message': str(e)}), 400
        except Exception as e:
            print(f"Error adding car: {e}")
            if image_path:
                saved_file = os.path.join(app.root_path, image_path.lstrip('/').replace('/', os.sep))
                if os.path.exists(saved_file):
                    os.remove(saved_file)
            return jsonify({'success': False, 'message': 'Error adding car'}), 500

    return render_template('admin/add_car.html')


@app.route('/admin/edit-car/<int:car_id>', methods=['GET', 'POST'])
def admin_edit_car(car_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    car = get_car_by_id(car_id)
    if not car:
        return "Car not found", 404

    if request.method == 'POST':
        image_path = None
        previous_image = car.get('image_url') or car.get('image') or ''
        is_json = request.is_json or request.content_type == 'application/json'
        expects_json = is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        conn = get_db_connection()
        if not conn:
            if expects_json:
                return jsonify({'success': False, 'message': 'Database connection failed'}), 500
            return render_template('admin/edit_car.html', car=car, error="Database connection failed")

        try:
            payload = (request.get_json() or {}) if is_json else request.form.to_dict()

            if not is_json:
                uploaded_image = request.files.get('image')
                if uploaded_image and uploaded_image.filename:
                    image_path = save_car_image(uploaded_image)
                    payload['image'] = image_path
                else:
                    payload['image'] = (request.form.get('current_image') or previous_image).strip()

            cursor = conn.cursor()
            update_car_record(cursor, car_id, payload)
            conn.commit()
            cursor.close()
            close_db_connection(conn)

            if image_path and previous_image and previous_image != image_path:
                delete_uploaded_car_image(previous_image)

            if expects_json:
                return jsonify({'success': True, 'message': 'Car updated successfully', 'redirect': '/admin/cars'}), 200
            return redirect(url_for('admin_cars'))
        except ValueError as e:
            if image_path:
                delete_uploaded_car_image(image_path)
            if expects_json:
                return jsonify({'success': False, 'message': str(e)}), 400
            return render_template('admin/edit_car.html', car=car, error=str(e))
        except Exception as e:
            print(f"Error updating car: {e}")
            if image_path:
                delete_uploaded_car_image(image_path)
            if expects_json:
                return jsonify({'success': False, 'message': 'Error updating car'}), 500
            return render_template('admin/edit_car.html', car=car, error="Error updating car")

    return render_template('admin/edit_car.html', car=car)


@app.route('/admin/delete-car/<int:car_id>', methods=['POST'])
def admin_delete_car(car_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        if not car:
            cursor.close()
            close_db_connection(conn)
            return jsonify({'success': False, 'message': 'Car not found'}), 404

        cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
        conn.commit()
        image_path = car.get('image_url') or car.get('image')
        delete_uploaded_car_image(image_path)
        cursor.close()
        close_db_connection(conn)
        return jsonify({'success': True, 'message': 'Car deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting car: {e}")
        return jsonify({'success': False, 'message': 'Error deleting car'}), 500


@app.route('/admin/cars/add', methods=['GET', 'POST'])
def admin_cars_add_alias():
    return admin_add_car()


@app.route('/admin/cars/edit/<int:car_id>', methods=['GET', 'POST'])
def admin_cars_edit_alias(car_id):
    return admin_edit_car(car_id)


@app.route('/admin/cars/delete/<int:car_id>', methods=['POST'])
def admin_cars_delete_alias(car_id):
    return admin_delete_car(car_id)


@app.route('/admin/cars/toggle/<int:car_id>', methods=['POST'])
def admin_toggle_car(car_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    try:
        payload = request.get_json(silent=True) or {}
        if 'available' not in payload:
            return jsonify({'success': False, 'message': 'Missing availability value'}), 400

        cursor = conn.cursor()
        set_car_availability(cursor, car_id, bool(payload.get('available')))
        conn.commit()
        cursor.close()
        close_db_connection(conn)
        return jsonify({'success': True, 'message': 'Car status updated successfully'}), 200
    except Exception as e:
        print(f"Error toggling car availability: {e}")
        return jsonify({'success': False, 'message': 'Error updating car status'}), 500


@app.route('/admin/cars/view/<int:car_id>')
def admin_view_car(car_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401

    car = get_car_by_id(car_id)
    if not car:
        return jsonify({'success': False, 'message': 'Car not found'}), 404

    return jsonify({
        'id': car.get('id'),
        'name': car.get('name'),
        'brand': car.get('brand'),
        'category': car.get('category'),
        'price': car.get('price'),
        'seats': car.get('seats'),
        'transmission': car.get('transmission'),
        'available': car.get('available', False),
        'image': car.get('image_url') or car.get('image')
    }), 200

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
        cursor.execute("""
            SELECT
                b.*,
                u.email AS user_email,
                CONCAT(u.first_name, ' ', u.last_name) AS user_name,
                u.phone AS phone,
                CONCAT(c.brand, ' ', c.model) AS car_name,
                c.image_url AS car_image,
                b.start_date AS pickup_date,
                b.end_date AS return_date,
                DATEDIFF(b.end_date, b.start_date) AS days,
                b.created_at AS booking_date,
                b.total_cost AS base_cost,
                0 AS discount_amount,
                '' AS discounts_applied
            FROM bookings b
            JOIN users u ON u.id = b.user_id
            JOIN cars c ON c.id = b.car_id
            ORDER BY b.created_at DESC
        """)
        bookings = cursor.fetchall()

        total_bookings = len(bookings)
        confirmed_bookings = sum(1 for booking in bookings if (booking.get('status') or '').lower() == 'confirmed')
        cancelled_bookings = sum(1 for booking in bookings if (booking.get('status') or '').lower() == 'cancelled')
        total_revenue = sum(
            float(booking.get('total_cost') or 0)
            for booking in bookings
            if (booking.get('status') or '').lower() == 'confirmed'
        )

        return render_template(
            'admin/bookings.html',
            bookings=bookings,
            total_bookings=total_bookings,
            confirmed_bookings=confirmed_bookings,
            cancelled_bookings=cancelled_bookings,
            total_revenue=total_revenue
        )
    except Error as e:
        print(f"Error fetching bookings: {e}")
        return render_template(
            'admin/bookings.html',
            bookings=[],
            total_bookings=0,
            confirmed_bookings=0,
            cancelled_bookings=0,
            total_revenue=0,
            error="Error fetching bookings"
        )
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_db_connection(conn)


@app.route('/admin/bookings/update/<int:booking_id>', methods=['POST'])
def admin_update_booking_status(booking_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401

    payload = request.get_json(silent=True) or {}
    new_status = (payload.get('status') or '').strip().lower()
    if new_status not in {'confirmed', 'cancelled'}:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT car_id FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        if not booking:
            cursor.close()
            close_db_connection(conn)
            return jsonify({'success': False, 'message': 'Booking not found'}), 404

        cursor.execute("UPDATE bookings SET status = %s WHERE id = %s", (new_status, booking_id))

        raw_cursor = conn.cursor()
        set_car_availability(raw_cursor, booking['car_id'], new_status != 'confirmed')
        raw_cursor.close()

        conn.commit()
        cursor.close()
        close_db_connection(conn)
        return jsonify({'success': True, 'message': 'Booking status updated successfully'}), 200
    except Exception as e:
        print(f"Error updating booking status: {e}")
        return jsonify({'success': False, 'message': 'Error updating booking status'}), 500


@app.route('/admin/reports')
def admin_reports():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin/reports.html')


@app.route('/admin/logout')
def admin_logout():
    clear_admin_session()
    return redirect(url_for('admin_login'))


# API Endpoint to check current session status
@app.route('/api/check-session')
def check_session():
    """Check if user is logged in and return session information."""
    if 'admin_id' in session:
        # Admin is logged in
        return jsonify({
            'logged_in': False,
            'admin': True,
            'role': 'admin',
            'admin_name': session.get('admin_name', 'Admin'),
            'admin_email': session.get('admin_email', ''),
            'admin_id': session.get('admin_id')
        })
    elif 'user_email' in session:
        # Regular user is logged in
        return jsonify({
            'logged_in': True,
            'admin': False,
            'role': 'user',
            'name': session.get('user_name', 'User'),
            'email': session.get('user_email', ''),
            'user_id': session.get('user_id')
        })
    else:
        # No user is logged in
        return jsonify({
            'logged_in': False,
            'admin': False,
            'role': None
        })


if __name__ == '__main__':
    print("🚗 Car Rental System Starting...")
    print("=" * 50)
    print("✓ Database configured securely")
    print("✓ Session security enabled")
    print("✓ Input validation active")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
