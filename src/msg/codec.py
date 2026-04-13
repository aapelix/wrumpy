import json
from .messages import Message


def encode(msg: Message) -> bytes:
    return json.dumps(msg).encode("utf-8")


def decode(data: bytes) -> Message:
    return json.loads(data.decode("utf-8"))
