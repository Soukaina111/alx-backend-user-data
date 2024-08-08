#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method for validating if endpoint requires auth
        Returns:
            bool: True if the path requires authentication, False otherwise
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Get the length of the current path
        path_size = len(path)
        # If the path length is 0, return True (no authentication required)
        if path_size == 0:
            return True

        # Check if the last character of the path is a slash
        slash_path = True if path[path_size - 1] == '/' else False

        tmp_path = path
        if not slash_path:
            tmp_path += '/'

        # Iterate through the list of excluded paths
        for exc in excluded_paths:
            # Get the length of the current excluded path
            exc_size = len(exc)
            # If the excluded path length is 0, skip it
            if exc_size == 0:
                continue

            if exc[exc_size - 1] != '*':
                if tmp_path == exc:
                    return False
            else:
                if exc[:-1] == path[:exc_path - 1]:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method that handles authorization header
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates current user
        """
        return None
