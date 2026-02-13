import requests
from requests.exceptions import RequestException
import re

BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/register"
TIMEOUT = 30

def test_user_registration_email_validation_jwt_token_return():
    # Helper function to register a user
    def register_user(username, email, password):
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        try:
            response = requests.post(REGISTER_URL, json=payload, timeout=TIMEOUT)
            return response
        except RequestException as e:
            raise AssertionError(f"Request to /register failed: {e}")

    # Unique username and email base for this test run
    import uuid
    unique_id = uuid.uuid4().hex[:8]

    valid_username = f"user_{unique_id}"
    valid_email = f"{unique_id}@example.com"
    valid_password = "StrongPass123!"

    # 1. Successful registration with valid username, email, password
    resp = register_user(valid_username, valid_email, valid_password)
    assert resp.status_code == 200, f"Expected 200 OK but got {resp.status_code} with body {resp.text}"
    json_response = resp.json()
    assert "access_token" in json_response, "Response JSON missing 'access_token'"
    assert json_response.get("token_type") == "bearer", "token_type should be 'bearer'"

    # The access_token should be a non-empty string
    access_token = json_response["access_token"]
    assert isinstance(access_token, str) and len(access_token) > 0, "Invalid access_token returned"

    # Simple email format validation for the registration email
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    assert re.match(email_regex, valid_email), "Provided email does not match email format"

    # 2. Duplicate username registration should be rejected (400)
    resp_dup_username = register_user(valid_username, f"diff_{valid_email}", valid_password)
    assert resp_dup_username.status_code == 400, f"Duplicate username should return 400 but got {resp_dup_username.status_code}"
    assert "Usuario ya existe" in resp_dup_username.text, "Expected error message for duplicate username"

    # 3. Invalid email format should be rejected (likely 422 Unprocessable Entity or 400)
    invalid_emails = ["plainaddress", "missing_at_sign.com", "missingdomain@.com", "missingdot@domaincom", "@missingusername.com"]
    for bad_email in invalid_emails:
        resp_bad_email = register_user(f"user_{uuid.uuid4().hex[:6]}", bad_email, valid_password)
        # Accepting 400 or 422 for validation errors depending on FastAPI response
        assert resp_bad_email.status_code in (400, 422), f"Invalid email '{bad_email}' should be rejected with 400/422 but got {resp_bad_email.status_code}"

test_user_registration_email_validation_jwt_token_return()