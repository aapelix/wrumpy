import assets.sheet
import pygame


class Stack:
    def __init__(self, path: str, frame_count: int):
        self.frames = assets.sheet.get_frames(path, frame_count)

    def draw(self, screen: pygame.Surface, pos: tuple[float, float], rotation: float):
        for i, img in enumerate(self.frames):
            rotated_img = pygame.transform.rotate(img, -rotation)
            screen.blit(
                rotated_img,
                (
                    pos[0] - rotated_img.get_width() // 2,
                    pos[1] - rotated_img.get_height() // 2 - i,
                ),
            )
