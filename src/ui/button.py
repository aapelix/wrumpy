from collections.abc import Callable
import const
import utils.font
import pygame


class Button:
    def __init__(
        self,
        value: str,
        pos: tuple[int, int],
        size: tuple[int, int],
        on_click: Callable[[], None],
        offset_y: int = 0,
    ):
        self.value = value
        self.pos = pos
        self.size = size

        self.on_click = on_click

        font = utils.font.get_font_small()
        self.text_surface = font.render(self.value, True, (0, 0, 0))
        self.offset_y = offset_y

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            mouse_canvas_pos = (
                mouse_pos[0] * const.CANVAS_WIDTH // const.WINDOW_WIDTH,
                mouse_pos[1] * const.CANVAS_HEIGHT // const.WINDOW_HEIGHT,
            )

            rect = pygame.Rect(*self.pos, *self.size)

            if rect.collidepoint(mouse_canvas_pos):
                self.on_click()

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 0, 0), (*self.pos, *self.size), 2)
        screen.blit(
            self.text_surface, (self.pos[0] + 5, self.pos[1] + 3 + self.offset_y)
        )
