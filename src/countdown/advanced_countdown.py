import tkinter as tk
import argparse
import time
from datetime import datetime, timedelta
from countdown.digital_display import RetroDigitalDisplay


class AdvancedCountdownTimer:
    def __init__(self, root, target_time=None, duration_minutes=5):
        self.root = root
        self.root.title("Advanced Retro Countdown Timer")
        self.root.geometry("1024x600")
        self.root.configure(bg="black")

        # Set the target time based on input
        if target_time:
            self.target_time = target_time
        else:
            self.target_time = datetime.now() + timedelta(minutes=duration_minutes)

        # Create the canvas for drawing
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create the header text
        self.header_font = tk.font.Font(family="Courier", size=30, weight="bold")
        self.header_text = self.canvas.create_text(
            512,
            100,
            text="The livestream starts in",
            fill="#00FF00",
            font=self.header_font,
        )

        # Create the custom digital display
        self.display = RetroDigitalDisplay(
            canvas=self.canvas,
            x=180,  # Starting x position
            y=200,  # y position
            size=120,  # Height of digits
            color="#FF00FF",  # Magenta color
            glow_color="#FF88FF",  # Light magenta glow
            thickness_ratio=0.15,  # Thickness of segments
        )

        # Create color cycling for 80s effect
        self.colors = [
            ("#FF00FF", "#FF88FF"),  # Magenta
            ("#00FFFF", "#88FFFF"),  # Cyan
            ("#FFFF00", "#FFFF88"),  # Yellow
            ("#FF00FF", "#FF88FF"),  # Back to magenta
        ]
        self.color_index = 0
        self.color_cycle_speed = 2.0  # seconds per color
        self.last_color_change = time.time()

        # Start the animation
        self.update_timer()

    def update_timer(self):
        # Calculate remaining time
        now = datetime.now()
        remaining = self.target_time - now

        # Check if countdown is complete
        if remaining.total_seconds() <= 0:
            # Display zeros and show completion message
            self.display.show_time(0, 0, 0)
            self.canvas.itemconfig(
                self.header_text, text="The livestream has started!", fill="#FF0000"
            )

            # Flash effect when timer ends
            if int(time.time()) % 2 == 0:
                self.display.set_color("#FF0000", "#FF8888")  # Red
            else:
                self.display.set_color("#880000", "#440000")  # Dark red

            # Continue updating even after countdown completes (for the flashing effect)
            self.root.after(500, self.update_timer)
            return

        # Extract hours, minutes, seconds
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        # Update the digital display
        self.display.show_time(hours, minutes, seconds)

        # Cycle colors for 80s effect
        current_time = time.time()
        if current_time - self.last_color_change > self.color_cycle_speed:
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.display.set_color(*self.colors[self.color_index])
            self.last_color_change = current_time

        # Blink colon every second for seconds ticking effect
        seconds_blink = int(time.time()) % 2 == 0
        self.display.show_colon(2, seconds_blink)
        self.display.show_colon(5, seconds_blink)

        # Schedule the next update
        self.root.after(100, self.update_timer)


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
    parser = argparse.ArgumentParser(description="Advanced Retro Countdown Timer")
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

    parser.add_argument(
        "--fullscreen", action="store_true", help="Run in fullscreen mode"
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

    # Set fullscreen if requested
    if args.fullscreen:
        root.attributes("-fullscreen", True)
        # Bind escape key to exit fullscreen
        root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    app = AdvancedCountdownTimer(root, target_time, duration_minutes)
    root.mainloop()


if __name__ == "__main__":
    main()
