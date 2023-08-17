#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify, Response
app = Flask(__name__)


@app.route('/')
def welcome() -> Response:
    """welcome route"""
    response_msg = {"message": "Bienvenue"}
    return jsonify(response_msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
