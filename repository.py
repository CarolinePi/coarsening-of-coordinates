from typing import Any

from aiopg.sa import create_engine

from config import DatabaseConfig


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

