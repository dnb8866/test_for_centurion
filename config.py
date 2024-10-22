import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

MODE = ''  # Установите 'TEST' для запуска тестов или '' в остальных случаях.

"""
POSTGRESQL
"""
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DB = "centurion"
POSTGRESQL_DB_TEST = "centurion_test"
SQLALCHEMY_DATABASE_URL = (f"postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:"
                           f"{POSTGRESQL_PORT}/{POSTGRESQL_DB}")

SQLALCHEMY_DATABASE_URL_TEST = (f"postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:"
                           f"{POSTGRESQL_PORT}/{POSTGRESQL_DB_TEST}")
