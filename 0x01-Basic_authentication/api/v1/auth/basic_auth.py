#!/usr/bin/env python3
""" Module for Basic Authentication """
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar

class BasicAuth(Auth):
    """ Class for Basic Authentication """

    def extract_base64_authorization_header(self, auth_header_str: str) -> str:
        """ Extracts Base64 Authorization Header """
        if auth_header_str is None:
            return None

        if not isinstance(auth_header_str, str):
            return None

        if not auth_header_str.startswith("Basic "):
            return None

        encoded_part = auth_header_str.split(' ', 1)[1]

        return encoded_part

    def decode_base64_authorization_header(self, encoded_str: str) -> str:
        """ Decodes the value of a base64 string """
        if encoded_str is None:
            return None
        if not isinstance(encoded_str, str):
            return None

        try:
            encoded_bytes = encoded_str.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            decoded_str = decoded_bytes.decode('utf-8')
        except BaseException:
            return None

        return decoded_str

    def extract_user_credentials(self, decoded_auth_str: str) -> (str, str):
        """
        Returns the user email and password from the
        Base64 decoded value
        """

        if decoded_auth_str is None:
            return None, None

        if not isinstance(decoded_auth_str, str):
            return None, None

        if ':' not in decoded_auth_str:
            return None, None

        credentials = decoded_auth_str.split(':', 1)

        return credentials[0], credentials[1]

    def user_object_from_credentials(self, email_str: str, pwd_str: str) -> TypeVar('User'):
        """
        Returns the User instance based on the user's
        email and password
        """
        if email_str is None or not isinstance(email_str, str):
            return None

        if pwd_str is None or not isinstance(pwd_str, str):
            return None

        try:
            found_users = User.search({'email': email_str})
        except Exception:
            return None

        for user in found_users:
            if user.is_valid_password(pwd_str):
                return user

        return None

    def current_user(self, req=None) -> TypeVar('User'):
        """ Overrides Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(req)

        if not auth_header:
            return None

        encoded_part = self.extract_base64_authorization_header(auth_header)

        if not encoded_part:
            return None

        decoded_str = self.decode_base64_authorization_header(encoded_part)

        if not decoded_str:
            return None

        email, pwd = self.extract_user_credentials(decoded_str)

        if not email or not pwd:
            return None

        user = self.user_object_from_credentials(email, pwd)

        return user
