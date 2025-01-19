import json
import pandas as pd
from datetime import datetime
from typing import Dict, Optional
from tqdm import tqdm
import pandas as pd
from datetime import datetime
from blastapi.builder.functions import (
    getWalletTokenTransfers,
    getTransaction,
)
import requests
from config import *


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


def fetch_all_pages(project_id, wallet_address, page_size=100):
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

def alchemy_getClassHashAt(network_url, block_number, contract_hash):
    url = network_url
    headers = {"accept": "application/json", "content-type": "application/json"}
    data = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "starknet_getClassHashAt",
        "params": [
            block_number,  # First parameter: block number
            contract_hash,  # Second parameter: contract hash
        ],
    }

    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(data)
        )  # Send the POST request
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Parse and return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def descriptionv3(tx, wallet_address, counterparty_address, amount_in, amount_out):
    description = "No description found"
    # Condition 1 : Transfer fee
    if counterparty_address == important_addresses["sequencer"]:
        description = "Transaction Fee"

    # Condition 2 : DeFi Interest
    class_hash_method = False
    network_url = "https://starknet-mainnet.g.alchemy.com/starknet/version/rpc/v0_7/up4Ow19ZZxwdQ6M11l9e8KBo8BdNAo_u"
    block_number = "latest"
    mother_classes = [
        "0x6a54af2934978ac59b27b91291d3da634f161fd5f22a2993da425893c44c64",
        #"0x18758d409574a66615683bf529b5ff4f5c84b09fcfea48102fa3153039ebc10", # Taken out after mistakenly labeling an "address of the Starknet Foundation which is used to payout grants" : “0x025c3ebe94f55ea8eb289cb34844f2630551bd198d9915c91dcd661a90a1dc1e”
        # Careful with 0-padding. Check function converter_address  
    ]
    response = alchemy_getClassHashAt(network_url, block_number, counterparty_address)
    if response and "result" in response and response["result"] in mother_classes:
        class_hash_method = True
    if class_hash_method:
        description = "DeFi Interest"

    # Condition 3 : DeFi Deposit
    if (
        not class_hash_method
        and amount_in is None
        and (
            counterparty_address in address_to_protocol
            or counterparty_address in address_to_pool
        )
    ):
        description = "DeFi Deposit"

    # Condition 4 : DeFi Withdrawal
    if (
        not class_hash_method
        and amount_out is None
        and (
            counterparty_address in address_to_protocol
            or counterparty_address in address_to_pool
        )
    ):
        description = "DeFi Withdrawal"

    # Condition 5 : Exchange
    if not class_hash_method and counterparty_address in addresses2exchanges_map:
        description = "Exchange"

    # Condition 6 : Transfer
    if (
        not class_hash_method
        and counterparty_address not in addresses2exchanges_map
        and counterparty_address not in address_to_protocol
        and description == "No description found"
    ):
        description = "Transfer"

    return description


def fill_datetime(tx):
    return datetime.fromisoformat(tx["blockTimestamp"].replace("Z", "")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def fill_counterparty_address(wallet_address, tx):
    address = address_converter(wallet_address)
    if address_converter(tx["fromAddress"]) == address:
        address = tx["toAddress"]
    else:
        address = tx["fromAddress"]
    return address_converter(address)


def fill_counterparty_name(counterparty_address, tx):
    class_hash_method = False
    network_url = "https://starknet-mainnet.g.alchemy.com/starknet/version/rpc/v0_7/up4Ow19ZZxwdQ6M11l9e8KBo8BdNAo_u"
    block_number = "latest"
    mother_classes = [
        "0x6a54af2934978ac59b27b91291d3da634f161fd5f22a2993da425893c44c64",
        #"0x18758d409574a66615683bf529b5ff4f5c84b09fcfea48102fa3153039ebc10", # Taken out after mistakenly labeling an "address of the Starknet Foundation which is used to payout grants" : “0x025c3ebe94f55ea8eb289cb34844f2630551bd198d9915c91dcd661a90a1dc1e”
    ]
    response = alchemy_getClassHashAt(network_url, block_number, counterparty_address)
    if response and "result" in response and response["result"] in mother_classes:
        class_hash_method = True
    is_nostra = any(
        [
            counterparty_address in address_to_pool,  # Nostra Pool
            counterparty_address in address_to_debt_token,  # Nostra Debt
            counterparty_address in address_to_ibc_token,  # Nostra IBC (should delete as these are token addresses)
            class_hash_method,  # Check if contract is Nostra
        ]
    )
    if is_nostra:
        return "Nostra"
    #if counterparty_address in addresses_to_PKLabs: # Remove PK Labs for privacy
    #    return "PK Labs"
    if counterparty_address in addresses2exchanges_map:
        return addresses2exchanges_map.get(counterparty_address, "")
    if counterparty_address in addresses_to_Starknet:
        return addresses_to_Starknet.get(counterparty_address, "")
    if counterparty_address in addresses2CEXs_map:
        return addresses2CEXs_map.get(counterparty_address, "")    
    return address_to_protocol.get(
        counterparty_address, ""
    )  # Write "" if unknown address


def fill_amount_in(tx, wallet_address):
    if tx["toAddress"] == wallet_address:
        value = int(tx["value"])
        decimals = int(tx.get("contractDecimals", 18))
        return f"{value / (10 ** decimals):.10f}"
    return None


def fill_amount_out(tx, wallet_address):
    if tx["fromAddress"] == wallet_address:
        value = int(tx["value"])
        decimals = int(tx.get("contractDecimals", 18))
        return f"{value / (10 ** decimals):.10f}"
    return None

def fill_currency_type(tx):
    verified = ""
    token_symbols = ["STRK", "ETH", "WBTC", "USDC", "USDT"]
    if tx.get("contractSymbol") in token_symbols:
        verified = "Verified"
    return verified


def fill_currency(tx):
    return tx.get("contractSymbol", "UNKNOWN")


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
            "Currency",
            "Currency Type",
            "Description",
            "Counterparty address",  
            "Counterparty name",
            "Transaction hash",
            "Blockchain",
            "Wallet",
        ]
    )

    # Use tqdm for the progress bar
    for operation_idx, tx in enumerate(tqdm(token_transfers, desc="Processing transactions", unit="tx")):
        tx_hash = tx["transactionHash"]
        counterparty_address = fill_counterparty_address(wallet_address, tx)
        counterparty_name = fill_counterparty_name(counterparty_address, tx)
        datetime_tx = fill_datetime(tx)
        amount_in_tx = fill_amount_in(tx, wallet_address)
        amount_out_tx = fill_amount_out(tx, wallet_address)
        currency_tx = fill_currency(tx)
        currency_type = fill_currency_type(tx)
        description_tx = descriptionv3(tx, wallet_address, counterparty_address, amount_in_tx, amount_out_tx)

        # Create a single-row DataFrame for the current operation
        record_df = pd.DataFrame(
            [
                {
                    "Transaction #": transaction_hash_mapping[tx_hash],
                    "Datetime": datetime_tx,
                    "Amount In": amount_in_tx,
                    "Amount Out": amount_out_tx,
                    "Currency": currency_tx,
                    "Currency Type" : currency_type,
                    "Description": description_tx,
                    "Counterparty address": counterparty_address,
                    "Counterparty name": counterparty_name,
                    "Transaction hash": tx["transactionHash"],
                    "Blockchain": "Starknet",
                    "Wallet": wallet_address,
                    }
                ]
            )

            # Concatenate the single-row DataFrame to the main DataFrame
            df = pd.concat([df, record_df], ignore_index=True)

    return df
