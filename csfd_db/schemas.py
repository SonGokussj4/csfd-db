from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = False


class UserCreate(UserBase):
    password: str


class UserCreateDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserInDB(UserCreateDBBase):
    hashed_password: str
