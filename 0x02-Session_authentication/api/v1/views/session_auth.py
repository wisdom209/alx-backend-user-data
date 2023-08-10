#!/usr/bin/env python3
"""session auth routes module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST SESSION DETAILS
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == '':
        return jsonify({"error": "email missing"}), 400

    if not password or password == '':
        return jsonify({"error": "password is missing"}), 400

    user = User.search({"email": email})

    if (not user or len(user) == 0):
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    res.set_cookie(session_name, session_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)  # nopep8
def session_logout() -> str:
    """ POST SESSION DETAILS
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
