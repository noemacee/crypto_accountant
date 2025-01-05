import logging
import os
import requests
from flask import Blueprint, request, jsonify, Response, session


wallet_routes = Blueprint("wallet_routes", __name__)
logger = logging.getLogger(__name__)

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend:5000")


@wallet_routes.route("/process_wallet", methods=["POST"])
def process_wallet():
    """Query the backend API to process a wallet."""
    logger.info("Received request to proxy /process_wallet to backend")

    # Get wallet_address and blockchain from the request
    data = request.json
    wallet_address = data.get("wallet_address")
    blockchain = data.get("blockchain")
    api_key = session.get("api_key")

    if not wallet_address:
        logger.warning("Missing wallet address in the request.")
        return jsonify({"error": "Wallet address is required"}), 400

    if not blockchain:
        logger.warning("Missing blockchain in the request.")
        return jsonify({"error": "Blockchain is required"}), 400

    if not api_key:
        logger.warning("Missing API key in the request headers.")
        return jsonify({"error": "API key is required"}), 400

    try:
        # Forward the request to the backend
        response = requests.post(
            f"{BACKEND_API_URL}/wallet/process_wallet",
            headers={"X-API-Key": api_key},
            json={"wallet_address": wallet_address, "blockchain": blockchain},
        )
        response.raise_for_status()
        logger.info("Request to backend /wallet/process_wallet was successful.")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error while forwarding request to backend: %s", str(e))
        return jsonify({"error": "Error processing wallet request"}), 500


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
