#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ 
    Hashes the provided password using bcrypt with a salt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        bytes: A salted, hashed password as a byte string.
    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ 
    Validates whether the provided password matches the hashed password.

    Args:
        hashed_password: A byte string representing the hashed password.
        password: A string representing the password to be validated.

    Returns:
        bool: True if the provided password matches the hashed password, False otherwise.
    """
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
