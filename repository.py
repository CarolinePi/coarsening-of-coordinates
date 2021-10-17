from typing import Any, List, Dict

from aiopg.sa import create_engine
from aiopg.sa.result import RowProxy
from sqlalchemy import select
from sqlalchemy.sql import Selectable

from config import DatabaseConfig
from models.base_model import BaseModel
from models.user import UserModel


class Repository:
    __slots__ = ('_dsn', '_engine', 'timeout')

    def __init__(self, config: DatabaseConfig) -> None:
        self._dsn = config.dsn
        self.timeout = config.timeout

    async def __aenter__(self) -> 'Repository':
        self._engine = await create_engine(self._dsn, timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._engine.close()
        await self._engine.wait_closed()

    async def _fetchall(self, query: Selectable) -> List[RowProxy]:
        async with self._engine.acquire() as connection:
            cursor = await connection.execute(query)
            resp: List[RowProxy] = await cursor.fetchall()
            return resp

    # async def _first(self, query: Selectable) -> RowProxy:
    #     async with self._engine.acquire() as connection:
    #         cursor = await connection.execute(query)
    #         resp: RowProxy = await cursor.first()
    #         return resp

    async def _scalar(self, query: Selectable) -> Any:
        async with self._engine.acquire() as connection:
            return await connection.scalar(query)

    async def insert_row_to_model(
        self, model: BaseModel, **kwargs: Dict[str, Any]
    ) -> int:
        return await self._scalar(
            model.__table__
            .insert()
            .values(**kwargs)
            .returning(model.id)
        )

    async def select_from_model_by_ids(
        self, model: BaseModel, ids: List[int]
    ) -> List[RowProxy]:
        return await self._fetchall(
            select([model]).where(model.id.in_(ids))
        )

    async def select_user_password(self, full_name: str) -> str:
        return await self._scalar(
            select([UserModel.password_hash])
            .where(UserModel.full_name == full_name)
        )
