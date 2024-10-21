import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import config
from src.utils.db import SqlAlchemyDb
from src.utils.models_orm import Base
from src.utils.repositories import ProductRepository, CategoryRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('Prepare database')
    await sql_db.prepare()
    yield
    logging.info("Application shutdown")


sql_db = SqlAlchemyDb(config.SQLALCHEMY_DATABASE_URL, Base)
product_repo = ProductRepository(sql_db)
category_repo = CategoryRepository(sql_db)
logger = logging.getLogger('uvicorn.error')
app = FastAPI(lifespan=lifespan)
