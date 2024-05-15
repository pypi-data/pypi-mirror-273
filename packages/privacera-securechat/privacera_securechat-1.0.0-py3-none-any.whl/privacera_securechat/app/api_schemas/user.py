from pydantic import BaseModel


class PostUserLoginRequest(BaseModel):
    user_name: str


class UserLoginResponse(BaseModel):
    user_id: int
    user_name: str
