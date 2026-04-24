from models import GamblerStatistics


class GameSessionManager:
    """
    Legacy session manager - not currently used in favor of simplified approach.
    Kept for reference and potential future expansion.
    """

    def __init__(self):
        self.active_sessions = {}
        self.completed_sessions = []

    def start_new_session(self, gambler_id, gambler_stats):
        """Start a new gaming session"""
        if gambler_id in self.active_sessions:
            raise Exception("Session already active for this gambler")

        self.active_sessions[gambler_id] = {
            "gambler_id": gambler_id,
            "stats": gambler_stats,
            "games_played": 0,
            "active": True
        }

        return self.active_sessions[gambler_id]

    def end_session(self, gambler_id):
        """End a gaming session"""
        if gambler_id not in self.active_sessions:
            raise Exception("No active session for this gambler")

        session = self.active_sessions.pop(gambler_id)
        session["active"] = False
        self.completed_sessions.append(session)

        return session

    def get_active_session(self, gambler_id):
        """Get active session for gambler"""
        return self.active_sessions.get(gambler_id)

    def continue_session(self, gambler_id, betting_service, rounds, bet_amount):
        session = self.active_sessions.get(gambler_id)

        if not session:
            raise Exception("No active session")

        for _ in range(rounds):
            if session.status != session.status.ACTIVE:
                break

            session.play_game(betting_service, bet_amount)

        if session.status != session.status.ACTIVE:
            self._end_session(gambler_id)

        return session.summary()

    # PAUSE
    def pause_session(self, gambler_id):
        self.active_sessions[gambler_id].pause()

    # RESUME
    def resume_session(self, gambler_id):
        self.active_sessions[gambler_id].resume()

    # END
    def end_session(self, gambler_id):
        session = self.active_sessions.pop(gambler_id)
        session._end(session.status, "MANUAL")
        self.completed_sessions.append(session)

    def _end_session(self, gambler_id):
        session = self.active_sessions.pop(gambler_id)
        self.completed_sessions.append(session)