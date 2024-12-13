from flask import Flask, render_template, request, jsonify, redirect
import requests

app = Flask(__name__)

# Backend API URL
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


@app.route("/download_csv", methods=["GET"])
def download_csv():
    """Proxy the file download from the backend."""
    file_path = request.args.get("path")
    if not file_path:
        return jsonify({"error": "File path is required"}), 400

    backend_response = requests.get(
        f"{BACKEND_API_URL}/download_csv?path={file_path}", stream=True
    )

    if backend_response.status_code == 200:
        return (
            backend_response.content,
            backend_response.status_code,
            backend_response.headers.items(),
        )
    else:
        return jsonify({"error": backend_response.text}), backend_response.status_code


@app.route("/usage_stats", methods=["GET"])
def usage_stats():
    """Query the backend API for usage statistics."""
    api_key = request.args.get("api_key")  # Use query parameters for API key

    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    # Make a GET request to the backend API
    response = requests.get(f"{BACKEND_API_URL}/usage_stats?api_key={api_key}")

    # Check if the backend responded with a valid JSON
    try:
        return jsonify(response.json())
    except requests.exceptions.JSONDecodeError:
        return jsonify({"error": "Backend did not return a valid JSON response"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
