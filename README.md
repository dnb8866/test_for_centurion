# Тестовое задание на FastAPI с использованием SQLAlchemy, Poetry, Alembic, Pytest
# Сервис REST API для управления продуктами.

## Установка
1. Сервис написан на Python 3.12.5.
2. Установите с использованием poetry (poetry install).
3. Создайте базу данных в PostgreSQL с названием centurion.
4. Создайте в корневой папке сервиса файл .env и укажите переменные:
   * POSTGRESQL_USER
   * POSTGRESQL_PASSWORD
   * POSTGRESQL_HOST (127.0.0.1)
   * POSTGRESQL_PORT (5432)

5. Примените миграции с помощью alembic (poetry run alembic upgrade head).
6. Запустите сервис из корневой папки сервиса с помощью команды: uvicorn main:app --host 127.0.0.1 --port 8000 --reload
7. Для просмотра документации используйте эндпоинт /docs или /redoc.
