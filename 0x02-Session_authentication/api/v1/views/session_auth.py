#!/usr/bin/env python3
"""Module for session authentication views."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Log in a user via POST /auth_session/login.

    Returns:
        - Logged in user
    """
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "Email missing"}), 400

    password = request.form.get('password')

    if not password:
        return jsonify({"error": "Password missing"}), 400

    try:
        found_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "No user found for this email"}), 404

    if not found_users:
        return jsonify({"error": "No user found for this email"}), 404

    for user in found_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "Wrong password"}), 401

    from api.v1.app import auth

    user = found_users[0]
    session_id = auth.create_session(user.id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """Log out a user via DELETE /auth_session/logout.

    Returns:
        - Empty dictionary if successful
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
