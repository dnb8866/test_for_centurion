import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

"""
SERVER
"""
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
LOG_LEVEL = 'info'


"""
POSTGRESQL
"""
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DB = "centurion"
SQLALCHEMY_DATABASE_URL = (f"postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:"
                           f"{POSTGRESQL_PORT}/{POSTGRESQL_DB}")
