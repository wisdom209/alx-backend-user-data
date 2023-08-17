#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import requests


def register_user(email: str, password: str) -> None:
    """register user"""
    url = 'http://localhost:5000/users'
    data = {'email': email, 'password': password}
    result = requests.post(url, data=data)
    assert result.status_code


def log_in_wrong_password(email: str, password: str) -> None:
    """log in wrong password"""
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    result = requests.post(url, data=data)
    assert result.status_code == 401, "unauthorized"


def profile_unloggged() -> None:
    """unlog profile"""
    url = 'http://localhost:5000/sessions'
    result = requests.delete(url)


def log_in(email: str, password: str) -> str:
    """log in"""
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    result = requests.post(url, data=data)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
