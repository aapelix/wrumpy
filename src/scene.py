from msg.messages import Message
import pygame
from abc import abstractmethod, ABCMeta


class Scene(metaclass=ABCMeta):
    """Base scene to be inherited from"""

    name: str

    @abstractmethod
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def update(self, dt: float):
        pass

    @abstractmethod
    def handle_msg(self, msg: Message):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass


class Manager:
    current_scene: Scene | None = None

    def switch(self, scene: Scene):
        self.current_scene = scene

    def handle_msg(self, msg: Message):
        if self.current_scene is not None:
            self.current_scene.handle_msg(msg)


manager = Manager()
