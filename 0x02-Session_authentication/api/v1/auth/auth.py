#!/usr/bin/env python3
""" Module for Authentication Handling """
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Class for managing API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required for a given path """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        is_slash_path = path[-1] == '/'  # Check if the path ends with a slash

        tmp_path = path if is_slash_path else path + '/'
        
        for exc in excluded_paths:
            if exc.endswith('*'):
                if exc[:-1] == path[:len(exc) - 1]:
                    return False
            elif tmp_path == exc:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieves the Authorization header from the request """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates the current user """
        return None

    def session_cookie(self, request=None):
        """ Returns the value of the session cookie from the request """
        if request is None:
            return None

        session_name = getenv("SESSION_NAME")

        if session_name is None:
            return None

        session_id = request.cookies.get(session_name)

        return session_id
