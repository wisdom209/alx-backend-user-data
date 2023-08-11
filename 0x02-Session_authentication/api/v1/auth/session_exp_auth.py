#!/usr/bin/env python3
"""session expiration module"""
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """Session expiration class"""
    user_id_by_session_id = {}
    session_dictionary = {}

    def __init__(self) -> None:
        """init method"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """create the session"""
        from datetime import datetime
        try:
            session_id = super().create_session(user_id)
        except:
            session_id = None

        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = self.session_dictionary

        self.session_dictionary['user_id'] = user_id

        self.session_dictionary['created_at'] = datetime.now()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """get user id for session"""
        if not session_id:
            return None
        if not self.user_id_by_session_id.get(session_id):
            return None

        if self.session_duration <= 0:
            return self.session_dictionary['user_id']

        if not self.session_dictionary.get('created_at'):
            return None

        from datetime import datetime, timedelta
        expiration_date = self.session_dictionary['created_at'] + timedelta(
            seconds=self.session_duration)

        current_time = datetime.now()

        if current_time > expiration_date:
            return None

        return self.session_dictionary['user_id']
