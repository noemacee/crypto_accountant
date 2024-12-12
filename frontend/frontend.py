from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Backend API URL (replace with actual URL if hosted on another server)
BACKEND_API_URL = "http://127.0.0.1:5000"


@app.route("/")
def index():
    """Render the main page."""
    return render_template("./index.html")


@app.route("/process_wallet", methods=["POST"])
def process_wallet():
    """Query the backend API to process a wallet."""
    wallet_address = request.form.get("wallet_address")
    if not wallet_address:
        return jsonify({"error": "Wallet address is required"}), 400

    # Make a POST request to the backend API
    response = requests.post(
        f"{BACKEND_API_URL}/process_wallet", json={"wallet_address": wallet_address}
    )

    # Pass the backend's response to the frontend
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(debug=True, port=3000)
