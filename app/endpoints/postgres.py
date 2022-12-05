from pydantic import BaseModel
from typing import Optional
from logging import getLogger

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

logger = getLogger(f'uvicorn.{__name__}')


class PostgresConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: Optional[str]

class Postgres:

    config_key = "postgres"

    def __init__(self, config: Optional[dict] = None):
        if config:
            self.init_config(config)

    def init_config(self, config: dict):
        if self.config_key in config:
            self.config = PostgresConfig(**config[self.config_key])
            self.uri = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
                self.config.user,
                self.config.password,
                self.config.host,
                self.config.port,
                self.config.database
            )
            self.engine = create_async_engine(self.uri)
            logger.info("[db] Postgres URI: %s", self.uri)
        else:
            raise ValueError(
                f"Expected {self.config_key} in configuration dict but found None."
            )

    def init_session(self):
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        return self.session

    async def init_db(self, metadata):
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
            logger.debug("[db] Created all tables: %s", metadata.tables.keys())