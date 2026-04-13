from typing import TypedDict, Literal, Union


class JoinMsg(TypedDict):
    type: Literal["join"]
    id: str


class PingMsg(TypedDict):
    type: Literal["ping"]
    ts: float


Message = Union[JoinMsg, PingMsg]
