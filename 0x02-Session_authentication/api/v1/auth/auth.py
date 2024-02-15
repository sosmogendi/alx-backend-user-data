#!/usr/bin/env python3
""" Module for API Authentication
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """ Class to Handle API Authentication """

    def require_auth(self, endpoint_path: str, excluded_paths: List[str]) -> bool:
        """ Validate if authentication is required for the given endpoint path """
        if endpoint_path is None or excluded_paths is None or excluded_paths == []:
            return True

        path_length = len(endpoint_path)
        if path_length == 0:
            return True

        ends_with_slash = True if endpoint_path[path_length - 1] == '/' else False

        temp_path = endpoint_path
        if not ends_with_slash:
            temp_path += '/'

        for excluded_path in excluded_paths:
            excluded_length = len(excluded_path)
            if excluded_length == 0:
                continue

            if excluded_path[excluded_length - 1] != '*':
                if temp_path == excluded_path:
                    return False
            else:
                if excluded_path[:-1] == endpoint_path[:excluded_length - 1]:
                    return False

        return True

    def authorization_header(self, request_obj=None) -> str:
        """ Retrieve the Authorization header from the Flask request object """
        if request_obj is None:
            return None

        return request_obj.headers.get("Authorization", None)

    def current_user(self, request_obj=None) -> TypeVar('User'):
        """ Validate the current user """
        return None

