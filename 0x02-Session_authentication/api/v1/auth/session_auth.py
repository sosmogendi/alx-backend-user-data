#!/usr/bin/env python3
""" Module for Session Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Session Authentication Class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session for the given user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The session ID generated.
        """

        if not isinstance(user_id, str) or user_id is None:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated with a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or None if not found.
        """

        if not isinstance(session_id, str) or session_id is None:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns the current user based on the session ID extracted from the request.

        Args:
            request: The request object.

        Returns:
            User: The User object associated with the current session ID.
        """

        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroys the user session, effectively logging the user out.

        Args:
            request: The request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """

        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except KeyError:
            pass

        return True
