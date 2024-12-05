from flask import Flask, request, jsonify
import logging
import os
import json
from sdk.utils.signature import verify_signature

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Environment variables
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "mySecret")


@app.route("/webhooks", methods=["POST"])
def handle_webhook():
    """
    Handle incoming webhook events.
    Validates the HMAC signature and processes the event.
    """
    # Raw request body and headers
    raw_body = request.data.decode("utf-8")
    auth_header = request.headers.get("Authorization", "").replace("Signature ", "")

    if not auth_header:
        logger.error("Missing Authorization header")
        return jsonify({"error": "Missing Authorization header"}), 400

    # Verify the webhook signature
    if not verify_signature(raw_body, auth_header, WEBHOOK_SECRET):
        logger.error("Invalid signature")
        return jsonify({"error": "Invalid signature"}), 401

    # Log and process the event payload
    logger.info(f"Valid webhook received: {raw_body}")
    event_data = json.loads(raw_body)

    print("Webhook Event:", event_data)

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3010)
