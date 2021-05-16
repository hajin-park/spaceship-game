#Client FPS display
import pygame


class GetFPS:
    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.SysFont('malgungothicsemilight', 16, True, False)
        self.fps = self.font.render(str(int(self.main.clock.get_fps())), True, pygame.Color('white'))
        self.current_fps = int(self.main.clock.get_fps())
        self.fps_rect = self.fps.get_rect()
        self.fps_rect.top = self.screen_rect.top + 3
        self.fps_rect.left = self.screen_rect.left + 10

    # ------------------------------ Update FPS display
    def _update_fps(self):
        if self.current_fps != int(self.main.clock.get_fps()):
            self.fps = self.font.render("FPS: " + str(int(self.main.clock.get_fps())), True, pygame.Color('white'))
        self.current_fps = int(self.main.clock.get_fps())

    # ------------------------------ Render display
    def blitme(self):
        self.screen.blit(self.fps, self.fps_rect)
