#!/usr/bin/env python3
"""Basic flask app"""
from auth import Auth
from db import DB
from flask import Flask, jsonify, Response, request,\
    abort, make_response, url_for, redirect
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
app = Flask(__name__)
auth_obj = Auth()


@app.route('/')
def welcome() -> Response:
    """welcome route"""
    response_msg = {"message": "Bienvenue"}
    return jsonify(response_msg)


@app.route('/users', methods=['POST'])
def users() -> Response:
    """users function"""
    try:
        email = request.form['email']
        password = request.form['password']
        auth_obj.register_user(email, password)
        return_msg = {"email": f"{email}", "message": "user created"}
        return jsonify(return_msg)
    except ValueError:
        return_msg = {"message": "email already registered"}
        return jsonify(return_msg), 400


@app.route("/sessions", strict_slashes=False, methods=["POST"])
def login() -> Response:
    """login function"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = auth_obj.valid_login(email, password)
    if not user:
        abort(401)
    else:
        session_id = auth_obj.create_session(email)
        if (session_id):
            value = {
                "email": "{}".format(email),
                "message": "logged in"}
            response = jsonify(value)
            response.set_cookie("session_id", session_id)
            return response
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout function"""
    if request.method == 'DELETE':
        session_id = request.cookies.get('session_id')
        user = auth_obj.get_user_from_session_id(session_id)
        if user:
            auth_obj.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    """get user profile function"""
    session_id = request.cookies.get('session_id')
    user = auth_obj.get_user_from_session_id(session_id)
    if user:
        return_msg = {"email": f"{user.email}"}
        return jsonify(return_msg)
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """get reset password token"""
    try:
        email = request.form.get('email')
        token = auth_obj.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
