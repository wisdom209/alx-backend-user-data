#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def welcome():
    """welcome route"""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
