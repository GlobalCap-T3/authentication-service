from pydantic import BaseModel

class ErrorResp(BaseModel):
    detail: str

class SuccessResp(BaseModel):
    message: str

class UserCreateResp(BaseModel):
    email: str
    first_name: str
    last_name: str

