from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..schemas.player import *
from ..models import GameModel, PlayerModel
from .utils import add_commit_refresh
from .generic import generate_basic_service_methods


class PlayerService:
    get, get_all, _, _, delete = generate_basic_service_methods(
        PlayerModel, PlayerResponse, PlayerCreate, None
    )

    @staticmethod
    async def get_by_token(ss: AsyncSession, token: str) -> PlayerExtendedResponse:
        result = await ss.execute(
            select(PlayerModel)
            .options(selectinload(PlayerModel.game).selectinload(GameModel.settings))
            .where(PlayerModel.token == token)
        )
        return PlayerExtendedResponse.model_validate(result.scalars().one())

    @staticmethod
    async def get_by_game_id(ss: AsyncSession, game_id: int) -> list[PlayerResponse]:
        result = await ss.execute(
            select(PlayerModel).where(PlayerModel.game_id == game_id)
        )
        return list(map(PlayerResponse.model_validate, result.scalars().all()))

    @staticmethod
    async def create(ss: AsyncSession, schema: PlayerCreate) -> PlayerWithTokenResponse:
        model = PlayerModel(**schema.model_dump())
        await add_commit_refresh(ss, model)
        return PlayerWithTokenResponse.model_validate(model)