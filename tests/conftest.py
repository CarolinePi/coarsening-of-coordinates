import pytest

from dl.repository import Repository

# TODO: setup db for test


class DatabaseConfig:
    def __init__(self, dsn):
        self.dsn = dsn
        self.timeout = 10


@pytest.fixture(scope="session")
def db_config():
    return DatabaseConfig(
        dsn='postgres://project_admin:password@10.254.0.1:5432/main'
    )


@pytest.fixture
async def repository(loop, db_config) -> Repository:
    return await Repository(db_config).__aenter__()
