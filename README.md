# TikTok Ads Creation – AI Agent

This repository contains a CLI-based AI-powered agent that guides a user through creating a TikTok Ad configuration via conversation.

The project focuses on **prompt design, API reasoning, guardrails, and failure handling**, rather than UI polish or model training, in line with the assignment requirements.

---

## Overview

The agent simulates a production-ready workflow for creating TikTok Ads by:

- Collecting ad inputs step-by-step via conversation
- Enforcing business rules deterministically
- Producing validated, structured ad payloads
- Attempting ad submission
- Interpreting and handling OAuth and API failures gracefully

TikTok Ads APIs and OAuth flows are **mocked intentionally** to emphasize reasoning, validation, and failure handling rather than external integration complexity.

---

## Architecture Principles

- **Deterministic control flow**: All validation and business rules are enforced in code
- **Guardrails over AI**: The LLM (Gemini) is optional and not trusted for correctness
- **Structured output**: Final ad configuration is validated using schemas
- **Failure-aware design**: API and OAuth errors are interpreted and explained clearly

---

## Project Structure

app/
├── main.py # CLI conversation flow and orchestration
├── schemas.py # Structured output using Pydantic
├── rules.py # Business rule enforcement (music logic)
├── oauth.py # Mocked OAuth Authorization Code flow
├── tiktok_api.py # Mocked TikTok Ads API
├── errors.py # Error interpretation and messaging
├── agent.py # Optional LLM integration (Gemini)


---

## Conversational Ad Creation

The agent guides the user through collecting the following required inputs:

| Field          | Rule                                   |
|---------------|-----------------------------------------|
| Campaign Name | Required, minimum 3 characters          |
| Objective     | Traffic or Conversions                  |
| Ad Text       | Required, maximum 100 characters        |
| CTA           | Required                                |
| Music         | Conditional logic enforced (see below)  |

Each input is validated immediately before moving to the next step.

---

## Music Logic (Primary Evaluation Area)

The system supports all required music scenarios:

### Case A: Existing Music ID
- User provides a Music ID
- ID is validated via mocked TikTok Ads API
- If rejected, the agent explains the failure and prompts next steps

### Case B: Custom / Uploaded Music
- User chooses to upload custom music
- Upload is simulated and a mock Music ID is generated
- Music is validated and rejection is handled gracefully

### Case C: No Music
- ✅ Allowed only when Objective = Traffic
- ❌ Blocked when Objective = Conversions
- Enforced **before submission**, not after API failure

---

## Structured Output

Once all inputs are valid, the agent produces a structured JSON payload:

```json
{
  "campaign_name": "example campaign",
  "objective": "Traffic",
  "creative": {
    "text": "Example ad text",
    "cta": "Shop Now",
    "music_id": null
  }
}

Schemas ensure correctness and prevent invalid submissions.

OAuth Handling (Mocked)

The project simulates a TikTok OAuth Authorization Code flow and handles:

Invalid client ID / secret

Missing Ads permission scope

Expired or revoked access token

Geo-restriction (403)

Instead of exposing raw errors, the agent:

Explains the issue in plain language

Suggests corrective actions

Distinguishes retryable vs non-retryable errors

Submission & Failure Handling

Ad submission is attempted via a mocked TikTok Ads API.

The agent handles:

Invalid OAuth tokens

Missing permissions

Invalid music IDs

Geo-restricted campaigns

For each failure, the agent:

Interprets the error

Explains it clearly to the user

Decides whether retry is possible or blocked

LLM Usage

The system optionally integrates Gemini for language generation

The LLM is not used for validation or business decisions

All rules and constraints are enforced deterministically in code

This ensures reliability and prevents hallucination-based failures.


How to Run
Install dependencies
pip install -r requirements.txt

Run the agent
python app/main.py

Notes

TikTok Ads API and OAuth flows are mocked to focus on reasoning and guardrails

No UI or frontend is included by design

The project prioritizes correctness, clarity, and failure handling over feature breadth

What Could Be Improved With More Time

Real TikTok Ads API integration

Token refresh automation

Persistent session storage

Richer conversational responses using the LLM

Web-based interface