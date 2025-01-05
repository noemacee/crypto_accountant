import logging
import os
import requests
from flask import Blueprint, render_template, redirect, session

index_routes = Blueprint("index", __name__)
logger = logging.getLogger(__name__)

# If needed, you can still define the backend URL here or import from a config
BACKEND_API_URL = os.getenv("BACKEND_API_URL")


@index_routes.route("/")
def index():
    """Render the main page."""
    logger.info("Rendering the main page.")
    return render_template("index.html")


@index_routes.route("/process_wallet")
def processor():
    """Render the processor page."""
    if not session.get("authenticated"):
        return redirect("/api")
    logger.info("Rendering the processor page.")
    return render_template("process_wallet.html")


@index_routes.route("/api")
def api():
    """Render the API page."""
    logger.info("Rendering the API page.")
    return render_template("api.html")
