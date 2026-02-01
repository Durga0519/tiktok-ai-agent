def validate_music_id(music_id: str):
    """
    Mock TikTok Ads API music validation
    """
    if music_id.startswith("bad"):
        return {
            "valid": False,
            "error": "Music ID rejected due to copyright violation."
        }

    return {"valid": True}


def submit_ad(payload: dict, token: str):
    """
    Mock TikTok Ads submission
    """
    if token == "expired":
        return {"error": "TOKEN_EXPIRED"}

    if payload["creative"]["music_id"] == "invalid":
        return {"error": "INVALID_MUSIC"}

    if payload["campaign_name"].lower().startswith("geo"):
        return {"error": "GEO_403"}

    return {
        "success": True,
        "ad_id": "mock_ad_123"
    }
