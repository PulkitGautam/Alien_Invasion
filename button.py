import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Setting Dimensions and Font
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)

        self.font = pygame.font.SysFont(None, 48)          #    None = Default Font     48 = Font Size

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):

        # Render Text as an Image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center