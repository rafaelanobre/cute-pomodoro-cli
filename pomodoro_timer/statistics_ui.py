import curses

from pomodoro_timer.config import PomodoroConfig
from pomodoro_timer.statistics import StatisticsManager
from pomodoro_timer.theme_manager import ThemeManager


class StatisticsUI:
    """Displays Pomodoro session statistics in a curses interface."""

    def __init__(self, stats_manager: StatisticsManager, theme_manager: ThemeManager, config: PomodoroConfig):
        self.stats_manager = stats_manager
        self.theme_manager = theme_manager
        self.config = config
        self.current_period = 'today'

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)
        self._init_colors()

        while True:
            self._display(stdscr)
            if not self._handle_input(stdscr):
                break

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        color_code = self.theme_manager.get_curses_color(self.config.color)
        curses.init_pair(1, color_code, -1)

    def _display(self, stdscr):
        stdscr.clear()
        height, _ = stdscr.getmaxyx()

        totals = self.stats_manager.get_totals(self.current_period)
        period_title = self.current_period.replace('_', ' ').title()

        total_work_minutes = self._calculate_work_minutes()

        current_y = height // 3

        self._center_text(stdscr, current_y, f"📊 POMODORO STATISTICS - {period_title}", 1)
        current_y += 1

        motivation = self._get_motivation_message(total_work_minutes, period_title)
        self._center_text(stdscr, current_y, motivation)
        current_y += 3

        self._center_text(stdscr, current_y, f"Work Sessions: {totals['work']}", 1)
        current_y += 1
        self._center_text(stdscr, current_y, f"Short Breaks: {totals['short_break']}", 1)
        current_y += 1
        self._center_text(stdscr, current_y, f"Long Breaks: {totals['long_break']}", 1)

        self._center_text(stdscr, height - 3, "[1] Today  [2] Week  [3] Month  [4] All Time  [Q] Quit")

        stdscr.refresh()

    def _center_text(self, stdscr, y, text, color_pair=0):
        _, width = stdscr.getmaxyx()
        x = (width - len(text)) // 2
        stdscr.addstr(y, x, text, curses.color_pair(color_pair))

    def _calculate_work_minutes(self):
        sessions = self.stats_manager.get_sessions(
            start_date=self.stats_manager._get_period_start(self.current_period)
            if self.current_period != 'all_time' else None
        )

        total_minutes = sum(
            session['duration']
            for session in sessions
            if session['type'] == 'work'
        )
        return total_minutes

    def _get_motivation_message(self, minutes, period):
        if minutes == 0:
            return f"No work sessions {period.lower()} yet. Time to lock in!"

        return f"You focused for {minutes} minutes! Keep this momentum going!"

    def _handle_input(self, stdscr):
        key = stdscr.getch()

        if key == ord('1'):
            self.current_period = 'today'
        elif key == ord('2'):
            self.current_period = 'week'
        elif key == ord('3'):
            self.current_period = 'month'
        elif key == ord('4'):
            self.current_period = 'all_time'
        elif key in [ord('q'), ord('Q'), 27]:
            return False

        return True