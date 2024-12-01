import json
import pandas as pd
from config import *
from datetime import datetime
from typing import Dict, Optional
from blastapi.builder.functions import (
    getWalletTokenTransfers,
    getTransaction,
)


def save_to_json(data, filename):
    """
    Save json type data to a file.
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to '{filename}'")
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")


def save_to_csv(df, output_file):
    """Save processed records to a CSV file."""
    try:
        df.to_csv(output_file, index=False)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def fetch_all_pages(
    project_id, wallet_address, page_size=100, output_file="wallet_token_transfers.json"
):
    """
    Fetch all wallet token transfers by handling pagination.
    Combines all results into a single JSON file and avoids redundancy.
    """
    all_transfers = []
    page_key = None

    while True:
        # Fetch a single page
        data = getWalletTokenTransfers(project_id, wallet_address, page_size, page_key)

        if not data:
            print("Failed to fetch data. Exiting...")
            break

        # Extract token transfers and append them to the list
        token_transfers = data.get("tokenTransfers", [])
        all_transfers.extend(token_transfers)

        # Check for the next page key
        page_key = data.get("nextPageKey")
        if not page_key:
            break

    return {"tokenTransfers": all_transfers}


def address_converter(address):
    """
    Convert the address to the format used by the RPC.

    The address always starts with 0x and is followed by 64 characters. If not,
    it is padded with zeros right after 0x. The address must also be in lowercase.
    """
    if not address.startswith("0x"):
        raise ValueError("Address must start with '0x'")

    # Strip "0x" and convert to lowercase
    address_body = address[2:].lower()

    # Pad the address to ensure it has 64 characters after "0x"
    padded_address = address_body.zfill(64)

    # Add "0x" prefix back
    return f"0x{padded_address}"


def process_transaction_call(transaction: Dict) -> Optional[str]:
    """
    Process transaction call data and return matching function name.

    Args:
        transaction (Dict): Transaction data containing calldata
        function_map (Dict[str, str]): Normalized function mapping

    Returns:
        Optional[str]: Matching function name or None
    """
    if not transaction or "calldata" not in transaction:
        print("Transaction or calldata missing.")
        return None

    # Normalize and check calldata against function map
    for call in transaction["calldata"]:
        normalized_call = address_converter(call)
        if normalized_call in call_func_addresses:
            return call_func_addresses[normalized_call]

    return None


def call_column(hash: str, project_id: str) -> Optional[str]:
    """
    Main function to process transaction hash and return function name.

    Args:
        hash (str): Transaction hash
        project_id (str): Project identifier

    Returns:
        Optional[str]: Matching function name or None
    """
    tx = getTransaction(project_id, hash)
    return process_transaction_call(tx)


def process_transactions(project_id, json_data, wallet_address):
    """Process transactions into the required structure."""

    token_transfers = json_data["tokenTransfers"]

    # Create a mapping of transaction hash to transaction number
    transaction_hash_mapping = {}
    current_transaction_number = 1

    # Assign transaction numbers in reverse order
    for tx in reversed(token_transfers):
        tx_hash = tx["transactionHash"]
        if tx_hash not in transaction_hash_mapping:
            transaction_hash_mapping[tx_hash] = current_transaction_number
            current_transaction_number += 1

    # Initialize the DataFrame
    df = pd.DataFrame(
        columns=[
            "Transaction #",
            "Datetime",
            "Amount In",
            "Amount Out",
            "Amount currency",
            "Description",
            "Counterparty address",
            "Counterparty name",
            "Transaction hash",
            "Blockchain",
            "Wallet",
            "transfer_from",
            "transfer_to",
            "transfer_amount",
            "token_address",
            "token_symbol",
            "token_name",
            "transfer_type",
            "call",
            "tx_hash",
            "block_number",
            "from_alias",
            "to_alias",
            "timestamp",
        ]
    )

    # Create records using the transaction hash mapping
    num_operations = len(token_transfers)

    for operation_idx, tx in enumerate(token_transfers, start=1):

        token_address = tx.get("contractAddress", "")
        # print the transaction number
        if (operation_idx % 10) == 0:
            print(f"Handling Operation #{operation_idx} out of {num_operations}")

        if all(
            token_address not in token_dict or token_dict[token_address] == ""
            for token_dict in [
                pool_tokens,
                debt_tokens,
                interest_bearing_and_collat_tokens,
            ]
        ):

            tx_hash = tx["transactionHash"]

            counterparty_address = (
                tx["toAddress"]
                if tx["fromAddress"] == wallet_address
                else tx["fromAddress"]
            )

            # Create a single-row DataFrame for the current operation
            record_df = pd.DataFrame(
                [
                    {
                        "Transaction #": transaction_hash_mapping[tx_hash],
                        "Datetime": datetime.fromisoformat(
                            tx["blockTimestamp"].replace("Z", "")
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                        "Amount In": (
                            f"{int(tx['value']) / (10 ** int(tx.get('contractDecimals', 18))):.10f}"
                            if tx["toAddress"] == wallet_address
                            else ""
                        ),
                        "Amount Out": (
                            f"{int(tx['value']) / (10 ** int(tx.get('contractDecimals', 18))):.10f}"
                            if tx["fromAddress"] == wallet_address
                            else ""
                        ),
                        "Amount currency": tx.get("contractSymbol", "UNKNOWN"),
                        "Description": (
                            "Transaction fee"
                            if tx.get("transfer_type", "") == "fee_transfer"
                            else "Transaction"
                        ),
                        "Counterparty address": counterparty_address,
                        "Counterparty name": (
                            protocol_addresses_map.get(counterparty_address)
                        ),
                        "Transaction hash": tx["transactionHash"],
                        "Blockchain": "Starknet",
                        "Wallet": wallet_address,
                        "transfer_from": tx["fromAddress"],
                        "transfer_to": tx["toAddress"],
                        "transfer_amount": f"{int(tx['value']) / (10 ** int(tx.get('contractDecimals', 18))):.10f}",
                        "token_address": tx.get("contractAddress", ""),
                        "token_symbol": tx.get("contractSymbol", "UNKNOWN"),
                        "token_name": tx.get("contractName", "UNKNOWN"),
                        "transfer_type": (
                            "fee_transfer"
                            if tx["toAddress"] == important_addresses["sequencer"]
                            else "execute"
                        ),
                        "call": (
                            "transfer"
                            if tx["toAddress"] == important_addresses["sequencer"]
                            else call_column(
                                tx["transactionHash"], project_id=project_id
                            )
                        ),
                        "tx_hash": tx["transactionHash"],
                        "block_number": tx["blockNumber"],
                        "from_alias": contract_addresses_map.get(
                            tx["fromAddress"]
                        ),  # Placeholder for alias mapping
                        "to_alias": contract_addresses_map.get(tx["toAddress"]),
                        "timestamp": tx["blockTimestamp"],
                    }
                ]
            )

            # Concatenate the single-row DataFrame to the main DataFrame
            df = pd.concat([df, record_df], ignore_index=True)
    return df
