from enum import Enum
from pydantic import BaseModel as BaseSchema, ConfigDict


class PlayerStatus(str, Enum):
    PLAYING = "PLAYING"
    SPECTATOR = "SPECTATOR"
    SEARCH = "SEARCH"


class PlayerBase(BaseSchema):
    nickname: str


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(PlayerBase):
    id: int
    status: PlayerStatus

    model_config = ConfigDict(from_attributes=True)


class PlayerResponse(PlayerUpdate):
    id: int
    token: str