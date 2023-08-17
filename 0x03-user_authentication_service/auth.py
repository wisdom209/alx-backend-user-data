#!/usr/bin/env python3
"""auth class"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialize class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password).decode('utf-8')
            user = self._db.add_user(email, hashed_password)
            return user
        raise (ValueError(f"user {email} already exists"))

    def valid_login(self, email: str, password: str) -> bool:
        """validate  password"""
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode('utf-8')
            pass_hash = user.hashed_password.encode('utf-8')
            checkpass = bcrypt.checkpw(password, pass_hash)
            return checkpass
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create a session id"""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=user.session_id)
            return user.session_id
        except NoResultFound:
            pass


def _hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pass


def _generate_uuid() -> str:
    """generate unique id"""
    from uuid import uuid4
    unique_id = str(uuid4())
    return unique_id
