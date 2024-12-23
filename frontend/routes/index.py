import logging
import os
import requests
from flask import Blueprint, render_template

index_routes = Blueprint("index", __name__)
logger = logging.getLogger(__name__)

# If needed, you can still define the backend URL here or import from a config
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend:5000")


@index_routes.route("/")
def index():
    """Render the main page."""
    logger.info("Rendering the main page.")
    return render_template("index.html")


