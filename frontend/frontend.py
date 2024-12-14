import logging
from flask import Flask, render_template, request, jsonify, redirect, Response
import requests
import os

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to logging.INFO for less verbose output
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Backend API URL
BACKEND_API_URL = "http://backend:5000"  # Backend Docker service


@app.route("/")
def index():
    """Render the main page."""
    logger.info("Rendering the main page.")
    return render_template("index.html")


@app.route("/process_wallet", methods=["POST"])
def process_wallet():
    """Query the backend API to process a wallet."""
    wallet_address = request.json.get("wallet_address")
    api_key = request.headers.get("X-API-Key")

    if not wallet_address:
        return jsonify({"error": "Wallet address required"}), 400

    if not api_key:
        return jsonify({"error": "API key required"}), 400

    try:
        response = requests.post(
            f"{BACKEND_API_URL}/wallet/process_wallet",
            headers={"X-API-Key": api_key},
            json={"wallet_address": wallet_address},
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info("Wallet processed successfully.")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred while processing wallet: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/download_csv", methods=["GET"])
def download_csv():
    """Proxy the file download from the backend."""
    file_path = request.args.get("path")
    if not file_path:
        logger.warning("File path missing in download request.")
        return jsonify({"error": "File path is required"}), 400

    try:
        backend_response = requests.get(
            f"{BACKEND_API_URL}/wallet/download_csv?path={file_path}", stream=True
        )
        backend_response.raise_for_status()  # Raise an exception for HTTP errors

        logger.info("File downloaded successfully: %s", file_path)
        return Response(
            backend_response.content,
            status=backend_response.status_code,
            headers=dict(backend_response.headers),
        )
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred while downloading file: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    """Frontend route for login that talks to the backend."""
    if request.method == "POST":
        # Get username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Send login credentials to the backend
        try:
            response = requests.post(
                f"{BACKEND_API_URL}/login",
                json={"username": username, "password": password},
            )
            if response.status_code == 200:
                # Backend login successful, redirect to index
                return redirect(("/"))
            elif response.status_code == 401:
                # Invalid credentials
                return "Invalid credentials, please try again.", 401
            else:
                # Other backend errors
                return f"Error: {response.text}", response.status_code
        except Exception as e:
            return f"An error occurred while logging in: {str(e)}", 500

    # Render the login form for GET requests
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Render the registration form."""
    return render_template("register.html")


@app.route("/metrics", methods=["GET"])
def metrics():
    """Render the metrics page."""
    return render_template("metrics.html")


@app.route("/usage_stats", methods=["POST"])
def usage_stats():
    """Query the backend API for usage statistics."""
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        logger.warning("API key missing in usage stats request.")
        return jsonify({"error": "API key is required"}), 400

    try:
        logger.debug("Fetching usage stats for API key: %s", api_key)
        response = requests.get(
            f"{BACKEND_API_URL}/usage_stats/usage_stats",  # No query parameter
            headers={"X-API-Key": api_key},  # Pass API key as a header
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info("Usage stats fetched successfully.")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred while fetching usage stats: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/all_usage_stats", methods=["GET"])
def all_usage_stats():
    """Query the backend API for all usage statistics."""
    # Forward to the backend API
    try:
        response = requests.get(f"{BACKEND_API_URL}/usage_stats/all_usage_stats")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("Starting the Flask application.")
    app.run(debug=True, host="0.0.0.0", port=3000)
