import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_user_logout_clears_auth_cookie():
    # Prepare unique user data for registration
    unique_suffix = uuid.uuid4().hex[:8]
    username = f"testuser_{unique_suffix}"
    password = "TestPassword123!"
    email = f"{unique_suffix}@example.com"

    session = requests.Session()

    try:
        # Register user
        register_payload = {
            "username": username,
            "password": password,
            "email": email
        }
        reg_resp = session.post(
            f"{BASE_URL}/register",
            json=register_payload,
            timeout=TIMEOUT
        )
        assert reg_resp.status_code == 200, f"Register failed: {reg_resp.text}"
        assert "access_token" in reg_resp.json()

        # Login user
        login_payload = {
            "username": username,
            "password": password,
            "remember_me": False
        }
        login_resp = session.post(
            f"{BASE_URL}/login",
            json=login_payload,
            timeout=TIMEOUT
        )
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        login_json = login_resp.json()
        assert "access_token" in login_json
        # Check that access_token cookie is set (httponly)
        cookies = login_resp.cookies
        assert "access_token" in cookies, "access_token cookie missing after login"

        # Before logout, confirm access_token cookie present in session.cookies
        assert "access_token" in session.cookies, "access_token cookie missing in session before logout"

        # Logout user - this should clear the access_token cookie
        logout_resp = session.post(
            f"{BASE_URL}/logout",
            timeout=TIMEOUT
        )
        assert logout_resp.status_code == 200, f"Logout failed: {logout_resp.text}"
        logout_json = logout_resp.json()
        assert logout_json.get("message") == "logged out"

        # After logout, the access_token cookie should be cleared/expired
        # We verify by checking if session cookies no longer contain 'access_token' or that its value is empty
        # Manually update session cookies with response cookies from logout (which clears the cookie)
        session.cookies.update(logout_resp.cookies)
        cookie_value = session.cookies.get("access_token")
        # It can be None or an empty string or expired (depends on implementation),
        # assert that cookie is either missing or empty string
        assert not cookie_value, "access_token cookie was not cleared after logout"

    finally:
        # Cleanup: no persistent user deletion endpoint described, so no explicit cleanup feasible
        # This test leaves a user registered; in real env a cleanup step might be needed.
        pass

test_user_logout_clears_auth_cookie()