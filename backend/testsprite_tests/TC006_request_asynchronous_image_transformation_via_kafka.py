import requests
import uuid
import io

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_request_async_image_transformation_via_kafka():
    session = requests.Session()

    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "TestPass123!"
    email = f"{username}@example.com"

    # Register user
    register_payload = {
        "username": username,
        "password": password,
        "email": email
    }
    r = session.post(f"{BASE_URL}/register", json=register_payload, timeout=TIMEOUT)
    assert r.status_code == 200, f"Registration failed: {r.text}"
    access_token = r.json().get("access_token")
    assert access_token, "No access token returned on registration"

    headers = {"Authorization": f"Bearer {access_token}"}

    image_id = None

    try:
        # Upload image to create a resource
        image_content = io.BytesIO(b"fake image content for testing")
        files = {"file": ("test_image.png", image_content, "image/png")}
        r = session.post(f"{BASE_URL}/images", headers=headers, files=files, timeout=TIMEOUT)
        assert r.status_code == 200, f"Image upload failed: {r.text}"
        image_resp = r.json()
        assert "id" in image_resp, f"No image id in response: {r.text}"
        try:
            image_id = int(image_resp["id"])
        except Exception:
            assert False, f"Image id is not an integer: {image_resp['id']}"

        # Request image transformation with valid image_id and auth
        transform_payload = {
            "transformations": {
                "resize": {"width": 100, "height": 100},
                "grayscale": True
            }
        }
        r = session.post(f"{BASE_URL}/images/{image_id}/transform", headers=headers, json=transform_payload, timeout=TIMEOUT)
        assert r.status_code == 200, f"Transform request failed: {r.text}"
        resp_json = r.json()
        assert "message" in resp_json
        assert "procesará en background" in resp_json["message"]

        # Request transformation with invalid image_id returns 404
        invalid_image_id = 9999999
        r = session.post(f"{BASE_URL}/images/{invalid_image_id}/transform", headers=headers, json=transform_payload, timeout=TIMEOUT)
        assert r.status_code == 404, f"Expected 404 for invalid image_id but got {r.status_code}"

        # Register a second user to test access control
        username2 = f"user_{uuid.uuid4().hex[:8]}"
        email2 = f"{username2}@example.com"
        register_payload2 = {
            "username": username2,
            "password": password,
            "email": email2
        }
        r = session.post(f"{BASE_URL}/register", json=register_payload2, timeout=TIMEOUT)
        assert r.status_code == 200, f"Second registration failed: {r.text}"
        access_token2 = r.json().get("access_token")
        assert access_token2, "No access token returned for second user"
        headers2 = {"Authorization": f"Bearer {access_token2}"}

        # Second user tries to request transformation on first user's image
        r = session.post(f"{BASE_URL}/images/{image_id}/transform", headers=headers2, json=transform_payload, timeout=TIMEOUT)
        assert r.status_code == 404, f"Expected 404 when requesting transform for image not owned by user2, got {r.status_code}"

    finally:
        # Cleanup: delete created image as original user
        if image_id:
            del_response = session.delete(f"{BASE_URL}/images/{image_id}", headers=headers, timeout=TIMEOUT)
            assert del_response.status_code == 200, f"Image deletion failed: {del_response.text}"

test_request_async_image_transformation_via_kafka()