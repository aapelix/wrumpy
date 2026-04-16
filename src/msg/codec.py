import json
from .messages import Message


def encode(msg: Message) -> bytes:
    return (json.dumps(msg) + "\n").encode("utf-8")


def decode(line: str) -> Message:
    return json.loads(line)
