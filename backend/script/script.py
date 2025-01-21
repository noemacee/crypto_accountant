import os
import requests
import dotenv

# Load the environment variables from the .env file
dotenv.load_dotenv(dotenv_path=".env")

BACKEND_PORT_HOST = os.getenv("BACKEND_PORT_HOST")
url = "http://localhost:" + BACKEND_PORT_HOST

# Construct the full URL
endpoint = url + f"/api_keys/generate_api_key"

# Payload to send in the request
payload = {"owner": "test"}  # Replace with the actual owner value

# Make the POST request
try:
    response = requests.post(endpoint, json=payload)
    if response.status_code == 201:
        print("API key generated successfully:", response.json())
    else:
        print("Failed to generate API key:", response.status_code, response.json())
except requests.RequestException as e:
    print("Error while making the request:", str(e))
