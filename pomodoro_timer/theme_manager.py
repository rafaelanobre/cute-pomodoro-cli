from pathlib import Path


class ThemeManager:
    def __init__(self):
        self.colors = {
            "pink": "\033[95m",
            "blue": "\033[96m",
            "default": "\033[0m"
        }
        self.reset = "\033[0m"

    def load_ascii_art(self, theme, art_type):
        art_path = Path(__file__).parent / "images" / theme / f"{art_type}.txt"
        try:
            return art_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            return "🍅"

    def get_color_code(self, color_name):
        return self.colors.get(color_name, self.colors["default"])

    def load_logo(self, color):
        logo_path = Path(__file__).parent / "images" / "logo.txt"
        try:
            logo = logo_path.read_text(encoding='utf-8')
            color_code = self.get_color_code(color)
            print(f"{color_code}{logo}{self.reset}")
        except FileNotFoundError:
            pass

    def apply_color(self, text, color_code):
        return f"{color_code}{text}{self.reset}"
