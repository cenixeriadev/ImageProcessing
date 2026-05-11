import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_TC006_request_async_image_transformation_via_kafka():
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "TestPass123!"
    email = f"{username}@example.com"

    # Register user
    register_resp = requests.post(
        f"{BASE_URL}/register",
        json={"username": username, "password": password, "email": email},
        timeout=TIMEOUT,
    )
    assert register_resp.status_code == 200, f"Registration failed: {register_resp.text}"
    token = register_resp.json().get("access_token")
    assert token and register_resp.json().get("token_type") == "bearer"

    headers = {"Authorization": f"Bearer {token}"}

    # Upload an image to have image_id for the transform request
    image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01" \
                    b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00" \
                    b"\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01" \
                    b"\xe2!\xbc33\x00\x00\x00\x00IEND\xaeB`\x82"
    files = {"file": ("test.png", image_content, "image/png")}
    upload_resp = requests.post(
        f"{BASE_URL}/images",
        headers=headers,
        files=files,
        timeout=TIMEOUT,
    )
    assert upload_resp.status_code == 200, f"Image upload failed: {upload_resp.text}"
    image_id = upload_resp.json().get("id")
    assert image_id and isinstance(image_id, str)

    try:
        # 1. Request transformation on valid image_id as authenticated user
        transformations = {"resize": {"width": 100, "height": 100}}
        transform_resp = requests.post(
            f"{BASE_URL}/images/{image_id}/transform",
            headers=headers,
            json={"transformations": transformations},
            timeout=TIMEOUT,
        )
        assert transform_resp.status_code == 200, f"Transform request failed: {transform_resp.text}"
        assert "message" in transform_resp.json()
        assert "background" in transform_resp.json()["message"].lower()

        # 2. Request transformation with invalid image_id should return 404
        invalid_image_id = str(uuid.uuid4())
        invalid_resp = requests.post(
            f"{BASE_URL}/images/{invalid_image_id}/transform",
            headers=headers,
            json={"transformations": transformations},
            timeout=TIMEOUT,
        )
        assert invalid_resp.status_code == 404

        # 3. Request transformation unauthorized (no token)
        unauthorized_resp = requests.post(
            f"{BASE_URL}/images/{image_id}/transform",
            json={"transformations": transformations},
            timeout=TIMEOUT,
        )
        assert unauthorized_resp.status_code == 401 or unauthorized_resp.status_code == 403

        # 4. Register another user and verify cannot request transform on first user's image
        username2 = f"user_{uuid.uuid4().hex[:8]}"
        email2 = f"{username2}@example.com"
        password2 = "AnotherPass123!"

        register_resp2 = requests.post(
            f"{BASE_URL}/register",
            json={"username": username2, "password": password2, "email": email2},
            timeout=TIMEOUT,
        )
        assert register_resp2.status_code == 200, f"Second user registration failed: {register_resp2.text}"
        token2 = register_resp2.json().get("access_token")
        assert token2 and register_resp2.json().get("token_type") == "bearer"
        headers2 = {"Authorization": f"Bearer {token2}"}

        forbidden_resp = requests.post(
            f"{BASE_URL}/images/{image_id}/transform",
            headers=headers2,
            json={"transformations": transformations},
            timeout=TIMEOUT,
        )
        # Expect 404 since user2 does not own the image and cannot transform it
        assert forbidden_resp.status_code == 404

    finally:
        # Clean up: delete the uploaded image using first user's token
        del_resp = requests.delete(
            f"{BASE_URL}/images/{image_id}",
            headers=headers,
            timeout=TIMEOUT,
        )
        # If 200 or 404 (already deleted), we consider cleanup succeeded
        assert del_resp.status_code in (200, 404)

test_TC006_request_async_image_transformation_via_kafka()