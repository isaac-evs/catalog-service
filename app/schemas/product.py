# app/schemas/product.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    sku: str
    inventory_count: int = 0
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    sku: Optional[str] = None
    inventory_count: Optional[int] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
