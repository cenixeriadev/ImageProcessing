import requests
import re
import time

BASE_URL = "http://localhost:8000"
REGISTER_ENDPOINT = f"{BASE_URL}/register"
TIMEOUT = 30

def test_user_registration_email_validation_jwt_token_return():
    unique_suffix = str(int(time.time()))
    # Valid user data
    valid_user = {
        "username": f"testuser123_{unique_suffix}",
        "email": f"testuser123_{unique_suffix}@example.com",
        "password": "StrongPass!123"
    }

    # Another user with different username but invalid email
    invalid_email_user = {
        "username": f"testuser456_{unique_suffix}",
        "email": "invalid-email-format",
        "password": "StrongPass!123"
    }

    # Duplicate username user data (same username as valid_user)
    duplicate_username_user = {
        "username": valid_user["username"],
        "email": f"differentemail_{unique_suffix}@example.com",
        "password": "StrongPass!123"
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Helper function to register a user
    def register_user(user_data):
        response = requests.post(
            REGISTER_ENDPOINT,
            json=user_data,
            headers=headers,
            timeout=TIMEOUT
        )
        return response

    # 1. Register with valid data - expect success 200 and JWT token returned
    response = register_user(valid_user)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}, response: {response.text}"
    json_resp = response.json()
    assert "access_token" in json_resp, "access_token missing in response"
    assert json_resp.get("token_type") == "bearer", f"Expected token_type bearer, got {json_resp.get('token_type')}"

    # Validate access_token is a JWT format (simple regex check)
    jwt_pattern = re.compile(r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$")
    assert jwt_pattern.match(json_resp["access_token"]), "access_token is not a valid JWT"

    # 2. Register with duplicate username - expect 400 and "Usuario ya existe" error
    response_dup = register_user(duplicate_username_user)
    assert response_dup.status_code == 400, f"Expected 400 for duplicate username, got {response_dup.status_code}"
    # The error message based on PRD is likely JSON string or plain text "Usuario ya existe"
    try:
        error_resp = response_dup.json()
        # It may be a dict with message or string
        if isinstance(error_resp, dict) and "detail" in error_resp:
            assert "Usuario ya existe" in error_resp["detail"], f"Unexpected error message {error_resp['detail']}"
        else:
            assert "Usuario ya existe" in str(error_resp)
    except Exception:
        # fallback check plain text
        assert "Usuario ya existe" in response_dup.text

    # 3. Register with invalid email - expect 422 or 400 and appropriate validation error
    response_invalid_email = register_user(invalid_email_user)
    # FastAPI usually returns 422 Unprocessable Entity for validation errors
    assert response_invalid_email.status_code in (400,422), f"Expected 400 or 422 for invalid email, got {response_invalid_email.status_code}"
    # Validate error mentions email or format issue
    try:
        json_error = response_invalid_email.json()
        errors = json_error.get("detail", [])
        assert any("email" in str(e).lower() for e in errors) or "value is not a valid email address" in str(errors), "Error does not mention invalid email"
    except Exception:
        # fallback: check text contains 'email'
        assert "email" in response_invalid_email.text.lower()

test_user_registration_email_validation_jwt_token_return()