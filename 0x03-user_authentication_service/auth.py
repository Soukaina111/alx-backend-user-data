#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from typing import Optional


def _hash_password(password: str) -> bytes:
    """ Creates password hash
    Args:
    password: user password
    Return:
    -hashed password
    """
    us_pwd = password.encode()
    return bcrypt.hashpw(us_pwd, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """
        Initialize authentication instances
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user if it does not exist, hashes the password
        saves the user then returns the user. If user already exists
        raise a ValueError
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(user.email))
        except (InvalidRequestError, NoResultFound):
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Locates user by email, if existing checks password
        if password is valid returns True otherwise False
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            else:
                return False
        except (InvalidRequestError, NoResultFound):
            return False

    def _generate_uuid(self) -> str:
        """
        Generates a UUID and returns it's
        string representation
        """
        return str(uuid4())

    def create_session(self, email: str) -> Optional[str]:
        """
        Finds user corresponding to email, generate session_id and store it
        in the database as user session_id and return the session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return user.session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Returns corresponding user found in session_id or if not found
        None
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        updates the user corresponding to user_id as None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except Exception as e:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Finds user corresponding to email, and populate it's
        reset_token or raise a ValueError exception if user
        doesn't exists
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return user.reset_token
        except Exception as e:
            raise ValueError
