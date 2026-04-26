#!/usr/bin/env python
"""Test the account creation fix"""
import json
import requests
import sys
import time

BASE_URL = "http://localhost:5000"

def test_signup_json():
    """Test account creation with JSON data"""
    print("\n" + "="*60)
    print("🧪 TESTING ACCOUNT CREATION FIX")
    print("="*60)
    
    # Generate unique email to avoid conflicts
    import random
    unique_id = random.randint(10000, 99999)
    test_email = f"testuser{unique_id}@example.com"
    
    # Test 1: Successful signup with JSON
    print("\n✅ Test 1: Create account with JSON data")
    data = {
        "fullname": "Test User",
        "email": test_email,
        "phone": "0987654321",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 201 and response.json().get('success'):
            print("   ✅ SUCCESS! Account created with JSON")
            return True
        else:
            print(f"   ❌ FAILED: {response.json().get('message')}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_password_mismatch():
    """Test password mismatch validation"""
    print("\n❌ Test 2: Password mismatch validation")
    data = {
        "fullname": "Test User",
        "email": "mismatch@example.com",
        "phone": "0987654321",
        "password": "password123",
        "confirm_password": "differentpass"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        
        if response.status_code == 400 and 'match' in result.get('message', '').lower():
            print("   ✅ CORRECT! Properly rejected mismatched passwords")
            return True
        else:
            print(f"   ❌ UNEXPECTED: {result.get('message')}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    # Wait for server to be ready
    print("\n⏳ Waiting for server to be ready...")
    for i in range(10):
        try:
            requests.get(f"{BASE_URL}/")
            print("✅ Server is ready!")
            break
        except:
            if i == 9:
                print("❌ Server not responding!")
                sys.exit(1)
            time.sleep(1)
    
    success = True
    success = test_signup_json() and success
    success = test_password_mismatch() and success
    
    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED! Account creation is fixed!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*60 + "\n")
