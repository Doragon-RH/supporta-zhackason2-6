from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., title="email")


class UserCreate(UserBase):
    password: str = Field(..., title="Password")


class User(UserBase):
    id: int = Field(0, title="ID")
    name: int = Field("", title="Name")
    user_id: int = Field("", title="User ID")
    created_at: datetime = Field(datetime.now(), title="Creation Date")

    class Config:
        orm_mode = True
