from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Literal

class AdvertisementCreate(BaseModel):
    title: str
    description: str
    price: float = Field(gt=0, description="Цена должна быть больше 0")
    contacts: str

class Advertisement(AdvertisementCreate):
    id: int
    author: str
    created_at: str

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    author: Optional[str] = None
    contacts: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: Literal["user", "admin"] = "user"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Literal["user", "admin"]] = None

class User(BaseModel):
    id : int
    username: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str
