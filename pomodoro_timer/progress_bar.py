class ProgressBar:
    """Generates visual progress bar representations for timer sessions."""

    def __init__(self, width: int = 50):
        self.width = width
        self.filled_char = "█"
        self.empty_char = "░"

    def render(self, elapsed_seconds: int, total_seconds: int) -> str:
        if total_seconds == 0:
            percentage = 0
        else:
            percentage = (elapsed_seconds / total_seconds) * 100

        rounded_percentage = round(percentage / 5) * 5

        filled_length = int(self.width * rounded_percentage / 100)
        empty_length = self.width - filled_length

        bar = self.filled_char * filled_length + self.empty_char * empty_length
        percentage_text = f"{rounded_percentage}%"

        return f"[{bar}] {percentage_text}"

    def get_milestone_message(self, percentage: float) -> str:
        if percentage >= 80:
            return "Almost done!"
        elif percentage >= 50:
            return "Halfway there!"
        elif percentage >= 25:
            return "Keep going!"
        return ""