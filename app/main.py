import time

from schemas import AdPayload, Creative
from rules import validate_music_rules
from tiktok_api import validate_music_id, submit_ad
from oauth import get_access_token
from errors import ERROR_MESSAGES


def main():
    print("\n🎯 TikTok Ad Creation Agent\n")
    print("Let's create your TikTok ad step by step.\n")

    # -----------------------------
    # Conversation State
    # -----------------------------
    state = {
        "campaign_name": None,
        "objective": None,
        "ad_text": None,
        "cta": None,
        "music_id": None
    }

    # -----------------------------
    # Campaign Name
    # -----------------------------
    while not state["campaign_name"]:
        name = input("Enter campaign name (min 3 characters): ").strip()
        if len(name) < 3:
            print("❌ Campaign name must be at least 3 characters.\n")
        else:
            state["campaign_name"] = name

    # -----------------------------
    # Objective
    # -----------------------------
    while not state["objective"]:
        obj = input("Choose objective (Traffic / Conversions): ").strip().lower()

        if obj == "traffic":
            state["objective"] = "Traffic"
        elif obj == "conversions":
            state["objective"] = "Conversions"
        else:
            print("❌ Objective must be Traffic or Conversions.\n")


    # -----------------------------
    # Ad Text
    # -----------------------------
    while not state["ad_text"]:
        text = input("Enter ad text (max 100 characters): ").strip()
        if not text:
            print("❌ Ad text is required.\n")
        elif len(text) > 100:
            print("❌ Ad text exceeds 100 characters.\n")
        else:
            state["ad_text"] = text

    # -----------------------------
    # CTA
    # -----------------------------
    while not state["cta"]:
        cta = input("Enter CTA (e.g. Shop Now, Learn More): ").strip()
        if not cta:
            print("❌ CTA is required.\n")
        else:
            state["cta"] = cta

    # -----------------------------
    # Music Logic (Case A / B / C)
    # -----------------------------
    while True:
        choice = input(
            "\nMusic options:\n"
            "1. Use existing music ID\n"
            "2. Upload custom music\n"
            "3. No music\n"
            "Choose 1 / 2 / 3: "
        ).strip()

        # Case A: Existing Music ID
        if choice == "1":
            music_id = input("Enter music ID: ").strip()
            result = validate_music_id(music_id)

            if not result["valid"]:
                print(f"❌ {result['error']}\n")
                continue

            state["music_id"] = music_id
            break

        # Case B: Custom Music Upload
        elif choice == "2":
            state["music_id"] = "custom_uploaded_music_id"
            print("✅ Custom music uploaded successfully.")
            break

        # Case C: No Music
        elif choice == "3":
            rule_check = validate_music_rules(
                state["objective"],
                None
            )

            if not rule_check["valid"]:
                print(f"❌ {rule_check['reason']}\n")
                continue

            state["music_id"] = None
            break

        else:
            print("❌ Invalid choice.\n")

    # -----------------------------
    # Build Final Payload
    # -----------------------------
    payload = AdPayload(
        campaign_name=state["campaign_name"],
        objective=state["objective"],
        creative=Creative(
            text=state["ad_text"],
            cta=state["cta"],
            music_id=state["music_id"]
        )
    )

    print("\n✅ Ad payload created successfully:\n")
    print(payload.model_dump_json(indent=2))

    # -----------------------------
    # OAuth Authentication
    # -----------------------------
    print("\n🔐 Authenticating with TikTok Ads...")

    auth_code = input(
        "Enter OAuth auth code "
        "(try: valid | invalid_client | no_scope | geo_blocked): "
    ).strip()

    auth_result = get_access_token(auth_code)

    if "error" in auth_result:
        print(f"❌ OAuth failed: {ERROR_MESSAGES[auth_result['error']]}")
        return

    access_token = auth_result["access_token"]
    expires_at = auth_result["expires_at"]

    # -----------------------------
    # Submission
    # -----------------------------
    print("\n📤 Submitting ad to TikTok Ads API...")

    # Simulate token expiration
    if time.time() > expires_at:
        access_token = "expired"

    result = submit_ad(payload.model_dump(), access_token)

    if "error" in result:
        print(f"❌ Submission failed: {ERROR_MESSAGES[result['error']]}")

        if result["error"] == "TOKEN_EXPIRED":
            print("🔁 Retry possible after re-authentication.")
        else:
            print("🚫 Fix the issue before retrying.")

        return

    # -----------------------------
    # Success
    # -----------------------------
    print("\n🎉 Ad submitted successfully!")
    print(f"Ad ID: {result['ad_id']}")


if __name__ == "__main__":
    main()
