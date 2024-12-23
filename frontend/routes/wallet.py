import logging
import os
import requests
from flask import Blueprint, request, jsonify, Response

wallet_routes = Blueprint("wallet_routes", __name__)
logger = logging.getLogger(__name__)

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend:5000")


@wallet_routes.route("/process_wallet", methods=["POST"])
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
        response.raise_for_status()
        logger.info("Wallet processed successfully.")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error while processing wallet: %s", str(e))
        return jsonify({"error": str(e)}), 500


@wallet_routes.route("/download_csv", methods=["GET"])
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
        backend_response.raise_for_status()
        logger.info("File downloaded successfully: %s", file_path)

        # Return streamed content with matching headers
        return Response(
            backend_response.content,
            status=backend_response.status_code,
            headers=dict(backend_response.headers),
        )
    except requests.exceptions.RequestException as e:
        logger.error("Error while downloading file: %s", str(e))
        return jsonify({"error": str(e)}), 500
