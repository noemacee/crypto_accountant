from flask import Blueprint, request, jsonify
from services.db import get_db_connection
import os
import logging
import psycopg2

# Blueprint for API key routes
api_keys_routes = Blueprint("api_keys_routes", __name__)
logger = logging.getLogger(__name__)


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
        logger.warning("API key is missing in the request.")
        return jsonify({"error": "API key is required"}), 400

    try:
        logger.debug("Connecting to the database...")
        conn = get_db_connection()
        with conn.cursor() as cursor:
            logger.debug("Executing query to validate API key: %s", api_key)
            cursor.execute(
                "SELECT COUNT(*) AS count FROM api_keys WHERE api_key = %s",
                (api_key,),
            )
            logger.debug("Query executed successfully.")
            result = cursor.fetchone()

            # Safely handle both dictionary and tuple responses
            count = result["count"] if isinstance(result, dict) else result[0]
            logger.debug("Query result: %s, Validation result: %s", result, count)

            is_valid = count > 0

        if is_valid:
            return jsonify({"message": "API key is valid"}), 200
        else:
            return jsonify({"error": "Invalid API key"}), 401

    except psycopg2.DatabaseError as db_err:
        logger.error("DB error occurred: %s", db_err)
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        logger.exception("Unexpected error occurred")
        return jsonify({"error": f"Unexpected error: {e}"}), 500
    finally:
        if conn:
            conn.close()
            logger.debug("Database connection closed.")


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
