import math
import random
from typing import TypedDict


class PlayerDict(TypedDict):
    id: int
    x: float
    y: float
    rotation: float


class Player:
    def __init__(self):
        self.id = random.getrandbits(32)

        self.x = 0.0
        self.y = 0.0
        self.v = 0.0
        self.rotation = 0.0

        self.throttle = 0.0
        self.turn = 0.0

        # these should come from db initially in the future
        self.acceleration = 100.0
        self.max_v = 150.0
        self.friction = 50.0

        self.turn_speed = 20.0

        self.tire_rotation = 0.0
        self.tire_turn_speed = 70.0
        self.tire_return_speed = 70.0
        self.tire_max_rotation = 30.0

    def update(self, dt: float):
        if self.throttle != 0:
            self.v += self.acceleration * self.throttle * dt
        else:
            if self.v > 0:
                self.v -= self.friction * dt
                if self.v < 0:
                    self.v = 0.0
            elif self.v < 0:
                self.v += self.friction * dt
                if self.v > 0:
                    self.v = 0.0

        self.v = max(-self.max_v, min(self.v, self.max_v))

        if self.turn != 0:
            self.tire_rotation += self.tire_turn_speed * self.turn * dt
        else:
            if self.tire_rotation > 0:
                self.tire_rotation -= self.tire_return_speed * dt
                if self.tire_rotation < 0:
                    self.tire_rotation = 0.0
            elif self.tire_rotation < 0:
                self.tire_rotation += self.tire_return_speed * dt
                if self.tire_rotation > 0:
                    self.tire_rotation = 0.0

        self.tire_rotation = max(
            -self.tire_max_rotation, min(self.tire_rotation, self.tire_max_rotation)
        )

        self.rotation += (
            self.tire_rotation * (self.v / self.max_v) * self.turn_speed * dt
        )

        rad = (self.rotation * math.pi) / 180
        self.x += math.sin(rad) * self.v * dt
        self.y -= math.cos(rad) * self.v * dt

    def to_dict(self) -> PlayerDict:
        return PlayerDict(
            id=self.id,
            x=self.x,
            y=self.y,
            rotation=self.rotation,
        )
