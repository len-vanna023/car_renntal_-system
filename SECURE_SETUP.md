# Secure Connection Setup Guide

## Overview
Your Car Rental System is now configured with security best practices:

### ✅ Security Features Implemented

#### 1. **Environment Variables**
   - Database credentials moved from hardcoded values to `.env` file
   - Google OAuth secrets stored securely
   - Flask secret key stored in environment

#### 2. **Connection Pooling**
   - MySQL connection pooling for better resource management
   - Connection reuse reduces overhead
   - Proper connection cleanup

#### 3. **Session Security**
   - `SESSION_COOKIE_HTTPONLY=True` - Prevents JavaScript access to cookies
   - `SESSION_COOKIE_SAMESITE=Lax` - CSRF protection
   - `SESSION_COOKIE_SECURE=True` - HTTPS only in production
   - Session timeout: 1 hour

#### 4. **Password Security**
   - All passwords hashed using werkzeug's secure hashing
   - Password strength validation (8+ chars, uppercase, lowercase, digits)
   - Parameterized queries prevent SQL injection

#### 5. **Database Security**
   - Proper table structure with constraints
   - Foreign keys for referential integrity
   - Unique constraints on sensitive fields
   - Indexes for performance and security
   - UTF-8 encoding for international support

#### 6. **Input Validation**
   - Email format validation
   - Phone number validation
   - XSS prevention with input sanitization
   - SQL injection prevention with parameterized queries

---

## Setup Instructions

### Step 1: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
Edit `config/.env` with your database credentials:

```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=car_rental_db
DB_PORT=3306

FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Step 3: Ensure MySQL is Running
```bash
# Windows
mysql -u root -p

# Or use MySQL Workbench
```

### Step 4: Run the Application
```bash
cd Car-Rental-System
python app/__init__.py
```

The database tables will be created automatically on first run.

---

## Security Configuration by Environment

### Development
- Debug enabled for development
- HTTP allowed (insecure cookies)
- Use for testing only

### Production
- Debug disabled
- HTTPS required (secure cookies)
- Update these settings in `config/.env`:
  ```
  FLASK_ENV=production
  SESSION_COOKIE_SECURE=True
  ```

---

## Important Notes

⚠️ **Before Deploying to Production:**

1. **Change Secret Key**
   ```python
   # Generate a strong secret key
   import secrets
   print(secrets.token_hex(32))
   ```
   Add to `.env`: `FLASK_SECRET_KEY=your-generated-key`

2. **Set Strong Database Password**
   - Change MySQL root password
   - Use strong, unique password

3. **Enable HTTPS**
   - Use SSL/TLS certificates
   - Update `SESSION_COOKIE_SECURE=True`

4. **Update Google OAuth**
   - Get real credentials from Google Cloud Console
   - Add authorized redirect URIs

5. **Use Environment-Specific Config**
   - Separate `.env.production` file
   - Never commit credentials to version control

---

## Connection String Format

The system uses this connection string:
```
mysql+pymysql://user:password@localhost:3306/car_rental_db
```

---

## Testing the Connection

Run this to verify secure setup:
```bash
python test_db_connection.py
```

Expected output:
```
✅ Connection successful
✅ Connection pool created
✅ Tables initialized
```

---

## Troubleshooting

**Connection Refused:**
- Ensure MySQL is running
- Check DB_HOST and DB_PORT in `.env`
- Verify user credentials

**Access Denied:**
- Check DB_USER and DB_PASSWORD in `.env`
- Verify MySQL user has correct privileges

**Module Not Found:**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

---

## Additional Security Recommendations

1. **Use environment-specific configs**
2. **Implement rate limiting** for login endpoints
3. **Add CSRF protection** to all forms
4. **Use parameterized queries** (already implemented)
5. **Regular security audits**
6. **Keep dependencies updated**
7. **Use Web Application Firewall (WAF)** in production

---

Last Updated: January 19, 2026
