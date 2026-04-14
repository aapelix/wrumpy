from scenes.game import GameScene
from msg.messages import CreateLobbyMsg
import net.task
from entities.car import Car
import pygame
from scene import Scene, manager


class MenuScene(Scene):
    test_car: Car
    sent_create_msg: bool = False

    def __init__(self):
        super().__init__("menu")
        self.test_car = Car((50, 50), 0)

    async def update(self, dt: float):
        self.test_car.rotation += 45 * dt

        if not self.sent_create_msg and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.sent_create_msg = True

            await net.task.send.put(
                CreateLobbyMsg(
                    type="create",
                )
            )

    def handle_msg(self, msg):
        if msg["type"] == "join":
            manager.switch(GameScene())

    def draw(self, screen: pygame.Surface):
        self.test_car.draw(screen)
