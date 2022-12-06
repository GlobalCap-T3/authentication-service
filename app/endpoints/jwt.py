from datetime import datetime, timedelta
from jose import jwt

from pydantic import BaseModel

class JWTModel(BaseModel):
    secret: str
    algorithm: str
    access_token_expire_minutes: int

class JWTAuthen:
    config_key = "jwt"
    def __init__(self, config: dict = {}):
        if config:
            self.init_config(config)

    def init_config(self, config):
        jwt_config = config.get(self.config_key)
        if jwt_config:
            self.config = JWTModel(**jwt_config)
            self.secret = self.config.secret
            self.algorithm = self.config.algorithm
            self.access_token_lifetime = timedelta(minutes=self.config.access_token_expire_minutes)

    def generate_access_token(self, sub: str):
        return self.generate_token(
            token_type="access_token",
            expires_after=self.access_token_lifetime,
            sub=sub
        )

    def generate_token(self, token_type: str, expires_after: timedelta, sub: str):
        expires_after = expires_after
        exp = datetime.utcnow() + expires_after
        payload = {
            "token_type": token_type,
            "exp": exp,
            "iat": datetime.utcnow(),
            "sub": str(sub)
        }
        encode_jwt = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return encode_jwt

    def decode_token(self, token):
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        return payload

    def verify_token(self, token):
        decode_token = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        return decode_token["expires"] >= datetime.utcnow()