import pytest
from sqlalchemy import select

from utils.models_orm import ProductOrm
from utils.schemas import Product

pytestmark = pytest.mark.asyncio


class TestProduct:

    async def test_create(self, session, product_repo, one_product):
        products = set(await session.execute(select(ProductOrm)))
        created_product = await product_repo.create(one_product)
        assert len(set(await session.execute(select(ProductOrm))) - products) == 1
        assert created_product.name == one_product.name
        assert created_product.price == one_product.price
        assert created_product.category_id == one_product.category_id

    async def test_get(self, session, product_repo, one_product_in_db):
        products = set(await session.execute(select(ProductOrm)))
        assert await product_repo.get(one_product_in_db.id) == Product.model_validate(one_product_in_db)
        assert set(await session.execute(select(ProductOrm))) == products

    async def test_list(self, session, product_repo, many_categories_and_products):
        products = set(await session.execute(select(ProductOrm)))
        assert len(await product_repo.list(category_id=1)) == 10
        assert len(await product_repo.list()) == 100
        products_query = await product_repo.list(limit=20)
        assert len(products_query) == 20
        created = [product.created for product in products_query]
        assert created == sorted(created, reverse=True)
        assert len(await product_repo.list(max_price=4.9)) == 5
        assert len(await product_repo.list(min_price=94.5)) == 5
        assert set(await session.execute(select(ProductOrm))) == products

    async def test_update(self, session, product_repo, one_product_in_db):
        products = set(await session.execute(select(ProductOrm)))
        one_product_in_db.name = 'Обновленное имя товара'
        updated_product = await product_repo.update(one_product_in_db)
        product = await product_repo.get(one_product_in_db.id)
        assert set(await session.execute(select(ProductOrm))) == products
        assert updated_product.name == product.name
        assert updated_product.price == product.price
        assert updated_product.category_id == product.category_id
        assert updated_product.updated == product.updated
        assert updated_product.created == product.created
        assert updated_product.description == product.description

    async def test_delete(self, session, product_repo, one_product_in_db):
        products = set(await session.execute(select(ProductOrm)))
        await product_repo.delete(one_product_in_db.id)
        assert len(products - set(await session.execute(select(ProductOrm)))) == 1
