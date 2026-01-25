from pydantic import BaseModel, Field
from typing import Optional

# Модель для создания
class Advertisement(BaseModel):
    title: str
    description: str
    price: float = Field(gt=0, description="Цена должна быть больше 0")
    author: str
    contacts: str

# Модель для обновления
class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    author: Optional[str] = None
    contacts: Optional[str] = None