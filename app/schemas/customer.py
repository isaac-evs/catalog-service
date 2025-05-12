# app/schemas/customer.py
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool = False

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool = True

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
