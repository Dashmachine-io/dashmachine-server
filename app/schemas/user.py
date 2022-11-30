from pydantic import BaseModel


class UserCreate(BaseModel):
    pass


class UserBase(BaseModel):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
