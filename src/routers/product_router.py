from fastapi import APIRouter, status, HTTPException

from src.engine import product_repo
from src.utils.schemas import ProductBase, Product

router = APIRouter(
    prefix='/products',
    tags=['Товары']
)


@router.get('')
async def get_products(
    offset: int = None,
    limit: int = None,
    text_in_name: str = None,
    text_in_description: str = None,
    min_price: float = None,
    max_price: float = None,
    category_id: int = None,
    is_published: bool = None
):
    try:
        res = await product_repo.list(
            offset=offset,
            limit=limit,
            text_in_name=text_in_name,
            text_in_description=text_in_description,
            min_price=min_price,
            max_price=max_price,
            category_id=category_id,
            is_published=is_published
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return res


@router.post('', status_code=status.HTTP_201_CREATED, response_model=Product)
async def create_product(product: ProductBase):
    try:
        res = await product_repo.create(product)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return res



@router.get('/{product_id}', response_model=Product)
async def get_product(product_id: int):
    product = await product_repo.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Продукт с id {product_id} не найден'
        )
    return product



@router.put('/{product_id}', response_model=Product)
async def update_product(product: Product):
    return await product_repo.update(product)


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    await product_repo.delete(product_id)