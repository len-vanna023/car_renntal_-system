# 🚗 Car Rental System - LuxeDrive

A comprehensive, full-stack car rental web application built with Python Flask, MySQL, and modern web technologies. Features include user authentication, admin dashboard, booking management, Google OAuth integration, and a responsive UI.

---

## ✨ Features

### 🎨 **Modern UI/UX**
- Fully responsive design (mobile, tablet, desktop)
- Beautiful gradient backgrounds and smooth animations
- TailwindCSS-powered styling
- Modern card-based layouts with hover effects
- Hamburger menu for mobile navigation
- Font Awesome icons throughout

### 🚗 **Car Management**
- Browse cars by categories (Luxury, Electric, Sports, SUV, Sedan)
- Detailed car specifications and features
- High-quality car images
- Real-time availability status
- Comprehensive car fields (brand, model, year, price, fuel type, transmission, etc.)
- Filter and search functionality

### 📅 **Booking System**
- Date-based booking with automatic availability tracking
- Booking conflict prevention
- View booking history
- Discount system:
  - **20% OFF** first booking after signup
  - **50% OFF** weekend bookings (Friday-Monday)
- Automatic price calculation with discounts
- Booking confirmation with details

### 👤 **User Authentication**
- Secure customer registration and login
- Password hashing with Werkzeug
- Session-based authentication
- Google OAuth integration (configurable)
- Email/Password validation
- Password confirmation on signup
- Profile management

### 🛡️ **Admin Panel**
- Separate admin authentication system
- Admin signup with secure access code
- Comprehensive admin dashboard with statistics
- Full CRUD operations for cars:
  - Add new cars with all specifications
  - Edit existing car details
  - Delete cars with confirmation
- View all bookings from customers
- Real-time statistics (total cars, bookings, categories)
- Admin-specific UI with orange gradient theme

### 🗄️ **Database Integration**
- MySQL database with proper schema
- Four main tables: `users`, `admin_accounts`, `cars`, `bookings`
- Connection pooling and error handling
- Database initialization scripts
- Sample data population scripts
- Transaction support

---

## 🛠️ Tech Stack

### Backend
- **Python**: 3.x
- **Flask**: 3.0.0 (Web framework)
- **MySQL**: 8.x (Database)
- **mysql-connector-python**: 8.2.0 (Database driver)
- **Werkzeug**: 3.0.1 (Security utilities)
- **Authlib**: 1.2.1 (OAuth integration)

### Frontend
- **HTML5** & **CSS3**
- **TailwindCSS**: Utility-first CSS framework
- **JavaScript**: Vanilla JS for interactivity
- **Font Awesome**: 6.4.0 (Icons)
- **Google Fonts**: Inter family

### Development Tools
- Python virtual environment
- Git version control
- Database migration scripts
- Testing scripts

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- MySQL Server (8.0 recommended)
- pip (Python package manager)

### Installation

1. **Clone or download the repository**
```bash
cd c:\Users\VANNA.LEN\Desktop\Car-Rental-System\Car-Rental-System
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure MySQL Database**

Edit `db_config.py` and update your MySQL password:
```python
def get_db_config():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'YOUR_PASSWORD_HERE',  # Change this
        'database': 'car_rental_db',
        'use_pure': True
    }
```

4. **Initialize Database**

Run the setup script:
```bash
python setup_mysql.py
```

Or manually create database and tables using `database_schema.sql`

5. **Run the Application**
```bash
python app.py
```

6. **Access the Application**
- **Customer Portal**: http://localhost:5000
- **Admin Portal**: http://localhost:5000/admin/login

---

## 📚 Default Credentials

### Admin Account
- **Username**: `admin`
- **Email**: `admin@luxedrive.com`
- **Password**: `Admin@123`

### Admin Access Code (for new admin signup)
- **Code**: `Admin@123`

### Test Customer (if created)
Use the signup form to create a customer account

---

## 📁 Project Structure

```
Car-Rental-System/
├── app.py                              # Main Flask application (40KB+)
├── db_config.py                        # Database configuration and connection
├── requirements.txt                    # Python dependencies
├── database_schema.sql                 # SQL schema for all tables
├── setup_mysql.py                      # Database initialization script
├── .env.example                        # Environment variables template
│
├── Admin Management Scripts/
│   ├── add_admin.py                    # Add new admin accounts
│   ├── check_admin.py                  # Verify admin accounts
│   ├── fix_admin_accounts.py           # Fix admin password issues
│   ├── restore_admin.py                # Restore default admin
│   └── verify_admin.py                 # Check admin login
│
├── Testing Scripts/
│   ├── test_admin_login.py             # Test admin authentication
│   ├── test_db_connection.py           # Test database connectivity
│   ├── test_signup.py                  # Test signup functionality
│   └── test_vanna_login.py             # Test specific user login
│
├── Car Management Scripts/
│   ├── add_sample_comprehensive_cars.py # Add sample car data
│   ├── migrate_cars_table.py           # Update cars table schema
│   └── view_comprehensive_cars.py      # View all cars in database
│
├── Documentation/
│   ├── README.md                       # This file
│   ├── START_HERE.md                   # Getting started guide
│   ├── QUICK_START.md                  # Quick reference
│   ├── COMPLETE_ADMIN_GUIDE.md         # Complete admin documentation
│   ├── DATABASE_SETUP_GUIDE.md         # Database setup instructions
│   ├── LOGIN_SYSTEM_GUIDE.md           # Authentication documentation
│   ├── GOOGLE_OAUTH_SETUP.md           # OAuth integration guide
│   └── WEEKEND_DISCOUNT_INFO.md        # Discount system details
│
├── static/
│   └── css/
│       └── custom.css                  # Custom styles and animations
│
└── templates/
    ├── base.html                       # Base template with navbar
    ├── index.html                      # Homepage
    ├── cars.html                       # Car listings
    ├── car_detail.html                 # Individual car page
    ├── login.html                      # Customer login
    ├── signup.html                     # Customer registration
    ├── bookings.html                   # User's booking history
    ├── about.html                      # About page
    ├── contact.html                    # Contact page
    └── admin/
        ├── login.html                  # Admin login
        ├── signup.html                 # Admin registration
        ├── dashboard.html              # Admin dashboard
        ├── add_car.html                # Add car form
        └── edit_car.html               # Edit car form
```

---

## 🗄️ Database Schema

### `users` Table (Customers)
- `id` (Primary Key, Auto Increment)
- `name` (VARCHAR 100)
- `email` (VARCHAR 100, Unique)
- `password` (VARCHAR 255, Hashed)
- `phone` (VARCHAR 20)
- `created_at` (DATETIME)

### `admin_accounts` Table
- `id` (Primary Key, Auto Increment)
- `username` (VARCHAR 50, Unique)
- `email` (VARCHAR 100, Unique)
- `password` (VARCHAR 255, Hashed)
- `full_name` (VARCHAR 100)
- `created_at` (TIMESTAMP)

### `cars` Table
- `id` (Primary Key, Auto Increment)
- `brand` (VARCHAR 50)
- `model` (VARCHAR 100)
- `year` (INT)
- `category` (VARCHAR 50)
- `price_per_day` (DECIMAL 10,2)
- `image` (VARCHAR 255)
- `description` (TEXT)
- `fuel_type` (VARCHAR 20)
- `transmission` (VARCHAR 20)
- `seats` (INT)
- `horsepower` (INT)
- `top_speed` (INT)
- `acceleration` (VARCHAR 20)
- `features` (TEXT, JSON format)
- `is_available` (BOOLEAN)
- `mileage` (VARCHAR 50)
- `color` (VARCHAR 30)
- `created_at` (TIMESTAMP)

### `bookings` Table
- `id` (Primary Key, Auto Increment)
- `user_id` (INT, Foreign Key)
- `car_id` (INT, Foreign Key)
- `start_date` (DATE)
- `end_date` (DATE)
- `total_price` (DECIMAL 10,2)
- `status` (VARCHAR 20)
- `created_at` (TIMESTAMP)

---

## 🌐 Application Routes

### Public Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage with featured cars |
| `/cars` | GET | Browse all available cars |
| `/car/<id>` | GET | View car details |
| `/login` | GET, POST | Customer login |
| `/signup` | GET, POST | Customer registration |
| `/logout` | GET | User logout |
| `/about` | GET | About the company |
| `/contact` | GET | Contact information |

### Protected User Routes (Requires Login)
| Route | Method | Description |
|-------|--------|-------------|
| `/book/<car_id>` | POST | Book a car |
| `/bookings` | GET | View user's bookings |

### Admin Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/admin/login` | GET, POST | Admin login |
| `/admin/signup` | GET, POST | Admin registration (requires code) |
| `/admin/logout` | GET | Admin logout |
| `/admin/dashboard` | GET | Admin dashboard |
| `/admin/add-car` | GET, POST | Add new car |
| `/admin/edit-car/<id>` | GET, POST | Edit car details |
| `/admin/delete-car/<id>` | POST | Delete car |

### OAuth Routes (Optional)
| Route | Method | Description |
|-------|--------|-------------|
| `/login/google` | GET | Initiate Google OAuth |
| `/auth/callback` | GET | Google OAuth callback |

---

## 💡 Usage Guide

### For Customers

**1. Sign Up**
- Navigate to `/signup`
- Fill in name, email, password
- Confirm password
- Accept terms and conditions
- Submit to create account
- Get 20% discount on first booking!

**2. Browse Cars**
- View all cars at `/cars`
- Filter by category (Luxury, Electric, Sports, SUV, Sedan)
- Click "View Details" to see specifications

**3. Book a Car**
- Select dates (start and end)
- System checks availability automatically
- Apply discounts (weekend = 50% off!)
- Confirm booking
- View in "My Bookings"

**4. View Bookings**
- Access `/bookings` when logged in
- See all past and upcoming rentals
- View booking details and total cost

### For Administrators

**1. Admin Login**
- Go to `/admin/login`
- Use default credentials or create admin account
- Admin signup requires access code: `Admin@123`

**2. Dashboard Overview**
- Total cars count
- Total bookings
- Cars by category
- Recent bookings list

**3. Add New Car**
- Click "Add Car" button (green, top right)
- Fill comprehensive form:
  - Basic: Brand, Model, Year
  - Pricing: Price per day
  - Specs: Fuel, Transmission, Seats, HP
  - Performance: Top Speed, Acceleration
  - Details: Features, Description, Image URL
  - Availability status
- Submit to add car to inventory

**4. Edit Car**
- Click "Edit" button on any car card
- Modify any fields
- Update changes

**5. Delete Car**
- Click "Delete" button
- Confirm deletion
- Car removed from database

**6. View All Bookings**
- See customer bookings from dashboard
- Track rental periods
- Monitor system usage

---

## 🎯 Key Features Explained

### Smart Booking System
- **Availability Check**: Automatically verifies if car is available for selected dates
- **Conflict Prevention**: Prevents double-booking
- **Date Validation**: Ensures start date is before end date and not in the past
- **Status Tracking**: Marks cars as unavailable during rental period

### Discount System
1. **First Booking Discount (20%)**
   - Automatically applied on user's first booking after signup/login
   - Tracked in session
   
2. **Weekend Discount (50%)**
   - Applied when booking includes Friday, Saturday, Sunday, or Monday
   - Automatically calculated

3. **Discount Stacking**: Both discounts can apply together!

### Security Features
- **Password Hashing**: Werkzeug's `generate_password_hash` and `check_password_hash`
- **Session Management**: Flask session with secret key
- **SQL Injection Prevention**: Parameterized queries
- **Admin Access Control**: Separate admin session and access code
- **CSRF Protection**: Built into forms

### OAuth Integration
- Google OAuth configured via Authlib
- Environment variable support for client credentials
- Seamless account creation for OAuth users

---

## 🔧 Configuration

### Environment Variables (.env)
```env
# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here

# Flask
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=car_rental_db
```

### MySQL Configuration
Edit `db_config.py`:
```python
def get_db_config():
    return {
        'host': 'localhost',          # Database host
        'user': 'root',                # MySQL username
        'password': '',                # MySQL password
        'database': 'car_rental_db',   # Database name
        'use_pure': True
    }
```

---

## 🧪 Testing

### Database Connection Test
```bash
python test_db_connection.py
```

### Admin Login Test
```bash
python test_admin_login.py
```

### Signup Test
```bash
python test_signup.py
```

### View Admin Accounts
```bash
python check_admin.py
```

### Add Test Admin
```bash
python add_admin.py
```

---

## 🐛 Troubleshooting

### Database Connection Issues
1. Verify MySQL service is running
2. Check credentials in `db_config.py`
3. Ensure `car_rental_db` database exists
4. Run `python test_db_connection.py`

### Admin Login Not Working
1. Run `python restore_admin.py` to reset admin
2. Use credentials: admin / Admin@123
3. Check `admin_accounts` table in database

### Cars Not Showing
1. Run `python add_sample_comprehensive_cars.py`
2. Check if `cars` table exists
3. Verify database connection

### Booking Errors
1. Check if user is logged in
2. Verify car availability
3. Ensure dates are valid
4. Check `bookings` table structure

---

## 🚀 Deployment

### For Production

1. **Update Secret Key**
```python
# In app.py
app.secret_key = 'generate-strong-random-key-here'
```

2. **Secure Database**
- Use strong MySQL password
- Create dedicated database user (not root)
- Enable SSL connections

3. **Environment Variables**
- Use `.env` file for secrets
- Never commit credentials to Git

4. **Use Production Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

5. **Set Debug Mode Off**
```python
# In app.py
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
```

6. **Enable HTTPS**
- Use reverse proxy (Nginx)
- SSL certificate (Let's Encrypt)

---

## 📖 Additional Documentation

- **COMPLETE_ADMIN_GUIDE.md** - Detailed admin features and usage
- **DATABASE_SETUP_GUIDE.md** - Step-by-step database configuration
- **LOGIN_SYSTEM_GUIDE.md** - Authentication flow and security
- **GOOGLE_OAUTH_SETUP.md** - Setting up Google OAuth integration
- **WEEKEND_DISCOUNT_INFO.md** - How the discount system works

---

## 🎨 UI/UX Design

### Color Palette
- **Customer Theme**: Purple gradient (#667eea → #764ba2)
- **Admin Theme**: Orange gradient (#f97316 → #ea580c)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Error**: Red (#ef4444)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Headings**: Bold, Large
- **Body**: Regular, Medium

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

---

## 📝 License

This project is for educational purposes. Feel free to use and modify for learning.

---

## 👨‍💻 Developer

Built with ❤️ using Flask, MySQL, TailwindCSS, and modern web technologies.

**Project Path**: `c:\Users\VANNA.LEN\Desktop\Car-Rental-System\Car-Rental-System`

---

## 🆘 Support

For issues or questions:
1. Check the documentation files in the project
2. Review `COMPLETE_ADMIN_GUIDE.md` for admin help
3. Run test scripts to diagnose problems
4. Check database connectivity with `test_db_connection.py`

**Happy Renting! 🚗💨**
