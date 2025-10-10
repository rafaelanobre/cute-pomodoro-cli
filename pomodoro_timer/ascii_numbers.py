

class ASCIINumbers:
    """Generates large ASCII art representations of numbers and colons."""

    DIGITS = {
        '0': [
            " ██████╗ ",
            "██╔═══██╗",
            "██║   ██║",
            "██║   ██║",
            "╚██████╔╝",
            " ╚═════╝ "
        ],
        '1': [
            " ██╗",
            "███║",
            "╚██║",
            " ██║",
            " ██║",
            " ╚═╝"
        ],
        '2': [
            "██████╗ ",
            "╚════██╗",
            " █████╔╝",
            "██╔═══╝ ",
            "███████╗",
            "╚══════╝"
        ],
        '3': [
            "██████╗ ",
            "╚════██╗",
            " █████╔╝",
            " ╚═══██╗",
            "██████╔╝",
            "╚═════╝ "
        ],
        '4': [
            "██╗  ██╗",
            "██║  ██║",
            "███████║",
            "╚════██║",
            "     ██║",
            "     ╚═╝"
        ],
        '5': [
            "███████╗",
            "██╔════╝",
            "███████╗",
            "╚════██║",
            "███████║",
            "╚══════╝"
        ],
        '6': [
            " ██████╗ ",
            "██╔════╝ ",
            "███████╗ ",
            "██╔═══██╗",
            "╚██████╔╝",
            " ╚═════╝ "
        ],
        '7': [
            "███████╗",
            "╚════██║",
            "    ██╔╝",
            "   ██╔╝ ",
            "   ██║  ",
            "   ╚═╝  "
        ],
        '8': [
            " ██████╗ ",
            "██╔═══██╗",
            "╚█████╔╝ ",
            "██╔═══██╗",
            "╚██████╔╝",
            " ╚═════╝ "
        ],
        '9': [
            " ██████╗ ",
            "██╔═══██╗",
            "╚██████╔╝",
            " ╚════██║",
            " █████╔╝ ",
            " ╚════╝  "
        ],
        ':': [
            "   ",
            "██╗",
            "╚═╝",
            "██╗",
            "╚═╝",
            "   "
        ]
    }

    @classmethod
    def render_time(cls, minutes: int, seconds: int) -> str:
        """ASCII art number generator for large countdown display."""
        time_str = f"{minutes:02d}:{seconds:02d}"
        digit_lines = [cls.DIGITS[char] for char in time_str]

        lines = []
        for row in range(6):
            line = " ".join(digit_lines[i][row] for i in range(len(time_str)))
            lines.append(line)

        return "\n".join(lines)