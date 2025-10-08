import argparse


class PomodoroConfig:
    def __init__(self):
        self.work_mins = 25
        self.short_break_mins = 5
        self.long_break_mins = 15
        self.number_of_cycles = 4
        self.theme = "default"
        self.color = "pink"

    @classmethod
    def from_args(cls):
        config = cls()
        config._parse_args()
        return config

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="Pomodoro Timer")
        parser.add_argument(
            "--theme",
            default=self.theme,
            choices=["default", "cats", "dogs"],
            help="Choose a theme for the timer"
        )
        parser.add_argument(
            "--color",
            default=self.color,
            choices=["pink", "blue", "default"],
            help="Choose a color for the timer display"
        )

        args = parser.parse_args()

        self.theme = args.theme
        self.color = args.color
