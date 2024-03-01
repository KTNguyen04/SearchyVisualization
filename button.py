import pygame
from settings import BUTTON_COLOR, BUTTON_DOWN_COLOR, GRAY_C, SHADE_COLOR, Settings


class Button:
    def __init__(self, s_v,  text,  pos=(0, 0)):

        self.screen = s_v.screen
        self.screen_rect = self.screen.get_rect()
        self.window = s_v.dashboard_rect
        self.width, self.height = Settings.button_width, Settings.button_height
        self.pos = pos
        self.text = text
        self.top_rect = pygame.Rect(
            self.pos, (self.width, self.height))
        self.top_color = BUTTON_COLOR

        self.font = pygame.font.SysFont(None, 30)

        self.text_suf = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_suf.get_rect(center=self.top_rect.center)

        self.bot_rect = pygame.Rect(pos,
                                    (self.width, self.height+Settings.button_shade))

        self.bot_color = SHADE_COLOR

    def draw(self):
        pygame.draw.rect(self.screen, self.bot_color,
                         self.bot_rect, border_radius=12,)
        pygame.draw.rect(self.screen, self.top_color,
                         self.top_rect, border_radius=12)
        self.screen.blit(self.text_suf, self.text_rect)

    def set_pos(self, pos):
        self.pos = pos

    def clicked(self):
        self.top_color = BUTTON_DOWN_COLOR

    def unclicked(self):
        self.top_color = BUTTON_COLOR
