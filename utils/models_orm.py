from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, BigInteger, TIMESTAMP, func, true, Numeric
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from utils.schemas import Category, Product, ProductBase


class Base(DeclarativeBase):
    type_annotation_map = {datetime: TIMESTAMP(timezone=True)}


class CreatedUpdatedBase(Base):
    __abstract__ = True
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class IsPublishedBase(Base):
    __abstract__ = True
    is_published: Mapped[bool] = mapped_column(server_default=true())


class CategoryOrm(CreatedUpdatedBase, IsPublishedBase):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    products: Mapped[list['ProductOrm']] = relationship("ProductOrm", back_populates="category")

    @classmethod
    def from_schema(cls, schema: Category):
        return cls(
            id=schema.id if 'id' in schema.__dict__ else None,
            name=schema.name,
            description=schema.description,
            is_published=schema.is_published,
            created=schema.created,
            updated=schema.updated
        )


class ProductOrm(CreatedUpdatedBase, IsPublishedBase):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'))
    category: Mapped[CategoryOrm] = relationship("CategoryOrm", back_populates="products")

    @classmethod
    def from_schema(cls, schema: Product | ProductBase):
        return cls(
            id=schema.id if 'id' in schema.__dict__ else None,
            name=schema.name,
            description=schema.description,
            price=schema.price,
            category_id=schema.category_id,
            is_published=schema.is_published,
            created=schema.created,
            updated=schema.updated
        )
