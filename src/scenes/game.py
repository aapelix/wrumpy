import net.task
from msg.messages import Message, Input, InputMsg
from entities.car import Car
import pygame
from scene import Scene


class GameScene(Scene):
    cars: dict[int, Car] = {}
    last_input: Input

    def __init__(self):
        super().__init__("game")
        self.last_input = Input(throttle=0, turn=0)

    async def update(self, dt: float):
        for car in self.cars.values():
            car.update(dt)

        throttle, turn = 0, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            throttle = 1
        elif keys[pygame.K_s]:
            throttle = -1

        if keys[pygame.K_a]:
            turn = -1
        elif keys[pygame.K_d]:
            turn = 1

        if (throttle, turn) != (self.last_input["throttle"], self.last_input["turn"]):
            self.last_input = Input(throttle=throttle, turn=turn)
            await net.task.send.put(
                InputMsg(
                    type="input",
                    input=Input(throttle=throttle, turn=turn),
                )
            )

    def handle_msg(self, msg: Message):
        if msg["type"] == "state":
            for player in msg["state"]["players"]:
                if player["id"] not in self.cars:
                    self.cars[player["id"]] = Car(
                        (player["x"], player["y"]), player["rotation"]
                    )

                car = self.cars[player["id"]]

                car.set_state((player["x"], player["y"]), player["rotation"])

    def draw(self, screen: pygame.Surface):
        for car in self.cars.values():
            car.draw(screen)
