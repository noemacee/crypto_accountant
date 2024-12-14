from flask import Flask
from dotenv import load_dotenv
from routes.wallet import wallet_routes
from routes.api_keys import api_keys_routes
from routes.usage_stats import usage_stats_routes
from routes.auth import auth_routes, User  # Import auth_routes and User

from flask_login import LoginManager

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "auth_routes.login"  # Redirect to 'login' if not logged in

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

# Initialize the Flask application
app = Flask(__name__)

# Configure Flask-Login
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)  # Load user by ID from the User class


# Register blueprints (modularized routes)
app.register_blueprint(wallet_routes, url_prefix="/wallet")
app.register_blueprint(api_keys_routes, url_prefix="/api_keys")
app.register_blueprint(usage_stats_routes, url_prefix="/usage_stats")
app.register_blueprint(auth_routes)  # Register the auth routes

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
