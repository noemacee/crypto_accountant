from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Backend API URL (replace with actual backend service name or IP)
BACKEND_API_URL = "http://backend:5000"  # Backend Docker service


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/process_wallet", methods=["POST"])
def process_wallet():
    """Query the backend API to process a wallet."""
    wallet_address = request.form.get("wallet_address")
    api_key = request.form.get("api_key")

    if not wallet_address or not api_key:
        return jsonify({"error": "Wallet address and API key are required"}), 400

    # Make a POST request to the backend API
    response = requests.post(
        f"{BACKEND_API_URL}/process_wallet",
        headers={"X-API-Key": api_key},  # Include API key in headers
        json={"wallet_address": wallet_address},
    )

    # Pass the backend's response to the frontend
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
