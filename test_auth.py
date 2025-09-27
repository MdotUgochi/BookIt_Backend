import requests
import json
import os

def test_auth_detailed():
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    print("🔍 Detailed Authentication Test")
    print("=" * 50)

    # 1️⃣ Check docs
    try:
        r = requests.get(f"{BASE_URL}/docs", timeout=5)
        if r.status_code == 200:
            print("✅ Server running")
        else:
            print(f"❌ Docs not accessible (status {r.status_code})")
            return
    except requests.RequestException as e:
        print(f"❌ Cannot connect: {e}")
        return

    # 2️⃣ Registration
    register_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "role": "user" 
    }
    r = requests.post(
        f"{BASE_URL}/auth/register",
        json=register_data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    print(f"Registration status: {r.status_code}")
    if r.status_code in [200, 201]:
        print("✅ Registration successful")
    elif r.status_code in [400, 422]:
        print("⚠️ Registration issue:", r.text)
    else:
        print("❌ Registration failed:", r.text)

    # 3️⃣ Login (form)
    login_form = {
        "username": register_data["email"],
        "password": register_data["password"]
    }
    r = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=5
    )
    print(f"Login status: {r.status_code}")
    if r.status_code == 200:
        token_data = r.json()
        access_token = token_data["access_token"]
        print(f"✅ Access token received: {access_token[:40]}...")

        # 4️⃣ Protected route
        headers = {"Authorization": f"Bearer {access_token}"}
        me = requests.get(f"{BASE_URL}/users/me", headers=headers, timeout=5)
        print(f"Protected endpoint status: {me.status_code}")
        if me.status_code == 200:
            print("✅ /users/me works:", me.json())
        else:
            print("❌ /users/me failed:", me.text)
    else:
        print("❌ Login failed:", r.text)

if __name__ == "__main__":
    test_auth_detailed()
