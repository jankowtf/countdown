class RetroDigitalDisplay:
    """A custom widget that draws digital clock-style segments for a more authentic 80s look."""

    def __init__(
        self,
        canvas,
        x,
        y,
        size=100,
        color="#FF00FF",
        glow_color="#FF88FF",
        thickness_ratio=0.2,
    ):
        """
        Initialize a new RetroDigitalDisplay

        Parameters:
        - canvas: tkinter Canvas to draw on
        - x, y: Position coordinates
        - size: Height of the digit
        - color: Primary color for the segments
        - glow_color: Secondary color for the glow effect
        - thickness_ratio: Thickness of segments as ratio of size
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.glow_color = glow_color
        self.width = size * 0.7  # Aspect ratio for digit width
        self.thickness = size * thickness_ratio
        self.segment_gap = self.thickness * 0.3

        # Segment IDs for each displayed character
        self.segments = {}
        self.current_value = None

    def _create_segment(self, points, tag):
        """Create a segment with glow effect."""
        # Create glow effect (larger polygon behind)
        glow = self.canvas.create_polygon(
            points, fill=self.glow_color, outline="", tags=f"{tag}_glow", state="hidden"
        )

        # Create the actual segment
        segment = self.canvas.create_polygon(
            points, fill=self.color, outline="", tags=tag, state="hidden"
        )

        return segment, glow

    def create_digit(self, position=0):
        """Create all segments for a digit at the specified position."""
        # Calculate position offset
        offset_x = position * (self.width + self.size * 0.3)

        # Define the segments (a-g) for the 7-segment display
        x, y = self.x + offset_x, self.y
        w, h = self.width, self.size
        t = self.thickness
        g = self.segment_gap

        # Segment a (top horizontal)
        a_points = [x + g, y, x + w - g, y, x + w - g - t, y + t, x + g + t, y + t]

        # Segment b (top right vertical)
        b_points = [
            x + w,
            y + g,
            x + w,
            y + h / 2 - g,
            x + w - t,
            y + h / 2 - g - t,
            x + w - t,
            y + g + t,
        ]

        # Segment c (bottom right vertical)
        c_points = [
            x + w,
            y + h / 2 + g,
            x + w,
            y + h - g,
            x + w - t,
            y + h - g - t,
            x + w - t,
            y + h / 2 + g + t,
        ]

        # Segment d (bottom horizontal)
        d_points = [
            x + g,
            y + h,
            x + w - g,
            y + h,
            x + w - g - t,
            y + h - t,
            x + g + t,
            y + h - t,
        ]

        # Segment e (bottom left vertical)
        e_points = [
            x,
            y + h / 2 + g,
            x,
            y + h - g,
            x + t,
            y + h - g - t,
            x + t,
            y + h / 2 + g + t,
        ]

        # Segment f (top left vertical)
        f_points = [
            x,
            y + g,
            x,
            y + h / 2 - g,
            x + t,
            y + h / 2 - g - t,
            x + t,
            y + g + t,
        ]

        # Segment g (middle horizontal)
        g_points = [
            x + g,
            y + h / 2,
            x + w - g,
            y + h / 2,
            x + w - g - t,
            y + h / 2 + t / 2,
            x + g + t,
            y + h / 2 + t / 2,
        ]

        # Create all segments
        segments = {}
        segments["a"] = self._create_segment(a_points, f"seg_{position}_a")
        segments["b"] = self._create_segment(b_points, f"seg_{position}_b")
        segments["c"] = self._create_segment(c_points, f"seg_{position}_c")
        segments["d"] = self._create_segment(d_points, f"seg_{position}_d")
        segments["e"] = self._create_segment(e_points, f"seg_{position}_e")
        segments["f"] = self._create_segment(f_points, f"seg_{position}_f")
        segments["g"] = self._create_segment(g_points, f"seg_{position}_g")

        self.segments[position] = segments
        return segments

    def create_colon(self, position=0):
        """Create a colon separator."""
        offset_x = position * (self.width + self.size * 0.3)
        x, y = self.x + offset_x, self.y
        r = self.thickness / 2

        # Upper dot
        upper_dot = self.canvas.create_oval(
            x - r,
            y + self.size * 0.3 - r,
            x + r,
            y + self.size * 0.3 + r,
            fill=self.color,
            outline="",
            tags=f"colon_{position}_1",
        )

        # Upper dot glow
        upper_glow = self.canvas.create_oval(
            x - r * 1.5,
            y + self.size * 0.3 - r * 1.5,
            x + r * 1.5,
            y + self.size * 0.3 + r * 1.5,
            fill=self.glow_color,
            outline="",
            tags=f"colon_{position}_1_glow",
        )

        # Lower dot
        lower_dot = self.canvas.create_oval(
            x - r,
            y + self.size * 0.7 - r,
            x + r,
            y + self.size * 0.7 + r,
            fill=self.color,
            outline="",
            tags=f"colon_{position}_2",
        )

        # Lower dot glow
        lower_glow = self.canvas.create_oval(
            x - r * 1.5,
            y + self.size * 0.7 - r * 1.5,
            x + r * 1.5,
            y + self.size * 0.7 + r * 1.5,
            fill=self.glow_color,
            outline="",
            tags=f"colon_{position}_2_glow",
        )

        # Store the colon segments
        self.segments[f"colon_{position}"] = {
            "dots": [upper_dot, lower_dot],
            "glows": [upper_glow, lower_glow],
        }

    def show_digit(self, position, digit):
        """
        Display a digit at the specified position.

        Parameters:
        - position: The position index for the digit
        - digit: The digit to display (0-9)
        """
        if position not in self.segments:
            self.create_digit(position)

        # Segment patterns for digits 0-9
        patterns = {
            0: "abcdef",
            1: "bc",
            2: "abged",
            3: "abgcd",
            4: "fgbc",
            5: "afgcd",
            6: "afedcg",
            7: "abc",
            8: "abcdefg",
            9: "abcfg",
        }

        # Hide all segments first
        for segment_key in "abcdefg":
            segment, glow = self.segments[position][segment_key]
            self.canvas.itemconfig(segment, state="hidden")
            self.canvas.itemconfig(glow, state="hidden")

        # Show active segments for the digit
        pattern = patterns.get(digit, "")
        for segment_key in pattern:
            segment, glow = self.segments[position][segment_key]
            self.canvas.itemconfig(segment, state="normal")
            self.canvas.itemconfig(glow, state="normal")

    def show_colon(self, position, visible=True):
        """Toggle the visibility of a colon."""
        colon_key = f"colon_{position}"
        if colon_key not in self.segments:
            self.create_colon(position)

        state = "normal" if visible else "hidden"
        for dot in self.segments[colon_key]["dots"]:
            self.canvas.itemconfig(dot, state=state)
        for glow in self.segments[colon_key]["glows"]:
            self.canvas.itemconfig(glow, state=state)

    def show_time(self, hours, minutes, seconds):
        """Display a time in HH:MM:SS format."""
        # Hours
        self.show_digit(0, hours // 10)
        self.show_digit(1, hours % 10)

        # Colon
        self.show_colon(2)

        # Minutes
        self.show_digit(3, minutes // 10)
        self.show_digit(4, minutes % 10)

        # Colon
        self.show_colon(5)

        # Seconds
        self.show_digit(6, seconds // 10)
        self.show_digit(7, seconds % 10)

    def set_color(self, color, glow_color=None):
        """Change the color of all segments."""
        self.color = color
        if glow_color:
            self.glow_color = glow_color

        # Update all existing segments
        for position in self.segments:
            if isinstance(position, int):
                for segment_key in "abcdefg":
                    if segment_key in self.segments[position]:
                        segment, glow = self.segments[position][segment_key]
                        self.canvas.itemconfig(segment, fill=self.color)
                        self.canvas.itemconfig(glow, fill=self.glow_color)
            elif position.startswith("colon_"):
                for dot in self.segments[position]["dots"]:
                    self.canvas.itemconfig(dot, fill=self.color)
                for glow in self.segments[position]["glows"]:
                    self.canvas.itemconfig(glow, fill=self.glow_color)
