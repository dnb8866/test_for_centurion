import config
from src.utils.db import SqlAlchemyDb
from src.utils.models_orm import Base
from src.utils.repositories import ProductRepository, CategoryRepository

sql_db = SqlAlchemyDb(config.SQLALCHEMY_DATABASE_URL_TEST, Base, test=True if config.MODE == 'TEST' else False)
product_repo = ProductRepository(sql_db)
category_repo = CategoryRepository(sql_db)
