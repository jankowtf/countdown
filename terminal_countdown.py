import argparse
import time
import os
from datetime import datetime, timedelta

# ANSI color codes for terminal 80s style
COLORS = {
    "bright_green": "\033[92m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_yellow": "\033[93m",
    "bright_red": "\033[91m",
    "reset": "\033[0m",
    "bold": "\033[1m",
    "bg_black": "\033[40m",
}

# ASCII art for header text
HEADER_TEXT = [
    "████████ ██   ██ ███████     ██      ██ ██    ██ ███████ ███████ ████████ ██████  ███████  █████  ███    ███",
    "   ██    ██   ██ ██          ██      ██ ██    ██ ██      ██         ██    ██   ██ ██      ██   ██ ████  ████",
    "   ██    ███████ █████       ██      ██ ██    ██ █████   ███████    ██    ██████  █████   ███████ ██ ████ ██",
    "   ██    ██   ██ ██          ██      ██  ██  ██  ██           ██    ██    ██   ██ ██      ██   ██ ██  ██  ██",
    "   ██    ██   ██ ███████     ███████ ██   ████   ███████ ███████    ██    ██   ██ ███████ ██   ██ ██      ██",
    "                                                                                                             ",
    "                ███████ ████████  █████  ██████  ████████ ███████     ██ ███    ██                           ",
    "                ██         ██    ██   ██ ██   ██    ██    ██          ██ ████   ██                           ",
    "                ███████    ██    ███████ ██████     ██    ███████     ██ ██ ██  ██                           ",
    "                     ██    ██    ██   ██ ██   ██    ██         ██     ██ ██  ██ ██                           ",
    "                ███████    ██    ██   ██ ██   ██    ██    ███████     ██ ██   ████                           ",
]

# ASCII art digits for 80s display (10 rows high)
DIGITS = {
    "0": [
        "  ████  ",
        " ██  ██ ",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        " ██  ██ ",
        "  ████  ",
    ],
    "1": [
        "   ██   ",
        "  ███   ",
        " ████   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        " ██████ ",
    ],
    "2": [
        " ██████ ",
        "██    ██",
        "      ██",
        "      ██",
        "   ████ ",
        " ████   ",
        "██      ",
        "██      ",
        "██      ",
        "████████",
    ],
    "3": [
        " ██████ ",
        "██    ██",
        "      ██",
        "      ██",
        "  █████ ",
        "      ██",
        "      ██",
        "      ██",
        "██    ██",
        " ██████ ",
    ],
    "4": [
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        "████████",
        "      ██",
        "      ██",
        "      ██",
        "      ██",
        "      ██",
    ],
    "5": [
        "████████",
        "██      ",
        "██      ",
        "██      ",
        "███████ ",
        "      ██",
        "      ██",
        "      ██",
        "██    ██",
        " ██████ ",
    ],
    "6": [
        " ██████ ",
        "██    ██",
        "██      ",
        "██      ",
        "███████ ",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        " ██████ ",
    ],
    "7": [
        "████████",
        "      ██",
        "     ██ ",
        "    ██  ",
        "   ██   ",
        "  ██    ",
        " ██     ",
        " ██     ",
        " ██     ",
        " ██     ",
    ],
    "8": [
        " ██████ ",
        "██    ██",
        "██    ██",
        "██    ██",
        " ██████ ",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        " ██████ ",
    ],
    "9": [
        " ██████ ",
        "██    ██",
        "██    ██",
        "██    ██",
        " ███████",
        "      ██",
        "      ██",
        "      ██",
        "██    ██",
        " ██████ ",
    ],
    ":": [
        "        ",
        "        ",
        "  ████  ",
        "  ████  ",
        "        ",
        "        ",
        "  ████  ",
        "  ████  ",
        "        ",
        "        ",
    ],
    " ": [
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
    ],
}


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def format_time(seconds):
    """Format seconds into HH:MM:SS string."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def parse_duration(duration_str):
    """
    Parse a duration string into seconds.
    Accepted formats:
    - "5" (5 minutes)
    - "5.5" (5 minutes, 30 seconds)
    - "5:30" (5 minutes, 30 seconds)
    - "1:30:45" (1 hour, 30 minutes, 45 seconds)
    """
    # If it's just a number, interpret as minutes
    try:
        return float(duration_str) * 60
    except ValueError:
        pass

    # Check if it's in time format (MM:SS or HH:MM:SS)
    if ":" in duration_str:
        parts = duration_str.split(":")

        if len(parts) == 2:  # MM:SS format
            try:
                minutes = int(parts[0])
                seconds = int(parts[1])
                return minutes * 60 + seconds
            except ValueError:
                pass

        elif len(parts) == 3:  # HH:MM:SS format
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                return hours * 3600 + minutes * 60 + seconds
            except ValueError:
                pass

    # If we get here, format wasn't recognized
    raise ValueError(f"Unrecognized duration format: {duration_str}")


def render_ascii_time(time_str, color):
    """Render the time in ASCII art."""
    lines = [""] * 10  # 10 rows high

    # Build each row of the display
    for char in time_str:
        digit = DIGITS.get(char, DIGITS[" "])
        for i in range(10):
            lines[i] += digit[i]

    # Return the colored ASCII art
    return "\n".join(
        [f"{COLORS['bg_black']}{color}{line}{COLORS['reset']}" for line in lines]
    )


def display_header(color):
    """Display the ASCII art header."""
    terminal_width = os.get_terminal_size().columns
    padding = max(0, (terminal_width - len(HEADER_TEXT[0])) // 2)
    pad_str = " " * padding

    for line in HEADER_TEXT:
        if len(line) > terminal_width:
            # Truncate if terminal too narrow
            line = line[: terminal_width - 3] + "..."
        print(
            f"{COLORS['bg_black']}{color}{COLORS['bold']}{pad_str}{line}{COLORS['reset']}"
        )
    print("\n")


def terminal_countdown(target_time=None, duration_seconds=300):
    """Run a terminal-based countdown timer with retro ASCII art display."""
    if target_time is None:
        target_time = datetime.now() + timedelta(seconds=duration_seconds)

    colors = [
        COLORS["bright_magenta"],
        COLORS["bright_cyan"],
        COLORS["bright_yellow"],
        COLORS["bright_green"],
    ]
    color_index = 0
    last_color_change = time.time()
    color_cycle_duration = 2  # seconds

    try:
        while True:
            clear_screen()

            # Calculate remaining time
            now = datetime.now()
            remaining = target_time - now

            # Current color based on time
            current_time = time.time()
            if current_time - last_color_change > color_cycle_duration:
                color_index = (color_index + 1) % len(colors)
                last_color_change = current_time

            current_color = colors[color_index]

            # Check if countdown is complete
            if remaining.total_seconds() <= 0:
                print(
                    f"\n\n{COLORS['bright_red']}{COLORS['bold']}{'THE LIVESTREAM HAS STARTED!'.center(os.get_terminal_size().columns)}{COLORS['reset']}\n\n"
                )
                print(render_ascii_time("00:00:00", COLORS["bright_red"]))
                time.sleep(1)
                continue

            # Display header and time
            display_header(current_color)
            time_str = format_time(int(remaining.total_seconds()))
            print(render_ascii_time(time_str, current_color))

            # Sleep briefly to prevent high CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print(f"{COLORS['reset']}\nCountdown stopped by user.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Terminal-based Retro Countdown Timer")
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--time", type=str, help="Target time in format HH:MM:SS or HH:MM"
    )

    group.add_argument(
        "--duration",
        type=str,
        default="5",
        help="Duration for countdown. Formats: minutes (5), decimal minutes (5.5), MM:SS (5:30), or HH:MM:SS (1:30:45)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Parse the target time if provided
    target_time = None
    if args.time:
        try:
            if len(args.time.split(":")) == 3:  # HH:MM:SS format
                target_time_obj = time.strptime(args.time, "%H:%M:%S")
            else:  # HH:MM format
                target_time_obj = time.strptime(args.time, "%H:%M")

            now = datetime.now()
            target_time = datetime(
                now.year,
                now.month,
                now.day,
                target_time_obj.tm_hour,
                target_time_obj.tm_min,
                getattr(target_time_obj, "tm_sec", 0),
            )

            # If the target time is in the past, add a day
            if target_time < now:
                target_time += timedelta(days=1)
        except ValueError:
            print("Invalid time format. Using default duration.")
            target_time = None

    # Parse duration
    duration_seconds = 300  # Default: 5 minutes
    try:
        if not args.time:  # Only if --time not specified
            duration_seconds = parse_duration(args.duration)
    except ValueError as e:
        print(f"Error: {e}")
        print("Using default duration (5 minutes).")

    # Start the terminal countdown
    terminal_countdown(target_time, duration_seconds)


if __name__ == "__main__":
    main()
