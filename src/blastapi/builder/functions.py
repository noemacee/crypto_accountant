import requests


def feed_builder_request(project_id, contract_name, params):
    """Send a GET request to the Starknet Builder API

    Args:
        project_id (str): The project ID
        contract_name (str): The contract name
        params (dict): The request parameters
    Returns:
        response (requests.models.Response): The response object

    """

    url = (
        "https://starknet-mainnet.blastapi.io/"
        + project_id
        + "/builder/"
        + contract_name
    )

    try:
        response = requests.get(url, params=params)  # Send the GET request

    except requests.exceptions.RequestException as e:
        print(e)
        return None

    # print("Calling "+ contract_name)

    return response


def getWalletTokenHistory(project_id, walletAddress):

    params = {"walletAddress": walletAddress}

    response = feed_builder_request(project_id, "getWalletTokenHistory", params)

    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        result = None

    return result


def getWalletTokenTransfers(project_id, walletAddress, pageSize, page_key=None):

    params = {
        "walletAddress": walletAddress,
        "pageSize": pageSize,
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


def getTransaction(project_id, transactionHash):
    url = (
        "https://starknet-mainnet.blastapi.io/" + project_id + "/builder/getTransaction"
    )
    # Define the parameters
    params = {"transactionHash": transactionHash}

    # Send the GET request
    try:
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON into a Python dictionary
            data_dict = response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
        return data_dict
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
