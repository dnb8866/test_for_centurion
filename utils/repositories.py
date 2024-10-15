from fastapi import HTTPException, status
from sqlalchemy import select, update

from utils.entities import Repository
from utils.models_orm import ProductOrm, CategoryOrm
from utils.schemas import Product, Category

async def query_is_published_offset_limit(
        query: select,
        is_published: bool | None = None,
        offset: int | None = None,
        limit: int | None = None
):
    if is_published is not None:
        query = query.where(ProductOrm.is_published == is_published)
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    return query


class ProductRepository(Repository):
    async def create(self, product: Product) -> Product:
        async with self.db.SessionLocal() as session:
            product_orm = ProductOrm.from_schema(product)
            session.add(product_orm)
            await session.commit()
            return Product.model_validate(product_orm)

    async def get(self, product_id: int) -> Product | None:
        async with self.db.SessionLocal() as session:
            product_orm = (await session.execute(
                select(ProductOrm)
                .where(ProductOrm.id == product_id)
            )).scalar_one_or_none()
            return Product.model_validate(product_orm) if product_orm else None

    async def list(
            self,
            offset: int | None = None,
            limit: int | None = None,
            text_in_name: str | None = None,
            text_in_description: str | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            category_id: int | None = None,
            is_published: bool | None = None
    ) -> list[Product] | None:
        query = select(ProductOrm).order_by(ProductOrm.created.desc())
        if text_in_name is not None:
            query = query.where(ProductOrm.name.ilike(f'%{text_in_name}%'))
        if text_in_description is not None:
            query = query.where(ProductOrm.description.ilike(f'%{text_in_description}%'))
        if min_price is not None:
            query = query.where(ProductOrm.price >= min_price)
        if max_price is not None:
            query = query.where(ProductOrm.price <= max_price)
        if category_id is not None:
            query = query.where(ProductOrm.category_id == category_id)
        query = await query_is_published_offset_limit(
            query,
            is_published,
            offset,
            limit
        )
        async with self.db.SessionLocal() as session:
            return (await session.execute(query)).scalars().all()


    async def update(self, product: Product) -> Product:
        async with self.db.SessionLocal() as session:
            await session.execute(
                update(ProductOrm)
                .values(
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    is_published=product.is_published,
                    category_id=product.category_id,
                ).where(ProductOrm.id == product.id)
            )
            await session.commit()
            product_orm = (await session.execute(
                select(ProductOrm).where(ProductOrm.id == product.id)
            )).scalar_one_or_none()
            return Product.model_validate(product_orm)

    async def delete(self, product_id: int) -> None:
        async with self.db.SessionLocal() as session:
            product_orm = (await session.execute(
                select(ProductOrm).where(ProductOrm.id == product_id)
            )).scalar_one_or_none()
            if not product_orm:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='При удалении продукт не был найден в БД'
            )
            await session.delete(product_orm)
            await session.commit()


class CategoryRepository(Repository):
    async def create(self, category: Category) -> Category:
        async with self.db.SessionLocal() as session:
            category_orm = CategoryOrm.from_schema(category)
            session.add(category_orm)
            await session.commit()
            return Category.model_validate(category_orm)

    async def get(self, category_id: int):
        async with self.db.SessionLocal() as session:
            category_orm = (await session.execute(
                select(CategoryOrm)
                .where(CategoryOrm.id == category_id)
            )).scalar_one_or_none()
            return Category.model_validate(category_orm)

    async def list(
            self,
            offset: int | None = None,
            limit: int | None = None,
            name: str | None = None,
            is_published: bool | None = None
    ):
        query = select(CategoryOrm).order_by(CategoryOrm.created.desc())
        if name is not None:
            query = query.where(CategoryOrm.name.ilike(f'%{name}%'))
        query = await query_is_published_offset_limit(
            query,
            is_published,
            offset,
            limit
        )
        async with self.db.SessionLocal() as session:
            return (await session.execute(query)).scalars().all()

    async def update(self, category: Category):
        async with self.db.SessionLocal() as session:
            await session.execute(
                update(CategoryOrm)
                .values(
                    name=category.name,
                    description=category.description,
                    is_published=category.is_published,
                ).where(CategoryOrm.id == category.id)
            )
            await session.commit()
            category_orm = (await session.execute(
                select(CategoryOrm).where(CategoryOrm.id == category.id)
            )).scalar_one_or_none()
            return Category.model_validate(category_orm)

    async def delete(self, category_id: int):
        async with self.db.SessionLocal() as session:
            category_orm = (await session.execute(
                select(CategoryOrm).where(CategoryOrm.id == category_id)
            )).scalar_one_or_none()
            if not category_orm:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='При удалении категория не быа найдена в БД'
                )
            await session.delete(category_orm)
            await session.commit()
