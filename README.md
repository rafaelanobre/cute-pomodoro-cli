# CLI Pomodoro Timer

> A simple and adorable CLI Pomodoro timer to help you stay focused and productive, in your terminal!

Happy focusing! ✨

This little command-line tool follows the classic Pomodoro Technique: a 25-minute focused work session, followed by a 5-minute short break. After four sessions, you get a longer 15-minute break.

## Features

* **Classic Pomodoro Workflow:** Automatically cycles through work sessions and short/long breaks.
* **Minimalist Terminal UI:** A clean, in-place countdown timer that doesn't clutter your screen.
* **Friendly Notifications:** Cute ascii messages and sound to let you know when to start and stop.
* **Lightweight & Simple:** No complex dependencies, just pure Python and playsound.

## Installation

You can get the timer running on your local machine in just a few steps.

1.  **Clone the repository**

2.  **Create and activate a virtual environment:**
    ```bash
    # Using uv
    uv venv
    source .venv/bin/activate
    ```
    ```bash
    # Or using Python's built-in venv
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the project in editable mode:**
    This command links the `pomodoro-init` command to your code, so any changes you make are instantly available.
    ```bash
    pip install -e .
    ```

## Usage

Once installed, you can run the timer from anywhere in your terminal!

```bash
# Basic usage with default settings (25min work, 5min short break, 15min long break, 4 cycles)
pomodoro-init

# Customize timer durations
pomodoro-init --work 30 --short-break 10 --long-break 20

# Set number of cycles before long break
pomodoro-init --cycles 6

# Choose a theme and color
pomodoro-init --theme cats --color blue

# Combine all options
pomodoro-init --work 50 --short-break 10 --cycles 3 --theme dogs --color pink
```

Available options:
- `--work MINUTES` - Duration of work sessions (default: 25)
- `--short-break MINUTES` - Duration of short breaks (default: 5)
- `--long-break MINUTES` - Duration of long break (default: 15)
- `--cycles NUMBER` - Number of work/break cycles before long break (default: 4)
- `--theme {default,cats,dogs}` - Choose an ASCII art theme
- `--color {pink,blue,default}` - Choose a color scheme

The timer will start immediately. To stop the timer at any time, simply press Ctrl+C.

## Future Features (Roadmap)
This timer is just getting started! Here are some of the features we'd love to add next:

- [ ] **Pomodoro Menu:** A simple text-based menu to start, pause, resume, and reset your Pomodoro sessions.

- [ ] **Task List Integration:** Add, complete, and view tasks for your current work session.

- [X] ~~**Session Statistics (Backend):** Track your completed Pomodoros and total focus time - data is now automatically saved to `~/.pomodoro/stats.json`! UI for viewing stats coming soon.~~

- [X] ~~**Customizable Timers:** Allow users to set their own durations for work and break sessions via command-line arguments, as well as how many sessions/cycles they want to focus on.~~

- [X] ~~**Sound Notifications:** Optional sound alerts for when a session ends.~~

- [X] ~~**Themes & Colors:** Customize the look of your timer with different color schemes and different asciis, such as cats, dogs, plants, anime, and so on!~~

- [X] ~~**Progress Bar:** Visual progress indicator showing elapsed/remaining time in the session.~~

- [X] ~~**Milestone Messages:** Cute encouraging messages at key moments (e.g., "Halfway there!" at 50%, "Almost done!" at 80%).~~

- [ ] **Decorative Borders:** Frame the countdown with cute borders or patterns to make it more visually appealing.

