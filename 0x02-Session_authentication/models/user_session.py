#!/usr/bin/env python3
"""Module for managing user sessions"""
from models.base import Base

class UserSession(Base):
    """Class representing a user session"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
