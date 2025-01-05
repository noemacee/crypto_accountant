from flask import Blueprint, request, jsonify, send_file
import os
import logging
from services.helpers import fetch_all_pages, save_to_csv, process_transactions
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
    """Processes wallet transactions based on blockchain and wallet address."""
    logger.info("Processing wallet transactions at /wallet/process_wallet")

    # Validate API key
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        logger.warning("API key missing in request headers.")
        return jsonify({"error": "API key is required"}), 400

    # Parse JSON body
    try:
        data = request.json
    except Exception as e:
        logger.error("Invalid JSON body: %s", str(e))
        return jsonify({"error": "Invalid JSON body"}), 400

    wallet_address = data.get("wallet_address")
    blockchain = data.get("blockchain")

    if not wallet_address:
        logger.warning("Missing wallet address in request.")
        return jsonify({"error": "Wallet address is required"}), 400

    if not blockchain:
        logger.warning("Missing blockchain in request.")
        return jsonify({"error": "Blockchain is required"}), 400

    try:
        # Define output file path
        output_csv_path = os.path.join(
            OUTPUT_DIR, f"{wallet_address}_{blockchain}_transactions.csv"
        )
        logger.debug("Output CSV path: %s", output_csv_path)

        # Fetch blockchain-specific transactions
        logger.info(
            "Fetching transactions for blockchain: %s, wallet: %s",
            blockchain,
            wallet_address,
        )

        # Example of blockchain-specific handling (e.g., StarkNet)
        if blockchain == "starknet":
            json_data = fetch_all_pages(PROJECT_ID, wallet_address)
        else:
            logger.warning("Unsupported blockchain: %s", blockchain)
            return jsonify({"error": f"Unsupported blockchain: {blockchain}"}), 400

        # If no data is found
        if not json_data:
            logger.warning(
                "No data found for wallet: %s on blockchain: %s",
                wallet_address,
                blockchain,
            )
            return (
                jsonify(
                    {
                        "message": f"No data found for wallet: {wallet_address} on blockchain: {blockchain}"
                    }
                ),
                404,
            )

        # Process transactions and save to CSV
        logger.info("Processing transactions for wallet: %s", wallet_address)
        df = process_transactions(PROJECT_ID, json_data, wallet_address)
        save_to_csv(df, output_csv_path)

        # Update API usage metrics
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
        return jsonify({"error": f"Error processing wallet: {str(e)}"}), 500


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
