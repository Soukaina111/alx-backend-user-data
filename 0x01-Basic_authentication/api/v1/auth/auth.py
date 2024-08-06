#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method for validating if endpoint requires auth
        Args:
            path (str): The current request path
            excluded_paths (List[str]): A list of paths that don't require authentication
        Returns:
            bool: True if the path requires authentication, False otherwise
        """
        # If any of the arguments are None or the list of excluded paths is empty, return True (no authentication required)
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Get the length of the current path
        path_size = len(path)
        # If the path length is 0, return True (no authentication required)
        if path_size == 0:
            return True

        # Check if the last character of the path is a slash
        slash_path = True if path[path_size - 1] == '/' else False

        # Create a temporary path variable, adding a slash if the original path didn't have one
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

            # Check if the last character of the excluded path is a wildcard (*)
            if exc[exc_size - 1] != '*':
                # If not, check if the temporary path matches the excluded path exactly
                if tmp_path == exc:
                    return False
            else:
                # If the last character is a wildcard, check if the excluded path prefix matches the temporary path
                if exc[:-1] == path[:exc_path - 1]:
                    return False

        # If no excluded path matched, return True (authentication required)
        return True

    def authorization_header(self, request=None) -> str:
        """ Method that handles authorization header
        Args:
            request (flask.Request, optional): The current request object. Defaults to None.
        Returns:
            str: The value of the 'Authorization' header, or None if the header is not present.
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates current user
        Args:
            request (flask.Request, optional): The current request object. Defaults to None.
        Returns:
            TypeVar('User'): The current user, or None if the user cannot be validated.
        """
        return None
