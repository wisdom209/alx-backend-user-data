#!/usr/bin/env python3
"""Basic authentication module"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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
        else:
            email, password = decoded_base64_authorization_header.split(':', 1)
            return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # nopep8
        """Returns user instance"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        user = User.search({'email': user_email})
        if not user or len(user) == 0 or not user[0]:
            return None
        user = user[0]
        if not user.is_valid_password(user_pwd):
            return None
        else:
            return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve user instance for a request"""
        if 'Authorization' not in request.headers:
            return None
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = self.extract_base64_authorization_header(auth_header)
            if auth_token:
                decoded_token = self.decode_base64_authorization_header(
                    auth_token)
                if decoded_token:
                    user_credentials = self.extract_user_credentials(
                        decoded_token)
                    if user_credentials[0] is not None:
                        user = self.user_object_from_credentials(
                            user_credentials[0], user_credentials[1])
                        return user
