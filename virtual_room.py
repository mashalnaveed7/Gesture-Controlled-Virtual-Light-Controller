import pygame
import sys

class VirtualRoom:
    """
    Renders a virtual room with a lamp that responds to:
    - ON/OFF state
    - Brightness (0-100%)
    - Position (x, y)
    - Color
    """

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Virtual Light Room")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

        # Room colors
        self.wall_color = (40, 40, 50)
        self.floor_color = (25, 25, 35)
        self.table_color = (90, 60, 40)

    def draw_room(self):
        """Draw static background: wall + floor + table."""
        # Wall (top 75% of screen)
        wall_height = int(self.height * 0.75)
        self.screen.fill(self.wall_color, (0, 0, self.width, wall_height))

        # Floor (bottom 25%)
        self.screen.fill(self.floor_color, (0, wall_height, self.width, self.height - wall_height))

        # Table
        table_width, table_height = 200, 30
        table_x = self.width // 2 - table_width // 2
        table_y = wall_height - 10
        pygame.draw.rect(self.screen, self.table_color, (table_x, table_y, table_width, table_height))
        # Table legs
        pygame.draw.rect(self.screen, self.table_color, (table_x + 10, table_y + table_height, 10, 40))
        pygame.draw.rect(self.screen, self.table_color, (table_x + table_width - 20, table_y + table_height, 10, 40))

    def draw_lamp(self, is_on, brightness, position, color_rgb):
        """
        Draws the lamp bulb and its glow.
        - is_on: bool
        - brightness: 0-100
        - position: [x, y]
        - color_rgb: (R, G, B) tuple
        """
        x, y = position

        if is_on:
            # Glow intensity scales with brightness
            glow_radius = int(40 + (brightness / 100) * 80)
            glow_alpha = int((brightness / 100) * 180)

            # Draw glow using a separate transparent surface
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_color = (*color_rgb, glow_alpha)
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surface, (x - glow_radius, y - glow_radius))

            bulb_color = color_rgb
        else:
            bulb_color = (60, 60, 60)  # dim gray bulb when off

        # Bulb body
        pygame.draw.circle(self.screen, bulb_color, (x, y), 25)
        pygame.draw.circle(self.screen, (200, 200, 200), (x, y), 25, 2)  # outline

        # Simple hanging wire
        pygame.draw.line(self.screen, (80, 80, 80), (x, 0), (x, y - 25), 3)

    def draw_status_panel(self, status):
        """Draw a status bar at the bottom with light info."""
        panel_y = self.height - 5
        panel_height = 5  # placeholder, replaced below with actual info box

        # Status box
        box_rect = pygame.Rect(10, self.height - 90, 300, 80)
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 1)

        status_text = "ON" if status["on"] else "OFF"
        status_color = (0, 255, 0) if status["on"] else (255, 0, 0)

        lines = [
            (f"Light: {status_text}", status_color),
            (f"Brightness: {status['brightness']}%", (255, 255, 0)),
            (f"Color: {status['color']}", (255, 255, 255)),
        ]

        for i, (text, color) in enumerate(lines):
            rendered = self.small_font.render(text, True, color)
            self.screen.blit(rendered, (20, self.height - 80 + i * 25))

    def render(self, status):
        """
        Full render pass for one frame.
        status: dict from LightController.get_status()
        """
        self.draw_room()

        color_rgb = status.get("color_rgb", (255, 255, 255))
        self.draw_lamp(status["on"], status["brightness"], status["position"], color_rgb)
        self.draw_status_panel(status)

        pygame.display.flip()

    def handle_events(self):
        """
        Returns False if the window should close, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def tick(self, fps=30):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()