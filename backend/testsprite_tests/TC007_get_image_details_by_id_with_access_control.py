import requests
from requests.exceptions import RequestException
import uuid
import io

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def register_user(username: str, email: str, password: str):
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    try:
        resp = requests.post(url, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        token = data.get("access_token")
        assert token is not None and data.get("token_type") == "bearer"
        return token
    except RequestException as e:
        raise RuntimeError(f"User registration failed: {e}")


def upload_image(token: str, filename="test-image.png", content=b"fakeimagecontent"):
    url = f"{BASE_URL}/images"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (filename, io.BytesIO(content), "image/png")}
    try:
        resp = requests.post(url, headers=headers, files=files, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        image_id = data.get("id")
        image_url = data.get("url")
        assert image_id and image_url
        return image_id
    except RequestException as e:
        raise RuntimeError(f"Image upload failed: {e}")


def delete_image(token: str, image_id: str):
    url = f"{BASE_URL}/images/{image_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.delete(url, headers=headers, timeout=TIMEOUT)
        # delete may return 200 or 404 (if already deleted)
        if resp.status_code not in (200, 404):
            resp.raise_for_status()
        return resp.status_code
    except RequestException as e:
        # If unable to delete, log error but do not fail cleanup
        pass


def get_image_details(token: str, image_id: str):
    url = f"{BASE_URL}/images/{image_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
        return resp
    except RequestException as e:
        raise RuntimeError(f"Get image details request failed: {e}")


def test_get_image_details_by_id_with_access_control():
    # Register user1 and user2
    username1 = f"user1_{uuid.uuid4().hex[:8]}"
    email1 = f"{username1}@example.com"
    password1 = "Password123!"
    token1 = register_user(username1, email1, password1)

    username2 = f"user2_{uuid.uuid4().hex[:8]}"
    email2 = f"{username2}@example.com"
    password2 = "Password123!"
    token2 = register_user(username2, email2, password2)

    image_id = None
    try:
        # user1 uploads an image
        image_id = upload_image(token1)

        # user1 tries to get the image details - expect 200 and correct id/url
        resp_owner = get_image_details(token1, image_id)
        assert resp_owner.status_code == 200
        data_owner = resp_owner.json()
        assert data_owner.get("id") == image_id
        assert "url" in data_owner and isinstance(data_owner["url"], str)

        # user2 tries to get the same image details - expect 404 (not found / unauthorized access)
        resp_other = get_image_details(token2, image_id)
        assert resp_other.status_code == 404

        # Unauthenticated request to get image details - expect 401 or 404 (likely 401)
        resp_unauth = requests.get(f"{BASE_URL}/images/{image_id}", timeout=TIMEOUT)
        assert resp_unauth.status_code in (401, 404)

        # Request with invalid image ID with user1 auth - expect 404
        invalid_image_id = str(uuid.uuid4())
        resp_invalid = get_image_details(token1, invalid_image_id)
        assert resp_invalid.status_code == 404

    finally:
        # Cleanup - delete image if created
        if image_id:
            delete_image(token1, image_id)


test_get_image_details_by_id_with_access_control()