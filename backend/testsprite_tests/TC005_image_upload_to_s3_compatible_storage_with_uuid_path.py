import requests
import uuid
import io

BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"
IMAGES_URL = f"{BASE_URL}/images"

def test_image_upload_to_s3_with_uuid_path():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "TestPassword123!"
    email = f"{username}@example.com"
    # Register user
    register_payload = {
        "username": username,
        "password": password,
        "email": email,
    }
    try:
        r = requests.post(REGISTER_URL, json=register_payload, timeout=30)
        assert r.status_code == 200, f"Register failed: {r.text}"
        token = r.json().get("access_token")
        assert token, "No access_token returned after register"
    except Exception as e:
        raise AssertionError(f"Exception during user registration: {e}")

    # Login user
    login_payload = {
        "username": username,
        "password": password,
        "remember_me": False,
    }
    try:
        r = requests.post(LOGIN_URL, json=login_payload, timeout=30)
        assert r.status_code == 200, f"Login failed: {r.text}"
        login_token = r.json().get("access_token")
        assert login_token, "No access_token returned after login"
    except Exception as e:
        raise AssertionError(f"Exception during user login: {e}")

    auth_header = {"Authorization": f"Bearer {login_token}"}

    # Prepare a small PNG image in memory for upload
    png_header = b"\x89PNG\r\n\x1a\n"
    fake_png_data = png_header + b"\x00" * 1024  # 1KB fake PNG data
    file_name = "test_image.png"
    files = {
        "file": (file_name, io.BytesIO(fake_png_data), "image/png")
    }

    image_id = None

    try:
        # Upload image with authentication
        upload_resp = requests.post(IMAGES_URL, files=files, headers=auth_header, timeout=30)
        assert upload_resp.status_code == 200, f"Image upload failed: {upload_resp.text}"
        resp_json = upload_resp.json()
        image_id_str = resp_json.get("id")
        url = resp_json.get("url")
        assert image_id_str is not None, "Response missing image id"
        assert url is not None and url != "", "Response missing url"

        # image_id is integer per spec
        try:
            image_id = int(image_id_str)
        except Exception:
            raise AssertionError("Returned image id is not an integer")

        # Verify url contains a UUID-based path (UUID format in URL path)
        # Extract the path part and check for uuid pattern
        # Since UUID is canonical 8-4-4-4-12 hex digits
        import re
        uuid_regex = re.compile(
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"
        )
        assert uuid_regex.search(url), "URL does not contain a valid UUID path"

        # Try uploading without auth header should return 401
        upload_resp_unauth = requests.post(IMAGES_URL, files=files, timeout=30)
        assert upload_resp_unauth.status_code == 401, "Unauthenticated upload should fail with 401"

    finally:
        # Cleanup: delete the uploaded image if created
        if image_id is not None:
            delete_url = f"{IMAGES_URL}/{image_id}"
            try:
                del_resp = requests.delete(delete_url, headers=auth_header, timeout=30)
                assert del_resp.status_code == 200, f"Image deletion failed: {del_resp.text}"
            except Exception as e:
                # Log deletion error but don't fail test because cleanup failed
                print(f"Cleanup deletion failed: {e}")

test_image_upload_to_s3_with_uuid_path()