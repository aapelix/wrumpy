import net.task
from scenes.base import Scene
from ui.button import Button
import utils.font
import const
from ui.input import Input
from msg.messages import Message, JoinLobbyMsg
import pygame
import utils.events


class JoinScene(Scene):
    def __init__(self, manager):
        super().__init__("join", manager)
        self.input = Input(
            "",
            (const.CANVAS_WIDTH // 2 - 50, const.CANVAS_HEIGHT // 2 - 11),
            (100, 22),
        )

        self.font = utils.font.get_font_small()
        self.back_button = Button(
            value="Back",
            pos=(20, 20),
            size=(60, 22),
            on_click=self._on_back_click,
        )
        self.join_button = Button(
            value="Join",
            pos=(const.CANVAS_WIDTH // 2 - 25, const.CANVAS_HEIGHT // 2 + 20),
            size=(50, 22),
            on_click=self._on_join_click,
        )
        self.join_pressed = False

    def update(self, dt: float):
        self.input.update(dt, utils.events.get_events())
        self.input.value = self.input.value[:6]
        self.back_button.update()
        self.join_button.update()

    def handle_msg(self, msg: Message):
        if msg["type"] == "join":
            self.manager.switch_by_name("game")

    def draw(self, screen: pygame.Surface):
        text_surface = self.font.render("Enter lobby ID:", True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(const.CANVAS_WIDTH // 2, const.CANVAS_HEIGHT // 2 - 25)
        )
        screen.blit(text_surface, text_rect)
        self.input.draw(screen)
        self.back_button.draw(screen)
        self.join_button.draw(screen)

    def _on_back_click(self):
        self.manager.switch_by_name("menu")

    def _on_join_click(self):
        if self.join_pressed:
            return

        if len(self.input.value) == 0:
            return

        self.join_pressed = True

        net.task.send.put_nowait(
            JoinLobbyMsg(
                type="join",
                id=int(self.input.value),
            )
        )
