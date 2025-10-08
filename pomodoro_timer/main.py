from pomodoro_timer.config import PomodoroConfig
from pomodoro_timer.theme_manager import ThemeManager
from pomodoro_timer.timer import PomodoroTimer

def main():
    config: PomodoroConfig = PomodoroConfig.from_args()
    theme_manager = ThemeManager()
    timer = PomodoroTimer(config, theme_manager)

    timer.start()

if __name__ == "__main__":
    main()