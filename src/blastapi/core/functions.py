import requests
import json


def feed_core_request(project_id: str, headers: dict, data: dict):
    """
    Send a POST request to the Starknet Core API

    Args:
        project_id (str): The project ID
        headers (dict): The request headers
        data (dict): The request data
    Returns:
        response (requests.models.Response): The response object
    """
    url = "https://starknet-mainnet.blastapi.io/" + project_id

    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(data)
        )  # Send the POST request

    except requests.exceptions.RequestException as e:
        print(e)
        return None

    return response


def starknet_blockNumber(project_id):
    # Define the headers
    headers = {"Content-Type": "application/json"}

    # Define the payload (same as the cURL -d parameter)
    data = {"jsonrpc": "2.0", "id": 0, "method": "starknet_blockNumber"}

    response = feed_core_request(project_id, headers, data)

    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        result = None

    return result.get("result")


def starknet_getTransactionReceipt(hash, project_id):
    # Define the headers

    headers = {"Content-Type": "application/json"}

    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "starknet_getTransactionReceipt",
        "params": {"transaction_hash": hash},
    }

    request = feed_core_request(project_id, headers, data)
    if request.status_code == 200:
        json = request.json()
    else:
        print(f"Error: {request.status_code}, {request.text}")
        json = None

    return json


def starknet_getClass(project_id, class_hash, block_id):
    # Define the headers
    headers = {"Content-Type": "application/json"}

    # Define the payload (same as the cURL -d parameter)
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "starknet_getClass",
        "params": {"block_id": block_id, "class_hash": class_hash},
    }

    response = feed_core_request(project_id, headers, data)

    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        result = None

    return result


def starknet_getClassHashAt(project_id, contract_address, block_id):
    # Define the headers
    headers = {"Content-Type": "application/json"}

    # Define the payload (same as the cURL -d parameter)
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "starknet_getClassHashAt",
        "params": {"block_id": block_id, "contract_address": contract_address},
    }

    response = feed_core_request(project_id, headers, data)

    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        result = None

    return result
