from db_config import get_db_connection

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute('SELECT id, email, password FROM admin_accounts')
admins = cursor.fetchall()

for admin in admins:
    print(f"Email: {admin['email']}")
    print(f"Password stored: {admin['password']}")
    print(f"Password length: {len(admin['password'])}")
    print(f"Starts with scrypt/pbkdf2: {admin['password'].startswith(('scrypt:', 'pbkdf2:'))}")
    print()

cursor.close()
conn.close()
