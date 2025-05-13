# app/schemas/address.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool = False

class AddressCreate(AddressBase):
    customer_id: int

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None

class AddressResponse(AddressBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
