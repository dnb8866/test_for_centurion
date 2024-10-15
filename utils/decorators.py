import logging
from functools import wraps

from fastapi import HTTPException, status

def try_except(detail: str):
    def outer(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logging.error(f'Ошибка функции {func.__name__} - {type(e)} {e}')
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=detail
                )
        return wrapper
    return outer