#!/usr/bin/env python3
"""
Route module for the API
"""

import os
from os import getenv
from typing import Tuple

from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.views import app_views

# Create a Flask application instance
app = Flask(__name__)

# Register the Blueprint for the API views
app.register_blueprint(app_views)

# Enable CORS for the /api/v1/* routes, allowing access from any origin
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Create a variable auth initialized to None after the CORS definition
auth = None

# Update api/v1/app.py for using SessionAuth instance for the variable
# auth depending of the value of the environment variable AUTH_TYPE. If
# AUTH_TYPE is equal to session_auth:
#   import SessionAuth from api.v1.auth.session_auth
#   create an instance of SessionAuth and assign it to the variable auth
auth_type = getenv('AUTH_TYPE', 'default')
if auth_type == "session_auth":
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
elif auth_type == 'session_db_auth':
    auth = SessionDBAuth()
elif auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()

# Define the 404 error handler
@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

# Define the 401 error handler
@app.errorhandler(401)
def unauthorized(error: Exception) -> Tuple[jsonify, int]:
    """Error handler for unauthorized requests.

    Args:
        error (Exception): The error raised.

    Returns:
        Tuple[jsonify, int]: JSON response with the error message and a 401
        status code.
    """
    return jsonify({"error": "Unauthorized"}), 401

# Define the 403 error handler
@app.errorhandler(403)
def forbidden(error: Exception) -> Tuple[jsonify, int]:
    """Error handler for unauthorized requests.

    Args:
        error (Exception): The error raised.

    Returns:
        Tuple[jsonify, int]: JSON response with the error message and a 401
        status code.
    """
    return jsonify({"error": "Forbidden"}), 403

# Define a before_request handler to handle authentication and authorization
@app.before_request
def handle_request():
    """
    Handle the request by checking for authentication and authorization.
    """
    # If auth is None, do nothing
    if auth is None:
        return

    # Create a list of excluded paths that don't require authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']

    # If the request path is not part of the excluded list, check authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # If both the authorization header and session cookie are missing, raise a 401 error
    auth_header = auth.authorization_header(request)
    session_cookie = auth.session_cookie(request)
    if auth_header is None and session_cookie is None:
        abort(401)

    # If the current user is not found, raise a 403 error
    user = auth.current_user(request)
    if user is None:
        abort(403)

    # Assign the current user to the request object
    request.current_user = user

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
