#!/usr/bin/env python3
"""Session auth class"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a session id"""
        if user_id is None or type(user_id) is not str:
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """gets user_id for session id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value:"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))  # nopep8
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """delete current session"""
        if request is None:
            return False
        if not self.session_cookie(request):
            return False
        if not self.user_id_for_session_id(self.session_cookie(request)):
            return False

        del self.user_id_by_session_id[self.session_cookie(request)]

        return True
