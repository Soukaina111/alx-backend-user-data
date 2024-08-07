#!/usr/bin/env python3
""" Module of Users views
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User

# View to get all users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    total = [user.to_json() for user in User.all()]
    return jsonify(total)

# View to get a single user
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    # If the user_id is "me" and there is no current_user, return a 404 error
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        else:
            # If the user_id is "me" and there is a current_user, return the
            # JSON representation of the current_user
            return jsonify(request.current_user.to_json())
    # If user_id is None, return a 404 error
    if user_id is None:
        abort(404)
    # Retrieve the user from the database using the User.get method
    user = User.get(user_id)
    # If the user was not found, return a 404 error
    if user is None:
        abort(404)
    # Return the JSON representation of the user
    return jsonify(user.to_json())

# View to delete a user
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    cs = User.get(user_id)
    if cs is None:
        abort(404)
    cs.remove()
    return jsonify({}), 200

# View to create a new user
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    ab = None
    error_msg = None
    try:
        ab = request.get_json()
    except Exception as e:
        ab = None
    if ab is None:
        error_msg = "Wrong format"
    if error_msg is None and ab.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and ab.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = ab.get("email")
            user.password = ab.get("password")
            user.first_name = ab.get("first_name")
            user.last_name = ab.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400

# View to update a user
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    ab = None
    try:
        ab = request.get_json()
    except Exception as e:
        ab = None
    if ab is None:
        return jsonify({'error': "Wrong format"}), 400
    if ab.get('first_name') is not None:
        user.first_name = ab.get('first_name')
    if ab.get('last_name') is not None:
        user.last_name = ab.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
