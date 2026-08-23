class LightController:
    """
    Manages the state of the virtual light:
    - ON/OFF
    - Brightness (0-100%)
    - Position (x, y)
    - Color
    """

    def __init__(self, screen_width=800, screen_height=600):
        self.is_on = False
        self.brightness = 50  # default 50%
        self.position = [screen_width // 2, screen_height // 2]  # center by default
        self.color_list = ["WHITE", "RED", "BLUE", "GREEN", "PURPLE", "YELLOW"]
        self.color_index = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

    # --- ON/OFF ---
    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    # --- Brightness ---
    def set_brightness(self, value):
        """Clamp brightness between 0 and 100."""
        self.brightness = max(0, min(100, int(value)))

    # --- Position ---
    def set_position(self, x, y):
        """Clamp position within screen bounds."""
        x = max(0, min(self.screen_width, x))
        y = max(0, min(self.screen_height, y))
        self.position = [x, y]

    # --- Color ---
    def next_color(self):
        """Cycle to the next color in the list."""
        self.color_index = (self.color_index + 1) % len(self.color_list)

    def get_color_name(self):
        return self.color_list[self.color_index]

    def get_color_rgb(self):
        """Returns an (R, G, B) tuple for the current color."""
        color_map = {
            "WHITE": (255, 255, 255),
            "RED": (255, 0, 0),
            "BLUE": (0, 0, 255),
            "GREEN": (0, 255, 0),
            "PURPLE": (160, 32, 240),
            "YELLOW": (255, 255, 0),
        }
        return color_map[self.get_color_name()]

    # --- Status (for debugging/testing) ---
    def get_status(self):
        return {
            "on": self.is_on,
            "brightness": self.brightness,
            "position": self.position,
            "color": self.get_color_name(),
            "color_rgb": self.get_color_rgb()
        }