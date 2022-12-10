from .jwt import JWTAuthen
from .postgres import Postgres

from app.models.model import Base

class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class EndpointsManager(Singleton):
    def init_config(self, config):
        self.postgres = Postgres(config)
        self.jwt = JWTAuthen(config)

    async def init_db(self):
        endpoints.postgres.init_session()
        await endpoints.postgres.init_db(Base.metadata)

endpoints = EndpointsManager()