import curses

from pomodoro_timer.config import PomodoroConfig
from pomodoro_timer.sound_manager import SoundManager
from pomodoro_timer.statistics import StatisticsManager
from pomodoro_timer.statistics_ui import StatisticsUI
from pomodoro_timer.storage import StorageManager
from pomodoro_timer.theme_manager import ThemeManager
from pomodoro_timer.timer import PomodoroTimer

def main():
    config: PomodoroConfig = PomodoroConfig.from_args()
    theme_manager = ThemeManager()
    sound_manager = SoundManager()
    storage_manager = StorageManager()
    statistics_manager = StatisticsManager(storage_manager)

    if config.show_stats:
        stats_ui = StatisticsUI(statistics_manager, theme_manager, config)
        curses.wrapper(stats_ui.run)
    else:
        timer = PomodoroTimer(
            config,
            theme_manager,
            sound_manager,
            statistics_manager
        )
        timer.start()

if __name__ == "__main__":
    main()