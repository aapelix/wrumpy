from msg.messages import Message
import pygame
from abc import abstractmethod, ABCMeta


class Scene(metaclass=ABCMeta):
    """Base scene to be inherited from"""

    name: str

    @abstractmethod
    def __init__(self, name: str, manager):
        self.name = name
        self.manager = manager

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def handle_msg(self, msg: Message):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
