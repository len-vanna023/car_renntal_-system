"""
Security utilities for the car rental system
- Input validation and sanitization
- SQL injection prevention
- Password security
- Session management
"""

import re
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number (basic validation)"""
    # Remove all non-digit characters
    digits = ''.join(c for c in phone if c.isdigit())
    return len(digits) >= 7  # At least 7 digits


def validate_password_strength(password):
    """
    Validate password strength
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"


def sanitize_input(value):
    """
    Sanitize user input to prevent XSS attacks
    - Removes potentially dangerous characters
    - Preserves legitimate content
    """
    if not value:
        return ''
    
    # Remove HTML/script tags
    value = re.sub(r'<[^>]*>', '', value)
    # Escape special characters
    return value.strip()


def login_required(f):
    """
    Decorator to require login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator to require admin login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin login required.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def require_https():
    """
    Ensure HTTPS is being used (check in production)
    """
    from flask import request
    if request.environ.get('HTTP_X_FORWARDED_PROTO', 'http') != 'https':
        # In production, you may want to enforce HTTPS
        return False
    return True
