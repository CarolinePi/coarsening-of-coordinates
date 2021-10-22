import dataclasses
from os import getenv
from pathlib import Path
from typing import List, Dict, Any

import trafaret as t

from trafaret_config import read_and_validate

APP_TRAFARET = t.Dict({
    'host': t.String(),
    'port': t.Int(),
    'domain': t.String(),
    'secret_key': t.String(),
    'secret_table': t.List(t.Int),
    'n': t.Float(),
})

DB_TRAFARET = t.Dict({
    'host': t.String(),
    'port': t.Int(),
    'db': t.String(),
    'user': t.String(),
    t.Key('password', optional=True): t.String(),   # TODO: substitution
    'timeout': t.Int(),
    'min_pool_size': t.Int(),
    'max_pool_size': t.Int(),
})

CONFIG_TRAFARET = t.Dict({
    'app': APP_TRAFARET,
    'db': DB_TRAFARET,
})


@dataclasses.dataclass
class AppConfig:
    host: str
    port: str
    domain: str
    secret_table: List[int]
    secret_key: bytes
    n: float

    def __init__(self, **kwargs: Dict[str, Any]):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


@dataclasses.dataclass
class DatabaseConfig:
    host: str
    port: str
    db: str
    user: str
    timeout: int
    min_pool_size: int
    max_pool_size: int
    password: str

    @property
    def dsn(self) -> str:
        return f'postgres://{self.user}:{self.password}@' \
               f'{self.host}:{self.port}/{self.db}'


@dataclasses.dataclass()
class Config:
    app: AppConfig
    db: DatabaseConfig


def parse_config(file_path: str) -> Config:
    config = read_and_validate(file_path, CONFIG_TRAFARET)
    if config is None:
        raise RuntimeError(f'Config not found: {config}')
    return Config(
        app=AppConfig(**config['app']),
        db=DatabaseConfig(**config['db'])
    )


def get_config() -> Config:
    # TODO: config_path = os.environ.get('CONFIG_PATH')
    config_path = f'{Path(__file__).parent}/config.yaml'
    return parse_config(config_path)


def _get_env(key: str) -> str:
    env = getenv(key)
    if env:
        return env
    raise RuntimeError(f'Variable \'{key}\' not set')
