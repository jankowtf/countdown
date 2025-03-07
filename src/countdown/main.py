import tkinter as tk
from tkinter import font as tkfont
import argparse
import time
from datetime import datetime, timedelta


class CountdownTimer:
    def __init__(self, root, target_time=None, duration_minutes=5):
        self.root = root
        self.root.title("Retro Countdown Timer")
        self.root.geometry("800x400")
        self.root.configure(bg="black")

        # Set the target time based on input
        if target_time:
            self.target_time = target_time
        else:
            self.target_time = datetime.now() + timedelta(minutes=duration_minutes)

        # Create the 80s style fonts
        self.header_font = tkfont.Font(family="Courier", size=24, weight="bold")
        self.timer_font = tkfont.Font(family="Courier", size=60, weight="bold")

        # Create the canvas for drawing
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create the text elements
        self.header_text = self.canvas.create_text(
            400,
            100,
            text="The livestream starts in",
            fill="#00FF00",
            font=self.header_font,
        )

        self.timer_text = self.canvas.create_text(
            400, 200, text="00:00:00", fill="#FF00FF", font=self.timer_font
        )

        # Start the timer update
        self.update_timer()

    def update_timer(self):
        # Calculate remaining time
        now = datetime.now()
        remaining = self.target_time - now

        # Check if countdown is complete
        if remaining.total_seconds() <= 0:
            self.canvas.itemconfig(self.timer_text, text="00:00:00", fill="#FF0000")
            self.canvas.itemconfig(
                self.header_text, text="The livestream has started!", fill="#FF0000"
            )
            return

        # Format the time
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Update the timer text
        self.canvas.itemconfig(self.timer_text, text=time_string)

        # Add 80s style glow effect (changing colors periodically)
        if int(time.time()) % 2 == 0:
            self.canvas.itemconfig(self.timer_text, fill="#FF00FF")  # Magenta
        else:
            self.canvas.itemconfig(self.timer_text, fill="#00FFFF")  # Cyan

        # Schedule the next update
        self.root.after(1000, self.update_timer)


def parse_duration(duration_str):
    """
    Parse a duration string into minutes (can be fractional).
    Accepted formats:
    - "5" (5 minutes)
    - "5.5" (5 minutes, 30 seconds)
    - "5:30" (5 minutes, 30 seconds)
    - "1:30:45" (1 hour, 30 minutes, 45 seconds)
    """
    # If it's just a number, interpret as minutes
    try:
        return float(duration_str)
    except ValueError:
        pass

    # Check if it's in time format (MM:SS or HH:MM:SS)
    if ":" in duration_str:
        parts = duration_str.split(":")

        if len(parts) == 2:  # MM:SS format
            try:
                minutes = int(parts[0])
                seconds = int(parts[1])
                return minutes + seconds / 60
            except ValueError:
                pass

        elif len(parts) == 3:  # HH:MM:SS format
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                return hours * 60 + minutes + seconds / 60
            except ValueError:
                pass

    # If we get here, format wasn't recognized
    raise ValueError(f"Unrecognized duration format: {duration_str}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Retro Countdown Timer")
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
    duration_minutes = 5.0  # Default: 5 minutes
    try:
        if not args.time:  # Only if --time not specified
            duration_minutes = parse_duration(args.duration)
    except ValueError as e:
        print(f"Error: {e}")
        print("Using default duration (5 minutes).")

    # Create the Tkinter application
    root = tk.Tk()
    app = CountdownTimer(root, target_time, duration_minutes)
    root.mainloop()


if __name__ == "__main__":
    main()
