def validate_music_rules(objective: str, music_id: str | None):
    """
    Enforce TikTok music rules BEFORE submission
    """
    if objective == "Conversions" and music_id is None:
        return {
            "valid": False,
            "reason": "Music is required for Conversion campaigns."
        }

    return {"valid": True}
