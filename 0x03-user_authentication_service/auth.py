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

    def get_user_from_session_id(self, session_id: str) -> User:
        """get a user by their session id"""
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """destroys a session"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """get reset token"""
        try:
            user = self._db.find_user_by(email=email)
            new_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_token)
            return new_token
        except NoResultFound:
            raise ValueError


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
