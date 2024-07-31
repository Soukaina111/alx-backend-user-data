#!/usr/bin/env python3
"""
Utility functions for hashing and verifying passwords using bcrypt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    # Encode the password to bytes before hashing
    password_bytes = password.encode('utf-8')
    # Generate a salt and hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates the provided password against the given hashed password.
    """
    # Encode the password to bytes before checking
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)
