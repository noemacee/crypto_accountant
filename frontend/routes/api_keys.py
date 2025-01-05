import logging
import os
import requests
from flask import Blueprint, render_template, request, redirect, jsonify, session

api_keys_routes = Blueprint("api_keys_routes", __name__)
logger = logging.getLogger(__name__)

BACKEND_API_URL = os.getenv("BACKEND_API_URL")


@api_keys_routes.route("/validate_api_key", methods=["POST"])
def validate_api_key():
    """Query the backend API for API key validation."""
    data = request.json
    api_key = data.get("api_key")
    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    try:
        logger.debug("Validating API key: %s", api_key)
        response = requests.post(
            f"{BACKEND_API_URL}/api_keys/validate_api_key",
            json={"api_key": api_key},
        )
        response.raise_for_status()
        logger.info("API key validation successful.")
        session["authenticated"] = True
        session["api_key"] = api_key
        return jsonify(response.json())  # Return the backend's response
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error occurred: %s", req_err)
        return jsonify({"error": f"Request error: {req_err}"}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": f"Unexpected error: {e}"}), 500


@api_keys_routes.route("/generate_api_key", methods=["POST"])
def generate_api_key():
    """Route to generate a new API key."""
    data = request.json
    owner = data.get("owner")
    if not owner:
        return jsonify({"error": "Owner is required"}), 400

    try:
        logger.debug("Generating API key for owner: %s", owner)
        response = requests.post(
            f"{BACKEND_API_URL}/api_keys/generate_api_key",
            json={"owner": owner},
        )
        response.raise_for_status()
        new_key_data = response.json()
        logger.info("API key generated successfully for owner: %s", owner)
        return jsonify(new_key_data)  # Return the backend's response
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error occurred: %s", req_err)
        return jsonify({"error": f"Request error: {req_err}"}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": f"Unexpected error: {e}"}), 500
