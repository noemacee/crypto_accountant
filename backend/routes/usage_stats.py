from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.db import execute_query

# Blueprint for usage stats routes
usage_stats_routes = Blueprint("usage_stats_routes", __name__)


@usage_stats_routes.route("/usage_stats", methods=["GET"])
def get_usage_stats():
    """
    Retrieve usage statistics for a specific API key.
    """
    api_key = request.args.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    try:
        stats = execute_query(
            """
            SELECT endpoint, COUNT(*) as count
            FROM api_usage
            WHERE api_key = %s
            GROUP BY endpoint
            """,
            params=(api_key,),
        )
        return jsonify({"usage": stats}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@usage_stats_routes.route("/all_usage_stats", methods=["GET"])
def get_all_usage_stats():
    """
    Retrieve usage statistics for all API keys (admin-only).
    """
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        stats = execute_query(
            """
            SELECT api_key, endpoint, COUNT(*) as count
            FROM api_usage
            GROUP BY api_key, endpoint
            ORDER BY api_key, endpoint
            """
        )
        return jsonify({"usage": stats}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
