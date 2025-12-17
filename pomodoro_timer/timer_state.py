from enum import Enum, auto


class TimerState(Enum):
    """Represents the current state of the Pomodoro timer."""
    RUNNING = auto()
    PAUSED = auto()
    SKIPPED = auto()
    QUIT = auto()
    COMPLETED = auto()
