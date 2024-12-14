from helpers import fetch_all_pages, process_transactions, save_to_csv
from services.db import execute_query
import os

PROJECT_ID = os.getenv("PROJECT_ID")
PAGE_SIZE = int(os.getenv("PAGE_SIZE", 100))  # Default to 100 if PAGE_SIZE is not set
OUTPUT_DIR = "./output"


def process_wallet_transactions(wallet_address):
    """
    Fetch and process wallet transactions.
    :param wallet_address: Wallet address to process.
    :return: Path to the saved CSV file.
    """
    if not PROJECT_ID:
        raise RuntimeError("PROJECT_ID is not set in the environment.")

    # Define output file path
    output_csv_path = os.path.join(OUTPUT_DIR, f"{wallet_address}_transactions.csv")

    # Fetch token transfers
    json_data = fetch_all_pages(
        project_id=PROJECT_ID,
        wallet_address=wallet_address,
        page_size=PAGE_SIZE,
    )
    if not json_data:
        raise ValueError(f"No data found for wallet: {wallet_address}")

    # Process transactions and save to CSV
    df = process_transactions(PROJECT_ID, json_data, wallet_address)
    save_to_csv(df, output_csv_path)

    return output_csv_path


def log_wallet_processing(wallet_address, api_key):
    """
    Log wallet processing activity to the database.
    :param wallet_address: Processed wallet address.
    :param api_key: API key used for processing.
    """
    execute_query(
        "INSERT INTO api_usage (api_key, endpoint) VALUES (%s, %s)",
        params=(api_key, f"/process_wallet for {wallet_address}"),
    )
