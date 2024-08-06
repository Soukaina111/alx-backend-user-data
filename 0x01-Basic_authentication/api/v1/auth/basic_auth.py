#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Authentication Class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract Base 64 Authorization Header """
        # Check if the authorization header is provided
        if authorization_header is None:
            return None

        # Check if the authorization header is a string
        if not isinstance(authorization_header, str):
            return None

        # Check if the authorization header starts with "Basic "
        if not authorization_header.startswith("Basic "):
            return None

        # Extract the encoded part of the authorization header
        encoded = authorization_header.split(' ', 1)[1]

        return encoded

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decodes the value of a base64 string """
        # Check if the base64 authorization header is provided
        if base64_authorization_header is None:
            return None

        # Check if the base64 authorization header is a string
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Encode the base64 authorization header to bytes
            encoded = base64_authorization_header.encode('utf-8')
            # Decode the base64 bytes to a string
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Returns the user email and password from the
        Base64 decoded value
        """
        # Check if the decoded base64 authorization header is provided
        if decoded_base64_authorization_header is None:
            return None, None

        # Check if the decoded base64 authorization header is a string
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        # Check if the decoded base64 authorization header contains a colon
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the decoded base64 authorization header into email and password
        credentials = decoded_base64_authorization_header.split(':', 1)

        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his
        email and password
        """
        # Check if the user email is provided and is a string
        if user_email is None or not isinstance(user_email, str):
            return None

        # Check if the user password is provided and is a string
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Search for users with the given email
            found_users = User.search({'email': user_email})
        except Exception:
            return None

        # Check if the password is valid for any of the found users
        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        # Get the authorization header from the request
        auth_header = self.authorization_header(request)

        # Check if the authorization header is provided
        if not auth_header:
            return None

        # Extract the base64 encoded part of the authorization header
        encoded = self.extract_base64_authorization_header(auth_header)

        # Check if the base64 encoded part is provided
        if not encoded:
            return None

        # Decode the base64 encoded part
        decoded = self.decode_base64_authorization_header(encoded)

        # Check if the decoded value is provided
        if not decoded:
            return None

        # Extract the user email and password from the decoded value
        email, pwd = self.extract_user_credentials(decoded)

        # Check if the user email and password are provided
        if not email or not pwd:
            return None

        # Get the user object based on the email and password
        user = self.user_object_from_credentials(email, pwd)

        return user
