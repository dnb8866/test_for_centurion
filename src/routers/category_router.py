from fastapi import APIRouter

from src.engine import product_repo

router = APIRouter(
    prefix='/category',
    tags=['Категории']
)


@router.get('/{category_id}')
async def get_products_in_category(category_id: int):
    return await product_repo.list(
        category_id=category_id,
        is_published=True
    )

