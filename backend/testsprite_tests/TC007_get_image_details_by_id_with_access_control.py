import requests
import tempfile
import os
import random
import string
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def register_user(username, password, email):
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "password": password,
        "email": email
    }
    resp = requests.post(url, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    assert "access_token" in data
    return data["access_token"]


def upload_image(token, file_path):
    url = f"{BASE_URL}/images"
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
        resp = requests.post(url, headers=headers, files=files, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    assert "id" in data and "url" in data
    return data["id"]


def get_image(token, image_id):
    url = f"{BASE_URL}/images/{image_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=TIMEOUT)


def delete_image(token, image_id):
    url = f"{BASE_URL}/images/{image_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(url, headers=headers, timeout=TIMEOUT)
    # Could be 200 or 404 if already deleted
    return resp


def test_TC007_get_image_details_by_id_with_access_control():
    # Register first user (owner)
    owner_username = f"owner_{random_string()}"
    owner_password = "StrongPass!123"
    owner_email = f"{owner_username}@example.com"
    owner_token = register_user(owner_username, owner_password, owner_email)

    # Register second user (non-owner)
    other_username = f"other_{random_string()}"
    other_password = "StrongPass!123"
    other_email = f"{other_username}@example.com"
    other_token = register_user(other_username, other_password, other_email)

    # Create a temporary file to upload
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp_file.write(os.urandom(1024))  # 1KB random content
        tmp_file.close()

        image_id = None
        try:
            # Owner uploads an image
            image_id = upload_image(owner_token, tmp_file.name)

            # Owner accesses the image details - expect 200
            resp_owner = get_image(owner_token, image_id)
            assert resp_owner.status_code == 200
            data_owner = resp_owner.json()
            assert "id" in data_owner and data_owner["id"] == image_id
            assert "url" in data_owner and isinstance(data_owner["url"], str) and data_owner["url"]

            # Non-owner accesses same image details - expect 404
            resp_other = get_image(other_token, image_id)
            assert resp_other.status_code == 404

            # Access with invalid token - expect 401 (per PRD for auth required endpoint)
            resp_invalid_auth = requests.get(f"{BASE_URL}/images/{image_id}",
                                            headers={"Authorization": "Bearer invalidtoken"},
                                            timeout=TIMEOUT)
            assert resp_invalid_auth.status_code == 401

            # Access without authentication - expect 401
            resp_no_auth = requests.get(f"{BASE_URL}/images/{image_id}", timeout=TIMEOUT)
            assert resp_no_auth.status_code == 401

            # Request non-existent image by owner - expect 404
            non_existent_id = str(uuid.uuid4())
            resp_non_exist = get_image(owner_token, non_existent_id)
            assert resp_non_exist.status_code == 404

        finally:
            # Cleanup: delete image by owner if created
            if image_id is not None:
                delete_resp = delete_image(owner_token, image_id)
                # Expect 200 or 404 if already deleted
                assert delete_resp.status_code in (200, 404)

    finally:
        os.unlink(tmp_file.name)


test_TC007_get_image_details_by_id_with_access_control()
