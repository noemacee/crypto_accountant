from flask import Blueprint, request, jsonify
from services.db import get_db_connection
import os

# Blueprint for API key routes
api_keys_routes = Blueprint("api_keys_routes", __name__)


@api_keys_routes.route("/generate_api_key", methods=["POST"])
def generate_api_key():
    """Generate a new API key for a user."""
    data = request.json
    owner = data.get("owner")
    if not owner:
        return jsonify({"error": "Owner is required"}), 400

    api_key = os.urandom(16).hex()  # Generate a random 32-character API key

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO api_keys (api_key, owner) VALUES (%s, %s) RETURNING api_key",
            (api_key, owner),
        )
        conn.commit()
        new_key = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"api_key": new_key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_keys_routes.route("/validate_api_key", methods=["POST"])
def validate_api_key():
    """Validate an API key."""
    data = request.json
    api_key = data.get("api_key")
    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM api_keys WHERE api_key = %s",
            (api_key,),
        )
        is_valid = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()

        if is_valid:
            return jsonify({"message": "API key is valid"}), 200
        else:
            return jsonify({"error": "Invalid API key"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_keys_routes.route("/api_keys", methods=["GET"])
def list_api_keys():
    """Retrieve a list of all API keys (admin-only)."""
    # Add admin authentication/authorization here if required
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, api_key, owner, created_at FROM api_keys")
        api_keys = cursor.fetchall()
        cursor.close()
        conn.close()

        return (
            jsonify(
                [
                    {
                        "id": row[0],
                        "api_key": row[1],
                        "owner": row[2],
                        "created_at": row[3],
                    }
                    for row in api_keys
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
