# Retro Countdown Timer

A Python-based countdown timer with an 80s aesthetic digital display. Perfect for livestreams, events, or any countdown needs.

## Features

- Displays "The livestream starts in" with a retro digital countdown
- 80s-style digital display with color-changing effects
- Configurable countdown duration or specific target time
- Multiple versions to suit different environments
- Simple and straightforward interface

## Requirements

- Python 3.12+
- For GUI versions: Tkinter (included with standard Python installation)
- For terminal version: Just Python (no additional dependencies)

## Versions

### Terminal Version (Recommended)

A terminal-based version with ASCII art and ANSI colors that works anywhere:

```bash
python terminal_countdown.py
```

### Basic GUI Version

The standard countdown timer with simple text display (requires Tkinter):

```bash
python main.py
```

### Advanced GUI Version

Enhanced version with custom-drawn 7-segment digital display and more visual effects (requires Tkinter):

```bash
python advanced_countdown.py
```

## Usage

Run the countdown timer with default settings (5 minute countdown):

```bash
python terminal_countdown.py
# or (if Tkinter is available)
python main.py
python advanced_countdown.py
```

Set a specific countdown duration:

```bash
# All versions now support flexible duration formats:
python terminal_countdown.py --duration 10        # 10 minutes
python terminal_countdown.py --duration 1:30      # 1 minute, 30 seconds
python terminal_countdown.py --duration 0:45      # 45 seconds
python terminal_countdown.py --duration 1:30:45   # 1 hour, 30 minutes, 45 seconds
python terminal_countdown.py --duration 2.5       # 2 minutes, 30 seconds

# Same for the GUI versions:
python main.py --duration 1:30
python advanced_countdown.py --duration 1:30:45
```

Set a specific target time (24-hour format):

```bash
python terminal_countdown.py --time 18:30    # Target 6:30 PM
# or (if Tkinter is available)
python main.py --time 18:30
python advanced_countdown.py --time 18:30:45
```

Run in fullscreen mode (advanced GUI version only):

```bash
python advanced_countdown.py --fullscreen
```

## Examples

1. Start a 1 minute and 30 seconds countdown with the terminal version:
   ```bash
   python terminal_countdown.py --duration 1:30
   ```

2. Count down to 8:45 PM:
   ```bash
   python terminal_countdown.py --time 20:45
   ```

3. GUI version with a 2-hour countdown in fullscreen:
   ```bash
   python advanced_countdown.py --duration 2:00:00 --fullscreen
   ```

## Customization

You can modify the following in the source files to customize the appearance:

- Terminal version: ASCII art digits, colors, and timing
- GUI versions: Font styles and sizes, colors, window size and layout
- Advanced GUI version: Segment thickness and glow effects

## Notes

- The terminal version works on any system with Python.
- The GUI versions require Tkinter, which is usually included with Python but may need to be installed separately on some systems.
- To exit the terminal version, use Ctrl+C.
