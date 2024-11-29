# Import modules
import requests
import json
import os
#from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# Import the project_id variable from the .env file in the current directory or hard-code it
project_id = os.getenv("PROJECT_ID")
project_id = '76ae4a83-28b3-48dc-837c-f1c6fa25dd9a'

# Define global constants
TRANSFER_EVENT = '0x99cd8bde557814842a3121e8ddfd433a539b8c9f14bf31ebf108d12e6196e9'
#sergei = '0x35b6530ef09e227ca9f92efb66df12d0da9fface35ecd53b53a918c7d4eaa75'
wallet_address ='0x35b6530ef09e227ca9f92efb66df12d0da9fface35ecd53b53a918c7d4eaa75'
sequencer_address = "0x1176a1bd84444c89232ec27754698e5d2e7e1a7f1539f12027f28b23ec9f3d8"

# Define a map from addresses to known contracts
addresses2contract_map = {
    # Ekubo
    "0x00000005dd3d2f4429af886cd1a3b08289dbcea99a294197e9eb43b0e0325b4b": "Ekubo Core",
    "0x02e0af29598b407c8716b17f6d2795eca1b471413fa03fb145a5e33722184067": "Ekubo Positions",
    "0x07b696af58c967c1b14c9dde0ace001720635a660a8e90c565ea459345318b30": "Ekubo Positions NFT",

    # Nostra
    "0x073f6addc9339de9822cab4dac8c9431779c09077f02ba7bc36904ea342dd9eb": "Nostra CDP Manager / Deferred Batch Call Adapter",
    "0x059a943ca214c10234b9a3b61c558ac20c005127d183b86a99a8f3c60a08b4ff": "Nostra Interest Rate Model",
    "0x1bcfcb651e98317dc042cb34d0e0226c7f83bca309b6c54d8f0df6ee4e5f721": "Nostra Flash Loan Adapter",

    # AVNU
    "0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f": "AVNU Exchange",
    "0x0360fb3a51bd291e5db0892b6249918a5689bc61760adcb350fe39cd725e1d22": "AVNU Fee Collector",
    "0x0759c955b1cfddb8fcab93fddb0da1902d55bfe98bc4605ecb8cd4c635bc085b": "AVNU Elite Role NFT",
    
    # Starknet
    "0x01176a1bd84444c89232ec27754698e5d2e7e1a7f1539f12027f28b23ec9f3d8": "StarkWare: Sequencer",

}

# Define a map from addresses to known protocols
addresses2counterparty_map = {
    # Ekubo
    "0x00000005dd3d2f4429af886cd1a3b08289dbcea99a294197e9eb43b0e0325b4b": "Ekubo",
    "0x02e0af29598b407c8716b17f6d2795eca1b471413fa03fb145a5e33722184067": "Ekubo",
    "0x07b696af58c967c1b14c9dde0ace001720635a660a8e90c565ea459345318b30": "Ekubo",
    
    # Nostra
    "0x073f6addc9339de9822cab4dac8c9431779c09077f02ba7bc36904ea342dd9eb": "Nostra",
    "0x059a943ca214c10234b9a3b61c558ac20c005127d183b86a99a8f3c60a08b4ff": "Nostra",
    "0x1bcfcb651e98317dc042cb34d0e0226c7f83bca309b6c54d8f0df6ee4e5f721": "Nostra",
    
    # AVNU
    "0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f": "AVNU",
    "0x0360fb3a51bd291e5db0892b6249918a5689bc61760adcb350fe39cd725e1d22": "AVNU",
    "0x0759c955b1cfddb8fcab93fddb0da1902d55bfe98bc4605ecb8cd4c635bc085b": "AVNU",
    
    # Starknet
    "0x01176a1bd84444c89232ec27754698e5d2e7e1a7f1539f12027f28b23ec9f3d8": "Starknet",
}

# Pool contracts data
pool_token = {
    
    #nostra : https://docs.nostra.finance/pools/deployed-contracts
    "0x068400056dccee818caa7e8a2c305f9a60d255145bac22d6c5c9bf9e2e046b71": "STRK/ETH",
    "0x07ae43abf704f4981094a4f3457d1abe6b176844f6cdfbb39c0544a635ef56b0": "STRK/USDC",
    "0x00c318445d5a5096e2ad086452d5c97f65a9d28cafe343345e0fa70da0841295": "USDC/USDT",
    "0x05ef8800d242c5d5e218605d6a10e81449529d4144185f95bf4b8fb669424516": "ETH/USDC",
    "0x052b136b37a7e6ea52ce1647fb5edc64efe23d449fc1561d9994a9f8feaa6753": "ETH/USDT",
    "0x05ae9c593b2bef20a8d69ae7abf1e6da551481f9efd83d03a9f05b6d7c9a78ec": "LORDS/ETH",
    "0x0285aa1c4bbeef8a183fb7245f096ddc4c99c6b2fedd1c1af52a634c83842804": "WBTC/ETH",
    "0x33c4141c8eb6ab8e7506c6f09c1a64b0995c9a5fa2ba6fa827845535b942786": "BRRR/ETH",
    "0x13e7962df51aba2afedbc1c86b0b61d36410f97fc75cb8f51e525559bef49f6": "STRONK/STRK",
    "0x0344653508c3b8831d6826712004f5bcff9d7a9a8fe720ba8e8b6005fb23c04d": "TONY/STRK",
    "0x05737b6463e8aab45d9237180ac68515a49fa3e0656f06b5831c15c69af83332": "AKU/STRK",
    "0x07d24fc0949e9579cb6e08bb65ffe39fd5dd78a47ad2e4eb52e49b97c2cd26db": "PAL/STRK",
    "0x076def79cc9a3a375779c163ad12996f99fbeb4acd68d7041529159bde897160": "nstSTRK/STRK",
    "0x03f8c9062f1bfe45f82cd70ed97ff053bc5836783ec66adfe3288eb1b43aa83b": "ETH/UNO",
    "0x03d51776d3ce07c211d5dbdf40a9333ec6d6d3a0b2853de1d6706f9ea3b88d45": "STRK/UNO",
    "0x01a2de9f2895ac4e6cb80c11ecc07ce8062a4ae883f64cb2b1dc6724b85e897d": "STRK/ETH (Degen)",
    "0x042543c7d220465bd3f8f42314b51f4f3a61d58de3770523b281da61dbf27c8a": "STRK/USDC (Degen)",
    "0x05e03162008d76cf645fe53c6c13a7a5fce745e8991c6ffe94400d60e44c210a": "ETH/USDC (Degen)",
    "0x01583919ffd78e87fa28fdf6b6a805fe3ddf52f754a63721dcd4c258211129a6": "WBTC/ETH (Degen)",
    "0x0577521a1f005bd663d0fa7f37f0dbac4d7f55b98791d280b158346d9551ff2b": "wstETH/ETH",
    "0x0362ec0c49a9c8f2d322d0ba6a8ec1214b9e4f7e80a17d462ec2585362547d95": "USDC/DAI",
    "0x05458b28f32b5f6e635895063ec0fe85c5a3864d257c4ae293edd5f66acf988d": "zUSDC/USDC",
    "0x07f232e7857effe04f7351e9bb2f1ebc2589bacca3380ae84efcc22067c1436e": "NSTR/USDC",
}

# Debt token data
debt_token = {
    # Nostra : https://docs.nostra.finance/lend-and-borrow/deployed-contracts/money-market-mainnet
    "0x0491480f21299223b9ce770f23a2c383437f9fbf57abc2ac952e9af8cdb12c97": "WBTC", 
    "0x00ba3037d968790ac486f70acaa9a1cab10cf5843bb85c986624b4d0e5a82e74": "ETH", 
    "0x063d69ae657bd2f40337c39bf35a870ac27ddf91e6623c2f52529db4c1619a51": "USDC",
    "0x066037c083c33330a8460a65e4748ceec275bbf5f28aa71b686cbc0010e12597": "DAIv0",
    "0x024e9b0d6bc79e111e6872bb1ada2a874c25712cf08dfc5bcf0de008a7cca55f": "UDST",
    "0x0348cc417fc877a7868a66510e8e0d0f3f351f5e6b0886a86b652fcb30a3d1fb": "wstETH",
    "0x035778d24792bbebcf7651146896df5f787641af9e2a3db06480a637fbc9fff8": "LORDS",
    "0x001258eae3eae5002125bebf062d611a772e8aea3a1879b64a19f363ebd00947": "STRK",
    "0x0292be6baee291a148006db984f200dbdb34b12fb2136c70bfe88649c12d934b": "nstSTRK",
    "0x04b036839a8769c04144cc47415c64b083a2b26e4a7daa53c07f6042a0d35792": "UNO",
    "0x03e0576565c1b51fcac3b402eb002447f21e97abb5da7011c0a2e0b465136814": "NSTR",
    "0x06726ec97bae4e28efa8993a8e0853bd4bad0bd71de44c23a1cd651b026b00e7": "DAI",
    "0x073fa792a8ad45303db3651c34176dc419bee98bfe45791ab12f884201a90ae2": "EKUBO",
    
}

# Interest bearing & Collateral token
interest_bearing_and_collat_token = {
    # Nostra : https://docs.nostra.finance/lend-and-borrow/deployed-contracts/money-market-mainnet
    "0x05b7d301fa769274f20e89222169c0fad4d846c366440afc160aafadd6f88f0c": "WBTC", 
    "0x057146f6409deb4c9fa12866915dd952aa07c1eb2752e451d7f3b042086bdeb8": "ETH", 
    "0x05dcd26c25d9d8fd9fc860038dcb6e4d835e524eb8a85213a8cda5b7fff845f6": "USDC",
    "0x04f18ffc850cdfa223a530d7246d3c6fc12a5969e0aa5d4a88f470f5fe6c46e9": "DAIv0",
    "0x0453c4c996f1047d9370f824d68145bd5e7ce12d00437140ad02181e1d11dc83": "UDST",
    "0x009377fdde350e01e0397820ea83ed3b4f05df30bfb8cf8055d62cafa1b2106a": "wstETH",
    "0x0739760bce37f89b6c1e6b1198bb8dc7166b8cf21509032894f912c9d5de9cbd": "LORDS",
    "0x07c2e1e733f28daa23e78be3a4f6c724c0ab06af65f6a95b5e0545215f1abc1b": "STRK",
    "0x067a34ff63ec38d0ccb2817c6d3f01e8b0c4792c77845feb43571092dcf5ebb5": "nstSTRK",
    "0x02a3a9d7bcecc6d3121e3b6180b73c7e8f4c5f81c35a90c8dd457a70a842b723": "UNO",
    "0x046ab56ec0c6a6d42384251c97e9331aa75eb693e05ed8823e2df4de5713e9a4": "NSTR",
    "": "DAI",
    "0x02360bd006d42c1a17d23ebe7ae246a0764dea4ac86201884514f86754ccc7b8": "EKUBO",
}

# Define the two main API call functions
def feed_core_request(project_id, headers, data):
    url = "https://starknet-mainnet.blastapi.io/" + project_id

    try : 
        response = requests.post(url, headers=headers, data=json.dumps(data))        # Send the POST request

    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
    return response
def feed_builder_request(project_id, contract_name, params):
    url = "https://starknet-mainnet.blastapi.io/" + project_id + "/builder/" + contract_name

    try:
        response = requests.get(url, params=params)        # Send the GET request
    
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
    print("Calling "+ contract_name)
    
    return response 

# Define "method" functions
def getWalletTokenHistory(project_id, walletAddress):
    
    params = {
        'walletAddress': walletAddress
    }
    
    response = feed_builder_request(project_id, "getWalletTokenHistory", params)

    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        result = None
        
    return result
def getWalletTokenTransfers(project_id, walletAddress, pageSize, page_key=None):
    
    params = {
        'walletAddress': walletAddress,
        'pageSize': pageSize,
    }
    
    if page_key:
        params["pageKey"] = page_key
    
    response = feed_builder_request(project_id, "getWalletTokenTransfers", params)

    if response.status_code == 200:
        result = response.json()
        
    else:
        print(f"Error: {response.status_code}, {response.text}")
        result = None
        
    return result
def fetch_all_pages(project_id, wallet_address, page_size=100, output_file="wallet_token_transfers.json"):
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
def starknet_getTransactionReceipt(hash):
    # Define the headers
    
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "starknet_getTransactionReceipt",
        "params": {
            "transaction_hash": hash
        },
    }

    request = feed_core_request(project_id, headers, data)
    if request.status_code == 200:
        json = request.json()
    else:
        print(f"Error: {request.status_code}, {request.text}")
        json = None
    
    return json
def operation_classifier (tx_hash):
    json_transactionReceipt = starknet_getTransactionReceipt(tx_hash) # This is the bottleneck of the function
    
    
    # The addresses are not padded for transactionReceipts
    
    
    
    all_transfer_events = []
    fee_events = []
    non_fee_events = []


    index = 1
    
    for i in range(len(json_transactionReceipt['result']['events']) - 1, 0, -1): # Loop through the events in reverse order
        
        if TRANSFER_EVENT in json_transactionReceipt['result']['events'][i]['keys']: 
            
            
            
            if sequencer_address in json_transactionReceipt['result']['events'][i]['data']:
                fee_events.append(index)
            else:
                non_fee_events.append(index)

            if wallet_address in json_transactionReceipt['result']['events'][i]['data']:
                all_transfer_events.append(index)
                index += 1
            else:
                all_transfer_events.append(-1)
    
    return all_transfer_events, fee_events, non_fee_events
def process_transactions(json_data, wallet_address):
    """Process transactions into the required structure."""

    token_transfers = json_data["tokenTransfers"]
    records = []


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
    df = pd.DataFrame(columns=[
        "Transaction #","Operation #", "Ignore", "Datetime", "Amount In", "Amount Out", "Amount currency",
        "Description", "Counterparty address", "Counterparty name", "Transaction hash",
        "Blockchain", "Wallet", "transfer_from", "transfer_to", "transfer_amount",
        "token_address", "token_symbol", "token_name", "transfer_type", "call",
        "tx_hash", "block_number", "from_alias", "to_alias", "timestamp"
    ])

    
    # Group operations by transaction hash
    grouped_transactions = {}
    for tx in token_transfers:
        tx_hash = tx["transactionHash"]
        if tx_hash not in grouped_transactions:
            grouped_transactions[tx_hash] = []
        grouped_transactions[tx_hash].append(tx)    
    
    
    
    ####
    
    # Create records using the transaction hash mapping
    for tx_hash, operations in grouped_transactions.items():

        all_transfer_events, fee_events, non_fee_events = operation_classifier(tx_hash)
        #print("all_transfer_events : ", all_transfer_events)
        
        
        #json_transactionReceipt = starknet_getTransactionReceipt(tx_hash) # This is the bottleneck of the function

        
        
        
        #print("toAddress : " + tx["toAddress"] + "fromAddress" + tx["fromAddress"] + "counterparty name :" )
        
        #if tx["toAddress"] == wallet_address:
            #print(addresses2contract_map.get(tx["fromAddress"], "toAddress"))
        #else:
            #print(addresses2contract_map.get(tx["toAddress"], "fromAddress"))
        
        for operation_index, tx in enumerate(operations, start=1): 
            
            counterparty_address = tx["toAddress"] if tx["fromAddress"] == wallet_address else tx["fromAddress"]
            
            token_address = tx.get("contractAddress", "")
            if (pool_token.get(token_address, "") == "" and debt_token.get(token_address, "") == "" and interest_bearing_and_collat_token.get(token_address, "") == ""):
                # Create a single-row DataFrame for the current operation
                record_df = pd.DataFrame([{
                    "Transaction #": transaction_hash_mapping[tx_hash],
                    "Operation #": operation_index,  # Sequential operation index
                    "Ignore": True,
                    "Datetime": datetime.fromisoformat(tx["blockTimestamp"].replace("Z", "")).strftime("%Y-%m-%d %H:%M:%S"),
                    "Amount In": f"{int(tx['value']) / (10 ** int(tx.get('contractDecimals', 18))):.10f}" if tx["toAddress"] == wallet_address else "",
                    "Amount Out": f"{int(tx['value']) / (10 ** int(tx.get('contractDecimals', 18))):.10f}" if tx["fromAddress"] == wallet_address else "",
                    "Amount currency": tx.get("contractSymbol", "UNKNOWN"),
                    "Description": "Transaction fee" if tx.get("transfer_type", "") == "fee_transfer" else "Transaction",
                    "Counterparty address": tx["toAddress"] if tx["fromAddress"] == wallet_address else tx["fromAddress"],
                    "Counterparty name": 
                        addresses2counterparty_map.get(tx["toAddress"], "") if (tx["fromAddress"] == wallet_address ) else addresses2counterparty_map.get(tx["fromAddress"], ""),
                    "Transaction hash": tx["transactionHash"],
                    "Blockchain": "Starknet",
                    "Wallet": wallet_address,
                    "transfer_from": tx["fromAddress"],
                    "transfer_to": tx["toAddress"],
                    "transfer_amount": f"{int(tx['value']) / (10 ** int(tx.get('contractDecimals', 18))):.10f}",
                    "token_address": tx.get("contractAddress", ""),
                    "token_symbol": tx.get("contractSymbol", "UNKNOWN"),
                    "token_name": tx.get("contractName", "UNKNOWN"),
                    "transfer_type": "fee_transfer" if (operation_index in fee_events) else "execute",
                    "call": "transfer",
                    "tx_hash": tx["transactionHash"],
                    "block_number": tx["blockNumber"],
                    "from_alias": addresses2contract_map.get(tx["fromAddress"]),  # Placeholder for alias mapping
                    "to_alias": addresses2contract_map.get(tx["toAddress"]),
                    "timestamp": tx["blockTimestamp"],
                }])


                # Concatenate the single-row DataFrame to the main DataFrame
                df = pd.concat([df, record_df], ignore_index=True)
    return df


# Other useful functions
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

# Main function
def main():
    """Main execution function."""
    # File paths and wallet address
    json_file_path = "wallet_token_transfers.json"    
    output_csv_path = "wallet_transactions.csv"
    wallet_address = "0x035b6530ef09e227ca9f92efb66df12d0da9fface35ecd53b53a918c7d4eaa75"

    # Fetch all token transfers using pagination and save to JSON
    print("Fetching all token transfers...")

    json_data = fetch_all_pages(project_id, wallet_address, page_size=100, output_file=json_file_path)
    
    if not json_data:
        print("No data to process. Exiting.")
        return

    # Process transactions
    print("Processing transactions...")
    df = process_transactions(json_data, wallet_address)

    # Save processed data to CSV
    print("Saving to CSV...")
    save_to_csv(df, output_csv_path)

    print("Process complete. Transactions saved to", output_csv_path)

# Execute main
if __name__ == "__main__":
    main()
