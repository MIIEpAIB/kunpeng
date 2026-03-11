from pydantic import BaseModel

from backend.app.schemas.common import AdminTokenData


class AdminLoginRequest(BaseModel):
    username: str
    password: str
    captcha: str


class AdminLoginResponse(AdminTokenData):
    pass


class AdminUserOut(BaseModel):
    id: int
    username: str
    status: int

    class Config:
        orm_mode = True

