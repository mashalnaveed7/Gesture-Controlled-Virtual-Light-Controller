import pygame
import cv2
import numpy as np

class VirtualRoom:
    """
    Professional dashboard-style UI combining:
    - Live webcam feed (left)
    - Virtual lamp room (right)
    - Status HUD (bottom)
    """

    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Gesture Controlled Virtual Light Controller")
        self.clock = pygame.time.Clock()

        # Fonts
        self.title_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.label_font = pygame.font.SysFont("Segoe UI", 20, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", 16)

        # Layout regions
        self.header_h = 60
        self.footer_h = 110
        self.cam_w = int(width * 0.45)
        self.room_w = width - self.cam_w

        # Palette (dark modern theme)
        self.bg_color = (18, 18, 24)
        self.header_color = (28, 28, 36)
        self.panel_color = (24, 24, 32)
        self.accent = (0, 200, 255)
        self.wall_color = (35, 35, 46)
        self.floor_color = (22, 22, 30)
        self.table_color = (94, 64, 42)
        self.border_color = (55, 55, 68)

    # ---------- Webcam frame conversion ----------
    def cv2_frame_to_surface(self, frame):
        """Convert an OpenCV BGR frame into a Pygame surface, resized to fit the cam panel."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.cam_w, self.height - self.header_h - self.footer_h))
        surface = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
        return surface

    # ---------- Header ----------
    def draw_header(self):
        pygame.draw.rect(self.screen, self.header_color, (0, 0, self.width, self.header_h))
        pygame.draw.line(self.screen, self.accent, (0, self.header_h), (self.width, self.header_h), 2)

        title = self.title_font.render("Gesture Controlled Virtual Light Controller", True, (240, 240, 245))
        self.screen.blit(title, (20, 14))

    # ---------- Webcam panel ----------
    def draw_webcam_panel(self, frame, gesture):
        y_offset = self.header_h
        surface = self.cv2_frame_to_surface(frame)
        self.screen.blit(surface, (0, y_offset))

        # Border around cam panel
        pygame.draw.rect(self.screen, self.border_color, (0, y_offset, self.cam_w, self.height - self.header_h - self.footer_h), 2)

        # Gesture badge overlay (top-left of cam feed)
        badge_text = f"Gesture: {gesture}"
        badge = self.label_font.render(badge_text, True, (255, 255, 255))
        badge_bg_rect = pygame.Rect(15, y_offset + 15, badge.get_width() + 24, badge.get_height() + 14)
        badge_surface = pygame.Surface((badge_bg_rect.width, badge_bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(badge_surface, (0, 0, 0, 160), badge_surface.get_rect(), border_radius=8)
        self.screen.blit(badge_surface, (badge_bg_rect.x, badge_bg_rect.y))
        self.screen.blit(badge, (badge_bg_rect.x + 12, badge_bg_rect.y + 7))

    # ---------- Virtual room ----------
    def draw_room(self):
        y_offset = self.header_h
        room_h = self.height - self.header_h - self.footer_h
        wall_h = int(room_h * 0.72)

        pygame.draw.rect(self.screen, self.wall_color, (self.cam_w, y_offset, self.room_w, wall_h))
        pygame.draw.rect(self.screen, self.floor_color, (self.cam_w, y_offset + wall_h, self.room_w, room_h - wall_h))

        # Table
        table_w, table_h = 220, 26
        table_x = self.cam_w + self.room_w // 2 - table_w // 2
        table_y = y_offset + wall_h - 8

        # Soft shadow under table
        shadow = pygame.Surface((table_w + 40, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 90), shadow.get_rect())
        self.screen.blit(shadow, (table_x - 20, table_y + table_h + 34))

        pygame.draw.rect(self.screen, self.table_color, (table_x, table_y, table_w, table_h), border_radius=4)
        pygame.draw.rect(self.screen, (60, 40, 26), (table_x + 14, table_y + table_h, 10, 44))
        pygame.draw.rect(self.screen, (60, 40, 26), (table_x + table_w - 24, table_y + table_h, 10, 44))

        pygame.draw.rect(self.screen, self.border_color, (self.cam_w, y_offset, self.room_w, room_h), 2)

        return y_offset

    def draw_lamp(self, is_on, brightness, position, color_rgb):
        x, y = position
        y_offset = self.header_h

        if is_on:
            max_radius = 130
            layers = 6
            for i in range(layers, 0, -1):
                r = int((max_radius / layers) * i * (brightness / 100))
                alpha = int((60 / layers) * i * (brightness / 100))
                if r <= 0 or alpha <= 0:
                    continue
                glow_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*color_rgb, alpha), (r, r), r)
                self.screen.blit(glow_surface, (x - r, y - r))

            bulb_color = color_rgb
            core_glow = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.circle(core_glow, (255, 255, 255, int(200 * (brightness / 100))), (35, 35), 35)
            self.screen.blit(core_glow, (x - 35, y - 35))
        else:
            bulb_color = (70, 70, 78)

        pygame.draw.line(self.screen, (90, 90, 100), (x, y_offset), (x, y - 24), 3)
        pygame.draw.circle(self.screen, bulb_color, (x, y), 24)
        pygame.draw.circle(self.screen, (220, 220, 225), (x, y), 24, 2)

    # ---------- Footer HUD ----------
    def draw_footer(self, status, fps):
        y = self.height - self.footer_h
        pygame.draw.rect(self.screen, self.header_color, (0, y, self.width, self.footer_h))
        pygame.draw.line(self.screen, self.accent, (0, y), (self.width, y), 2)

        cards = [
            ("LIGHT", "ON" if status["on"] else "OFF", (0, 220, 120) if status["on"] else (220, 60, 60)),
            ("BRIGHTNESS", f"{status['brightness']}%", (255, 210, 0)),
            ("COLOR", status["color"], (200, 200, 255)),
            ("POSITION", f"{status['position'][0]}, {status['position'][1]}", (180, 180, 190)),
            ("FPS", f"{int(fps)}", (150, 150, 160)),
        ]

        card_w = self.width // len(cards)
        for i, (label, value, color) in enumerate(cards):
            cx = i * card_w + 24
            label_surf = self.small_font.render(label, True, (140, 140, 150))
            value_surf = self.label_font.render(value, True, color)
            self.screen.blit(label_surf, (cx, y + 22))
            self.screen.blit(value_surf, (cx, y + 46))
            if i > 0:
                pygame.draw.line(self.screen, self.border_color, (i * card_w, y + 15), (i * card_w, y + self.footer_h - 15), 1)

    # ---------- Full render ----------
    def render(self, frame, gesture, status, fps):
        self.screen.fill(self.bg_color)
        self.draw_header()
        self.draw_webcam_panel(frame, gesture)
        self.draw_room()
        self.draw_lamp(status["on"], status["brightness"], status["position"], status["color_rgb"])
        self.draw_footer(status, fps)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return False
        return True

    def tick(self, fps=30):
        self.clock.tick(fps)
        return self.clock.get_fps()

    def quit(self):
        pygame.quit()