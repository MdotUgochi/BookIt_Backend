# test_mercy_user.py - Test with mercy@example.com

import requests
import json

def test_mercy_user():
    BASE_URL = "http://127.0.0.1:8000"
    
    print("🔍 Testing with mercy@example.com")
    print("=" * 50)
    
    # Login with mercy user credentials
    print("1️⃣ Logging in...")
    login_data = {
        "username": "mercy@example.com",
        "password": "1234go"  
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"Access token: {access_token[:50]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test protected endpoint
    print("\n2️⃣ Testing /users/me...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! /users/me is working!")
            user_data = response.json()
            print("User Profile:")
            print(json.dumps(user_data, indent=2))
        elif response.status_code == 500:
            print("❌ 500 Internal Server Error")
            print("Check your server logs for the detailed error!")
            print("Common causes:")
            print("- Missing schemas/user.py file")
            print("- Import errors in users router")
            print("- Database connection issues")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request error: {e}")
    
    # Test PATCH /users/me
    print("\n3️⃣ Testing PATCH /users/me...")
    update_data = {
        "name": "Mercy Updated"
    }
    
    try:
        response = requests.patch(
            f"{BASE_URL}/users/me",
            json=update_data,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"PATCH Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Profile update successful!")
            updated_data = response.json()
            print("Updated Profile:")
            print(json.dumps(updated_data, indent=2))
        else:
            print(f"❌ Update failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Update error: {e}")

if __name__ == "__main__":
    test_mercy_user()