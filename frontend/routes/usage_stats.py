import logging
import os
import requests
from flask import Blueprint, request, render_template, jsonify

usage_routes = Blueprint("usage_routes", __name__)
logger = logging.getLogger(__name__)

BACKEND_API_URL = os.getenv("BACKEND_API_URL")


@usage_routes.route("/metrics", methods=["GET"])
def metrics():
    """Render the metrics page."""
    return render_template("metrics.html")


@usage_routes.route("/usage_stats", methods=["POST"])
def usage_stats():
    """Query the backend API for usage statistics."""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        logger.warning("API key missing in usage stats request.")
        return jsonify({"error": "API key is required"}), 400

    try:
        logger.debug("Fetching usage stats for API key: %s", api_key)
        response = requests.get(
            f"{BACKEND_API_URL}/usage_stats/usage_stats",
            headers={"X-API-Key": api_key},
        )
        response.raise_for_status()
        logger.info("Usage stats fetched successfully.")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred while fetching usage stats: %s", str(e))
        return jsonify({"error": str(e)}), 500


@usage_routes.route("/all_usage_stats", methods=["GET"])
def all_usage_stats():
    """Query the backend API for all usage statistics."""
    try:
        response = requests.get(f"{BACKEND_API_URL}/usage_stats/all_usage_stats")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
