from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None
    price: Decimal
    category_id: int
    is_published: bool = True
    created: datetime = None
    updated: datetime = None


class Product(ProductBase):
    id: int




class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None
    is_published: bool = True
    created: datetime = None
    updated: datetime = None


class Category(CategoryBase):
    id: int
