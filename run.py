import requests
import os
from dotenv import load_dotenv
import pandas as pd
from src.config import WALLET_ADDRESSES, PAGE_SIZE
from src.helpers import fetch_all_pages, save_to_csv, process_transactions


# Main function
def main():
    """Main execution function."""
    # Load environment variables
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    print("Project ID:", project_id)

    if not WALLET_ADDRESSES:
        print("No wallet addresses found in config.py. Exiting.")
        return

    for wallet_address in WALLET_ADDRESSES:
        print(f"Processing wallet: {wallet_address}")
        output_csv_path = f"./{wallet_address}_wallet_transactions.csv"

        print("Fetching all token transfers...")
        json_data = fetch_all_pages(
            project_id=project_id,
            wallet_address=wallet_address,
            page_size=PAGE_SIZE,
        )

        if not json_data:
            print(f"No data to process for wallet: {wallet_address}. Skipping.")
            continue

        print("Processing transactions...")
        df = process_transactions(
            project_id=project_id, json_data=json_data, wallet_address=wallet_address
        )
        print("Processing complete.")

        print("Saving to CSV...")
        save_to_csv(df, output_csv_path)

    print("All wallets processed.")


if __name__ == "__main__":
    main()
