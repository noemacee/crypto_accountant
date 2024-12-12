from flask import Flask, jsonify, request, send_file
import os
from dotenv import load_dotenv
import psycopg2
import sys
import os

from src.config import WALLET_ADDRESSES, PAGE_SIZE
from src.helpers import fetch_all_pages, save_to_csv, process_transactions


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@db:5432/accounter_db"
)

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()


@app.route("/process_wallet", methods=["POST"])
def process_wallet():
    """API endpoint to process a wallet."""
    # Get API key from headers
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    # Validate API key and log usage
    valid, error_response, status_code = validate_and_log(api_key, "/process_wallet")
    if not valid:
        return jsonify(error_response), status_code

    # Process the wallet (existing logic)
    data = request.json
    wallet_address = data.get("wallet_address")
    if not wallet_address:
        return jsonify({"error": "Wallet address is required"}), 400

    project_id = os.getenv("PROJECT_ID")
    if not project_id:
        return jsonify({"error": "PROJECT_ID is not set in the environment"}), 500

    try:
        print(f"Processing wallet: {wallet_address}")
        output_csv_path = f"./{wallet_address}_wallet_transactions.csv"

        print("Fetching all token transfers...")
        json_data = fetch_all_pages(
            project_id=project_id,
            wallet_address=wallet_address,
            page_size=PAGE_SIZE,
        )

        if not json_data:
            return (
                jsonify(
                    {"message": f"No data to process for wallet: {wallet_address}"}
                ),
                404,
            )

        print("Processing transactions...")
        df = process_transactions(
            project_id=project_id, json_data=json_data, wallet_address=wallet_address
        )
        print("Processing complete.")

        print("Saving to CSV...")
        save_to_csv(df, output_csv_path)

        return jsonify({"message": "Processing complete", "csv_path": output_csv_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download_json")
def download_json():
    """Serve the JSON file as a downloadable link."""
    file_path = request.args.get("path")
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True, mimetype="application/json")


# Establish a connection to the database
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


# API to generate and store a new API key
@app.route("/generate_api_key", methods=["POST"])
def generate_api_key():
    owner = request.json.get("owner")
    if not owner:
        return jsonify({"error": "Owner is required"}), 400

    api_key = os.urandom(16).hex()  # Generate a 32-character random API key

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO api_keys (api_key, owner) VALUES (%s, %s) RETURNING api_key",
            (api_key, owner),
        )
        conn.commit()
        new_key = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"api_key": new_key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to log API usage
@app.route("/log_usage", methods=["POST"])
def log_usage():
    data = request.json
    api_key = data.get("api_key")
    endpoint = data.get("endpoint")

    if not api_key or not endpoint:
        return jsonify({"error": "API key and endpoint are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO api_usage (api_key, endpoint) VALUES (%s, %s)",
            (api_key, endpoint),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Usage logged successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to retrieve API usage stats
@app.route("/usage_stats", methods=["GET"])
def usage_stats():
    api_key = request.args.get("api_key")
    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT endpoint, COUNT(*) FROM api_usage WHERE api_key = %s GROUP BY endpoint",
            (api_key,),
        )
        stats = cursor.fetchall()
        cursor.close()
        conn.close()
        return (
            jsonify(
                {"usage": [{"endpoint": row[0], "count": row[1]} for row in stats]}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def validate_and_log(api_key, endpoint):
    """Validate the API key and log the API call."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the API key exists in the database
        cursor.execute("SELECT COUNT(*) FROM api_keys WHERE api_key = %s", (api_key,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            conn.close()
            return False, {"error": "Invalid API key"}, 401

        # Log the API usage
        cursor.execute(
            "INSERT INTO api_usage (api_key, endpoint) VALUES (%s, %s)",
            (api_key, endpoint),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, None, None
    except Exception as e:
        return False, {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
