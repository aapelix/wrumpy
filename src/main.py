import net.task

import const
from scene import Scene
from scenes.menu import MenuScene
import asyncio
import pygame
import sys
import platform

HOST = "localhost"
PORT = 5555

if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

    if not aio.cross.simulator:  # noqa: F821
        PORT += 20000
        platform.window.python.websocket.url = "ws://"


pygame.init()

current_scene: Scene


async def main():
    global current_scene

    net.task.run(HOST, PORT)

    screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
    canvas = pygame.Surface((const.CANVAS_WIDTH, const.CANVAS_HEIGHT))

    clock = pygame.time.Clock()

    current_scene = MenuScene()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            msg = net.task.socket_in.get_nowait()
            print(f"got {msg}")
        except asyncio.QueueEmpty:
            pass

        await current_scene.update(dt)

        screen.fill((0, 0, 0))
        canvas.fill((255, 255, 255))

        current_scene.draw(canvas)
        screen.blit(
            pygame.transform.scale(canvas, screen.get_size()),
            (0, 0),
        )
        pygame.display.update()

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
