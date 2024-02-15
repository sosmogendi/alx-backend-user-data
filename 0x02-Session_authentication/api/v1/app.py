#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

authentication = None
authentication_type = getenv("AUTH_TYPE")

if authentication_type == "basic_auth":
    authentication = BasicAuth()

@app.errorhandler(404)
def handle_not_found(error) -> str:
    """ Handles 404 Not Found error """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def handle_unauthorized(error) -> str:
    """ Handles 401 Unauthorized error """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def handle_forbidden(error) -> str:
    """ Handles 403 Forbidden error """
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def validate_request() -> str:
    """ Before Request Handler
    Validates incoming requests, including authentication checks.
    """
    if authentication is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']  # Add the new path here

    if not authentication.require_auth(request.path, excluded_paths):
        return

    if authentication.authorization_header(request) is None and authentication.session_cookie(request) is None:
        abort(401)

    if authentication.authorization_header(request) is None:
        abort(401)

    if authentication.current_user(request) is None:
        abort(403)

    request.current_user = authentication.current_user(request)  # Assigning current user

@app.route('/api/v1/status')
def get_status():
    """Endpoint to get the status"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
