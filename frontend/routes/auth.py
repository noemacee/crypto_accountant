import logging
import os
import requests
from flask import Blueprint, render_template, request, redirect

auth_routes = Blueprint("auth_routes", __name__)
logger = logging.getLogger(__name__)

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend:5000")


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    """Frontend route for login that talks to the backend."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            response = requests.post(
                f"{BACKEND_API_URL}/login",
                json={"username": username, "password": password},
            )
            if response.status_code == 200:
                return redirect("/")
            elif response.status_code == 401:
                return "Invalid credentials, please try again.", 401
            else:
                return f"Error: {response.text}", response.status_code
        except Exception as e:
            return f"An error occurred while logging in: {str(e)}", 500

    # Render the login form for GET requests
    return render_template("login.html")


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    """Render the registration form."""
    # Depending on your needs, you could also forward the POST to the backend
    if request.method == "POST":
        # e.g. forward to backend ...
        pass
    return render_template("register.html")
