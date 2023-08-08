#!/usr/bin/env python3
"""Basic authentication module"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # nopep8
        """base64 decoding function"""
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_str = base64.b64decode(base64_authorization_header)
            return decoded_str.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # nopep8
        """Extract user credentials"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(':')[0]
        password = decoded_base64_authorization_header.split(':')[1]
        return (email, password)
