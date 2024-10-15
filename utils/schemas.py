from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    category_id: int
    is_published: bool = True
    created: datetime = None
    updated: datetime = None

    class Config:
        from_attributes = True


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_published: bool = True
    created: datetime = None
    updated: datetime = None

    class Config:
        from_attributes = True


class Category(CategoryBase):
    id: int
