from typing import TypedDict, Literal, Union
from lobby.player import PlayerDict


class JoinLobbyMsg(TypedDict):
    type: Literal["join"]
    id: int


class CreateLobbyMsg(TypedDict):
    type: Literal["create"]


class State(TypedDict):
    players: list[PlayerDict]


class StateMsg(TypedDict):
    type: Literal["state"]
    state: State


class Input(TypedDict):
    throttle: float
    turn: float


class InputMsg(TypedDict):
    type: Literal["input"]
    input: Input


Message = Union[JoinLobbyMsg, CreateLobbyMsg, StateMsg, InputMsg]
