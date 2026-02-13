
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** backend
- **Date:** 2026-02-13
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001 user registration with email validation and jwt token return
- **Test Code:** [TC001_user_registration_with_email_validation_and_jwt_token_return.py](./TC001_user_registration_with_email_validation_and_jwt_token_return.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/90f5c340-8aea-410e-812e-673fc38e8693
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002 user login with remember me feature and jwt token in cookie
- **Test Code:** [TC002_user_login_with_remember_me_feature_and_jwt_token_in_cookie.py](./TC002_user_login_with_remember_me_feature_and_jwt_token_in_cookie.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/595ab6f0-81e7-4a4c-940f-69cc5c561ab6
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003 user logout clears authentication cookie
- **Test Code:** [TC003_user_logout_clears_authentication_cookie.py](./TC003_user_logout_clears_authentication_cookie.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/ab05133a-44df-4d2f-9fd1-33a2777ba4b0
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004 authenticated user profile retrieval
- **Test Code:** [TC004_authenticated_user_profile_retrieval.py](./TC004_authenticated_user_profile_retrieval.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/ef091237-f1d1-44a7-bb4b-3b9ad7745a46
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005 image upload to s3 compatible storage with uuid path
- **Test Code:** [TC005_image_upload_to_s3_compatible_storage_with_uuid_path.py](./TC005_image_upload_to_s3_compatible_storage_with_uuid_path.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/5d45dfd4-b4aa-4c39-8c0e-71f8c6a4be0f
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006 request asynchronous image transformation via kafka
- **Test Code:** [TC006_request_asynchronous_image_transformation_via_kafka.py](./TC006_request_asynchronous_image_transformation_via_kafka.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/eb1b2fd9-2719-4bfe-b2f1-7d9038d7ebad
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007 get image details by id with access control
- **Test Code:** [TC007_get_image_details_by_id_with_access_control.py](./TC007_get_image_details_by_id_with_access_control.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/urllib3/connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/var/task/urllib3/connectionpool.py", line 534, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "/var/task/urllib3/connection.py", line 565, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "/var/lang/lib/python3.12/http/client.py", line 1430, in getresponse
    response.begin()
  File "/var/lang/lib/python3.12/http/client.py", line 331, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "/var/lang/lib/python3.12/http/client.py", line 292, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/lang/lib/python3.12/socket.py", line 720, in readinto
    return self._sock.recv_into(b)
           ^^^^^^^^^^^^^^^^^^^^^^^
ConnectionResetError: [Errno 104] Connection reset by peer

The above exception was the direct cause of the following exception:

urllib3.exceptions.ProxyError: ('Unable to connect to proxy', ConnectionResetError(104, 'Connection reset by peer'))

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/var/task/requests/adapters.py", line 667, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/var/task/urllib3/connectionpool.py", line 841, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/var/task/urllib3/util/retry.py", line 519, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='tun.testsprite.com', port=8080): Max retries exceeded with url: http://localhost:8000/register (Caused by ProxyError('Unable to connect to proxy', ConnectionResetError(104, 'Connection reset by peer')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 117, in <module>
  File "<string>", line 61, in test_TC007_get_image_details_by_id_with_access_control
  File "<string>", line 23, in register_user
  File "/var/task/requests/api.py", line 115, in post
    return request("post", url, data=data, json=json, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/task/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/task/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/task/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/task/requests/adapters.py", line 694, in send
    raise ProxyError(e, request=request)
requests.exceptions.ProxyError: HTTPConnectionPool(host='tun.testsprite.com', port=8080): Max retries exceeded with url: http://localhost:8000/register (Caused by ProxyError('Unable to connect to proxy', ConnectionResetError(104, 'Connection reset by peer')))

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/69e2e183-bc4f-445f-bd18-112f9815aa13
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008 delete image by id with secure ownership verification
- **Test Code:** [TC008_delete_image_by_id_with_secure_ownership_verification.py](./TC008_delete_image_by_id_with_secure_ownership_verification.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/e033221d-4754-43c9-9221-ccf7efb399bf/6f6bf1e4-a046-4bc0-9809-9256ed4f1fde
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **87.50** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---