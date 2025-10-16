from pathlib import Path
import json
import sys

class StorageManager:
    """Handles loading and saving of user settings and session data."""

    def __init__(self) -> None:
        self.base_dir: Path = Path.home() / ".pomodoro"
        self.ensure_data_dir()

    def ensure_data_dir(self) -> Path:
        path = Path(self.base_dir)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path

    def get_file_path(self, filename: str) -> Path:
        return self.base_dir / filename

    def load_json(self, file_path: str) -> dict:
        path = self.get_file_path(file_path)
        if not path.exists():
            return {}
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: Corrupted JSON file at {path}: {e}", file=sys.stderr)
            backup_path = path.with_suffix('.json.bak')
            path.rename(backup_path)
            print(f"Corrupted file backed up to {backup_path}", file=sys.stderr)
            return {}

    def save_json(self, file_path: str, data: dict) -> None:
        self.ensure_data_dir()
        path = self.get_file_path(file_path)

        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error writing to {path}: {e}", file=sys.stderr)
            raise