from pygame.math import lerp
import pygame
from stack import Stack


class Car:
    body: Stack
    tire: Stack
    pos: tuple[float, float]
    rotation: float

    def __init__(self, pos: tuple[float, float], angle: float):
        self.pos = pos
        self.rotation = angle

        self.body = Stack("assets/sprites/cars/red/body.png", 7)

        self.target_pos = pos
        self.target_rot = angle

        self.last_pos = pos
        self.last_rot = angle

        self.t = 1.0

    def set_state(self, pos, rot):
        self.last_pos = self.pos
        self.last_rot = self.rotation

        self.target_pos = pos
        self.target_rot = rot

        self.t = 0.0

    def update(self, dt: float):
        self.t = min(self.t + dt * 10, 1)

        self.pos = (
            lerp(self.last_pos[0], self.target_pos[0], self.t),
            lerp(self.last_pos[1], self.target_pos[1], self.t),
        )
        self.rotation = lerp(self.last_rot, self.target_rot, self.t)

    def draw(self, screen: pygame.Surface):
        self.body.draw(screen, self.pos, self.rotation)
