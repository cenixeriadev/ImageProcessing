import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def test_user_login_with_remember_me_and_jwt_cookie():
    # Generate unique user info for registration
    unique_suffix = str(uuid.uuid4()).replace("-", "")
    username = f"user_{unique_suffix}"
    password = "TestPass123!"
    email = f"{unique_suffix}@example.com"

    register_url = f"{BASE_URL}/register"
    login_url = f"{BASE_URL}/login"

    user_data = {
        "username": username,
        "password": password,
        "email": email
    }

    login_data = {
        "username": username,
        "password": password,
        "remember_me": True
    }

    # Register user
    register_resp = requests.post(register_url, json=user_data, timeout=TIMEOUT)
    assert register_resp.status_code == 200, f"Registration failed: {register_resp.text}"
    register_json = register_resp.json()
    assert "access_token" in register_json
    assert register_json.get("token_type") == "bearer"

    # Login with correct credentials and remember_me=True
    login_resp = requests.post(login_url, json=login_data, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"

    login_json = login_resp.json()
    assert "access_token" in login_json, "JWT token missing in login response"
    assert login_json.get("token_type") == "bearer"

    # Check that httponly cookie is set with the token
    cookies = login_resp.cookies
    access_token_cookie = cookies.get("access_token")
    assert access_token_cookie is not None, "access_token cookie not set on login"
    # httponly cookie attribute cannot be checked directly via requests cookies,
    # but absence of the cookie would be a failure.

    # Try login with invalid credentials
    invalid_login_data = {
        "username": username,
        "password": "WrongPassword!",
        "remember_me": False
    }
    invalid_login_resp = requests.post(login_url, json=invalid_login_data, timeout=TIMEOUT)
    assert invalid_login_resp.status_code == 401, f"Invalid login did not return 401 but {invalid_login_resp.status_code}"

# Execute the test function
test_user_login_with_remember_me_and_jwt_cookie()