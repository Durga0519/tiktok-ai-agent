import time

def get_access_token(auth_code: str):
    """
    Mock TikTok OAuth Authorization Code flow
    """
    if auth_code == "invalid_client":
        return {"error": "INVALID_CLIENT"}

    if auth_code == "no_scope":
        return {"error": "MISSING_SCOPE"}

    if auth_code == "geo_blocked":
        return {"error": "GEO_403"}

    return {
        "access_token": "mock_access_token",
        "expires_at": time.time() + 5  # short expiry for testing
    }
