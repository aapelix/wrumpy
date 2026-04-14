import random
from msg.messages import Message
from msg.codec import encode
import asyncio
from .lobby import Lobby
from .player import Player

lobbies: dict[int, Lobby] = {}
lobby_id_by_writer: dict[asyncio.StreamWriter, int] = {}

TICK_RATE = 20


def handle_msg(writer: asyncio.StreamWriter, msg: Message):
    lobby_id = lobby_id_by_writer.get(writer)
    if lobby_id:
        lobby = lobbies[lobby_id]
        lobby.handle_message(writer, msg)
    else:
        match msg["type"]:
            case "join":
                lobby_id = msg["id"]
                if lobby_id in lobbies:
                    lobby = lobbies[lobby_id]
                    lobby.players[writer] = Player()
                    lobby_id_by_writer[writer] = lobby_id

                    writer.write(encode({"type": "join", "id": lobby_id}))
                else:
                    print(f"lobby {lobby_id} does not exist")
            case "create":
                lobby_id = random.randint(100000, 999999)
                if lobby_id in lobbies:
                    handle_msg(writer, msg)
                    return

                lobby = Lobby()
                lobby.players[writer] = Player()
                lobbies[lobby_id] = lobby
                lobby_id_by_writer[writer] = lobby_id

                writer.write(encode({"type": "join", "id": lobby_id}))
            case _:
                print(f"unknown message type: {msg['type']}")


async def game_loop():
    while True:
        dead_lobbies = []

        for id, lobby in lobbies.items():
            if len(lobby.players) == 0:
                dead_lobbies.append(id)
                continue

            lobby.update(1 / TICK_RATE)

            msg = lobby.to_msg()
            data = encode(msg)

            if data == lobby.last_state:
                continue
            else:
                lobby.last_state = data

            dead = []

            for writer in lobby.players.keys():
                try:
                    writer.write(data)
                    await writer.drain()
                except Exception:
                    dead.append(writer)

            for writer in dead:
                del lobby.players[writer]
                del lobby_id_by_writer[writer]

        for id in dead_lobbies:
            del lobbies[id]

        await asyncio.sleep(1 / TICK_RATE)
