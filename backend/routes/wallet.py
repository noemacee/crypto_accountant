from flask import Blueprint, request, jsonify, send_file
import os
import logging
from helpers import fetch_all_pages, save_to_csv, process_transactions
from config import PAGE_SIZE
from services.db import execute_query

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Change to logging.INFO for less verbose output
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Blueprint for wallet routes
wallet_routes = Blueprint("wallet_routes", __name__)

# Load environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")


@wallet_routes.route("/process_wallet", methods=["POST"])
def process_wallet():
    """Processes a wallet's transactions."""
    logger.info("Received request to /wallet/process_wallet")

    # Validate API key
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        logger.warning("Missing API Key in the request headers.")
        return jsonify({"error": "API key is required"}), 400

    # Retrieve wallet address from request
    try:
        data = request.json
    except Exception as e:
        logger.error("Error parsing JSON request body: %s", str(e))
        return jsonify({"error": "Invalid JSON body"}), 400

    wallet_address = data.get("wallet_address")
    if not wallet_address:
        logger.warning("Missing wallet address in request data: %s", data)
        return jsonify({"error": "Wallet address is required"}), 400

    if not PROJECT_ID:
        logger.error("PROJECT_ID environment variable is not set.")
        return jsonify({"error": "PROJECT_ID is not set in the environment"}), 500

    try:
        # Define output file path
        output_csv_path = os.path.join(OUTPUT_DIR, f"{wallet_address}_transactions.csv")
        logger.debug("Output CSV path: %s", output_csv_path)

        # Fetch token transfers
        logger.info("Fetching token transfers for wallet: %s", wallet_address)
        json_data = fetch_all_pages(
            project_id=PROJECT_ID,
            wallet_address=wallet_address,
            page_size=PAGE_SIZE,
        )
        if not json_data:
            logger.warning("No data found for wallet: %s", wallet_address)
            return (
                jsonify({"message": f"No data found for wallet: {wallet_address}"}),
                404,
            )

        # Process transactions and save to CSV
        logger.info("Processing transactions for wallet: %s", wallet_address)
        df = process_transactions(PROJECT_ID, json_data, wallet_address)
        save_to_csv(df, output_csv_path)

        logger.info("Updating API usage metrics for API key: %s", api_key)
        execute_query(
            """
            INSERT INTO api_usage (api_key, endpoint, timestamp)
            VALUES (%s, %s, NOW())
            """,
            params=(api_key, "/wallet/process_wallet"),
        )

        logger.info("Processing complete. CSV saved at: %s", output_csv_path)
        return (
            jsonify({"message": "Processing complete", "csv_path": output_csv_path}),
            200,
        )
    except Exception as e:
        logger.error("Error processing wallet: %s", str(e))
        return jsonify({"error": str(e)}), 500


@wallet_routes.route("/download_csv", methods=["GET"])
def download_csv():
    """Download a CSV file containing processed wallet data."""
    file_path = request.args.get("path")
    if not file_path:
        logger.warning("File path is missing in the request.")
        return jsonify({"error": "File path is required"}), 400

    logger.debug("Full file path for download: %s", file_path)

    if not os.path.exists(file_path):
        logger.warning("File not found: %s", file_path)
        return jsonify({"error": "File not found"}), 404

    logger.info("File found. Preparing to send: %s", file_path)
    return send_file(file_path, as_attachment=True, mimetype="text/csv")
