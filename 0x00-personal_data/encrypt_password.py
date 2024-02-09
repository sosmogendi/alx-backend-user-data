#!/usr/bin/env python3
"""
Module for password encryption and validation
"""
import bcrypt

def encrypt_password(plain_password: str) -> bytes:
    """Hashes a password using bcrypt"""
    encoded_password = plain_password.encode()
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password

def validate_password(hashed_password: bytes, plain_password: str) -> bool:
    """Checks if a password matches its hashed version"""
    return bcrypt.checkpw(plain_password.encode(), hashed_password)
