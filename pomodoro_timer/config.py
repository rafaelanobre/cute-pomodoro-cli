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
        parser.add_argument(
            "--work",
            type=int,
            default=self.work_mins,
            metavar="MINUTES",
            help="Duration of work sessions in minutes (default: 25)"
        )
        parser.add_argument(
            "--short-break",
            type=int,
            default=self.short_break_mins,
            metavar="MINUTES",
            help="Duration of short breaks in minutes (default: 5)"
        )
        parser.add_argument(
            "--long-break",
            type=int,
            default=self.long_break_mins,
            metavar="MINUTES",
            help="Duration of long break in minutes (default: 15)"
        )
        parser.add_argument(
            "--cycles",
            type=int,
            default=self.number_of_cycles,
            metavar="NUMBER",
            help="Number of work/break cycles before long break (default: 4)"
        )

        args = parser.parse_args()

        self.theme = args.theme
        self.color = args.color
        self.work_mins = args.work
        self.short_break_mins = args.short_break
        self.long_break_mins = args.long_break
        self.number_of_cycles = args.cycles
