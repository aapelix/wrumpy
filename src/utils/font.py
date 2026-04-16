import pygame

font_small: pygame.Font | None = None


def load_fonts():
    global font_small
    font_small = pygame.Font("assets/fonts/font-small.ttf", 16)


def get_font_small() -> pygame.Font:
    if font_small is None:
        raise Exception("Fonts not loaded")
    return font_small
