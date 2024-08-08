#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


# Create the Flask app instance
app = Flask(__name__)

# Register the app_views blueprint with the Flask app
app.register_blueprint(app_views)

# Enable CORS (Cross-Origin Resource Sharing) for the /api/v1/* route
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the authentication object based on the environment variable
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


# Define a custom error handler for 404 (Not Found) errors
@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


# Define a custom error handler for 401 (Unauthorized) errors
@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


# Define a custom error handler for 403 (Forbidden) errors
@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


# Define a before_request hook to handle authentication and authorization
@app.before_request
def before_request() -> str:
    """ Before Request Handler
    Requests Validation
    """
    # If the authentication object is not defined, return
    if auth is None:
        return

    # Define a list of excluded paths that don't require authentication
    dead_path = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    # Check if the requested path requires authentication
    if not auth.require_auth(request.path, dead_path):
        return

    # Check if the authorization header is present in the request
    if auth.authorization_header(request) is None:
        abort(401)

    # Check if the current user is authenticated
    if auth.current_user(request) is None:
        abort(403)


# Entry point of the application
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")

    # Run the Flask app
    app.run(host=host, port=port)
