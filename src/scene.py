import pygame
from abc import abstractmethod, ABCMeta


class Scene(metaclass=ABCMeta):
    """Base scene to be inherited from"""

    name: str

    @abstractmethod
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
