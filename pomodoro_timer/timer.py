import time
import curses

from typing import Optional
from _curses import window

from pomodoro_timer.config import PomodoroConfig
from pomodoro_timer.theme_manager import ThemeManager
from pomodoro_timer.ascii_numbers import ASCIINumbers


class PomodoroTimer:
    """Full-screen TUI Pomodoro timer using curses for professional display."""

    def __init__(self, config: PomodoroConfig, theme_manager: ThemeManager):
        self.config = config
        self.theme_manager = theme_manager
        self.stdscr: Optional[window] = None
        self.color_pair: int = 0

    def start(self):
        try:
            curses.wrapper(self._run_timer_loop)
        except KeyboardInterrupt:
            pass

    def _run_timer_loop(self, stdscr: window) -> None:
        self.stdscr = stdscr
        self._initialize_curses()

        try:
            self._show_welcome_screen()

            for cycle in range(self.config.number_of_cycles):
                self._run_work_session(cycle + 1)

                if cycle < self.config.number_of_cycles - 1:
                    self._run_short_break(cycle + 1)
                else:
                    self._run_long_break()

            self._show_completion_screen()

        except KeyboardInterrupt:
            self._show_exit_message()

    def _initialize_curses(self):
        curses.curs_set(0)
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)

        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            color_num = self.theme_manager.get_curses_color(self.config.color)
            curses.init_pair(1, color_num, -1)
            self.color_pair = curses.color_pair(1)

    def _get_screen_dimensions(self):
        height, width = self.stdscr.getmaxyx()
        return height, width

    def _clear_screen(self):
        self.stdscr.clear()
        self.stdscr.refresh()

    def _display_centered(self, content: str, y_offset: int = 0, bold: bool = False):
        height, width = self._get_screen_dimensions()
        lines = content.split('\n')
        start_y = max(0, (height - len(lines)) // 2 + y_offset)

        attr = self.color_pair
        if bold:
            attr |= curses.A_BOLD

        max_line_width = max(len(line.rstrip()) for line in lines) if lines else 0
        block_start_x = max(0, (width - max_line_width) // 2)

        for i, line in enumerate(lines):
            y_pos = start_y + i
            if 0 <= y_pos < height:
                stripped_line = line.rstrip()
                self._safe_addstr(y_pos, block_start_x, stripped_line, attr)

        self.stdscr.refresh()

    def _safe_addstr(self, y: int, x: int, text: str, attr: int = 0):
        try:
            self.stdscr.addstr(y, x, text, attr)
        except curses.error:
            pass

    def _show_welcome_screen(self):
        self._clear_screen()
        logo = self.theme_manager.load_logo()
        welcome_message = "Welcome to the Pomodoro Timer!"

        content = f"{logo}\n\n{welcome_message}" if logo else welcome_message
        self._display_centered(content)
        time.sleep(2)

    def _show_session_intro(self, ascii_art: str, message: str):
        self._clear_screen()
        content = f"{ascii_art}\n\n{message}" if ascii_art else message
        self._display_centered(content)
        time.sleep(2)

    def _run_countdown(self, minutes: int, session_display: str, ascii_art: str = ""):
        seconds = minutes * 60
        height, width = self._get_screen_dimensions()

        self._clear_screen()

        if ascii_art:
            static_content = f"{ascii_art}\n\n{session_display}"
        else:
            static_content = session_display

        static_lines = static_content.split('\n')
        static_height = len(static_lines)

        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            ascii_timer = ASCIINumbers.render_time(mins, secs)
            timer_lines = ascii_timer.split('\n')

            total_height = static_height + 2 + len(timer_lines)
            start_y = max(0, (height - total_height) // 2)

            attr = self.color_pair | curses.A_BOLD

            for i, line in enumerate(static_lines):
                y_pos = start_y + i
                if 0 <= y_pos < height:
                    x_pos = max(0, (width - len(line)) // 2)
                    self.stdscr.move(y_pos, 0)
                    self.stdscr.clrtoeol()
                    self._safe_addstr(y_pos, x_pos, line, attr)

            timer_start_y = start_y + static_height + 2
            for i, line in enumerate(timer_lines):
                y_pos = timer_start_y + i
                if 0 <= y_pos < height:
                    x_pos = max(0, (width - len(line)) // 2)
                    self.stdscr.move(y_pos, 0)
                    self.stdscr.clrtoeol()
                    self._safe_addstr(y_pos, x_pos, line, attr)

            controls = "Press Ctrl+C to quit"
            self.stdscr.move(height - 2, 0)
            self.stdscr.clrtoeol()
            self._safe_addstr(height - 2, (width - len(controls)) // 2, controls, curses.A_DIM)

            self.stdscr.refresh()
            time.sleep(1)
            seconds -= 1

    def _run_work_session(self, cycle: int):
        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "work")
        message = f"🍅 Work Session {cycle} - {self.config.work_mins} minutes\nStay focused! 🍅"

        self._show_session_intro(ascii_art, message)
        self._run_countdown(self.config.work_mins, message, ascii_art)

    def _run_short_break(self, cycle: int):
        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "short_break")
        message = f"☕ Short Break {cycle} - {self.config.short_break_mins} minutes\nTake a short break! ☕"

        self._show_session_intro(ascii_art, message)
        self._run_countdown(self.config.short_break_mins, message, ascii_art)

    def _run_long_break(self):
        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "long_break")
        message = f"🎉 Work done! Long Break - {self.config.long_break_mins} minutes\nYou've earned it! 🎉"

        self._show_session_intro(ascii_art, message)
        self._run_countdown(self.config.long_break_mins, message, ascii_art)

    def _show_completion_screen(self):
        self._clear_screen()
        completion_message = "✨ Pomodoro session complete! ✨\n\nWhat did you create in this time?"
        self._display_centered(completion_message)
        time.sleep(2)

        self._prompt_restart()

    def _prompt_restart(self):
        self._clear_screen()
        prompt = "Start another session? (y/n)"
        self._display_centered(prompt)

        curses.curs_set(1)
        curses.echo()

        height, width = self._get_screen_dimensions()

        while True:
            try:
                self.stdscr.move(height // 2 + 2, width // 2)
                self.stdscr.refresh()
                key = self.stdscr.getch()

                if key in [ord('y'), ord('Y')]:
                    curses.curs_set(0)
                    curses.noecho()
                    self._run_timer_loop(self.stdscr)
                    break
                elif key in [ord('n'), ord('N')]:
                    break
            except KeyboardInterrupt:
                break

    def _show_exit_message(self):
        self._clear_screen()
        self._display_centered("👋 Timer stopped.\nSee you next time!")
        self.stdscr.refresh()
        time.sleep(1)