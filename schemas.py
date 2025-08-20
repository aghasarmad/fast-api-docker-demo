from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class TeaBase(BaseModel):
    name: str
    origin: Optional[str] = None


class TeaCreate(TeaBase):
    pass


class TeaRead(TeaBase):
    id: UUID

    class Config:
        orm_mode = True  # Allows returning SQLAlchemy models directly
