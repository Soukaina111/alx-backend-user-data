#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """ Creates password hash
        Args:
        password: user password
        Return:
        -hashed password
        """
        us_pwd = password.encode()
        return bcrypt.hashpw(us_pwd, bcrypt.gensalt())
