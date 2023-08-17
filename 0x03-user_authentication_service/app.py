#!/usr/bin/env python3
"""Basic flask app"""
from auth import Auth
from db import DB
from flask import Flask, jsonify, Response, request, abort, make_response
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


@app.route('/sessions', methods=['POST'])
def login() -> Response:
    """login route"""
    email = request.form['email']
    password = request.form['password']

    valid_login = auth_obj.valid_login(email, password)

    if not valid_login:
        abort(401)
    session_id = auth_obj.create_session(email)

    return_msg = {"email": f"{email}", "message": "logged in"}

    resp = make_response(jsonify(return_msg))
    resp.set_cookie('session_id', session_id)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
