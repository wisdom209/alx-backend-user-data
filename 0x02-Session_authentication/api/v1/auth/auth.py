#!/usr/bin/env python3
"""authentication module"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""
        other_path = None
        if path is not None and type(path) is str:
            if path[-1] == '/':
                other_path = path[:-1]
            else:
                other_path = path + '/'

        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path in excluded_paths or other_path in excluded_paths:
            return False

        for x in excluded_paths:
            if x.endswith("*"):
                str_check = x[:-1]
                if path.startswith(str_check):
                    return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Get authorization header function"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

        return None

    def current_user(self, request=None) -> TypeVar('user'):
        """get current user"""
        return None

    def session_cookie(self, request=None):
        """get session cookie"""
        if request is None:
            return None

        sesion_cookie_name = os.environ.get("SESSION_NAME", "_my_session_id")
        cookie_value = request.cookies.get(sesion_cookie_name)
        return cookie_value
