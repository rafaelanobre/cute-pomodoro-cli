import time
import sys

WORK_MINS = 25
SHORT_BREAK_MINS = 5
LONG_BREAK_MINS = 15
NUMBER_OF_CYCLES = 4

def countdown(minutes, label):
    seconds = minutes * 60
    print(f"🍅 {label} started for {minutes} minutes! Stay focused! 🍅")

    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer_display = f"  {mins:02d}:{secs:02d}"

        print(timer_display, end='\r')

        time.sleep(1)
        seconds -= 1

    print(f"\n🎉 Time for a break! {label} finished. 🎉\n")

def main():
    print("Welcome to the Pomodoro Timer!")
    try:
        for cycle in range(NUMBER_OF_CYCLES):
            # Work session
            countdown(WORK_MINS, f"Work Session {cycle + 1}")

            # Break session
            if cycle < NUMBER_OF_CYCLES - 1:
                countdown(SHORT_BREAK_MINS, "Short Break")
            else:
                countdown(LONG_BREAK_MINS, "Long Break")

        print("Pomodoro session complete! Great work! ✨")

    except KeyboardInterrupt:
        print("\n👋 Timer stopped. See you next time!")
        sys.exit(0)

if __name__ == "__main__":
    main()