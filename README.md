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

## Installation

### Direct Usage (Recommended)

You can run the scripts directly from the repository:

```bash
# Clone the repository
git clone https://github.com/your-username/countdown.git
cd countdown

# Install the package in development mode
pip install -e .
```

### Via pip (Coming Soon)

```bash
pip install retro-countdown
```

## Versions

### Terminal Version (Recommended)

A terminal-based version with ASCII art and ANSI colors that works anywhere:

```bash
# Run directly
python countdown-terminal.py

# Or if installed via pip
countdown-terminal
```

### Basic GUI Version

The standard countdown timer with simple text display (requires Tkinter):

```bash
# Run directly 
python countdown-gui.py

# Or if installed via pip
countdown-gui
```

### Advanced GUI Version

Enhanced version with custom-drawn 7-segment digital display and more visual effects (requires Tkinter):

```bash
# Run directly
python countdown-advanced.py

# Or if installed via pip
countdown-advanced
```

## Usage

Run the countdown timer with default settings (5 minute countdown):

```bash
python countdown-terminal.py
# or (if Tkinter is available)
python countdown-gui.py
python countdown-advanced.py
```

Set a specific countdown duration:

```bash
# All versions support flexible duration formats:
python countdown-terminal.py --duration 10        # 10 minutes
python countdown-terminal.py --duration 1:30      # 1 minute, 30 seconds
python countdown-terminal.py --duration 0:45      # 45 seconds
python countdown-terminal.py --duration 1:30:45   # 1 hour, 30 minutes, 45 seconds
python countdown-terminal.py --duration 2.5       # 2 minutes, 30 seconds

# Same for the GUI versions:
python countdown-gui.py --duration 1:30
python countdown-advanced.py --duration 1:30:45
```

Set a specific target time (24-hour format):

```bash
python countdown-terminal.py --time 18:30    # Target 6:30 PM
# or (if Tkinter is available)
python countdown-gui.py --time 18:30
python countdown-advanced.py --time 18:30:45
```

Run in fullscreen mode (advanced GUI version only):

```bash
python countdown-advanced.py --fullscreen
```

## Examples

1. Start a 1 minute and 30 seconds countdown with the terminal version:
   ```bash
   python countdown-terminal.py --duration 1:30
   ```

2. Count down to 8:45 PM:
   ```bash
   python countdown-terminal.py --time 20:45
   ```

3. GUI version with a 2-hour countdown in fullscreen:
   ```bash
   python countdown-advanced.py --duration 2:00:00 --fullscreen
   ```

## Project Structure

```
countdown/
├── README.md
├── countdown-advanced.py  # Entry point for advanced GUI version
├── countdown-gui.py       # Entry point for basic GUI version
├── countdown-terminal.py  # Entry point for terminal version
├── pyproject.toml         # Python package configuration
└── src/
    └── countdown/         # Actual package code
        ├── __init__.py
        ├── advanced_countdown.py
        ├── digital_display.py
        ├── main.py
        └── terminal_countdown.py
```

## Development

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/your-username/countdown.git
cd countdown

# Install in development mode
pip install -e .

# Run tests (coming soon)
pytest
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
