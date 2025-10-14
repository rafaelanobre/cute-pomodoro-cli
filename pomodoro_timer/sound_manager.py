import os
from pathlib import Path
from threading import Thread
from playsound import playsound


class SoundManager:
    """Manages sound playback for timer notifications."""

    def __init__(self):
        self.sound_path = self._get_sound_path()

    def _get_sound_path(self) -> str:
        current_dir = Path(__file__).parent
        sound_file = current_dir / "assets" / "timer-sound.mp3"
        return str(sound_file)

    def play_notification(self):
        if not os.path.exists(self.sound_path):
            return

        thread = Thread(target=self._play_sound, daemon=True)
        thread.start()

    def _play_sound(self):
        try:
            playsound(self.sound_path)
        except Exception:
            pass