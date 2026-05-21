import pygame.font
from label import Label
from settings import Settings

class InputBox:
    """A class to represent input from the user
    to change game's settings
    """
    def __init__(self, ai_game, msg, position, size, settings_obj, attr_name, action=None):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()

        # Set the dimensions and properties of the button.
        self.width, self.height = size
        self.font = pygame.font.SysFont(None, 48)
        self.action = action

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.midleft = position

        # States variables
        self.active = False
        self.color_active = (0, 0, 0)
        self.color_inactive = (200, 180, 55)
        self.color = self.color_inactive


        # Dinamic msg
        self.msg = str(msg)
        # Dinamic settings
        self.settings_obj = settings_obj
        self.attr_name = attr_name


        # The button message needs to be prepped only once.
        self._prep_msg()


    def handle_mouse_event(self, event):
        """Checks click events on inputboxes"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos): # event.pos returns x, y pos
                self.active = True
            else:
                self.active = False
            self._prep_msg()

    def handle_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.msg) <= 1:
                        self.msg = "0"
                    else:
                        self.msg = self.msg[:-1]
                elif event.unicode:
                    if event.unicode.isdigit() or (event.unicode == "." and "." not in self.msg):
                        if self.msg[0] == "0":
                            self.msg = event.unicode
                        else:
                            self.msg += event.unicode
                if event.key == pygame.K_RETURN:
                    if not self.msg:
                        self.msg = "0"
                    setattr(self.settings_obj ,self.attr_name , float(self.msg))
                    self.active = False

            # Font and state
            self._prep_msg()


    def _prep_msg(self):
        """Turn msg into a rendered image and center text on the button."""
        self.color = self.color_active if self.active else self.color_inactive

        self.msg_image = self.font.render(self.msg, True, self.color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midleft = self.rect.midleft
        self.rect.width = max(self.msg_image.get_width(), self.width)

    def draw_input(self):
        """Draw blank inputbox and then draw message."""
        self.screen.blit(self.msg_image, self.msg_image_rect)