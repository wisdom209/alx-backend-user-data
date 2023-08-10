#!/usr/bin/env python3
"""authentication module"""
from flask import request
from typing import List, TypeVar


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
