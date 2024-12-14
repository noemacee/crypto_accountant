from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask import jsonify

# Create a Blueprint for auth routes
auth_routes = Blueprint("auth_routes", __name__)


class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    @property
    def is_active(self):
        # For simplicity, all users are considered active. Customize as needed.
        return True

    @property
    def is_authenticated(self):
        # Flask-Login automatically uses `UserMixin` for this
        return True

    @property
    def is_anonymous(self):
        # This user is not anonymous
        return False

    # Mock user database
    @staticmethod
    def get(user_id):
        users = {
            "1": User("1", "admin_user", "admin"),
            "2": User("2", "regular_user", "user"),
        }
        return users.get(user_id)


@auth_routes.route("/login", methods=["POST"])
def login_backend():
    """Backend route to authenticate the user."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Simple mock validation (replace with real validation logic)
    if username == "admin" and password == "password":  # Example only
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@auth_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_routes.login"))
