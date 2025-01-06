from flask import Flask
from dotenv import load_dotenv
from routes.wallet import wallet_routes
from routes.api_keys import api_keys_routes
from routes.usage_stats import usage_stats_routes
from routes.auth import auth_routes
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

# Initialize the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Register blueprints (modularized routes)
app.register_blueprint(wallet_routes, url_prefix="/wallet")
app.register_blueprint(api_keys_routes, url_prefix="/api_keys")
app.register_blueprint(usage_stats_routes, url_prefix="/usage_stats")
app.register_blueprint(auth_routes)


@app.route("/")
def test():
    return "Server is running"


# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
