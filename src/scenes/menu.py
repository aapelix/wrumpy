from scenes.base import Scene
from ui.button import Button
from msg.messages import CreateLobbyMsg
import net.task
from entities.car import Car
import pygame


class MenuScene(Scene):
    test_car: Car
    sent_create_msg: bool = False
    create_button: Button
    join_button: Button

    def __init__(self, manager):
        super().__init__("menu", manager)
        self.test_car = Car((50, 50), 0)
        self.create_button = Button(
            value="Create",
            pos=(20, 100),
            size=(80, 22),
            on_click=self._on_create_click,
            offset_y=2,
        )
        self.join_button = Button(
            value="Join",
            pos=(20, 130),
            size=(80, 22),
            on_click=self._on_join_click,
        )

    def update(self, dt: float):
        self.test_car.rotation += 45 * dt
        self.create_button.update()
        self.join_button.update()

    def handle_msg(self, msg):
        if msg["type"] == "join":
            self.manager.switch_by_name("game")

    def draw(self, screen: pygame.Surface):
        self.test_car.draw(screen)
        self.create_button.draw(screen)
        self.join_button.draw(screen)

    def _on_create_click(self):
        if self.sent_create_msg:
            return

        self.sent_create_msg = True
        net.task.send.put_nowait(
            CreateLobbyMsg(
                type="create",
            )
        )

    def _on_join_click(self):
        self.manager.switch_by_name("join")
