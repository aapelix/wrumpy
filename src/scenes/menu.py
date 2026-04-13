import net.task
from msg.messages import PingMsg
from entities.car import Car
import pygame
from scene import Scene


class MenuScene(Scene):
    test_car: Car

    def __init__(self):
        super().__init__("menu")
        self.test_car = Car((50, 50), 0)

    async def update(self, dt: float):
        self.test_car.angle += 45 * dt

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            await net.task.send.put(PingMsg(ts=pygame.time.get_ticks() / 1000.0))

    def draw(self, screen: pygame.Surface):
        self.test_car.draw(screen)
