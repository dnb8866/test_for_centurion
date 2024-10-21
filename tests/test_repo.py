import pytest
from sqlalchemy import select

from utils.models_orm import ProductOrm, CategoryOrm
from utils.schemas import Product, Category

pytestmark = pytest.mark.asyncio


class TestProductRepo:

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
        assert updated_product.name == 'Обновленное имя товара'
        assert updated_product.price == product.price
        assert updated_product.category_id == product.category_id
        assert updated_product.updated == product.updated
        assert updated_product.created == product.created
        assert updated_product.description == product.description

    async def test_delete(self, session, product_repo, one_product_in_db):
        products = set(await session.execute(select(ProductOrm)))
        await product_repo.delete(one_product_in_db.id)
        assert len(products - set(await session.execute(select(ProductOrm)))) == 1


class TestCategoryRepo:

    async def test_create(self, session, category_repo, one_category):
        categories = set(await session.execute(select(CategoryOrm)))
        created_product = await category_repo.create(one_category)
        assert len(set(await session.execute(select(CategoryOrm))) - categories) == 1
        assert one_category.name == created_product.name

    async def test_get(self, session, category_repo, one_category_in_db):
        categories = set(await session.execute(select(CategoryOrm)))
        assert await category_repo.get(one_category_in_db.id) == Category.model_validate(one_category_in_db)
        assert set(await session.execute(select(CategoryOrm))) == categories

    async def test_list(self, session, category_repo, many_categories_and_products):
        categories = set(await session.execute(select(CategoryOrm)))
        assert len(await category_repo.list()) == 10
        categories_query = await category_repo.list(limit=5)
        assert len(categories_query) == 5
        created = [category.created for category in categories_query]
        assert created == sorted(created, reverse=True)
        assert set(await session.execute(select(CategoryOrm))) == categories

    async def test_update(self, session, category_repo, one_category_in_db):
        categories = set(await session.execute(select(CategoryOrm)))
        one_category_in_db.name = 'Обновленное имя категории'
        updated_category = await category_repo.update(one_category_in_db)
        category = await category_repo.get(one_category_in_db.id)
        assert set(await session.execute(select(CategoryOrm))) == categories
        assert updated_category.name == 'Обновленное имя категории'
        assert updated_category.updated == category.updated
        assert updated_category.created == category.created
        assert updated_category.description == category.description

    async def test_delete(self, session, category_repo, one_category_in_db):
        categories = set(await session.execute(select(CategoryOrm)))
        await category_repo.delete(one_category_in_db.id)
        assert len(categories - set(await session.execute(select(CategoryOrm)))) == 1