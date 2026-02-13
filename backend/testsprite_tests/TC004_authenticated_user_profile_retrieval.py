import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def test_authenticated_user_profile_retrieval():
    # Generate random user data for registration
    random_suffix = uuid.uuid4().hex[:8]
    username = f"testuser_{random_suffix}"
    password = "TestPassword123!"
    email = f"{random_suffix}@example.com"

    headers = {"Content-Type": "application/json"}

    # Register a new user to get token
    register_payload = {
        "username": username,
        "password": password,
        "email": email
    }
    register_resp = requests.post(f"{BASE_URL}/register", json=register_payload, headers=headers, timeout=TIMEOUT)
    assert register_resp.status_code == 200, f"Registration failed: {register_resp.text}"
    register_json = register_resp.json()
    assert "access_token" in register_json and register_json.get("token_type") == "bearer"
    token = register_json["access_token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    try:
        # Successful profile retrieval with valid token
        me_resp = requests.get(f"{BASE_URL}/me", headers=auth_header, timeout=TIMEOUT)
        assert me_resp.status_code == 200, f"/me with valid token failed: {me_resp.text}"
        profile = me_resp.json()
        # Validate presence and types of expected fields
        assert isinstance(profile.get("id"), (int, str)) and profile.get("id"), "Invalid or missing id"
        assert profile.get("username") == username, "Username mismatch"
        assert profile.get("email") == email, "Email mismatch"
        assert "created_at" in profile and profile["created_at"], "Missing created_at"
        assert "last_login" in profile, "Missing last_login"

        # Profile retrieval with invalid token
        invalid_token_header = {"Authorization": "Bearer invalid.token.value"}
        invalid_resp = requests.get(f"{BASE_URL}/me", headers=invalid_token_header, timeout=TIMEOUT)
        assert invalid_resp.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {invalid_resp.status_code}"

        # Profile retrieval with missing token
        missing_token_resp = requests.get(f"{BASE_URL}/me", timeout=TIMEOUT)
        assert missing_token_resp.status_code == 401, f"Expected 401 Unauthorized for missing token, got {missing_token_resp.status_code}"

    finally:
        # Cleanup: no direct delete user endpoint provided, so skipping deletion.
        # If such an endpoint existed, we would delete the user here.
        pass


test_authenticated_user_profile_retrieval()