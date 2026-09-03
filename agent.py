import json
import os
import joblib

from google import genai

from tools import (
    retry_payment,
    generate_payment_link,
    send_notification,
    defer_recovery
)


# Load ML model and preprocessor
model = joblib.load("models/recovery_model.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")


def get_decision(probability, retry_count):

    if probability >= 75 and retry_count <= 1:
        return "Retry Payment"

    elif probability >= 75 and retry_count > 1:
        return "Generate Payment Link"

    elif probability >= 40:
        return "Send Notification"

    else:
        return "Defer Recovery"


def execute_action(action, transaction_id, amount):

    if action == "Retry Payment":
        return retry_payment(transaction_id, amount)

    elif action == "Generate Payment Link":
        return generate_payment_link(transaction_id, amount)

    elif action == "Send Notification":
        return send_notification(transaction_id, amount)

    else:
        return defer_recovery(transaction_id, amount)


def ask_recovery_agent(agent_context):

    probability = agent_context["recovery_probability"]
    recommended_action = agent_context["recommended_action"]

    prompt = f"""
You are an AI Revenue Recovery Agent.

Your job is to explain the recovery decision for a failed payment.

IMPORTANT:
- The ML model's recovery probability is authoritative.
- The recommended action is already determined by the decision engine.
- DO NOT change or contradict the recommended action.
- Use the exact probability provided below.

Transaction Information:
{json.dumps(agent_context, indent=2)}

Authoritative ML Prediction:
Recovery Probability: {probability}%

Authoritative Recommended Action:
{recommended_action}

Write a concise response in exactly this format:

Decision: {recommended_action}
Recovery Probability: {probability}%
Reason: <explain the decision using the transaction information>
Customer Message: <short customer-friendly message>

The customer message MUST match the selected action.
"""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text