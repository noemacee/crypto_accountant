from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from src.config import WALLET_ADDRESSES, PAGE_SIZE
from src.helpers import fetch_all_pages, save_to_csv, process_transactions

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()


@app.route("/process_wallet", methods=["POST"])
def process_wallet():
    """API endpoint to process a wallet."""
    data = request.json
    wallet_address = data.get("wallet_address")
    if not wallet_address:
        return jsonify({"error": "Wallet address is required"}), 400

    project_id = os.getenv("PROJECT_ID")
    if not project_id:
        return jsonify({"error": "PROJECT_ID is not set in the environment"}), 500

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
            jsonify({"message": f"No data to process for wallet: {wallet_address}"}),
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


# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
