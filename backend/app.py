import os
import logging
from flask import Flask

# Import the backend route modules (blueprints)
from routes.auth import auth_routes
from routes.wallet import wallet_routes
from routes.usage_stats import usage_stats_routes
from routes.api_keys import api_keys_routes

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """Factory function to create and configure the Flask backend."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Register blueprints
    app.register_blueprint(auth_routes, url_prefix="/")  # or some prefix
    app.register_blueprint(wallet_routes, url_prefix="/wallet")
    app.register_blueprint(usage_stats_routes, url_prefix="/usage_stats")
    app.register_blueprint(api_keys_routes, url_prefix="/api_keys")

    return app


if __name__ == "__main__":
    app = create_app()
    logger.info("Starting the BACKEND Flask application on port 5000.")
    app.run(debug=True, host="0.0.0.0", port=5000)
