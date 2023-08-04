#!/usr/bin/env python3
"""password encryption module"""
import bcrypt


def hash_password(password: str) -> bytes:
    "hash password"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check password match"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
