from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv

class SessionExpAuth(SessionAuth):
    """Class for Session Authentication with Expiration"""

    def __init__(self):
        """Constructor method for SessionExpAuth"""
        try:
            session_duration = int(getenv('SESSION_DURATION', '0'))
        except ValueError:
            session_duration = 0

        self.session_duration = max(0, session_duration)

    def create_session(self, user_id=None):
        """Create a session with expiration"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }

        self.user_id_by_session_id[session_id] = session_data

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id from session_id, considering expiration"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_data = self.user_id_by_session_id[session_id]
        created_at = session_data.get('created_at')

        if created_at is None:
            return None

        if self.session_duration > 0:
            expiration_time = created_at + timedelta(seconds=self.session_duration)
            if expiration_time < datetime.utcnow():
                return None

        return session_data.get('user_id')
