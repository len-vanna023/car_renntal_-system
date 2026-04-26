#!/usr/bin/env python
"""Check actual database schema"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.models.db_config import get_db_connection, close_db_connection
from mysql.connector import Error

def check_users_table():
    """Check the actual schema of users table"""
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database!")
        return
    
    try:
        cursor = conn.cursor()
        
        # Get table structure
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        
        print("\n📋 USERS TABLE STRUCTURE:")
        print("="*60)
        for col in columns:
            print(f"   {col[0]:20} {col[1]:30} {col[2] or ''}")
        
        cursor.close()
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if conn and conn.is_connected():
            close_db_connection(conn)

if __name__ == "__main__":
    check_users_table()
