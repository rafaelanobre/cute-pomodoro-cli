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
pomodoro-init
```

The timer will start immediately. To stop the timer at any time, simply press Ctrl+C.

## Future Features (Roadmap)
This timer is just getting started! Here are some of the features we'd love to add next:

- [ ] **Pomodoro Menu:** A simple text-based menu to start, pause, resume, and reset your Pomodoro sessions.

- [ ] **Task List Integration:** Add, complete, and view tasks for your current work session.

- [ ] **Session Statistics:** Track your completed Pomodoros and total focus time by day, week, month, year and total to see your productivity soar!

- [ ] **Customizable Timers:** Allow users to set their own durations for work and break sessions via command-line arguments (e.g., pomodoro-init --work 30 --break 10).

- [ ] **Sound Notifications:** Optional sound alerts for when a session ends.

- [ ] **Themes & Colors:** Customize the look of your timer with different color schemes and different asciis, such as cats, dogs, plants, anime, and so on!

