import requests
import uuid
import io

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def register_user(username, password, email):
    payload = {"username": username, "password": password, "email": email}
    r = requests.post(f"{BASE_URL}/register", json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    assert "access_token" in data
    return data["access_token"]


def upload_image(token, file_bytes, filename="test-image.png"):
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (filename, file_bytes, "image/png")}
    r = requests.post(f"{BASE_URL}/images", headers=headers, files=files, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    assert "id" in data and "url" in data
    return int(data["id"])


def delete_image(token, image_id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{BASE_URL}/images/{image_id}", headers=headers, timeout=TIMEOUT)
    return r


def get_image(token, image_id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/images/{image_id}", headers=headers, timeout=TIMEOUT)
    return r


def test_delete_image_by_id_with_secure_ownership_verification():
    # Register two users
    username1 = f"user1_{uuid.uuid4().hex[:8]}"
    username2 = f"user2_{uuid.uuid4().hex[:8]}"
    password = "StrongPass!23"
    email1 = f"{username1}@example.com"
    email2 = f"{username2}@example.com"

    token1 = register_user(username1, password, email1)
    token2 = register_user(username2, password, email2)

    # Upload an image as user1
    image_content = io.BytesIO(b"PNGDATA" * 100)  # fake image content
    image_id = None

    try:
        image_id = upload_image(token1, image_content)

        # User1 deletes their own image successfully
        r_delete_owner = delete_image(token1, image_id)
        assert r_delete_owner.status_code == 200
        resp = r_delete_owner.json()
        assert resp.get("message") == "Imagen eliminada exitosamente"

        # Confirm image is deleted (should return 404)
        r_get_deleted = get_image(token1, image_id)
        assert r_get_deleted.status_code == 404

        # Upload another image as user1 for ownership test
        image_id = upload_image(token1, io.BytesIO(b"PNGDATA" * 100))

        # User2 tries to delete user1's image -> should be 404 (not found or unauthorized)
        r_delete_not_owner = delete_image(token2, image_id)
        assert r_delete_not_owner.status_code == 404

        # Confirm image still exists for user1
        r_get_owner = get_image(token1, image_id)
        assert r_get_owner.status_code == 200

        # Test deletion of invalid/non-existent image id returns 404
        invalid_id = 99999999
        r_delete_invalid = delete_image(token1, invalid_id)
        assert r_delete_invalid.status_code == 404

    finally:
        # Cleanup: try deleting the image if still exists and owned by user1
        if image_id is not None:
            try:
                delete_image(token1, image_id)
            except Exception:
                pass


test_delete_image_by_id_with_secure_ownership_verification()