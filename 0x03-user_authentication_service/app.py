#!/usr/bin/env python3
"""
A simple Flask app with user authentication features.
This app provides endpoints
for user registration, login, logout, profile retrieval, and password reset.
"""
import logging

from flask import Flask, abort, jsonify, redirect, request

from auth import Auth

logging.disable(logging.WARNING)


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET /
    Returns a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    POST /users
    Registers a new user with the provided email and password.
    """
    # Get the email and password from form data
    email, password = request.form.get("email"), request.form.get("password")
    try:
        # Register the user
        AUTH.register_user(email, password)
        # Respond with the following JSON payload:
        # {"email": "<registered email>", "message": "user created"}
        return jsonify({"email": email, "message": "user created"})
    # and return a 400 status code
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST /sessions
    Logs in a user with the provided email and password.
    If the credentials are invalid, returns a 401 Unauthorized response.
    """
    # Get user credentials from form data
    email, password = request.form.get("email"), request.form.get("password")
    # Check if the user's credentials are valid
    if not AUTH.valid_login(email, password):
        abort(401)
    # Create a new session for the user
    session_id = AUTH.create_session(email)
    # Construct a response with a JSON payload
    response = jsonify({"email": email, "message": "logged in"})
    # Set a cookie with the session ID on the response
    response.set_cookie("session_id", session_id)
    # Return the response
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    DELETE /sessions
    """
    # Get the session ID from the "session_id" cookie in the request
    session_id = request.cookies.get("session_id")
    # Retrieve the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    # Destroy the session associated with the user
    AUTH.destroy_session(user.id)
    # Redirect to the home route
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    GET /profile
    Retrieves the email of the user
    associated with the session ID stored in the "session_id" cookie.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    # Return the user's email as a JSON payload
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Generates a reset password token for the provided email.
    """
    # Retrieve the email from the form data
    email = request.form.get("email")
    try:
        # Attempt to generate a reset token for the given email
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # If the email is not found in the database, raise a 403 error
        abort(403)
    # Return a JSON payload containing the email and reset token
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password
    Updates the password for
    the user associated with the provided email and reset token.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        # Attempt to update the password with the new password
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        # If the reset token is invalid, return an HTTP 403 error
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
