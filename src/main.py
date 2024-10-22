from fastapi import status, HTTPException

from src.engine import app, product_repo
from src.utils.decorators import try_except
from src.utils.schemas import Product, ProductBase


@app.get('/category/{category_id}')
@try_except(detail='Ошибка получения списка продуктов категории')
async def get_products_in_category(category_id: int):
    return await product_repo.list(
        category_id=category_id,
        is_published=True
    )


@app.get('/products')
# @try_except(detail='Ошибка получения списка продуктов')
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


@app.post('/products', status_code=status.HTTP_201_CREATED, response_model=Product)
# @try_except(detail='Ошибка создания продукта')
async def create_product(product: ProductBase):
    print(product)
    try:
        res = await product_repo.create(product)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return res



@app.get('/products/{product_id}', response_model=Product)
@try_except(detail='Ошибка получение продукта')
async def get_product(product_id: int):
    product = await product_repo.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Продукт с id {product_id} не найден'
        )
    return product



@app.post('/products/{product_id}', response_model=Product)
@try_except(detail='Ошибка обновления продукта')
async def update_product(product: Product):
    return await product_repo.update(product)


@app.delete('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
@try_except(detail='Ошибка удаления продукта')
async def delete_product(product_id: int):
    await product_repo.delete(product_id)


@app.get('/')
async def main_page():
    return {'text': 'ok'}


def start():
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == '__main__':
    start()
