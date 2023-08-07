from flask import request
"""authentication module"""
from typing import List, TypeVar


class Auth():
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""
        return False

    def authorization_header(self, request=None) -> str:
        """Get authorization header function"""
        return None

    def current_user(self, request=None) -> TypeVar('user'):
        return None
