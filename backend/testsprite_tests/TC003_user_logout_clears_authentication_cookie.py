import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_user_logout_clears_authentication_cookie():
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "TestPass123!"
    email = f"{username}@example.com"

    session = requests.Session()
    try:
        # Register user
        register_resp = session.post(
            f"{BASE_URL}/register",
            json={"username": username, "password": password, "email": email},
            timeout=TIMEOUT,
        )
        assert register_resp.status_code == 200
        register_json = register_resp.json()
        assert "access_token" in register_json
        assert register_json.get("token_type") == "bearer"

        # Login user
        login_resp = session.post(
            f"{BASE_URL}/login",
            json={"username": username, "password": password, "remember_me": False},
            timeout=TIMEOUT,
        )
        assert login_resp.status_code == 200
        login_json = login_resp.json()
        assert "access_token" in login_json
        assert login_json.get("token_type") == "bearer"

        # Check that cookie 'access_token' is set
        assert "access_token" in session.cookies and session.cookies.get("access_token")

        # Logout user
        logout_resp = session.post(f"{BASE_URL}/logout", timeout=TIMEOUT)
        assert logout_resp.status_code == 200
        logout_json = logout_resp.json()
        assert logout_json.get("message") == "logged out"

        # Confirm cookie deleted or expired by checking cookie value
        access_token_cookie = session.cookies.get("access_token")
        # The cookie might be cleared (None) or emptied string after logout
        assert access_token_cookie is None or access_token_cookie == ""

        # Optionally, verify that authenticated endpoint now fails (GET /me)
        me_resp = session.get(f"{BASE_URL}/me", timeout=TIMEOUT)
        assert me_resp.status_code == 401

    finally:
        # Clean-up: If API supports user deletion, would delete user here.
        # No user delete endpoint specified, so no action.
        pass

test_user_logout_clears_authentication_cookie()