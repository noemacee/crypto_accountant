from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

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


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")  # Add proper password validation
        user = User.get("1") if username == "admin" else User.get("2")  # Example logic

        if user:  # Replace with real authentication logic
            login_user(user)
            return redirect(url_for("index"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")


@auth_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_routes.login"))
