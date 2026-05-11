import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def test_authenticated_user_profile_retrieval():
    # Prepare test user data
    unique_suffix = str(uuid.uuid4())[:8]
    username = f"testuser_{unique_suffix}"
    password = "StrongPassw0rd!"
    email = f"{username}@example.com"

    user_token = None

    try:
        # Register a new user
        register_resp = requests.post(
            f"{BASE_URL}/register",
            json={"username": username, "password": password, "email": email},
            timeout=TIMEOUT,
        )
        assert register_resp.status_code == 200, f"Register failed: {register_resp.text}"
        register_json = register_resp.json()
        assert "access_token" in register_json and register_json["token_type"] == "bearer"
        user_token = register_json["access_token"]

        headers = {"Authorization": f"Bearer {user_token}"}

        # Use valid token to access /me
        me_resp = requests.get(f"{BASE_URL}/me", headers=headers, timeout=TIMEOUT)
        assert me_resp.status_code == 200, f"/me endpoint failed: {me_resp.text}"
        user_data = me_resp.json()
        # Validate required fields present
        for field in ("id", "username", "email", "created_at", "last_login"):
            assert field in user_data, f"Missing field '{field}' in /me response"
        # Fields except last_login should be non-empty
        for field in ("id", "username", "email", "created_at"):
            assert user_data[field], f"Field '{field}' is empty in /me response"
        assert user_data["username"] == username
        assert user_data["email"] == email

        # Test /me with invalid token
        invalid_headers = {"Authorization": "Bearer invalidtoken123"}
        invalid_resp = requests.get(f"{BASE_URL}/me", headers=invalid_headers, timeout=TIMEOUT)
        assert invalid_resp.status_code == 401, f"Expected 401 for invalid token but got {invalid_resp.status_code}"

        # Test /me with missing token (no auth header)
        missing_resp = requests.get(f"{BASE_URL}/me", timeout=TIMEOUT)
        assert missing_resp.status_code == 401, f"Expected 401 for missing token but got {missing_resp.status_code}"

    finally:
        if user_token:
            # Logout user to clear cookie and invalidate session if supported
            try:
                requests.post(f"{BASE_URL}/logout", headers={"Authorization": f"Bearer {user_token}"}, timeout=TIMEOUT)
            except Exception:
                pass


test_authenticated_user_profile_retrieval()
