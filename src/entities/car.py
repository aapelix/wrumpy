import pygame
from stack import Stack


class Car:
    body: Stack
    tire: Stack
    pos: tuple[int, int]
    angle: int

    def __init__(self, pos: tuple[int, int], angle: int):
        self.pos = pos
        self.angle = angle

        self.body = Stack("assets/sprites/cars/red/body.png", 7)

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        self.body.draw(screen, self.pos, self.angle)
