import time
import curses

from typing import Optional
from _curses import window

from pomodoro_timer.config import PomodoroConfig
from pomodoro_timer.statistics import StatisticsManager
from pomodoro_timer.theme_manager import ThemeManager
from pomodoro_timer.ascii_numbers import ASCIINumbers
from pomodoro_timer.progress_bar import ProgressBar
from pomodoro_timer.sound_manager import SoundManager
from pomodoro_timer.timer_state import TimerState


class PomodoroTimer:
    """Full-screen TUI Pomodoro timer using curses for professional display."""

    def __init__(
            self,
            config: PomodoroConfig,
            theme_manager: ThemeManager,
            sound_manager: SoundManager,
            statistics_manager: StatisticsManager,
    ):
        self.config = config
        self.theme_manager = theme_manager
        self.sound_manager = sound_manager
        self.statistics_manager = statistics_manager
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
                work_result = self._run_work_session(cycle + 1)
                if work_result == TimerState.QUIT:
                    self._show_exit_message()
                    return

                if cycle < self.config.number_of_cycles - 1:
                    break_result = self._run_short_break(cycle + 1)
                    if break_result == TimerState.QUIT:
                        self._show_exit_message()
                        return
                else:
                    long_break_result = self._run_long_break()
                    if long_break_result == TimerState.QUIT:
                        self._show_exit_message()
                        return

            self._show_completion_screen()

        except KeyboardInterrupt:
            self._show_exit_message()

    def _initialize_curses(self):
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)
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

    def _render_countdown_display(self, seconds: int, total_seconds: int,
                                   progress_bar, static_lines: list,
                                   static_height: int, layout_start_y: int,
                                   last_milestone: str) -> str:
        """Render the countdown display and return the current milestone."""
        height, width = self._get_screen_dimensions()

        mins, secs = divmod(seconds, 60)
        ascii_timer = ASCIINumbers.render_time(mins, secs)
        timer_lines = ascii_timer.split('\n')

        elapsed_seconds = total_seconds - seconds
        progress_display = progress_bar.render(elapsed_seconds, total_seconds)
        percentage = (elapsed_seconds / total_seconds) * 100 if total_seconds > 0 else 0
        milestone = progress_bar.get_milestone_message(percentage)

        attr = self.color_pair | curses.A_BOLD
        ascii_timer_height = 6

        current_y = layout_start_y

        max_static_width = max(len(line.rstrip()) for line in static_lines) if static_lines else 0
        static_block_x = max(0, (width - max_static_width) // 2)

        for i, line in enumerate(static_lines):
            y_pos = current_y + i
            if 0 <= y_pos < height:
                self.stdscr.move(y_pos, 0)
                self.stdscr.clrtoeol()
                stripped_line = line.rstrip()
                self._safe_addstr(y_pos, static_block_x, stripped_line, attr)

        timer_start_y = current_y + static_height + 2

        max_timer_width = max(len(line) for line in timer_lines) if timer_lines else 0
        timer_block_x = max(0, (width - max_timer_width) // 2)

        for i, line in enumerate(timer_lines):
            y_pos = timer_start_y + i
            if 0 <= y_pos < height:
                self.stdscr.move(y_pos, 0)
                self.stdscr.clrtoeol()
                self._safe_addstr(y_pos, timer_block_x, line, attr)

        progress_start_y = timer_start_y + ascii_timer_height + 2

        if milestone:
            milestone_y = progress_start_y
            if 0 <= milestone_y < height:
                self.stdscr.move(milestone_y, 0)
                self.stdscr.clrtoeol()
                line_x = max(0, (width - len(milestone)) // 2)
                self._safe_addstr(milestone_y, line_x, milestone, self.color_pair)
        elif last_milestone:
            milestone_y = progress_start_y
            if 0 <= milestone_y < height:
                self.stdscr.move(milestone_y, 0)
                self.stdscr.clrtoeol()

        progress_y = progress_start_y + 2 if milestone else progress_start_y
        if 0 <= progress_y < height:
            self.stdscr.move(progress_y, 0)
            self.stdscr.clrtoeol()
            line_x = max(0, (width - len(progress_display)) // 2)
            self._safe_addstr(progress_y, line_x, progress_display, attr)

        controls = "Press [P] to Pause  |  Press Ctrl+C to quit"
        if height - 2 > progress_y + 3:
            self.stdscr.move(height - 2, 0)
            self.stdscr.clrtoeol()
            self._safe_addstr(height - 2, (width - len(controls)) // 2, controls, curses.A_DIM)

        self.stdscr.refresh()
        return milestone

    def _show_pause_menu(self, elapsed_seconds: int, total_seconds: int,
                        session_type: str) -> str:
        """Display pause menu overlay and return user's choice."""
        height, width = self._get_screen_dimensions()

        elapsed_minutes = elapsed_seconds / 60
        total_minutes = total_seconds / 60
        percentage = (elapsed_seconds / total_seconds * 100) if total_seconds > 0 else 0

        menu_width = 60
        menu_height = 14
        menu_y = (height - menu_height) // 2
        menu_x = (width - menu_width) // 2

        menu_lines = [
            "╔" + "═" * (menu_width - 2) + "╗",
            "║" + " " * (menu_width - 2) + "║",
            "║" + "TIMER PAUSED".center(menu_width - 2) + "║",
            "║" + " " * (menu_width - 2) + "║",
            "║" + f"Session: {session_type.replace('_', ' ').title()}".center(menu_width - 2) + "║",
            "║" + f"Progress: {elapsed_minutes:.1f} / {total_minutes:.0f} min ({percentage:.0f}%)".center(menu_width - 2) + "║",
            "║" + " " * (menu_width - 2) + "║",
            "║" + "[R] Resume Timer".center(menu_width - 2) + "║",
            "║" + "[S] Skip to Next Session".center(menu_width - 2) + "║",
            "║" + "[T] Restart Current Session".center(menu_width - 2) + "║",
            "║" + "[Q] Quit Entirely".center(menu_width - 2) + "║",
            "║" + " " * (menu_width - 2) + "║",
            "╚" + "═" * (menu_width - 2) + "╝",
        ]

        attr = self.color_pair | curses.A_BOLD
        for i, line in enumerate(menu_lines):
            y = menu_y + i
            if 0 <= y < height:
                self._safe_addstr(y, menu_x, line, attr)

        self.stdscr.refresh()

        # Temporarily enable blocking input for menu
        self.stdscr.nodelay(False)
        while True:
            key = self.stdscr.getch()

            if key in [ord('r'), ord('R'), ord('p'), ord('P')]:
                self.stdscr.nodelay(True)  # Restore non-blocking
                return 'resume'
            elif key in [ord('s'), ord('S')]:
                self.stdscr.nodelay(True)
                return 'skip'
            elif key in [ord('t'), ord('T')]:
                self.stdscr.nodelay(True)
                return 'restart'
            elif key in [ord('q'), ord('Q')]:
                self.stdscr.nodelay(True)
                return 'quit'

    def _run_countdown(self, minutes: int, session_display: str,
                       session_type: str, ascii_art: str = "") -> TimerState:
        """Run countdown with pause/resume capability."""
        total_seconds = minutes * 60
        seconds = total_seconds
        state = TimerState.RUNNING

        height, width = self._get_screen_dimensions()
        progress_bar_width = min(60, width - 20)
        progress_bar = ProgressBar(width=progress_bar_width)

        self._clear_screen()

        if ascii_art:
            static_content = f"{ascii_art}\n\n{session_display}"
        else:
            static_content = session_display

        static_lines = static_content.split('\n')
        static_height = len(static_lines)

        ascii_timer_height = 6
        progress_bar_height = 3
        spacing = 4

        total_layout_height = static_height + spacing + ascii_timer_height + spacing + progress_bar_height
        layout_start_y = max(0, (height - total_layout_height) // 2)

        last_milestone = ""

        while seconds > 0 and state == TimerState.RUNNING:
            last_milestone = self._render_countdown_display(
                seconds, total_seconds, progress_bar, static_lines,
                static_height, layout_start_y, last_milestone
            )

            # Non-blocking sleep with input checking (10 x 0.1s = 1 second)
            for _ in range(10):
                time.sleep(0.1)
                key = self.stdscr.getch()

                if key in [ord('p'), ord('P')]:
                    state = TimerState.PAUSED
                    elapsed_seconds = total_seconds - seconds

                    menu_result = self._show_pause_menu(
                        elapsed_seconds, total_seconds, session_type
                    )

                    if menu_result == 'resume':
                        state = TimerState.RUNNING
                        # Redraw the screen after resuming
                        self._clear_screen()
                    elif menu_result == 'skip':
                        # Record partial session before skipping
                        elapsed_minutes = elapsed_seconds / 60
                        if elapsed_minutes >= 1:
                            self.statistics_manager.record_session(
                                session_type, elapsed_minutes
                            )
                        return TimerState.SKIPPED
                    elif menu_result == 'restart':
                        # Reset to beginning
                        seconds = total_seconds
                        state = TimerState.RUNNING
                        self._clear_screen()
                    elif menu_result == 'quit':
                        # Record partial session before quitting
                        elapsed_minutes = elapsed_seconds / 60
                        if elapsed_minutes >= 1:
                            self.statistics_manager.record_session(
                                session_type, elapsed_minutes
                            )
                        return TimerState.QUIT

                    break  # Exit the 0.1s sleep loop

            if state == TimerState.RUNNING:
                seconds -= 1

        return TimerState.COMPLETED if seconds == 0 else state

    def _run_work_session(self, cycle: int) -> TimerState:
        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "work")
        message = f"🍅 Work Session {cycle} - {self.config.work_mins} minutes\nStay focused!"

        self._show_session_intro(ascii_art, message)
        result = self._run_countdown(self.config.work_mins, message, "work", ascii_art)

        if result == TimerState.COMPLETED:
            self.statistics_manager.record_session("work", self.config.work_mins)
            self.sound_manager.play_notification()

        return result

    def _run_short_break(self, cycle: int) -> TimerState:
        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "short_break")
        message = f"☕ Short Break {cycle} - {self.config.short_break_mins} minutes\nTake a short break!"

        self._show_session_intro(ascii_art, message)
        result = self._run_countdown(self.config.short_break_mins, message, "short_break", ascii_art)

        if result == TimerState.COMPLETED:
            self.statistics_manager.record_session("short_break", self.config.short_break_mins)
            self.sound_manager.play_notification()

        return result

    def _run_long_break(self) -> TimerState:
        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "long_break")
        message = f"🎉 Work done! Long Break - {self.config.long_break_mins} minutes\nYou've earned it!"

        self._show_session_intro(ascii_art, message)
        result = self._run_countdown(self.config.long_break_mins, message, "long_break", ascii_art)

        if result == TimerState.COMPLETED:
            self.statistics_manager.record_session("long_break", self.config.long_break_mins)
            self.sound_manager.play_notification()

        return result

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