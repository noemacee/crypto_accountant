import requests
import os
from dotenv import load_dotenv
import json
import argparse
import pandas as pd
from src.config import *
from src.helpers import fetch_all_pages, save_to_csv, process_transactions


# Main function
def main(wallet_address: str):
    """Main execution function."""
    # File paths and wallet address
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    print("Project ID:", project_id)

    output_csv_path = "./" + wallet_address + "_wallet_transactions.csv"

    print("Fetching all token transfers...")

    json_data = fetch_all_pages(
        project_id=project_id,
        wallet_address=wallet_address,
        page_size=PAGE_SIZE,
    )

    if not json_data:
        print("No data to process. Exiting.")
        return

    print("Processing transactions...")
    df = process_transactions(
        project_id=project_id, json_data=json_data, wallet_address=wallet_address
    )
    print("Processing complete.")

    print("Saving to CSV...")
    save_to_csv(df, output_csv_path)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Address Converter for RPC")
    parser.add_argument(
        "wallet_address", type=str, help="The wallet address to be converted"
    )

    # Parse arguments from the command line
    args = parser.parse_args()

    # Execute main with the parsed arguments
    main(args.wallet_address)
