from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class Db(ABC):
    @abstractmethod
    async def prepare(self):
        """Подготовка БД, создание таблиц."""

    @abstractmethod
    async def clean(self):
        """Очистка БД."""


class Repository(ABC):
    """Абстрактный класс для работы с объектами БД."""

    def __init__(self, db: Db):
        self.db = db

    @abstractmethod
    async def create(self, obj: T) -> T:
        """
        Создание объекта в БД.
        :param obj: Объект для создания.
        :return: Созданный объект.
        """

    @abstractmethod
    async def get(self, obj_id: int) -> T:
        """
        Получение объекта из БД.
        :param obj_id: Идентификатор объекта.
        :return: Полученный объект.
        """

    @abstractmethod
    async def list(self, offset: int = None, limit: int = None, **kwargs) -> list[T]:
        """
        Получение списка объектов из БД с возможностью фильтрации.
        :param offset: Смещение для получения списка объектов.
        :param limit: Максимальное число объектов для получения.
        :param kwargs: Фильтры для получения списка объектов.
        :return: Список объектов.
        """

    @abstractmethod
    async def update(self, obj: T) -> T:
        """
        Обновление объекта в БД.
        :param obj: Объект для обновления.
        :return: Обновленный объект.
        """

    async def delete(self, obj_id: int) -> None:
        """
        Удаление объекта из БД.
        :param obj_id: Идентификатор объекта.
        """


