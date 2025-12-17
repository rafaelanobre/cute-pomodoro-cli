from datetime import datetime, timedelta
from collections import Counter
from pomodoro_timer.storage import StorageManager


class StatisticsManager:
    """Manages users statistics for the Pomodoro Timer application."""

    def __init__(self, storage_manager: StorageManager) -> None:
        self.storage_manager = storage_manager
        self.data = storage_manager.load_json('stats.json')

        if not self.data or 'sessions' not in self.data:
            self.data = {"sessions": []}

    def record_session(self, session_type: str, duration: float) -> None:
        """Record a completed or partial session."""
        session = {
            "date": datetime.now().isoformat(),
            "type": session_type,
            "duration": round(duration, 2),
            "partial": duration % 1 != 0
        }
        self.data["sessions"].append(session)
        self.storage_manager.save_json('stats.json', self.data)

    def get_sessions(self, start_date: datetime = None, end_date: datetime = None) -> list:
        if start_date is None and end_date is None:
            return self.data["sessions"]

        filtered_sessions = []
        for session in self.data["sessions"]:
            session_date = datetime.fromisoformat(session["date"])

            if start_date and session_date < start_date:
                continue
            if end_date and session_date > end_date:
                continue

            filtered_sessions.append(session)

        return filtered_sessions

    def get_totals(self, period: str = 'all_time') -> dict:
        start_date = self._get_period_start(period) if period != 'all_time' else None
        sessions = self.get_sessions(start_date=start_date)

        session_types = [session["type"] for session in sessions]
        counts = Counter(session_types)

        return {
            "work": counts.get("work", 0),
            "short_break": counts.get("short_break", 0),
            "long_break": counts.get("long_break", 0),
            "total": len(sessions)
        }

    def _get_period_start(self, period: str) -> datetime:
        now = datetime.now()

        if period == 'today':
            return now.replace(hour=0, minute=0, second=0, microsecond=0)

        elif period == 'week':
            days_since_monday = now.weekday()
            start_of_week = now - timedelta(days=days_since_monday)
            return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        elif period == 'month':
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        return now