import requests
import uuid
import io

BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/register"
IMAGES_URL = f"{BASE_URL}/images"

TEST_USERNAME = f"testuser_{uuid.uuid4().hex[:8]}"
TEST_PASSWORD = "TestPass123!"
TEST_EMAIL = f"{TEST_USERNAME}@example.com"

def test_image_upload_to_s3_with_uuid_path():
    # Register new user to get token
    register_payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "email": TEST_EMAIL
    }
    register_resp = requests.post(REGISTER_URL, json=register_payload, timeout=30)
    assert register_resp.status_code == 200, f"Registration failed: {register_resp.text}"
    register_json = register_resp.json()
    token = register_json.get("access_token")
    assert token and isinstance(token, str), "No access_token in registration response"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Prepare an in-memory image file (PNG)
    image_content = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\nIDATx\xdac\xf8\x0f\x00\x01\x01\x01\x00"
        b"\x18\xdd\x03\xfd\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    image_filename = "test_image.png"
    files = {
        "file": (image_filename, io.BytesIO(image_content), "image/png")
    }

    image_id = None
    try:
        upload_resp = requests.post(IMAGES_URL, headers=headers, files=files, timeout=30)
        assert upload_resp.status_code == 200, f"Image upload failed: {upload_resp.text}"
        upload_json = upload_resp.json()
        image_id = upload_json.get("id")
        image_url = upload_json.get("url")
        assert isinstance(image_id, str) and len(image_id) > 0, "Invalid or missing image ID"
        assert isinstance(image_url, str) and len(image_url) > 0, "Invalid or missing image URL"
        # Check if the image_url contains a UUID pattern indicating UUID-based path
        # Typical UUID regex pattern: 8-4-4-4-12 hex digits
        import re
        uuid_pattern = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
        assert uuid_pattern.search(image_url), "Image URL does not contain UUID path"
    finally:
        # Clean up: delete uploaded image if it was created
        if image_id:
            delete_url = f"{IMAGES_URL}/{image_id}"
            delete_resp = requests.delete(delete_url, headers=headers, timeout=30)
            # If deletion fails, just print warning but do not raise
            if delete_resp.status_code != 200:
                print(f"Warning: Failed to delete image {image_id}: {delete_resp.status_code} {delete_resp.text}")

test_image_upload_to_s3_with_uuid_path()