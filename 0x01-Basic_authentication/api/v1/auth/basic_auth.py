#!/usr/bin/env python3
"""Basic authentication module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # nopep8
        """extract authorization header function"""
        if not authorization_header:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        auth_password = authorization_header.split()[1]
        return auth_password
