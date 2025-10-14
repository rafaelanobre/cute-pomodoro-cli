import curses
from pathlib import Path


class ThemeManager:
    """Manages ASCII art loading and color mappings for both ANSI and curses."""

    def __init__(self):
        self.ansi_colors = {
            "pink": "\033[95m",
            "blue": "\033[96m",
            "default": "\033[0m"
        }
        self.curses_colors = {
            "pink": curses.COLOR_MAGENTA,
            "blue": curses.COLOR_CYAN,
            "default": -1
        }
        self.reset = "\033[0m"

    def load_ascii_art(self, theme, art_type):
        art_path = Path(__file__).parent / "assets" / theme / f"{art_type}.txt"
        try:
            return art_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            return ""

    def load_logo(self):
        logo_path = Path(__file__).parent / "assets" / "logo.txt"
        try:
            return logo_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            return ""

    def get_ansi_color_code(self, color_name):
        return self.ansi_colors.get(color_name, self.ansi_colors["default"])

    def get_curses_color(self, color_name):
        return self.curses_colors.get(color_name, self.curses_colors["default"])

    def apply_ansi_color(self, text, color_code):
        return f"{color_code}{text}{self.reset}"
