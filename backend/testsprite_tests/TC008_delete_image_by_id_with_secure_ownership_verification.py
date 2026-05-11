import requests
import io

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def register_user(username: str, email: str, password: str):
    url = f"{BASE_URL}/register"
    payload = {"username": username, "email": email, "password": password}
    resp = requests.post(url, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    return data["access_token"]


def upload_image(token: str, image_content: bytes, image_name: str = "test_image.png"):
    url = f"{BASE_URL}/images"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (image_name, io.BytesIO(image_content), "image/png")}
    resp = requests.post(url, headers=headers, files=files, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()  # Expected keys: id, url


def delete_image(token: str, image_id: str):
    url = f"{BASE_URL}/images/{image_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.delete(url, headers=headers, timeout=TIMEOUT)


def get_image(token: str, image_id: str):
    url = f"{BASE_URL}/images/{image_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=TIMEOUT)


def test_TC008_delete_image_by_id_with_secure_ownership_verification():
    # Register two users (owner and another user)
    owner_username = "owner_user_tc008"
    owner_email = "owner_tc008@example.com"
    owner_password = "StrongPass!123"

    other_username = "other_user_tc008"
    other_email = "other_tc008@example.com"
    other_password = "StrongPass!456"

    owner_token = register_user(owner_username, owner_email, owner_password)
    other_token = register_user(other_username, other_email, other_password)

    # Upload an image as owner
    image_content = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00"
        b"\x00\x00\nIDATx\xdac`\x00\x00\x00\x02\x00\x01\xe2!"
        b"\xbc\x33\x00\x00\x00\x00IEND\xaeB`\x82"
    )  # 1x1 PNG pixel
    image_data = upload_image(owner_token, image_content)
    image_id = image_data["id"]

    try:
        # Attempt to delete with owner token - should succeed
        delete_resp = delete_image(owner_token, image_id)
        assert delete_resp.status_code == 200, f"Expected 200 OK, got {delete_resp.status_code}"
        resp_json = delete_resp.json()
        assert resp_json.get("message") == "Imagen eliminada exitosamente"

        # Confirm image is deleted - GET should return 404
        get_resp_owner = get_image(owner_token, image_id)
        assert get_resp_owner.status_code == 404

        # Confirm other user cannot delete the same image again (already deleted)
        delete_resp_other = delete_image(other_token, image_id)
        assert delete_resp_other.status_code == 404

        # Upload another image to test unauthorized delete by other user
        image_data_2 = upload_image(owner_token, image_content)
        image_id_2 = image_data_2["id"]

        # Attempt delete as other user - should return 404 (not found or no ownership)
        delete_resp_other_unauth = delete_image(other_token, image_id_2)
        assert delete_resp_other_unauth.status_code == 404

        # Confirm owner can still get the image (not deleted by other user)
        get_resp_owner_2 = get_image(owner_token, image_id_2)
        assert get_resp_owner_2.status_code == 200

        # Cleanup: delete image as owner
        cleanup_delete = delete_image(owner_token, image_id_2)
        assert cleanup_delete.status_code == 200

        # Attempt delete by non-existing image ID with owner token (random UUID)
        import uuid

        random_uuid = str(uuid.uuid4())
        invalid_delete_resp = delete_image(owner_token, random_uuid)
        assert invalid_delete_resp.status_code == 404

    finally:
        # Cleanup in case test failed before deletion
        # Delete any remaining images by owner
        for img_id in [image_id, image_id_2]:
            # Try deleting; ignore errors
            try:
                delete_image(owner_token, img_id)
            except Exception:
                pass


test_TC008_delete_image_by_id_with_secure_ownership_verification()