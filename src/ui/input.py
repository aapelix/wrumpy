import const
import utils.font
import pygame


class Input:
    def __init__(self, value: str, pos: tuple[int, int], size: tuple[int, int]):
        self.value = value
        self.pos = pos
        self.size = size
        self.font = utils.font.get_font_small()
        self.focus = False
        self.show_cursor = False
        self.cursor_timer = 0.0

    def update(self, dt: float, events: list[pygame.event.Event]):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                mouse_canvas_pos = (
                    mouse_pos[0] * const.CANVAS_WIDTH // const.WINDOW_WIDTH,
                    mouse_pos[1] * const.CANVAS_HEIGHT // const.WINDOW_HEIGHT,
                )

                rect = pygame.Rect(*self.pos, *self.size)

                if rect.collidepoint(mouse_canvas_pos):
                    self.focus = True
                    self.show_cursor = True
                else:
                    self.focus = False
                    self.show_cursor = False
                    self.cursor_timer = 0.0

        if self.focus:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.show_cursor = not self.show_cursor
                self.cursor_timer = 0.0

            for event in events:
                if event.type == pygame.TEXTINPUT:
                    if event.text.isdigit():
                        self.value += event.text
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.value = self.value[:-1]

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 0, 0), (*self.pos, *self.size), 2)
        text_surface = self.font.render(self.value, True, (0, 0, 0))
        screen.blit(text_surface, (self.pos[0] + 5, self.pos[1] + 5))
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.pos[0] + 5 + text_surface.get_width(),
                self.pos[1] + 3,
                2 if self.show_cursor else 0,
                16,
            ),
        )

    def __str__(self):
        return self.value
