from msg.codec import encode
import asyncio
from msg.messages import StateMsg, Message
from .player import Player


class Lobby:
    last_state: bytes

    def __init__(self):
        self.players: dict[asyncio.StreamWriter, Player] = {}
        self.last_state = encode(self.to_msg())

    def update(self, dt: float):
        for player in self.players.values():
            player.update(dt)

    def handle_message(self, writer: asyncio.StreamWriter, msg: Message):
        if msg["type"] == "input":
            player = self.players[writer]
            player.throttle = msg["input"]["throttle"]
            player.turn = msg["input"]["turn"]

    def to_msg(self) -> StateMsg:
        return StateMsg(
            type="state",
            state={"players": [player.to_dict() for player in self.players.values()]},
        )
