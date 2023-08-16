#!/usr/bin/env python3
"""auth class"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pass
