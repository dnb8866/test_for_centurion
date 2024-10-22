from fastapi import APIRouter

from src.engine import product_repo
from src.utils.decorators import try_except

router = APIRouter(
    prefix='/category',
    tags=['Категории']
)


@router.get('/{category_id}')
@try_except(detail='Ошибка получения списка продуктов категории')
async def get_products_in_category(category_id: int):
    return await product_repo.list(
        category_id=category_id,
        is_published=True
    )

