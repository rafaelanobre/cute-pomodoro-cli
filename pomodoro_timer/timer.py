import time
import sys

from pomodoro_timer.config import PomodoroConfig
from pomodoro_timer.theme_manager import ThemeManager


class PomodoroTimer:
    def __init__(self, config: PomodoroConfig, theme_manager: ThemeManager):
        self.config = config
        self.theme_manager = theme_manager
        self.color = theme_manager.get_color_code(config.color)

    def start(self):
        self._display_welcome_message()

        try:
            for cycle in range(self.config.number_of_cycles):
                self._handle_work_session(cycle + 1)

                if cycle < self.config.number_of_cycles - 1:
                    self._handle_short_break(cycle + 1)
                else:
                    self._handle_long_break()

            self._display_completion_message()

        except KeyboardInterrupt:
            self._handle_interrupt()

    def countdown(self, minutes):
        seconds = minutes * 60

        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            timer_display = self.theme_manager.apply_color(f"  {mins:02d}:{secs:02d}", self.color)

            print(timer_display, end='\r')

            time.sleep(1)
            seconds -= 1


    def _display_welcome_message(self):
        self.theme_manager.load_logo(self.config.color)
        print(self.theme_manager.apply_color("Welcome to the Pomodoro Timer!", self.color))

    def _handle_work_session(self, cycle):
        minutes = self.config.work_mins
        label = f"Work Session {cycle}"

        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "work")
        print(self.theme_manager.apply_color(ascii_art, self.color))

        print(f"🍅 {label} started for {minutes} minutes! Stay focused! 🍅")

        self.countdown(minutes)

    def _handle_short_break(self, cycle):
        minutes = self.config.short_break_mins
        label = f"Short Break {cycle}"

        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "short_break")
        print(self.theme_manager.apply_color(ascii_art, self.color))

        print(f"☕ {label} started for {minutes} minutes! Take a short break! ☕")

        self.countdown(minutes)

    def _handle_long_break(self):
        minutes = self.config.long_break_mins
        label = "Long Break"

        ascii_art = self.theme_manager.load_ascii_art(self.config.theme, "long_break")
        print(self.theme_manager.apply_color(ascii_art, self.color))

        print(f"🎉 Work done! {label} started for {minutes} minutes! 🎉")

        self.countdown(minutes)

    def _handle_interrupt(self):
        print("\n👋 Timer stopped. See you next time!")
        sys.exit(0)

    def _display_completion_message(self):
        print(self.theme_manager.apply_color("✨ Pomodoro session complete! What did you created in this time? ✨", self.color))

        while True:
            restart = input(self.theme_manager.apply_color("Do you want to start another session? (y/n): ", self.color)).strip().lower()
            if restart == 'y':
                self.start()
                break
            elif restart == 'n':
                self._handle_interrupt()
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")