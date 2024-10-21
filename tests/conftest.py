from datetime import datetime, timedelta
from decimal import Decimal
from random import randint, random

import pytest
from mimesis import Food
from mimesis.locales import Locale
from sqlalchemy.ext.asyncio import AsyncSession
from unicodedata import category

import config
from utils.db import SqlAlchemyDb
from utils.models_orm import Base, ProductOrm, CategoryOrm
from utils.repositories import ProductRepository, CategoryRepository


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def db():
    return SqlAlchemyDb(config.SQLALCHEMY_DATABASE_URL_TEST, Base, test=True)


@pytest.fixture(scope="session")
def category_repo(db):
    return CategoryRepository(db)


@pytest.fixture(scope="session")
def product_repo(db):
    return ProductRepository(db)


@pytest.fixture
async def session(db):
    await db.clean()
    await db.prepare()
    async with db.SessionLocal() as session:
        yield session


@pytest.fixture
def one_category():
    return CategoryOrm(name="Test Category")


@pytest.fixture
async def one_category_in_db(session: AsyncSession, one_category):
    session.add(one_category)
    await session.commit()
    await session.refresh(one_category)
    return one_category


@pytest.fixture
def one_product(one_category_in_db):
    return ProductOrm(name="Продукт 1", price=Decimal('100.2'), category_id=one_category_in_db.id)


@pytest.fixture
async def one_product_in_db(session: AsyncSession, one_product):
    session.add(one_product)
    await session.commit()
    await session.refresh(one_product)
    return one_product


@pytest.fixture
async def many_categories_and_products(session: AsyncSession):
    food = Food(locale=Locale.RU)
    now_time = datetime.now()
    categories = []
    products = []
    for i in range(10):
        categories.append(CategoryOrm(name=food.fruit(), created=now_time-timedelta(days=i)))
    for i in range(100):
        category_id = i % 10 + 1
        products.append(
            ProductOrm(
                name=food.spices(),
                price=Decimal(str(i+0.1)),
                category_id=category_id,
                created=now_time-timedelta(days=i)
            )
        )
    session.add_all(categories)
    session.add_all(products)
    await session.commit()
