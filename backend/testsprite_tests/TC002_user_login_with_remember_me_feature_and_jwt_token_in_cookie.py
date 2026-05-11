import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_user_login_with_remember_me_and_jwt_cookie():
    # Generate unique username and email for registration
    unique_suffix = str(uuid.uuid4())
    username = f"testuser_{unique_suffix}"
    password = "SafePass123!"
    email = f"{username}@example.com"

    register_url = f"{BASE_URL}/register"
    login_url = f"{BASE_URL}/login"

    # Register a new user first
    register_payload = {
        "username": username,
        "password": password,
        "email": email
    }
    register_resp = requests.post(register_url, json=register_payload, timeout=TIMEOUT)
    assert register_resp.status_code == 200, f"Registration failed: {register_resp.text}"
    register_json = register_resp.json()
    assert "access_token" in register_json
    assert register_json.get("token_type") == "bearer"

    try:
        # Successful login with remember_me = True
        login_payload = {
            "username": username,
            "password": password,
            "remember_me": True
        }
        login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        login_json = login_resp.json()
        # Validate presence of JWT access_token and token_type
        assert "access_token" in login_json
        assert login_json.get("token_type") == "bearer"

        # Check if 'access_token' cookie is set and is HttpOnly
        cookies = login_resp.cookies
        access_token_cookie = cookies.get("access_token")
        assert access_token_cookie, "access_token cookie not set"

        # Since requests doesn't expose HttpOnly flag directly,
        # we check the 'Set-Cookie' header to confirm HttpOnly flag presence
        set_cookie_headers = login_resp.headers.get("Set-Cookie")
        assert set_cookie_headers and "HttpOnly" in set_cookie_headers, "HttpOnly flag not set on cookie"

        # Successful login with remember_me = False (default)
        login_payload_no_remember = {
            "username": username,
            "password": password
        }
        login_resp2 = requests.post(login_url, json=login_payload_no_remember, timeout=TIMEOUT)
        assert login_resp2.status_code == 200, f"Login without remember_me failed: {login_resp2.text}"
        json2 = login_resp2.json()
        assert "access_token" in json2
        assert json2.get("token_type") == "bearer"
        cookies2 = login_resp2.cookies
        access_token_cookie2 = cookies2.get("access_token")
        assert access_token_cookie2, "access_token cookie not set on login without remember_me"
        set_cookie_headers2 = login_resp2.headers.get("Set-Cookie")
        assert set_cookie_headers2 and "HttpOnly" in set_cookie_headers2, "HttpOnly flag missing on cookie without remember_me"

        # Test invalid credentials -> 401 Unauthorized
        invalid_login_payload = {
            "username": username,
            "password": "WrongPass123!",
            "remember_me": True
        }
        invalid_resp = requests.post(login_url, json=invalid_login_payload, timeout=TIMEOUT)
        assert invalid_resp.status_code == 401, f"Invalid login did not return 401: {invalid_resp.status_code} {invalid_resp.text}"
    finally:
        # Cleanup: no logout endpoint tested here, user can remain for DB cleanup manually if needed
        pass

test_user_login_with_remember_me_and_jwt_cookie()