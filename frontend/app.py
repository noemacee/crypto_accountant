import os
import logging
from flask import Flask

# Import the blueprints
from routes.index import index_routes
from routes.auth import auth_routes
from routes.wallet import wallet_routes
from routes.usage_stats import usage_routes
from routes.api_keys import api_keys_routes

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """Factory function to create and configure the Flask frontend."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Register blueprints
    app.register_blueprint(index_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(wallet_routes)
    app.register_blueprint(usage_routes)
    app.register_blueprint(api_keys_routes)

    return app


if __name__ == "__main__":
    app = create_app()
    logger.info("Starting the FRONTEND Flask application on port 3000.")
    app.run(debug=True, host="0.0.0.0", port=3000)
