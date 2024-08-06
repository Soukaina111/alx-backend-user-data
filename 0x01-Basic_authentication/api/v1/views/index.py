#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


# Define a route handler for the '/status' endpoint, which returns the status of the API
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


# Define a route handler for the '/stats' endpoint, which returns the number of each object
@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    # Import the User model to retrieve the count
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


# Define a route handler for the '/unauthorized' endpoint, which raises a 401 Unauthorized error
@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized
    Return:
      - raises a 401 error by using abort
    """
    abort(401)


# Define a route handler for the '/forbidden' endpoint, which raises a 403 Forbidden error
@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ GET /api/v1/forbidden
    Return:
      - raises a 403 error by using abort
    """
    abort(403)
