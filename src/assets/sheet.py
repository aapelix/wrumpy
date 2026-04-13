import pygame

frame_cache: dict[str, list[pygame.Surface]] = {}


def get_frames(path: str, frame_count: int) -> list[pygame.Surface]:
    if path in frame_cache:
        return frame_cache[path]

    img = pygame.image.load(path).convert_alpha()

    frame_w = img.get_width() // frame_count
    frame_h = img.get_height()

    frames: list[pygame.Surface] = []
    for x in range(frame_count):
        frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
        frame.blit(img, (0, 0), (x * frame_w, 0, frame_w, frame_h))
        frames.append(frame)

    frame_cache[path] = frames
    return frames
