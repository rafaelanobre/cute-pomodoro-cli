import time
import sys
import argparse
from pathlib import Path

WORK_MINS = 25
SHORT_BREAK_MINS = 5
LONG_BREAK_MINS = 15
NUMBER_OF_CYCLES = 4

COLORS = {
    "pink": "\033[95m",
    "blue": "\033[96m",
    "default": "\033[0m"
}
RESET = "\033[0m"

def load_ascii_art(theme, art_type):
    art_path = Path(__file__).parent / "images" / theme / f"{art_type}.txt"
    try:
        return art_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return "🍅"

def get_color_code(color_name):
    return COLORS.get(color_name, COLORS["default"])

def countdown(minutes, label, theme="default", color="pink"):
    seconds = minutes * 60
    color_code = get_color_code(color)

    if "Work Session" in label:
        ascii_art = load_ascii_art(theme, "work")
        print(f"{color_code}{ascii_art}{RESET}")

    print(f"{color_code}🍅 {label} started for {minutes} minutes! Stay focused! 🍅{RESET}")

    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer_display = f"{color_code}  {mins:02d}:{secs:02d}{RESET}"

        print(timer_display, end='\r')

        time.sleep(1)
        seconds -= 1

    if "Break" in label:
        if "Long" in label:
            ascii_art = load_ascii_art(theme, "long_break")
        else:
            ascii_art = load_ascii_art(theme, "short_break")
        print(f"\n{color_code}{ascii_art}{RESET}")

    print(f"\n{color_code}🎉 Time for a break! {label} finished. 🎉{RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Pomodoro Timer")
    parser.add_argument("--theme", default="default", choices=["default", "cats", "dogs"],
                       help="Choose a theme for the timer")
    parser.add_argument("--color", default="pink", choices=["pink", "blue", "default"],
                       help="Choose a color for the timer display")

    args = parser.parse_args()

    logo_path = Path(__file__).parent / "images" / "logo.txt"
    try:
        logo = logo_path.read_text(encoding='utf-8')
        color_code = get_color_code(args.color)
        print(f"{color_code}{logo}{RESET}")
    except FileNotFoundError:
        pass

    color_code = get_color_code(args.color)
    print(f"{color_code}Welcome to the Pomodoro Timer!{RESET}")

    try:
        for cycle in range(NUMBER_OF_CYCLES):
            countdown(WORK_MINS, f"Work Session {cycle + 1}", args.theme, args.color)

            if cycle < NUMBER_OF_CYCLES - 1:
                countdown(SHORT_BREAK_MINS, "Short Break", args.theme, args.color)
            else:
                countdown(LONG_BREAK_MINS, "Long Break", args.theme, args.color)

        color_code = get_color_code(args.color)
        print(f"{color_code}Pomodoro session complete! Great work! ✨{RESET}")

    except KeyboardInterrupt:
        print(f"\n👋 Timer stopped. See you next time!")
        sys.exit(0)

if __name__ == "__main__":
    main()