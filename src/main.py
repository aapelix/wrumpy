import net.task

import const
from scene import manager
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


async def main():

    net.task.run(HOST, PORT)

    screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
    canvas = pygame.Surface((const.CANVAS_WIDTH, const.CANVAS_HEIGHT))

    clock = pygame.time.Clock()

    manager.switch(MenuScene())

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            msg = net.task.socket_in.get_nowait()
            print(f"got {msg}")
            manager.handle_msg(msg)
        except asyncio.QueueEmpty:
            pass

        if manager.current_scene is None:
            await asyncio.sleep(0)
            screen.fill((255, 255, 255))
            pygame.display.update()
            continue

        await manager.current_scene.update(dt)

        screen.fill((0, 0, 0))
        canvas.fill((255, 255, 255))

        manager.current_scene.draw(canvas)
        screen.blit(
            pygame.transform.scale(canvas, screen.get_size()),
            (0, 0),
        )
        pygame.display.update()

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
